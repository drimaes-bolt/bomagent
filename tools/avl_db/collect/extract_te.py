# -*- coding: utf-8 -*-
"""TE Connectivity 공식 제품 정보 파일(Connectors.zip, Excel 데이터 피드)의 *_Attributes.xlsx → AVL 행.
TE 파일은 영국식 단위다(온도 °F, 피치 inch). °C·mm로 환산해 적고 note에 밝힌다. 가격·재고는 파일에 없다.
실행: python extract_te.py <Connectors_excel.zip> <출력 json>"""
import io
import json
import re
import sys
import warnings
import zipfile

import openpyxl

warnings.filterwarnings('ignore')
SRC, OUT = sys.argv[1:3]
STD_PITCH = [0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.635, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0, 1.0, 1.1, 1.25, 1.27, 1.3, 1.5, 1.75, 1.8, 2.0, 2.2, 2.29, 2.5, 2.54, 2.8, 3.0, 3.5, 3.81, 3.96,
             4.0, 4.2, 5.0, 5.08, 6.0, 6.35, 7.0, 7.5, 7.62, 8.0, 8.5, 10.0, 10.16, 12.7, 15.0, 20.0]


def clean(v):
    if v is None:
        return None
    s = str(v).strip()
    return None if s in ('', '-', '—', 'N/A') else s


def pitch_mm(v):
    s = clean(v)
    if not s:
        return None
    try:
        mm = float(s) * 25.4
    except ValueError:
        return None
    if mm < 0.25:   # 0, .003 같은 값은 피치가 아니거나 단위가 다른 칸이라 비운다
        return None
    best = min(STD_PITCH, key=lambda x: abs(x - mm))
    return ('%g' % best) if abs(best - mm) <= 0.02 else ('%.2f' % mm).rstrip('0').rstrip('.')


def temp_c(v):
    s = clean(v)
    if not s:
        return None
    m = re.match(r'^\s*(-?\d+(?:\.\d+)?)\s*[–-]\s*(-?\d+(?:\.\d+)?)\s*$', s.replace('—', '–'))
    if not m:
        return None
    lo, hi = (round((float(x) - 32) * 5 / 9) for x in m.groups())
    return '%d~%d°C' % (lo, hi)


def num(v, unit=''):
    s = clean(v)
    if not s:
        return None
    try:
        f = float(s)
        return ('%g' % f) + unit
    except ValueError:
        return s


z = zipfile.ZipFile(SRC)
rows, per_cat = [], {}
for name in sorted(n for n in z.namelist() if n.endswith('_Attributes.xlsx')):
    wb = openpyxl.load_workbook(io.BytesIO(z.read(name)), read_only=True)
    ws = wb.active
    ws.reset_dimensions()
    it = ws.iter_rows(values_only=True)
    hdr = list(next(it))
    hi = {h: i for i, h in enumerate(hdr) if h}
    n = 0
    for r in it:
        if not r or not r[0]:
            continue
        g = lambda k: clean(r[hi[k]]) if k in hi and hi[k] < len(r) else None
        pn = g('TE Part Number')
        cat = g('End Node Category') or name.replace('_Attributes.xlsx', '')
        series = g('Series') or g('ProductFamily') or cat
        series = ', '.join(dict.fromkeys(x.strip() for x in series.split(',') if x.strip()))[:80]
        mount = g('Connector Mounting Type') or g('PCB Mount Orientation')
        orient = g('PCB Mount Orientation')
        feats = []
        if g('Brand'):
            feats.append(g('Brand'))
        if g('Product Description'):
            feats.append(g('Product Description')[:60])
        if g('Connector System'):
            feats.append(g('Connector System'))
        if g('Connector & Housing Type'):
            feats.append(g('Connector & Housing Type'))
        if orient and orient != mount:
            feats.append(orient)
        if g('Shielded') in ('Yes', 'Shielded'):
            feats.append('Shielded')
        if g('Part Status') and g('Part Status') != 'Active':
            feats.append(g('Part Status'))
        pos = g('Number of Positions') or g('Number of Contacts')
        rw = g('Number of Rows')
        sp = {
            'pitch': pitch_mm(g('Centerline (Pitch)')),
            'positions': (num(pos) + (' (' + num(rw) + '열)' if rw else '')) if pos else None,
            'current': num(g('Contact Current Rating (Max)'), 'A'),
            'voltage': num(g('Operating Voltage'), 'V'),
            'mounting': mount,
            'application': g('Circuit Application'),
            'temp': temp_c(g('Operating Temperature Range')),
            'features': '; '.join(feats) or None,
        }
        sp = {k: v for k, v in sp.items() if v}
        rows.append({'domain': 'Connector', 'agent': 'private:te-excel-feed', 'vendor': 'TE_Connectivity', 'doc': 'Connector/TE_Connectivity/TE_Product_Information_Files_Connectors',
                     'page': None, 'level': '부품번호', 'series': series, 'part_number': pn, 'type': cat, 'specs': sp,
                     'note': 'TE 원본은 inch·°F: 피치는 mm, 온도는 °C로 환산(표준 피치에 맞춰 반올림)', 'verify': '공식 내보내기'})
        n += 1
    per_cat[name.replace('_Attributes.xlsx', '')] = n
doc = {'domain': 'Connector', 'vendor': 'TE_Connectivity', 'file': 'Connector/TE_Connectivity/TE_Product_Information_Files_Connectors',
       'title': 'TE Connectivity Product Information Files - Connectors (Excel data feed)', 'doc_type': 'Official data feed (Excel)', 'doc_date': '2026-11',
       'pages': 0, 'source_url': 'https://www.te.com/en/services/xml-download.html', 'policy': '공식 데이터 피드. 약관: 개인·비상업 다운로드 문구와 피드 안내문이 달라 TE 확인 권장', 'agent_note': '분류별 zip, 119개 소분류'}
io.open(OUT, 'w', encoding='utf-8').write(json.dumps({'docs': [doc], 'rows': rows}, ensure_ascii=False))
print('rows', len(rows), 'categories', len(per_cat))
print(json.dumps(rows[1], ensure_ascii=False)[:700])
print('with pitch', sum(1 for r in rows if 'pitch' in r['specs']), 'temp', sum(1 for r in rows if 'temp' in r['specs']), 'current', sum(1 for r in rows if 'current' in r['specs']))
