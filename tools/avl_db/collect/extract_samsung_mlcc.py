# -*- coding: utf-8 -*-
"""삼성전기 제품 검색(MLCC)의 'List Download' 파일(품번만 9,416개) → AVL 행.
사양은 삼성전기 MLCC 카탈로그(R13 Capacitor/Samsung_EM/MLCC_2512.pdf 6~8쪽)의 품번 체계표로 해독한다.
표에 없거나 모호한 코드(허용오차 H·L·U·V 등)는 해독하지 않고 비운다. 번호를 합성하지 않는다(목록의 품번만 쓴다).
실행: python extract_samsung_mlcc.py <mlcc_list.xlsx> <출력 json>"""
import io
import json
import re
import sys
import warnings

import openpyxl

warnings.filterwarnings('ignore')
SRC, OUT = sys.argv[1:3]

SIZE = {'R1': ('008004', '0201'), '02': ('01005', '0402'), '03': ('0201', '0603'), '05': ('0402', '1005'), '10': ('0603', '1608'), '21': ('0805', '2012'),
        '31': ('1206', '3216'), '32': ('1210', '3225'), '42': ('1808', '4520'), '43': ('1812', '4532'), '55': ('2220', '5750'),
        'L5': ('0204', '0510'), 'L6': ('0304', '0610'), '01': ('0306', '0816'), '19': ('0503', '1209')}
DIEL = {'C': 'C0G', 'G': 'X8G', 'A': 'X5R', 'X': 'X6S', 'W': 'X6T', 'B': 'X7R', 'K': 'JIS-B', 'Y': 'X7R(S)', 'Z': 'X7S', 'F': 'X7T', 'M': 'Y5V', 'E': 'X8M', 'J': 'X8L'}
TOL = {'N': '±0.03pF', 'A': '±0.05pF', 'B': '±0.1pF', 'C': '±0.25pF', 'D': '±0.5pF', 'G': '±2%', 'J': '±5%', 'K': '±10%', 'M': '±20%', 'Z': '-20~+80%'}
VOLT = {'S': '2.5', 'R': '4', 'Q': '6.3', 'P': '10', 'O': '16', 'A': '25', 'L': '35', 'B': '50', 'C': '100', 'D': '200', 'E': '250', 'F': '350',
        'G': '500', 'H': '630', 'I': '1000', 'J': '2000', 'K': '3000'}


def cap(code):
    c = code.upper()
    try:
        if 'R' in c:
            pf = float(c.replace('R', '.'))
        else:
            pf = int(c[:2]) * 10 ** int(c[2])
    except Exception:
        return None
    if pf >= 1e6:
        v, u = pf / 1e6, 'μF'
    elif pf >= 1e3:
        v, u = pf / 1e3, 'nF'
    else:
        v, u = pf, 'pF'
    return (('%g' % round(v, 4)) + u), pf


wb = openpyxl.load_workbook(SRC)
parts = [r[0] for r in wb.active.iter_rows(values_only=True) if r and r[0] and r[0] != 'Part Number']
rows, bad = [], 0
for pn in parts:
    m = re.match(r'^CL([0-9A-Z]{2})([A-Z])([0-9R]{3})([A-Z])([A-Z])', pn)
    if not m:
        bad += 1
        continue
    sz, di, cc, tl, vc = m.groups()
    sp = {}
    if sz in SIZE:
        sp['size_inch'], sp['size_metric'] = SIZE[sz]
    if di in DIEL:
        sp['dielectric'] = DIEL[di]
    c = cap(cc)
    if c:
        sp['capacitance'] = c[0]
    t = TOL.get(tl)
    if tl == 'F' and c:
        t = '±1pF' if c[1] < 10 else '±1%'
    if t:
        sp['tolerance'] = t
    if vc in VOLT:
        sp['voltage'] = VOLT[vc] + 'V'
    rows.append({'domain': 'Capacitor', 'agent': 'private:samsung-list-download', 'vendor': 'Samsung_EM', 'doc': 'Capacitor/Samsung_EM/Samsung_EM_Product_Search_MLCC_List',
                 'page': None, 'level': '부품번호', 'series': 'CL' + sz + (' (' + SIZE[sz][0] + '/' + SIZE[sz][1] + ')' if sz in SIZE else ''), 'part_number': pn, 'type': 'MLCC',
                 'specs': sp, 'note': '품번 코드 해독(삼성전기 MLCC 카탈로그 6~8쪽). 해독표에 없는 코드는 비움', 'verify': '품번 해독'})
doc = {'domain': 'Capacitor', 'vendor': 'Samsung_EM', 'file': 'Capacitor/Samsung_EM/Samsung_EM_Product_Search_MLCC_List',
       'title': 'Samsung Electro-Mechanics Product Search - MLCC "List Download" (품번 목록)', 'doc_type': 'Official export (List Download)', 'doc_date': '2026-11',
       'pages': 0, 'source_url': 'https://product.samsungsem.com/mlcc/basic-search.do', 'policy': '공식 내보내기(품번만, 사양은 카탈로그 품번 체계표로 해독)', 'agent_note': '약관 10(2): 영리 목적 이용·복제·배포는 사전 동의 필요로 읽힘'}
io.open(OUT, 'w', encoding='utf-8').write(json.dumps({'docs': [doc], 'rows': rows}, ensure_ascii=False))
full = sum(1 for r in rows if len(r['specs']) >= 5)
print('parts', len(parts), 'rows', len(rows), 'unparsed', bad, 'rows with >=5 spec fields', full)
print(json.dumps(rows[0], ensure_ascii=False)[:500])
