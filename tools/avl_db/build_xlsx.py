# -*- coding: utf-8 -*-
"""검증을 마친 제품 행으로 AVL 엑셀과 도메인별 공급 제품 엑셀을 만든다.
실행: python build_xlsx.py <scratchpad> <R13루트> <R09 md> <출력 폴더>
입력: scratchpad/final_rows.json (행), scratchpad/final_docs.json (문서별 추출 메모)
양식은 루트 Inventory.xlsx를 따른다: 1행 제목, 2행 설명, 3행 연두색(CCFFCC) 머리글, 본문 Tahoma 10, 틀 고정."""
import collections
import csv
import io
import json
import os
import re
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

SP, ROOT, R09, OUT = sys.argv[1:5]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avl_schema import DOMAIN_KO, DOMAINS, HEAD_COLS, SPECS, TAIL_COLS, VENDORS  # noqa: E402

os.makedirs(OUT, exist_ok=True)
rows = json.load(io.open(os.path.join(SP, 'final_rows.json'), encoding='utf-8'))
docs_note = json.load(io.open(os.path.join(SP, 'final_docs.json'), encoding='utf-8'))
man = {r['file']: r for r in csv.DictReader(io.open(os.path.join(ROOT, 'manifest.csv'), encoding='utf-8-sig'))}

# ---- R09 표: 제조사 속성(국가·생산 위치·사업분야·순위)
r09 = {}
sec = None
for line in io.open(R09, encoding='utf-8'):
    m = re.match(r'##\s+(\d+)\.\s', line)
    if m:
        sec = int(m.group(1))
        continue
    c = [x.strip() for x in line.strip().strip('|').split('|')]
    if sec and len(c) == 5 and c[0].isdigit():
        r09[(sec, c[1])] = {'rank': int(c[0]), 'country': c[2], 'fab': c[3], 'biz': c[4]}
SEC = {'MCU': 2, 'MOSFET': 3, 'Resistor': 4, 'Capacitor': 5, 'Inductor': 6, 'Power_IC': 7, 'Diode': 8, 'Driver_IC': 9, 'Sensor': 12, 'Wireless_IC': 13, 'Connector': 15}

TITLE = Font(name='맑은 고딕', size=14, bold=True)
NOTE = Font(name='맑은 고딕', size=9, color='555555')
HEAD = Font(name='맑은 고딕', size=10, bold=True)
BODY = Font(name='Tahoma', size=10)
FILL = PatternFill('solid', fgColor='CCFFCC')
THIN = Side(style='thin', color='BFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def sheet(ws, title, note, headers, widths, data, freeze_col=1):
    ws['A1'] = title
    ws['A1'].font = TITLE
    ws['A2'] = note
    ws['A2'].font = NOTE
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        c = ws.cell(3, i, h)
        c.font, c.fill, c.border = HEAD, FILL, BORDER
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[3].height = 30
    for r, row in enumerate(data, 4):
        for i, v in enumerate(row, 1):
            c = ws.cell(r, i, v if v not in ('', None) else None)
            c.font, c.border = BODY, BORDER
            c.alignment = Alignment(vertical='top', wrap_text=True)
    ws.freeze_panes = ws.cell(4, freeze_col + 1)
    ws.auto_filter.ref = f"A3:{get_column_letter(len(headers))}{max(3, 3 + len(data))}"


# ---- 문서 정보
def doc_info(rel):
    m = man[rel]
    return m['title'], m['doc_date'], m['pages']


by_dom = collections.defaultdict(list)
for r in rows:
    by_dom[r['domain']].append(r)
ORDER = {d[0]: i for i, d in enumerate(DOMAINS)}

# ---- 도메인별 제품 엑셀
counts = {}
for code, ko, _ in DOMAINS:
    rs = by_dom.get(code, [])
    if not rs:
        continue
    rs = sorted(rs, key=lambda r: (r['vendor'], r['doc'], str(r.get('type') or ''), r['series'], str(r.get('part_number') or '')))
    specs = SPECS[code]
    headers = ['No'] + [h for _, h, _ in HEAD_COLS] + [h for _, h, _ in specs] + [h for _, h, _ in TAIL_COLS]
    widths = [6] + [w for _, _, w in HEAD_COLS] + [w for _, _, w in specs] + [w for _, _, w in TAIL_COLS]
    data = []
    for n, r in enumerate(rs, 1):
        title, date, _ = doc_info(r['doc'])
        row = [n, VENDORS[r['vendor']][0], r['level'], r['series'], r.get('part_number'), r.get('type')]
        row += [(r.get('specs') or {}).get(k) for k, _, _ in specs]
        row += [r.get('note'), title, r['page'], date, r.get('verify')]
        data.append(row)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = '제품 리스트'
    sheet(ws, f'AVL 공급 제품 리스트 · {ko}',
          f'제조사 Selection Guide·Catalog(R13)에서 뽑은 공급 가능 제품. 문서에 인쇄된 사양을 그대로 옮겼고 문서에 없는 값은 비웠다. ERP 코드는 연구소가 설계에 적용할 때 처음 채번하므로 이 표에는 없다. 기준일 2026-11-27',
          headers, widths, data, freeze_col=4)
    # 문서 목록
    ws2 = wb.create_sheet('문서 목록')
    dd = []
    for n, d in enumerate(sorted([x for x in docs_note if x['domain'] == code], key=lambda x: (x['vendor'], x['doc'])), 1):
        title, date, pages = doc_info(d['doc'])
        dd.append([n, VENDORS[d['vendor']][0], title, date, pages, d['doc'], d['rows'], d.get('note')])
    sheet(ws2, f'출처 문서 · {ko}', '이 표의 제품 행이 나온 PDF. 파일은 references/R13_Vendor_Guides/ 아래에 있다(PDF는 git에 올리지 않는다).',
          ['No', '제조사', '문서 제목', '문서 기준일', '쪽 수', '파일(R13 기준)', '추출 행 수', '추출 메모(범위·한계)'], [6, 24, 48, 12, 8, 56, 10, 70], dd, 2)
    # 읽는 법
    ws3 = wb.create_sheet('읽는 법')
    ex = [
        ['구분', '계열 = 시리즈·제품군 한 줄(사양은 범위). 부품번호 = 문서가 형명과 점 사양을 직접 적은 행'],
        ['사양 값', '문서에 인쇄된 표기를 단위와 함께 그대로 옮겼다. 여러 값은 `;` 또는 `, `로 잇는다. 비어 있으면 문서에 없다는 뜻이다'],
        ['한계', '문서 한 권이 그 제조사의 전 제품을 다루지 않는다. 이 표는 확보한 문서에 나온 제품만 담는다. 제조사별 범위는 [문서 목록] 시트'],
        ['ERP 코드', '이 표의 제품에는 ERP 코드를 붙이지 않았다. 연구소가 설계에 적용할 때 사내 기존 품목을 먼저 찾고 없을 때 규칙대로 처음 채번한다(docs/08)'],
        ['단가·재고·납기', '문서에 없고 이 표에 넣지 않는다'],
        ['원문 대조', '제품 행마다 원문 PDF 텍스트와 자동으로 대조했다. 계열명·부품번호가 그 쪽에 있는지는 모든 행이 통과했다. 사양 숫자는 행 일치(부품번호 줄 근처에 있음) · 쪽 일치(같은 쪽에 있음) · 확인 필요(찾지 못함, 열이 밀렸을 수 있다) · 이름·쪽 일치(사양 숫자 없음) · 그림 확인(글꼴이 깨진 문서라 쪽 그림을 직접 대조). 확인 필요 행은 원문을 열어 확인한다'],
    ]
    sheet(ws3, '읽는 법', '', ['항목', '설명'], [16, 120], ex, 1)
    fn = os.path.join(OUT, f'AVL_Parts_{code}.xlsx')
    wb.save(fn)
    counts[code] = len(rs)

# ---- AVL 엑셀
pairs = collections.OrderedDict()
for code, ko, _ in DOMAINS:
    vs = collections.defaultdict(list)
    for r in by_dom.get(code, []):
        vs[r['vendor']].append(r)
    for v, rs in vs.items():
        pairs[(code, v)] = rs
avl_rows = []
cav_cache = collections.defaultdict(list)
for r in csv.DictReader(io.open(os.path.join(ROOT, 'manifest.csv'), encoding='utf-8-sig')):
    if r['caveat']:
        cav_cache[(r['domain'], r['vendor'])].append(r['caveat'])


def short(c):
    return c if len(c) <= 70 else c[:68] + '…'


for (code, v), rs in sorted(pairs.items(), key=lambda kv: (ORDER[kv[0][0]], SEC and r09.get((SEC[kv[0][0]], VENDORS[kv[0][1]][1]), {}).get('rank', 99), kv[0][1])):
    info = r09.get((SEC[code], VENDORS[v][1]), {})
    docs = sorted({r['doc'] for r in rs})
    dates = sorted(doc_info(d)[1] for d in docs)
    titles = [doc_info(d)[0] for d in docs]
    types = sorted({r.get('type') for r in rs if r.get('type')})
    cav = []
    for c in cav_cache.get((code, v), []):
        if c not in cav:
            cav.append(c)
    avl_rows.append([DOMAIN_KO[code], VENDORS[v][0], v, info.get('country'), info.get('fab'), info.get('biz'), info.get('rank'),
                     len(docs), len(rs), ', '.join(types[:8]) + (' 외' if len(types) > 8 else ''), ' / '.join(titles[:3]) + (' 외' if len(titles) > 3 else ''),
                     dates[-1] if dates else None, ' / '.join(short(c) for c in cav[:2])])

wb = openpyxl.Workbook()
ws = wb.active
ws.title = '요약'
summ = []
for code, ko, _ in DOMAINS:
    ps = [k for k in pairs if k[0] == code]
    if not ps:
        continue
    summ.append([ko, len(ps), counts.get(code, 0), len({r['doc'] for r in by_dom[code]}), ', '.join(VENDORS[k[1]][0] for k in sorted(ps, key=lambda k: r09.get((SEC[code], VENDORS[k[1]][1]), {}).get('rank', 99)))])
summ.append(['합계', sum(s[1] for s in summ), sum(s[2] for s in summ), sum(s[3] for s in summ), ''])
sheet(ws, 'DaBOM AVL(Approved Vendor List) · 부품 카테고리별 제조사', '기준일 2026-11-27. 제조사 Selection Guide를 확보한 제조사만 AVL에 올렸다(문서를 확보하지 못한 제조사는 제외). 제조사 속성과 순위는 R09(EP_Vendor_List_by_Category). 시연용이며 실제 승인 여부를 뜻하지 않는다',
      ['카테고리', 'AVL 제조사 수', '공급 제품 행 수', '출처 문서 수(도메인별)', 'AVL 제조사'], [24, 14, 14, 20, 110], summ, 1)
wsA = wb.create_sheet('전체 AVL')
heads = ['No', '카테고리', '제조사', '제조사 키', '국가(HQ)', '주요 생산·파운드리 위치', '주요 사업분야', 'R09 순위', '출처 문서 수', '공급 제품 행 수', '제품 유형', '출처 문서(대표)', '문서 기준일(최신)', '비고(한계)']
wid = [6, 18, 28, 18, 14, 28, 30, 9, 10, 10, 36, 56, 14, 56]
sheet(wsA, 'AVL 전체 목록', '카테고리 × 제조사. 같은 제조사가 여러 카테고리에 있으면 카테고리마다 한 행이다', heads, wid, [[n] + r for n, r in enumerate(avl_rows, 1)], 3)
for code, ko, _ in DOMAINS:
    sub = [r for r in avl_rows if r[0] == ko]
    if not sub:
        continue
    w = wb.create_sheet(ko.replace('/', '·')[:28])
    sheet(w, f'AVL · {ko}', f'{ko} 카테고리의 AVL 제조사. 공급 제품은 AVL_Parts_{code}.xlsx', heads, wid, [[n] + r for n, r in enumerate(sub, 1)], 3)
wb.save(os.path.join(OUT, 'AVL_List.xlsx'))
print('AVL rows', len(avl_rows), 'parts', counts)
