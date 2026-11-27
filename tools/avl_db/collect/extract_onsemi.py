# -*- coding: utf-8 -*-
"""onsemi 제품 선택기의 공식 `Export > CSV`(소분류 페이지별) → AVL 행.
열 이름이 소분류마다 다르므로 열 이름 별칭 표로 사양 열에 대응시킨다. 'Reference Price'(참고 단가)는 읽지도 옮기지도 않는다.
실행: python extract_onsemi.py <csv 폴더> <출력 json>"""
import csv
import glob
import io
import json
import os
import re
import sys

SRC, OUT = sys.argv[1:3]
CFG = {
    # 파일 이름: (도메인, 제품 유형 이름, 계열 열 후보)
    'mosfet-low-medium': ('MOSFET', '저·중전압 MOSFET', ['Silicon Family']),
    'mosfet-high-voltage': ('MOSFET', '고전압 MOSFET', ['Silicon Family']),
    'mosfet-small-signal': ('MOSFET', '소신호 MOSFET', ['Silicon Family']),
    'mosfet-sic': ('MOSFET', 'SiC MOSFET', ['Family']),
    'mosfet-gan': ('MOSFET', 'GaN FET', ['Family']),
    'pic-offline-controllers': ('Power_IC', 'AC-DC 오프라인 컨트롤러', ['Topology']),
    'pic-offline-regulators': ('Power_IC', 'AC-DC 오프라인 레귤레이터', ['Control Mode']),
    'pic-pfc': ('Power_IC', 'PFC 컨트롤러', ['PFC Mode']),
    'pic-secondary-side': ('Power_IC', '2차측 컨트롤러', []),
    'pic-dcdc-controllers': ('Power_IC', 'DC-DC 컨트롤러', ['Topology']),
    'pic-dcdc-converters': ('Power_IC', 'DC-DC 컨버터', ['Topology']),
    'pic-led-drivers': ('Power_IC', 'LED 드라이버', ['Topology']),
    'drv-integrated-driver-mosfet': ('Driver_IC', '드라이버 + MOSFET 통합', []),
    'diode-rectifiers': ('Diode', '정류 다이오드', ['Type']),
    'diode-schottky': ('Diode', '쇼트키 다이오드', ['Configuration']),
    'diode-zener': ('Diode', '제너 다이오드', ['Type']),
    'diode-small-signal-switching': ('Diode', '소신호 스위칭 다이오드', ['Type']),
    'diode-esd': ('Diode', 'ESD 보호 다이오드', ['Type']),
    'diode-rf': ('Diode', 'RF 다이오드', ['Type']),
    'diode-sic': ('Diode', 'SiC 다이오드', ['Family']),
}
# 사양 키 → 열 이름 후보(앞에서부터 값이 있는 첫 열). 단위는 열 이름에 있으므로 값 뒤에 붙인다.
ALIAS = {
    'MOSFET': {
        'polarity': [('Channel Polarity', '')],
        'vds': [('V(BR)DSS Min (V)', 'V'), ('Blocking Voltage BVDSS (V)', 'V'), ('VDS (V)', 'V'), ('BVDSS (V)', 'V')],
        'rds_on': [('RDS(on) Max @ VGS = 10 V (mΩ)', 'mΩ@10V'), ('RDS(on) Max @ VGS = 4.5 V (mΩ)', 'mΩ@4.5V'), ('RDS(on) Max @ VGS = 2.5 V (mΩ)', 'mΩ@2.5V'),
                   ('RDS(on) Typ @ 25°C (mΩ)', 'mΩ typ')],
        'id': [('ID Max (A)', 'A'), ('Id Max (A)', 'A'), ('ID(max) (A)', 'A')],
        'package': [('Package Name', ''), ('Package Type', '')],
        'technology': [('Silicon Family', ''), ('Family', '')],
        'qg': [('Qg Typ @ VGS = 10 V (nC)', 'nC@10V'), ('Qg Typ @ VGS = 4.5 V (nC)', 'nC@4.5V'), ('Qg Total (nC)', 'nC')],
        'features': [('Gate Level', ''), ('Configuration', '')],
    },
    'Power_IC': {
        'topology': [('Topology', ''), ('PFC Mode', ''), ('Control Mode', '')],
        'vout': [('VO Typ (V)', 'V'), ('VOUT (V)', 'V'), ('Vref Typ (V)', 'V ref')],
        'iout': [('IO Typ (A)', 'A'), ('IO Max (A)', 'A'), ('ICC Max (A)', 'A')],
        'freq': [('fSW Typ (kHz)', 'kHz'), ('fsw Typ (kHz)', 'kHz'), ('fSW (kHz)', 'kHz')],
        'package': [('Package Type', '')],
        'features': [('Control Mode', ''), ('V(BR)DSS Max (V)', 'V BVDSS'), ('RDS(ON) Typ (Ω)', 'Ω RDS(on)'), ('Frequency Operation', 'freq.'), ('Efficiency (%)', '% eff.')],
    },
    'Driver_IC': {
        'channels': [],
        'voltage': [('VIN (V) Typ', 'V'), ('VCIN (V) Typ', 'V')],
        'current': [('IO (A) Max', 'A')],
        'package': [('Package Type', '')],
        'features': [('PWM Level', ''), ('fmax (MHz) Max', 'MHz max')],
    },
    'Diode': {
        'v_rrm': [('VRRM Max (V)', 'V'), ('VRRM Min (V)', 'V'), ('VR Min (V)', 'V'), ('V(BR) Min (V)', 'V'), ('VR Max (V)', 'V'), ('VRWM Max (V)', 'V'), ('VZ Nom (V)', 'V'), ('VZ Typ (V)', 'V'), ('VZ (V)', 'V'), ('Blocking Voltage VRRM (V)', 'V'), ('VRRM (V)', 'V')],
        'i_f': [('IO(rec) Max (A)', 'A'), ('IF Max (A)', 'A'), ('IO Max (A)', 'A'), ('IF(AV) Max (A)', 'A'), ('IF (A)', 'A'), ('IF(max) (A)', 'A'), ('IF(ave) (A)', 'A')],
        'v_f': [('VFM Max (V)', 'V'), ('VF Max (V)', 'V'), ('VF Typ (V)', 'V'), ('VF (Max)', 'V')],
        'channels': [('Configuration', ''), ('Channels', ''), ('Number of Channels', ''), ('Number of Lines', '선')],
        'package': [('Package Type', '')],
        'features': [('Type', ''), ('Family', ''), ('Interface', ''), ('Direction', ''), ('trr Max (ns)', 'ns trr'), ('C Max (pF)', 'pF'), ('CD Max (pF)', 'pF'), ('Cj Max (pF)', 'pF'), ('PPK Max (W)', 'W PPK'), ('IFSM Max (A)', 'A IFSM'), ('Package Size (mm)', 'mm')],
    },
}
BOOLS = ['Stand-by Mode', 'Short Circuit Protection', 'Soft Start', 'Latch', 'Brown-out', 'Over Power Compensation', 'UVP', 'Inhibition', 'UVLO']
PUNCT = re.compile(r'[\s,;]+$')


def norm(h):
    return re.sub(r'\s+', ' ', (h or '').strip())


def clean(v):
    v = PUNCT.sub('', (v or '').strip())
    v = re.sub(r'\s+', ' ', v)
    return None if v in ('', '-', '- -', '-, -') else v


rows, unmapped, per = [], {}, {}
for path in sorted(glob.glob(os.path.join(SRC, '*.csv'))):
    label = os.path.basename(path)[:-4]
    if label not in CFG:
        continue
    dom, tname, serkeys = CFG[label]
    text = io.open(path, encoding='utf-8-sig', errors='replace').read()
    rd = list(csv.reader(io.StringIO(text)))
    hdr = [norm(h) for h in rd[0]]
    hi = {h: i for i, h in enumerate(hdr) if h}
    used = set()
    n = 0
    for r in rd[1:]:
        if not r or not r[0].strip():
            continue
        g = lambda k: clean(r[hi[k]]) if k in hi and hi[k] < len(r) else None
        sp = {}
        for key, cands in ALIAS[dom].items():
            if key == 'features':
                vals = []
                for col, unit in cands:
                    v = g(col)
                    if v is not None:
                        used.add(col)
                        vals.append(v + (' ' + unit if unit else ''))
                if dom == 'Power_IC':
                    for col in BOOLS:
                        if g(col) == 'Yes':
                            used.add(col)
                            vals.append(col)
                if vals:
                    sp['features'] = '; '.join(dict.fromkeys(vals))
                continue
            for col, unit in cands:
                v = g(col)
                if v is not None:
                    used.add(col)
                    sp[key] = v + unit
                    break
        if dom == 'Power_IC':
            lo = g('VCC Min (V)') or g('VIN Min (V)')
            hv = g('VCC Max (V)') or g('VIN Max (V)')
            used.update(['VCC Min (V)', 'VCC Max (V)', 'VIN Min (V)', 'VIN Max (V)'])
            if lo and hv:
                sp['vin'] = lo + '~' + hv + 'V'
            elif hv:
                sp['vin'] = hv + 'V max'
            elif lo:
                sp['vin'] = lo + 'V min'
        # 온도: TA Min/Max, Tj Max
        if g('TA Min (°C)') and g('TA Max (°C)'):
            sp['temp'] = g('TA Min (°C)') + '~' + g('TA Max (°C)') + '°C'
            used.update(['TA Min (°C)', 'TA Max (°C)'])
        elif g('Tj Max (°C)'):
            sp['temp'] = 'Tj max ' + g('Tj Max (°C)') + '°C'
            used.add('Tj Max (°C)')
        sp = {k: v for k, v in sp.items() if v}
        series = None
        for k in serkeys:
            if g(k):
                series = g(k)
                used.add(k)
                break
        pn = g('Product Group')
        st = g('Status')
        rows.append({'domain': dom, 'agent': 'private:onsemi-export', 'vendor': 'onsemi', 'doc': dom + '/onsemi/Product_Selector_Export_' + label, 'page': None, 'level': '부품번호',
                     'series': series or tname, 'part_number': pn, 'type': tname, 'specs': sp, 'note': ('상태: ' + st) if st else None, 'verify': '공식 내보내기'})
        n += 1
    per[label] = n
    unmapped[label] = [h for h in hdr if h and h not in used and h not in ('Product Group', 'Status', 'Compliance', 'Reference Price', 'MSL Type', 'MSL Temp (°C)')]
docs = []
for label, n in per.items():
    dom, tname, _ = CFG[label]
    docs.append({'domain': dom, 'vendor': 'onsemi', 'file': dom + '/onsemi/Product_Selector_Export_' + label, 'title': 'onsemi 제품 선택기 Export(CSV): ' + tname, 'doc_type': 'Official export (CSV)',
                 'doc_date': '2026-11', 'pages': 0, 'source_url': 'https://www.onsemi.com/products/', 'policy': '공식 내보내기. 약관: 복제·재배포 제한 문구 있음. robots Crawl-delay 10 준수', 'agent_note': '참고 단가 열은 제외'})
io.open(OUT, 'w', encoding='utf-8').write(json.dumps({'docs': docs, 'rows': rows}, ensure_ascii=False))
print('rows', len(rows), per)
for k, v in unmapped.items():
    print(k, 'unmapped:', v)
