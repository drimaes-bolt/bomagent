# -*- coding: utf-8 -*-
"""final_rows.json → 목업용 DATA.avl(avl_data.json). 실행: python -I build_data_avl.py <scratchpad> <R13루트> <R09 md>
행 배열: [제조사 번호, 구분(0 계열·1 부품번호), 계열, 부품번호, 유형, 문서 번호, 쪽, 비고, 원문 대조, ...사양(cat.cols 순서)]"""
import collections
import csv
import io
import json
import os
import re
import sys

SP, ROOT, R09 = sys.argv[1:4]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avl_schema import DOMAIN_KO, DOMAINS, SPECS, VENDORS  # noqa: E402

import gzip
_fp = os.path.join(SP, 'final_rows.json')
rows = json.load(io.open(_fp, encoding='utf-8')) if os.path.exists(_fp) else json.load(gzip.open(_fp + '.gz', 'rt', encoding='utf-8'))
man = {r['file']: r for r in csv.DictReader(io.open(os.path.join(ROOT, 'manifest.csv'), encoding='utf-8-sig'))}
SEC = {'MCU': 2, 'MOSFET': 3, 'Resistor': 4, 'Capacitor': 5, 'Inductor': 6, 'Power_IC': 7, 'Diode': 8, 'Driver_IC': 9, 'Sensor': 12, 'Wireless_IC': 13, 'Connector': 15}
r09, sec = {}, None
for line in io.open(R09, encoding='utf-8'):
    m = re.match(r'##\s+(\d+)\.\s', line)
    if m:
        sec = int(m.group(1))
        continue
    c = [x.strip() for x in line.strip().strip('|').split('|')]
    if sec and len(c) == 5 and c[0].isdigit():
        r09[(sec, c[1])] = {'rank': int(c[0]), 'country': c[2], 'fab': c[3], 'biz': c[4]}


def cut(s, n):
    s = (s or '').strip()
    return s if len(s) <= n else s[:n - 1] + '…'


by = collections.defaultdict(list)
for r in rows:
    by[r['domain']].append(r)
cats = []
for code, ko, _ in DOMAINS:
    rs = by.get(code, [])
    if not rs:
        continue
    cols = [[k, h, w * 7 if w * 7 >= 80 else 80] for k, h, w in SPECS[code]]
    vkeys = sorted({r['vendor'] for r in rs}, key=lambda v: (r09.get((SEC[code], VENDORS[v][1]), {}).get('rank', 99), v))
    vidx = {v: i for i, v in enumerate(vkeys)}
    docs, didx = [], {}
    for r in sorted(rs, key=lambda r: (vidx[r['vendor']], r['doc'])):
        if r['doc'] not in didx:
            m = man[r['doc']]
            didx[r['doc']] = len(docs)
            docs.append({'t': m['title'], 'd': m['doc_date'], 'p': int(m['pages'] or 0), 'f': r['doc'], 'v': vidx[r['vendor']]})
    vendors = []
    for v in vkeys:
        info = r09.get((SEC[code], VENDORS[v][1]), {})
        vendors.append({'k': v, 'name': VENDORS[v][0], 'short': v.replace('_', ' '), 'country': info.get('country', ''), 'fab': info.get('fab', ''), 'biz': info.get('biz', ''),
                        'rank': info.get('rank', 0), 'docs': [i for i, d in enumerate(docs) if d['v'] == vidx[v]], 'n': sum(1 for r in rs if r['vendor'] == v)})
    LV = {'계열': 0, '부품번호': 1, '사양 조합': 2}
    S, sidx = [''], {'': 0}

    def si(x):
        x = '' if x is None else str(x)
        i = sidx.get(x)
        if i is None:
            i = sidx[x] = len(S)
            S.append(x)
        return i

    out = []
    for r in sorted(rs, key=lambda r: (vidx[r['vendor']], didx[r['doc']], str(r.get('type') or ''), r['series'], str(r.get('part_number') or ''))):
        sp = r.get('specs') or {}
        # 문자열은 분류별 사전 번호로 적는다(같은 값이 많이 되풀이되어 파일이 작아진다). 0, 1, 5번 칸(제조사·구분·문서)은 숫자 그대로
        out.append([vidx[r['vendor']], LV[r['level']], si(r['series']), si(r.get('part_number')), si(r.get('type')), didx[r['doc']],
                    si(r.get('page')), si(cut(r.get('note'), 160)), si(r.get('verify'))] + [si(sp.get(k)) for k, _, _ in SPECS[code]])
    cats.append({'id': code, 'ko': ko, 'cols': cols, 'vendors': vendors, 'docs': docs, 'S': S, 'rows': out})
data = {'asOf': '2026-11-27', 'cats': cats}
s = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
io.open(os.path.join(SP, 'avl_data.json'), 'w', encoding='utf-8').write(s)
print('avl_data.json', len(s), 'bytes', len(s.encode('utf-8')), 'rows', sum(len(c['rows']) for c in cats), 'cats', len(cats), 'vendors', sum(len(c['vendors']) for c in cats))
