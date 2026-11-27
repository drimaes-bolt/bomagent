# -*- coding: utf-8 -*-
"""ROHM 제너 다이오드와 Panasonic OS-CON의 '사양 조합' 행(문서에 형명이 없던 행)에 문서의 형명 규칙으로 부품번호를 조립해 채운다.
실행: python derive_rohm_panasonic_pn.py <입력 final_rows.json[.gz]> <출력 final_rows.json.gz> [--docs <입력 final_docs.json[.gz]> <출력 final_docs.json>] [--report 보고서.txt]
Walsin은 derive_walsin_pn.py가 먼저 처리한다(같은 규칙, DEC-21). 이 스크립트는 그 결과를 입력으로 받는다.

- ROHM 제너(ROHM_Diodes_ShortForm_Catalog_2024.pdf): PDF 34쪽 Product No. Explanation과 22·23쪽 위쪽 예시(EDZV FH T2R 3.6 B, YDZV FH TR 13).
  형명 = 시리즈 + 등급 코드 + 테이핑 코드 + 제너 전압 + 세부 구분. 등급 코드는 표 머리글의 Automotive Grade Code이고 AEC-Q101 YES인 행에만 붙인다.
  테이핑 코드는 표 머리글의 Taping Code(34쪽 포장표와 패키지가 일치함). BZX84BxxLY·BZX84CxxLY는 시리즈 이름의 xx 자리에 표의 전압 구분(2V4)을 넣고 뒤에 등급·테이핑 코드를 붙인다.
- Panasonic OS-CON SMD(Panasonic_Devices_and_Solutions_Catalogue_2025.pdf): PDF 37쪽 Part Number explanation. 형명 = 정격전압 코드 + 시리즈 + 정격용량 코드 + 허용오차 M(±20%).
  용량·전압이 범위로 인쇄된 개요표 행은 형명이 정해지지 않아 건드리지 않는다.
"""
import collections
import copy
import gzip
import io
import json
import re
import sys
from decimal import Decimal

SRC, DST = sys.argv[1], sys.argv[2]
REPORT = sys.argv[sys.argv.index('--report') + 1] if '--report' in sys.argv else None
DOCS = sys.argv[sys.argv.index('--docs') + 1:sys.argv.index('--docs') + 3] if '--docs' in sys.argv else None

ROHM_DOC = 'Diode/ROHM/ROHM_Diodes_ShortForm_Catalog_2024.pdf'
PANA_DOC = 'Capacitor/Panasonic/Panasonic_Devices_and_Solutions_Catalogue_2025.pdf'
TAG = '주문 코드 조합'

# ROHM 22·23쪽 표 머리글(Series Name / Automotive Grade Code / Taping Code). 시리즈 이름 → (형명 앞머리, 전압 뒤 접미, 등급 코드, 테이핑 코드)
ROHM_Z = {
    'ADZ series': ('ADZ', '', None, 'T15R'), 'CDZV series': ('CDZV', '', None, 'T2R'), 'EDZV series': ('EDZV', '', 'FH', 'T2R'),
    'UFZV series': ('UFZV', '', 'FH', 'TE-17'), 'UDZV series': ('UDZV', '', 'FH', 'TE-17'), 'UDZLV series': ('UDZLV', '', 'FH', 'TE-17'),
    'TFZV series': ('TFZV', '', None, 'TR'), 'YFZV series': ('YFZV', '', 'FH', 'TR'),
    'TDZV series': ('TDZV', '', None, 'TR'), 'YDZV series': ('YDZV', '', 'FH', 'TR'),
    'BZX84BxxLY series': ('BZX84B', 'LY', 'FH', 'T116'), 'BZX84CxxLY series': ('BZX84C', 'LY', 'FH', 'T116'),
    'KDZV series': ('KDZV', '', 'TF', 'TR'), 'KDZLV series': ('KDZLV', '', 'TF', 'TR'), 'PDZV series': ('PDZV', '', 'TF', 'TR'), 'PTZ series': ('PTZ', '', 'TF', 'TE25'),
}
ROHM_NOTE = '주문 코드로 조립(PDF 34쪽 Product No. Explanation·%d쪽 예시): 시리즈+등급 코드(AEC-Q101 행만)+테이핑 코드+제너 전압·세부 구분'
ROHM_NOTE_BZX = '주문 코드로 조립(PDF 34쪽): 시리즈명의 xx 자리에 표의 전압 구분을 넣고 등급 코드+테이핑 코드를 붙임'

# Panasonic 37쪽 OS-CON SMD 형명 설명의 코드: 전압·용량은 숫자 그대로, 소수점은 R(2.5→2R5, 4.7→4R7), 허용오차 ±20%=M
PANA_NOTE = '주문 코드로 조립(PDF 37쪽 Part Number explanation OS-CON SMD): 전압 코드+시리즈+용량 코드+허용오차 M(±20%)'


def num_code(x):
    """숫자를 형명 코드로: 16→'16', 2.5→'2R5', 4.7→'4R7', 470→'470'"""
    x = Decimal(x).normalize()
    s = format(x, 'f')
    return s.replace('.', 'R')


def derive_rohm(r):
    s, sp = r['series'], r['specs']
    cfg = ROHM_Z.get(s)
    if not cfg:
        return None, None, '이 시리즈의 머리글 코드를 읽지 않음'
    pre, post, grade, taping = cfg
    m = re.search(r'VZ sub-division (\S+?);', sp.get('features') or '')
    if not m:
        return None, None, '전압 세부 구분을 찾지 못함'
    label = m.group(1)
    auto = sp.get('aec') == 'AEC-Q101'
    if auto and not grade:
        return None, None, '차량용 행인데 머리글에 등급 코드가 없음'
    g = grade if auto else ''
    pn = pre + label + post + g + taping if post else pre + g + taping + label
    return pn, (ROHM_NOTE_BZX if post else ROHM_NOTE % (22 if int(r['page']) == 22 else 23)), None


def derive_pana(r):
    sp = r['specs']
    cap, volt = sp.get('capacitance') or '', sp.get('voltage') or ''
    if '~' in cap or '~' in volt:
        return None, None, '용량·전압이 범위로만 인쇄되어 형명을 하나로 정할 수 없음'
    if not (sp.get('features') or '').startswith('OS-CON SMD'):
        return None, None, '형명 설명이 OS-CON SMD 쪽에만 있음(POSCAP은 전압 코드가 둘이고 특수 코드가 선택이라 하나로 정해지지 않음)'
    mc = re.match(r'^([\d.]+)μF$', cap)
    mv = re.match(r'^([\d.]+)V$', volt)
    if not mc or not mv:
        return None, None, '용량·전압 표기를 코드로 바꿀 수 없음'
    return num_code(mv.group(1)) + r['series'] + num_code(mc.group(1)) + 'M', PANA_NOTE, None


def load(p):
    return json.load(gzip.open(p, 'rt', encoding='utf-8')) if p.endswith('.gz') else json.load(io.open(p, encoding='utf-8'))


rows = load(SRC)
existing = {(r['domain'], r['vendor'], r['part_number'].upper()) for r in rows if r.get('part_number')}
out, stat, fails = [], collections.Counter(), collections.Counter()
seen = set()
for r in rows:
    pick = None
    if r['level'] == '사양 조합' and not r.get('part_number'):
        if r['vendor'] == 'ROHM' and r['doc'] == ROHM_DOC:
            pick = ('ROHM 제너', derive_rohm)
        elif r['vendor'] == 'Panasonic' and r['doc'] == PANA_DOC:
            pick = ('Panasonic', derive_pana)
        elif r['vendor'] in ('Vishay', 'Power_Integrations', 'TE_Connectivity'):
            fails[(r['vendor'], '문서에 형명 규칙이 인쇄돼 있지 않음')] += 1
            n = copy.deepcopy(r)
            n['note'] = '형명 미조립: 문서에 형명 규칙이 없음; ' + (r.get('note') or '')
            out.append(n)
            continue
    if not pick:
        out.append(r)
        continue
    kind, fn = pick
    pn, rule, why = fn(r)
    if why:
        n = copy.deepcopy(r)
        n['note'] = '형명 미조립: ' + why + '; ' + (r.get('note') or '')
        out.append(n)
        fails[(kind, why)] += 1
        continue
    k = (r['domain'], r['vendor'], pn.upper())
    if k in existing or k in seen:
        stat[kind + ' 같은 형명이 이미 있어 뺌'] += 1
        out.append(r)
        continue
    seen.add(k)
    n = copy.deepcopy(r)
    n['part_number'] = pn
    n['level'] = '부품번호'
    n['note'] = rule
    n['verify'] = TAG if r.get('verify') == '쪽 일치' else TAG + '·' + (r.get('verify') or '')
    out.append(n)
    stat[kind + ' 조립한 형명 행'] += 1

if DOCS:
    docs = load(DOCS[0])
    cnt = collections.Counter((r['domain'], r['doc'], r['level']) for r in out)
    for d in docs:
        if d['vendor'] in ('ROHM', 'Panasonic') and d['doc'] in (ROHM_DOC, PANA_DOC):
            k = 'ROHM 제너' if d['vendor'] == 'ROHM' else 'Panasonic'
            n_ok = stat[k + ' 조립한 형명 행']
            n_no = sum(v for (kk, _), v in fails.items() if kk == k)
            d['rows'] = sum(v for (dm, dc, lv), v in cnt.items() if dc == d['doc'])
            d['individual'] = cnt[(d['domain'], d['doc'], '부품번호')] + cnt[(d['domain'], d['doc'], '사양 조합')]
            d['series_only'] = cnt[(d['domain'], d['doc'], '계열')]
            d['note'] = (d.get('note') or '') + (' [2026-11-28 갱신] 형명 없이 풀었던 사양 조합 행 %d개 중 %d개에 문서의 형명 규칙으로 형명을 조립해 채웠다(원문 대조 "주문 코드 조합"). 못 채운 %d행은 사유를 비고 앞에 적었다.' % (n_ok + n_no, n_ok, n_no))
    io.open(DOCS[1], 'w', encoding='utf-8').write(json.dumps(docs, ensure_ascii=False))

rep = ['입력 %d행 → 출력 %d행' % (len(rows), len(out))]
rep += ['%s: %d' % kv for kv in sorted(stat.items())]
rep.append('--- 조립하지 못한 행(사유별) ---')
for (kind, why), n in sorted(fails.items(), key=lambda x: -x[1]):
    rep.append('%6d  %s | %s' % (n, kind, why))
print('\n'.join(rep))
if REPORT:
    io.open(REPORT, 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
with gzip.open(DST, 'wt', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
