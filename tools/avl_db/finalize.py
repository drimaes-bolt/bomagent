# -*- coding: utf-8 -*-
"""검증 결과를 정리해 최종 행(final_rows.json)과 문서 메모(final_docs.json)를 만든다.
- 제외: Taiyo MLCC 소개 문서의 마케팅 행, LCMC/LCMG 커패시터 행(그림 대조에서 비드로 확인)
- verify 열: 행 일치(부품번호 줄 근처에 사양 숫자) · 쪽 일치(같은 쪽에 사양 숫자) · 확인 필요 · 그림 확인(Taiyo, 쪽 이미지를 직접 대조)
실행: python -I finalize.py <scratchpad> <R13루트>"""
import collections
import glob
import io
import json
import os
import re
import subprocess
import sys

SP, ROOT = sys.argv[1], sys.argv[2]
PAT = sys.argv[3] if len(sys.argv) > 3 else 'parts_*.json'   # 에이전트 JSON 이름 패턴
rows = json.load(io.open(os.path.join(SP, 'rows_checked.json'), encoding='utf-8'))
NUM = re.compile(r'(?<![0-9A-Za-z.])\d+(?:\.\d+)?')
cache = {}


def page_lines(rel, pg):
    k = (rel, pg)
    if k not in cache:
        t = subprocess.run(['pdftotext', '-layout', '-f', str(pg), '-l', str(pg), '-q', os.path.join(ROOT, rel), '-'], capture_output=True, timeout=120).stdout.decode('utf-8', 'replace')
        t = re.sub(r'(?<=\d),(?=\d{3}(?!\d))', '', t)   # 천 단위 쉼표 정리: 5,600pF → 5600pF
        cache[k] = t.split('\n')
    return cache[k]


def nrm(s):
    return re.sub(r'[^0-9a-z]', '', s.lower())


ncache = {}


def norm_lines(rel, pg):
    k = (rel, pg)
    if k not in ncache:
        ncache[k] = [nrm(l) for l in page_lines(rel, pg)]
    return ncache[k]


def match(x, have):
    for c in have:
        for m in (1, 1000, 0.001, 1e6, 1e-6):   # pF·nF·µF, Ω·mΩ 같은 단위 환산
            if abs(c * m - x) <= 1e-9 + 1e-6 * abs(x):
                return True
    return False


def frac(nums, have):
    nums = sorted(set(nums))
    if not nums:
        return None
    return sum(1 for n in nums if match(float(n), have)) / len(nums)


DROP_TY = 'ty2025_b_mlcc_e_2512.pdf'
out, dropped = [], collections.Counter()
for r in rows:
    doc = r['doc']
    fm = 'Microcontroller_Pocket_Guide' in doc and r['series'] in ('FM3', 'FM4')   # 원문이 'FM 3'처럼 기호와 함께 인쇄돼 대조기가 놓친 행(직접 확인)
    if r['check'] not in ('ok', 'page_off') and not ('Taiyo' in doc or 'inductor_e_2501' in doc or fm):
        dropped['검증 실패'] += 1
        continue
    if doc.endswith(DROP_TY):
        dropped['Taiyo MLCC 마케팅 소개'] += 1
        continue
    if r['_domain'] == 'Capacitor' and doc.endswith('ty2025_b_hr_auto_e_2512.pdf') and r['series'].startswith('LCMC'):
        dropped['LCMC/LCMG는 비드(커패시터 아님)'] += 1
        continue
    # 사양 숫자 대조
    nums = []
    for k, v in (r.get('specs') or {}).items():
        if k in ('features', 'aec', 'package', 'packages', 'target', 'core', 'peripherals', 'technology', 'standard', 'interfaces', 'application', 'memory'):
            continue
        if r['_domain'] == 'Capacitor' and k in ('tolerance', 'temp'):   # 매트릭스 쪽 밖의 시리즈 공통 사양표에서 온 값이라 같은 쪽 숫자 대조에 쓰지 않는다
            continue
        nums += NUM.findall(str(v))
    verify = None
    if 'Taiyo' in doc or 'inductor_e_2501' in doc:
        verify = '그림 확인'
    else:
        pg = str(r['page']).split('-')[0].split(',')[0].strip()
        if pg.isdigit() and nums:
            ls = page_lines(doc, int(pg))
            page_have = {float(x) for x in NUM.findall(' '.join(ls))}
            f_page = frac(nums, page_have)
            f_near = None
            if r.get('part_number'):
                pn = nrm(r['part_number'])
                nls = norm_lines(doc, int(pg))
                idx = [i for i, l in enumerate(nls) if pn and pn in l]
                if idx:
                    ctx = ' '.join(' '.join(ls[max(0, i - 2): i + 3]) for i in idx[:2])
                    f_near = frac(nums, {float(x) for x in NUM.findall(ctx)})
            if f_near is not None and f_near >= 0.6:
                verify = '행 일치'
            elif f_page is not None and f_page >= 0.6:
                verify = '쪽 일치'
            else:
                verify = '확인 필요'
        else:
            verify = '이름·쪽 일치'   # 사양 숫자가 없는 행: 이름과 쪽만 원문과 대조했다
    r['verify'] = verify
    out.append({'domain': r['_domain'], 'agent': r['_agent'], 'vendor': r['vendor'], 'doc': r['doc'], 'page': r.get('page'), 'level': r['level'],
                'series': r['series'], 'part_number': r.get('part_number'), 'type': r.get('type'), 'specs': r.get('specs') or {}, 'note': r.get('note'), 'verify': verify})

json.dump(out, io.open(os.path.join(SP, 'final_rows.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# 문서 메모: 에이전트 JSON의 docs를 모으고 행 수는 최종 행으로 다시 센다
cnt = collections.Counter((r['domain'], r['doc']) for r in out)
docs = {}
for p in sorted(glob.glob(os.path.join(SP, PAT))):
    d = json.load(io.open(p, encoding='utf-8'))
    for x in d.get('docs', []):
        docs[(d['domain'], x['file'])] = {'domain': d['domain'], 'doc': x['file'], 'vendor': x['file'].split('/')[1], 'note': x.get('note'), 'agent': d.get('agent')}
lvc = collections.Counter((r['domain'], r['doc'], r['level']) for r in out)
for (dm, f), v in docs.items():
    v['rows'] = cnt.get((dm, f), 0)
    v['individual'] = lvc.get((dm, f, '부품번호'), 0) + lvc.get((dm, f, '사양 조합'), 0)
    v['series_only'] = lvc.get((dm, f, '계열'), 0)
k1 = ('Capacitor', 'Capacitor/Taiyo_Yuden/' + DROP_TY)
if k1 in docs:
    docs[k1]['note'] = '1쪽 마케팅 소개(MLCC Business Trends): 제품 계열명이 없어 행을 만들지 않았다'
k2 = ('Capacitor', 'Capacitor/Taiyo_Yuden/ty2025_b_hr_auto_e_2512.pdf')
if k2 in docs:
    docs[k2]['note'] = (docs[k2]['note'] or '') + ' / LCMC·LCMG는 쪽 그림 대조에서 페라이트 비드로 확인되어 커패시터에서 제외(인덕터에 있음)'
json.dump(sorted(docs.values(), key=lambda x: (x['domain'], x['doc'])), io.open(os.path.join(SP, 'final_docs.json'), 'w', encoding='utf-8'), ensure_ascii=False)

by = collections.Counter(r['domain'] for r in out)
print('final rows', len(out), dict(by))
print('dropped', dict(dropped))
print('verify', dict(collections.Counter(r['verify'] for r in out)))
vend = collections.defaultdict(set)
for r in out:
    vend[r['domain']].add(r['vendor'])
print({k: sorted(v) for k, v in vend.items()})
