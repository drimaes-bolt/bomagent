# -*- coding: utf-8 -*-
"""에이전트가 뽑은 제품 행을 원문 PDF 텍스트와 대조한다. 실행: python -I verify_rows.py <scratchpad> <R13루트> [parts 파일 패턴]
출력: rows_checked.json (행마다 check: ok | page_off | absent | bad_doc | bad_schema), 요약."""
import collections
import csv
import glob
import io
import json
import os
import re
import subprocess
import sys

SP, ROOT = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avl_schema import DOMAINS, SPECS, VENDORS  # noqa: E402

CACHE = os.path.join(SP, 'txt_cache')
os.makedirs(CACHE, exist_ok=True)
man = {r['file']: r for r in csv.DictReader(io.open(os.path.join(ROOT, 'manifest.csv'), encoding='utf-8-sig'))}


def norm(s):
    return re.sub(r'[^0-9a-z]', '', (s or '').lower())


def page_texts(rel, shift=False):
    key = rel.replace('/', '__') + ('.shift' if shift else '') + '.json'
    cp = os.path.join(CACHE, key)
    if os.path.exists(cp):
        return json.load(io.open(cp, encoding='utf-8'))
    p = os.path.join(ROOT, rel)
    t = subprocess.run(['pdftotext', '-layout', '-q', p, '-'], capture_output=True, timeout=300).stdout.decode('utf-8', 'replace')
    pages = t.split('\f')
    if shift:  # Taiyo Yuden 글꼴 코드 밀림: 문자 코드 -1
        pages = [''.join(chr(ord(c) - 1) if 33 < ord(c) < 127 else c for c in pg) for pg in pages]
    out = [norm(pg) for pg in pages]
    json.dump(out, io.open(cp, 'w', encoding='utf-8'))
    return out


def main_name(s):
    s = re.split(r'\s[\(/,]', s or '')[0]
    return norm(s)


rows_all = []
pat = sys.argv[3] if len(sys.argv) > 3 else 'parts_*.json'
for p in sorted(glob.glob(os.path.join(SP, pat))):
    d = json.load(io.open(p, encoding='utf-8'))
    for r in d['rows']:
        r['_agent'] = d.get('agent')
        r['_domain'] = d['domain']
        r['_src'] = os.path.basename(p)
        rows_all.append(r)

stat = collections.Counter()
by_agent = collections.defaultdict(collections.Counter)
allowed = {dm: {k for k, _, _ in SPECS[dm]} for dm in SPECS}
pages_cache = {}
for r in rows_all:
    dm = r['_domain']
    chk = 'ok'
    why = ''
    rel = r.get('doc')
    if rel not in man or man[rel]['domain'] != dm or r.get('vendor') not in VENDORS or man[rel]['vendor'] != r.get('vendor'):
        chk, why = 'bad_doc', 'doc/vendor/domain 불일치'
    elif not r.get('series') or r.get('level') not in ('계열', '부품번호', '사양 조합'):
        chk, why = 'bad_schema', 'series 또는 level 누락'
    elif not isinstance(r.get('specs'), dict) or set(r['specs']) - allowed.get(dm, set()):
        chk, why = 'bad_schema', 'specs 키 오류: ' + ','.join(sorted(set((r.get('specs') or {}).keys()) - allowed.get(dm, set())))
    else:
        shift = 'Taiyo' in rel or rel.endswith('inductor_e_2501.pdf')
        if (rel, shift) not in pages_cache:
            pages_cache[(rel, shift)] = page_texts(rel, shift)
        pt = pages_cache[(rel, shift)]
        needle = norm(r.get('part_number')) if r.get('part_number') else main_name(r['series'])
        alt = main_name(r['series'])
        # 쪽 번호 해석
        pg = str(r.get('page') or '')
        nums = []
        for part in re.split(r'[,;]', pg):
            m = re.match(r'\s*(\d+)\s*-\s*(\d+)\s*$', part)
            if m:
                nums += list(range(int(m.group(1)), int(m.group(2)) + 1))
            elif part.strip().isdigit():
                nums.append(int(part))
        if not nums or max(nums) > len(pt):
            chk, why = 'page_off', '쪽 번호 오류'
        else:
            on = ' '.join(pt[n - 1] for n in nums if 0 < n <= len(pt))
            if needle and needle in on or (alt and len(alt) >= 3 and alt in on):
                chk = 'ok'
            else:
                whole = ' '.join(pt)
                if (needle and needle in whole) or (alt and len(alt) >= 3 and alt in whole):
                    chk, why = 'page_off', '문서에는 있으나 해당 쪽에 없음'
                else:
                    # 단어 대조: 표의 여러 칸을 합쳐 지은 계열명(예: 'SMM 0102, 0204')과 ™ 같은 기호를 가린다
                    raw = re.sub(r'[™®©]', ' ', (r.get('series') or '') + ' ' + (r.get('part_number') or ''))
                    toks = [norm(t) for t in re.findall(r'[A-Za-z0-9]+', raw) if len(t) >= 2 or t.isdigit()]
                    toks = [t for t in toks if t and t not in ('series', 'and', 'the', 'for', 'with', 'through', 'type', 'new', 'high', 'low')]
                    hit_pg = sum(1 for t in toks if t in on)
                    hit_all = sum(1 for t in toks if t in whole)
                    if toks and hit_pg >= max(1, int(0.8 * len(toks) + 0.5)):
                        chk, why = 'ok', '단어 대조'
                    elif toks and hit_all >= max(1, int(0.8 * len(toks) + 0.5)):
                        chk, why = 'page_off', '단어는 문서에 있으나 해당 쪽에 없음'
                    else:
                        chk, why = 'absent', '문서 어디에도 없음'
    r['check'], r['why'] = chk, why
    stat[chk] += 1
    by_agent[(r['_agent'], dm)][chk] += 1

json.dump(rows_all, io.open(os.path.join(SP, 'rows_checked.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('total', len(rows_all), dict(stat))
for k, v in sorted(by_agent.items()):
    print(k, dict(v))
