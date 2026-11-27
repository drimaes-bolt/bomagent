# -*- coding: utf-8 -*-
"""Walsin 카탈로그의 '사양 조합' 행(문서에 형명이 없던 행)에 주문 코드(How To Order)로 부품번호를 조립해 채운다.
실행: python derive_walsin_pn.py <입력 final_rows.json[.gz]> <출력 final_rows.json.gz> [--docs <입력 final_docs.json[.gz]> <출력 final_docs.json>] [--report 보고서.txt]

규칙은 두 카탈로그가 직접 인쇄한 것만 쓴다. 문서에 없는 값은 만들지 않고, 조립하지 못한 행은 그대로 두고 비고에 사유를 적는다.
- MLCC(Walsin_MLCC_Catalog_2026-11.pdf): PDF 5쪽 How To Order와 시리즈별 "Explanation of Part Numbers".
  크기+유전체+정전용량+허용오차+정격전압+단자+포장. 정전용량·전압은 "유효숫자 2자리 + 0의 개수, R은 소수점".
  단자·포장은 각 시리즈의 문서 예시 값(C 또는 M 또는 K, T=7인치 릴)을 쓴다. 허용오차가 여러 개인 칸은 허용오차마다 한 행으로 푼다.
- 칩 저항(Walsin_Chip_Resistor_Catalog_2025.pdf): PDF 4쪽 How To Order. WW(저저항)는 시리즈명+저항 코드+허용오차+T+L,
  WA04P(감쇠기)는 PDF 21쪽 규칙(WA04P+감쇠량+X+허용오차+T+L). 저항 범위만 있는 계열 행은 값이 정해지지 않아 건드리지 않는다.
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

MLCC_DOC = 'Capacitor/Walsin/Walsin_MLCC_Catalog_2026-11.pdf'
RES_DOC = 'Resistor/Walsin/Walsin_Chip_Resistor_Catalog_2025.pdf'
TAG = '주문 코드 조합'

# --- 5쪽 How To Order 글자표 ---
DIEL = {'NP0': 'N', 'X8G': 'G', 'X7R': 'B', 'X7S': 'A', 'X7T': 'T', 'X7P': 'P', 'X6S': 'S', 'X5R': 'X'}
TOL = {'±0.05pF': 'A', '±0.1pF': 'B', '±0.25pF': 'C', '±0.5pF': 'D', '±1%': 'F', '±2%': 'G', '±5%': 'J', '±10%': 'K', '±20%': 'M',
       '-20/+80%': 'Z', '±0.02pF': 'P', '±0.03pF': 'Q'}
# 시리즈 이름에 쓰는 크기 코드. 문서 목록에 1825가 없다(없는 값은 만들지 않는다)
SIZE2 = {'01005': '02', '0201': '03', '0402': '15', '0505': '11', '0603': '18', '0805': '21', '1111': '22', '1206': '31', '1210': '32',
         '1808': '42', '1812': '43', '2211': '52', '2220': '55', '2225': '56'}
# 시리즈 이름 → (형명 앞머리, 크기 표기: 'inch' 인치 그대로 | 'code' 두 자리 코드, 단자 코드, 문서 예시가 있는 PDF 쪽)
MLCC = {
    'General Purpose Capacitors': ('', 'inch', 'C', 8),
    '01R5 series': ('', 'inch', 'C', 14),
    'Middle & High Voltage Capacitors': ('', 'inch', 'C', 15),
    'High Voltage Capacitors_Surface Coating Type': ('', 'inch', 'M', 18),
    'RF series': ('RF', 'code', 'C', 19), 'UF series': ('UF', 'code', 'C', 21), 'RT series': ('RT', 'code', 'C', 22),
    'HH series': ('HH', 'code', 'C', 23), 'MT series': ('MT', 'code', 'C', 25), 'ST series': ('ST', 'code', 'C', 28),
    'VT series': ('VT', 'code', 'C', 31), 'MG series': ('MG', 'code', 'C', 33), 'HT series': ('HT', 'code', 'C', 36),
    'S2 series': ('S2', 'code', 'K', 38), 'S3 series': ('S3', 'code', 'K', 41), 'SH series, Ag-poly': ('SH', 'code', 'C', 44),
    'SG series, Cu-poly': ('SG', 'code', 'C', 51), 'TT series': ('TT', 'code', 'C', 52), 'FT series': ('FT', 'code', 'C', 53),
    'M series': ('M', 'code', 'L', 54), 'V series': ('V', 'code', 'M', 56),
}
SAFETY = ('S2 series', 'S3 series')
MEGA = ('M series', 'V series')


def cap_code(text):
    """'0.1pF'→'0R1', '4.7µF'→'475'. 두 자리 유효숫자로 나타낼 수 없으면 None"""
    m = re.match(r'^([\d.]+)\s*(pF|nF|µF|μF|uF)$', text.strip())
    if not m:
        return None
    pf = Decimal(m.group(1)) * {'pF': 1, 'nF': 1000, 'µF': 10 ** 6, 'μF': 10 ** 6, 'uF': 10 ** 6}[m.group(2)]
    if pf < 10:
        s = format(pf.normalize(), 'f')
        ip, _, fp = s.partition('.')
        if len(fp) == 1:
            return ip + 'R' + fp if ip != '0' else '0R' + fp           # 1.5→1R5, 0.5→0R5
        if len(fp) == 2 and ip == '0':
            return 'R' + fp                                             # 0.47→R47, 0.05→R05
        if not fp:
            return ip + 'R0'                                            # 1→1R0
        return None
    n, z = int(pf), 0
    while n % 10 == 0 and n >= 100:
        n //= 10
        z += 1
    if n >= 100:
        return None
    return '%02d%d' % (n, z) if n >= 10 else None


def volt_code(v):
    """볼트 값 → 3자리 코드. 4→4R0, 6.3→6R3, 100→101, 1000→102. 1250V만 문서 범례의 12E"""
    v = Decimal(str(v))
    if v == 1250:
        return '12E'
    if v < 10:
        return format(v, '.1f').replace('.', 'R')
    n, z = int(v), 0
    while n % 10 == 0 and n >= 100:
        n //= 10
        z += 1
    return '%02d%d' % (n, z) if n < 100 else None


def parse_volts(text):
    m = re.match(r'^([\d.]+)V$', (text or '').strip())
    return m.group(1) if m else None


def split_tol(t):
    return [x.strip() for x in re.split(r',\s*', t or '') if x.strip()]


def derive_mlcc(r):
    """→ ([(부품번호, 허용오차 글자, 허용오차 표기)], 비고 규칙문, None) 또는 (None, None, 실패 사유)"""
    s, sp, note = r['series'], r['specs'], r.get('note') or ''
    if s not in MLCC:
        return None, None, '이 시리즈의 형명 설명을 읽지 않음'
    pre, size_mode, term, expl = MLCC[s]
    size = sp.get('size_inch')
    if size_mode == 'code':
        sz = SIZE2.get(size)
        if not sz:
            return None, None, '크기 %s의 코드가 주문 코드 목록에 없음' % size
    else:
        sz = '01R5' if size == '01005' else size
    diel = DIEL.get(sp.get('dielectric'))
    if not diel:
        return None, None, '유전체 %s의 코드가 없음' % sp.get('dielectric')
    cap = cap_code(sp.get('capacitance') or '')
    if not cap:
        return None, None, '정전용량 %s를 코드로 쓸 수 없음' % sp.get('capacitance')
    thk = (re.search(r'thickness symbol ([A-Z])', sp.get('features') or '') or [None, None])[1]
    if s in SAFETY:
        m = re.search(r'peak impulse (\d+)V', sp.get('features') or '')
        volt = volt_code(m.group(1)) if m else None
        if not volt:
            return None, None, '서지(임펄스) 전압을 찾지 못함'
        if "'+' 표시: 표면 코팅" in note:
            term = 'M'
        elif "'+' 표시(문서에 각주 없음)" in note:
            return None, None, "'+' 표시에 각주가 없어 단자 코드(K 또는 M)를 정할 수 없음"
    else:
        vt = parse_volts(sp.get('voltage'))
        volt = volt_code(vt) if vt else None
        if not volt:
            return None, None, '전압 %s를 코드로 쓸 수 없음' % sp.get('voltage')
    tols = split_tol(sp.get('tolerance'))
    tol_note = ''
    if not tols:
        if s == 'FT series':
            tols, tol_note = ['±20%'], '; 허용오차 M은 같은 쪽 형명표가 모두 ±20%라서'
        elif s == 'M series':
            tols, tol_note = ['±10%'], '; 허용오차 K는 문서 예시 기준(별표 칸만 M)'
        else:
            return None, None, '허용오차가 없음'
    pkg = 'G' if thk == 'R' and size in ('1825', '2220', '2225') else 'T'
    out = []
    for t in tols:
        tc = TOL.get(t)
        if not tc:
            return None, None, '허용오차 %s의 코드가 없음' % t
        if s in MEGA:
            mm = re.search(r'적층 (\d)칩', note)
            if not mm or not thk:
                return None, None, '적층 수 또는 두께 기호가 없음'
            pn = '%s%s%s%s%s%s%s%s%s' % (pre, mm.group(1), sz, diel, cap, tc, volt, thk, term)
        else:
            pn = '%s%s%s%s%s%s%s%s' % (pre, sz, diel, cap, tc, volt, term, pkg)
        out.append((pn, tc, t))
    if s in MEGA:
        rule = '주문 코드로 조립(PDF %d쪽 형명 설명): 적층 수·두께 코드 포함, 제어 코드 %s 기준%s' % (expl, term, tol_note)
    elif s in SAFETY:
        rule = '주문 코드로 조립(PDF %d쪽 형명 설명): 전압 코드는 서지 전압, 단자 %s·포장 T 기준%s' % (expl, term, tol_note)
    else:
        rule = '주문 코드로 조립(PDF 5·%d쪽): 단자 %s·포장 %s(%s 릴) 기준%s' % (expl, term, pkg, '7인치' if pkg == 'T' else '13인치', tol_note)
    return out, rule, None


def mohm_code(text):
    """'0.5mΩ'→'R0L5', '0.75mΩ'→'0L75', '15.5mΩ'→'15L5', '5mΩ'→'R005', '100mΩ'→'R100' (PDF 4쪽 저항 코드 예)"""
    m = re.match(r'^([\d.]+)\s*(mΩ|Ω)$', text.strip())
    if not m:
        return None
    mo = Decimal(m.group(1)) * (1000 if m.group(2) == 'Ω' else 1)
    if mo == mo.to_integral_value():
        return 'R%03d' % int(mo) if mo < 1000 else None
    ip, _, fp = format(mo.normalize(), 'f').partition('.')
    c = ip + 'L' + fp
    c = 'R' + c if len(c) == 3 else c
    return c if len(c) == 4 else None


RES_TOL = {'±0.5%': 'D', '±1%': 'F', '±2%': 'G', '±5%': 'J'}
DB_TOL = {'±0.1dB': 'A', '±0.3dB': 'B', '±0.4dB': 'C', '±0.8dB': 'D', '±1.0dB': 'E', '±1.5dB': 'F', '±2.0dB': 'G', '±2.5dB': 'H'}


def derive_res(r):
    s, sp = r['series'], r['specs']
    if re.match(r'^WW\d\d[A-Z]$', s):
        code = mohm_code(sp.get('resistance') or '')
        if not code:
            return None, None, '저항값 %s를 코드로 쓸 수 없음' % sp.get('resistance')
        out = []
        for t in split_tol(sp.get('tolerance')):
            tc = RES_TOL.get(t)
            if not tc:
                return None, None, '허용오차 %s의 코드가 없음' % t
            out.append((s + code + tc + 'TL', tc, t))
        if not out:
            return None, None, '허용오차가 없음'
        return out, '주문 코드로 조립(PDF 4쪽): 저항 코드+허용오차+포장 T+단자 L. 전력·TCR 접미 코드는 제외', None
    if s == 'WA04P':
        m = re.search(r'attenuator, ([\d.]+)dB', sp.get('features') or '')
        if not m:
            return None, None, '감쇠량을 찾지 못함'
        db = Decimal(m.group(1))
        code = 'R05' if db == Decimal('0.5') else 'R15' if db == Decimal('1.5') else '%03d' % int(db) if db == db.to_integral_value() else None
        if not code:
            return None, None, '감쇠량 코드가 없음'
        t = (sp.get('tolerance') or '').strip()
        tc = DB_TOL.get(t, 'P' if t in ('', '-') else None)
        if not tc:
            return None, None, '허용오차 %s의 코드가 없음' % t
        return [('WA04P' + code + 'X' + tc + 'TL', tc, t)], '주문 코드로 조립(PDF 21쪽): 감쇠량+임피던스 X(50Ω)+허용오차+포장 T+단자 L', None
    return None, None, '저항값이 구간으로만 인쇄되어 형명을 하나로 정할 수 없음'


def residual(note):
    n = re.sub(r"^사양 조합\(문서에 형명 없음\)[;:]?\s*", '', note or '')
    n = re.sub(r"칸 기호 '[A-Z]'=제품 두께 기호\(외형 표 7쪽\);?\s*", '', n)
    n = re.sub(r"적층 \d칩;?\s*", '', n)
    return n.strip(' ;')


def load(p):
    return json.load(gzip.open(p, 'rt', encoding='utf-8')) if p.endswith('.gz') else json.load(io.open(p, encoding='utf-8'))


rows = load(SRC)
printed = {(r['domain'], r['vendor'], (r.get('part_number') or '').upper()) for r in rows if r.get('part_number')}
out, stat, fails, dup = [], collections.Counter(), collections.Counter(), 0
seen = {}
for r in rows:
    if r['vendor'] != 'Walsin' or r['level'] != '사양 조합' or r.get('part_number') or r['doc'] not in (MLCC_DOC, RES_DOC):
        out.append(r)
        continue
    fn = derive_mlcc if r['doc'] == MLCC_DOC else derive_res
    pns, rule, why = fn(r)
    kind = 'MLCC' if r['doc'] == MLCC_DOC else '저항'
    if why:
        n = copy.deepcopy(r)
        n['note'] = (r.get('note') or '') + ' / 형명 미조립: ' + why
        out.append(n)
        fails[(kind, r['series'], why)] += 1
        continue
    stat[kind + ' 원본 사양 조합 행'] += 1
    for pn, tc, tt in pns:
        k = (r['domain'], r['vendor'], pn.upper())
        if k in printed:
            stat[kind + ' 문서에 인쇄된 형명과 같아 뺌'] += 1
            continue
        if k in seen:   # 안전 인증 시리즈(S2·S3)의 UL/TUV 열과 CQC 열은 형명 규칙이 같다. 같은 제품이라 한 행으로 합치고 인증 표기를 같이 남긴다
            prev = seen[k]
            v = (r['specs'].get('voltage') or '').strip()
            pf, rf = prev['specs'].get('features') or '', r['specs'].get('features') or ''
            if 'CQC' in rf and 'CQC' not in pf and 'UL/TUV' in pf:
                prev['specs']['features'] = pf.replace('UL/TUV', 'UL/TUV, CQC')
                if v:
                    prev['specs']['voltage'] = (prev['specs'].get('voltage') or '') + '; CQC ' + v
            elif 'UL/TUV' in rf and 'UL/TUV' not in pf and 'CQC' in pf:
                prev['specs']['features'] = pf.replace('CQC', 'UL/TUV, CQC')
                if v:
                    prev['specs']['voltage'] = v + '; CQC ' + (prev['specs'].get('voltage') or '')
            dup += 1
            stat[kind + ' 같은 형명 합침'] += 1
            continue
        n = copy.deepcopy(r)
        n['part_number'] = pn
        n['level'] = '부품번호'
        n['specs']['tolerance'] = tt
        res = residual(r.get('note'))
        n['note'] = rule + ('; ' + res if res else '')
        n['verify'] = TAG if r.get('verify') == '쪽 일치' else TAG + '·' + (r.get('verify') or '')
        seen[k] = n
        out.append(n)
        stat[kind + ' 조립한 형명 행'] += 1

if DOCS:   # 엑셀 '출처 문서' 시트가 쓰는 문서별 행 수와 메모
    docs = load(DOCS[0])
    cnt = collections.Counter((r['domain'], r['doc'], r['level']) for r in out)
    for d in docs:
        if d['doc'] in (MLCC_DOC, RES_DOC) and d['vendor'] == 'Walsin':
            k = 'MLCC' if d['doc'] == MLCC_DOC else '저항'
            nf = sum(n for (kk, _, _), n in fails.items() if kk == k)
            d['rows'] = sum(n for (dm, dc, lv), n in cnt.items() if dc == d['doc'])
            d['individual'] = cnt[(d['domain'], d['doc'], '부품번호')] + cnt[(d['domain'], d['doc'], '사양 조합')]
            d['series_only'] = cnt[(d['domain'], d['doc'], '계열')]
            d['note'] = (d.get('note') or '') + (' [2026-11-27 갱신] 형명 없이 풀었던 사양 조합 칸 %d개 중 %d개에 문서의 주문 코드 규칙으로 형명을 조립해 채웠다'
                                                 '(원문 대조 "주문 코드 조합", 허용오차가 여럿인 칸은 허용오차마다 한 행). 조립하지 못한 %d행은 사유를 비고에 적었다.' % (stat[k + ' 원본 사양 조합 행'] + nf, stat[k + ' 원본 사양 조합 행'], nf))
    io.open(DOCS[1], 'w', encoding='utf-8').write(json.dumps(docs, ensure_ascii=False))

rep = ['입력 %d행 → 출력 %d행' % (len(rows), len(out))]
rep += ['%s: %d' % kv for kv in sorted(stat.items())]
rep.append('--- 조립하지 못한 행(사유별) ---')
for (kind, s, why), n in sorted(fails.items(), key=lambda x: -x[1]):
    rep.append('%6d  %s | %s | %s' % (n, kind, s, why))
rep.append('조립하지 못한 행 합계 %d' % sum(fails.values()))
print('\n'.join(rep))
if REPORT:
    io.open(REPORT, 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
with gzip.open(DST, 'wt', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
