# -*- coding: utf-8 -*-
"""기획 현황판 만들기.

docs/의 표(기능·화면·질의·결정·미결·데이터 준비)와 문서별 변경 이력을 읽어
briefing/DaBOM_plan_board_20261123.html 한 파일을 만든다.

실행(폴더 루트에서):  python tools/build_plan_board.py
- 표준 라이브러리만 쓴다. 문서를 고친 뒤 다시 실행하면 현황판이 갱신된다.
- 화면 모양은 tools/plan_board_template.html 에 있다. 이 스크립트는 그 안의
  /*__PLAN_DATA__*/ 자리에 JSON을 넣기만 한다.
- 표를 읽는 규칙: 각 문서 표의 첫 칸이 ID 형식(예: MAT-10, DEC-13, `rnd/import`)인 행만 읽는다.
"""
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, 'tools', 'plan_board_template.html')
OUT = os.path.join(ROOT, 'briefing', 'DaBOM_plan_board_20261123.html')

MODS = ['IMP', 'MAT', 'BLD', 'COD', 'CFM', 'TRK', 'ALR', 'CST', 'MDM', 'PRD', 'QLT']
DEPTS = [('rnd', '연구소'), ('pm', '생산관리'), ('pe', '생산기술'), ('mp', '자재/구매'),
         ('acc', '회계'), ('qa', '품질'), ('mdm', '기준정보'), ('sales', '영업')]
ID_RE = re.compile(r'\b(' + '|'.join(MODS) + r')-(\d{2})((?:\s*[~·]\s*\d{2})*)')
BARE_RE = re.compile(r'`(' + '|'.join(MODS) + r')`')
Q_RE = re.compile(r'\b([DPMFQ])-(\d+)')


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def table_rows(md, first):
    """첫 칸이 정규식 first 와 맞는 표 행"""
    out = []
    for line in md.split('\n'):
        if line.startswith('|'):
            c = cells(line)
            if c and re.fullmatch(first, c[0]):
                out.append(c)
    return out


def clean(s):
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)   # 링크 → 글자
    return s.replace('`', '').replace('**', '').strip()


def ids_in(text):
    t = text.replace('`', '')
    out = []
    for m in ID_RE.finditer(t):
        mod, prev, rest = m.group(1), int(m.group(2)), m.group(3)
        nums = [prev]
        for sep, n in re.findall(r'([~·])\s*(\d{2})', rest):
            n = int(n)
            nums += list(range(prev + 1, n + 1)) if sep == '~' else [n]
            prev = n
        out += [f'{mod}-{x:02d}' for x in nums]
    return list(dict.fromkeys(out))


def stage_key(s):
    if '범위 밖' in s:
        return 'out'
    m = re.search(r'\d', s)
    return m.group(0) if m else 'tbd'


def users_to_depts(text):
    m = {'연구소': 'rnd', '구매': 'mp', '자재': 'mp', '생산관리': 'pm', '생산기술': 'pe', '회계': 'acc',
         '품질': 'qa', '기준정보': 'mdm', '관리자': 'mdm', '영업': 'sales'}
    out = [v for k, v in m.items() if k in text]
    if '전 부서' in text:
        out += ['rnd', 'pm', 'mp']
    return list(dict.fromkeys(out))


def main():
    d04, d13, d03, d11, d05 = (read(f'docs/{n}') for n in
                                ['04_기능_범위.md', '13_화면_목록.md', '03_부서별_활용.md', '11_결정_미결_목록.md', '05_데이터와_ERP연동.md'])

    modules = [{'code': clean(c[0]), 'name': clean(c[1]), 'purpose': clean(c[2]), 'users': clean(c[3]), 'stage': clean(c[4])}
               for c in table_rows(d04, r'`(' + '|'.join(MODS) + r')`') if len(c) >= 5]   # 1장 모듈 표(5열)만. 3장 범위 표(2열)는 뺀다
    mod_users = {m['code']: users_to_depts(m['users']) for m in modules}

    feats = []
    for c in table_rows(d04, r'(' + '|'.join(MODS) + r')-\d{2}'):
        basis = clean(c[4]) if len(c) > 4 else ''
        mod = c[0][:3]
        feats.append({'id': c[0], 'mod': mod, 'name': clean(c[1]), 'desc': clean(c[2]), 'stage': clean(c[3]),
                      'sk': stage_key(c[3]), 'basis': basis, 'screens': [], 'depts': [], 'queries': [],
                      'isNew': bool(re.search(r'docs/14|DEC-1[3-7]', basis)) or mod in ('PRD', 'QLT')})
    F = {f['id']: f for f in feats}

    # 화면
    screens = []
    for c in table_rows(d13, r'`(' + '|'.join(k for k, _ in DEPTS) + r')/[\w-]+`'):
        addr = clean(c[0])
        raw = c[4]
        ids = ids_in(raw)
        bare = BARE_RE.findall(raw)
        sc = {'addr': addr, 'dept': addr.split('/')[0], 'name': clean(c[1]), 'q': clean(c[2]), 'comp': clean(c[3]),
              'refs': clean(raw), 'ids': ids, 'bare': bare, 'stage': clean(c[5]), 'status': clean(c[6])}
        screens.append(sc)
        for fid in ids:
            if fid in F:
                F[fid]['screens'].append(addr)
    # 모듈 이름만 적은 화면(예: `IMP`): ID로 화면이 연결되지 않은 그 모듈의 1단계 기능을 이 화면이 보여 준다고 본다
    explicit = {f['id'] for f in feats if f['screens']}
    for sc in screens:
        for mod in sc['bare']:
            for f in feats:
                if f['mod'] == mod and f['sk'] == '1' and f['id'] not in explicit and sc['addr'] not in f['screens']:
                    f['screens'].append(sc['addr'])
    S = {s['addr']: s for s in screens}

    # 질의
    queries = []
    for c in table_rows(d03, r'[DPMFQ]-\d+(~[DPMFQ]-\d+)?'):
        qid = c[0]
        dept = {'D': 'rnd', 'P': 'mp', 'M': 'pm', 'F': 'acc', 'Q': 'qa'}[qid[0]]
        if '생산기술' in c[1]:
            dept = 'pe'
        fs = ids_in(c[-1])
        queries.append({'id': qid, 'dept': dept, 'sit': clean(c[1]), 'ex': clean(c[2]), 'out': clean(c[3]), 'feats': fs})
        for fid in fs:
            if fid in F and qid not in F[fid]['queries']:
                F[fid]['queries'].append(qid)
    QD = {q['id']: q['dept'] for q in queries}

    for f in feats:
        ds = [S[a]['dept'] for a in f['screens']] + [QD[q] for q in f['queries'] if q in QD]
        if not ds:
            ds = mod_users.get(f['mod'], [])
        f['depts'] = [k for k, _ in DEPTS if k in ds]
        st = [S[a]['status'] for a in f['screens']]
        f['status'] = 'demo' if any(x.startswith('시연') for x in st) else 'preview' if st else 'none'

    decisions = [{'id': c[0], 'text': clean(c[1]), 'status': clean(c[2]), 'date': clean(c[3]), 'basis': clean(c[4]), 'doc': clean(c[5])}
                 for c in table_rows(d11, r'DEC-\d+')]
    issues = [{'id': c[0], 'text': clean(c[1]), 'why': clean(c[2]), 'owner': clean(c[3]), 'when': clean(c[4]), 'doc': clean(c[5])}
              for c in table_rows(d11, r'OI-\d+')]
    assumptions = [{'id': c[0], 'text': clean(c[1]), 'basis': clean(c[2])} for c in table_rows(d11, r'AS-\d+')]
    dts = [{'id': c[0], 'data': clean(c[1]), 'now': clean(c[2]), 'how': clean(c[3]), 'owner': clean(c[4]), 'stage': clean(c[5])}
           for c in table_rows(d05, r'DT-\d+')]

    docs = []
    for path in ['README.md'] + sorted(glob.glob(os.path.join(ROOT, 'docs', '*.md'))):
        rel = os.path.relpath(os.path.join(ROOT, path), ROOT).replace('\\', '/')
        md = read(rel)
        title = (re.search(r'^# (.+)$', md, re.M) or [None, rel])[1]
        hist = table_rows(md, r'v[\d.]+')
        last = hist[-1] if hist else ['', '', '']
        docs.append({'file': rel, 'title': clean(title), 'ver': last[0], 'date': last[1], 'last': clean(last[2])})

    data = {
        'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'depts': [{'k': k, 'name': n} for k, n in DEPTS],
        'modules': modules, 'features': feats, 'screens': screens, 'queries': queries,
        'decisions': decisions, 'issues': issues, 'assumptions': assumptions, 'datatasks': dts, 'docs': docs,
        'mockup': 'index.html',
    }
    tpl = open(TPL, encoding='utf-8').read()
    if '/*__PLAN_DATA__*/' not in tpl:
        sys.exit('템플릿에 /*__PLAN_DATA__*/ 자리가 없다')
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = tpl.replace('/*__PLAN_DATA__*/', js)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    n = len(feats)
    print(f'기획 현황판: {os.path.relpath(OUT, ROOT)}')
    print(f'  기능 {n} (시연 {sum(f["status"] == "demo" for f in feats)} · 미리보기 {sum(f["status"] == "preview" for f in feats)} · 화면 없음 {sum(f["status"] == "none" for f in feats)})'
          f' · 화면 {len(screens)} · 질의 {len(queries)} · 결정 {len(decisions)} · 미결 {len(issues)} · 데이터 준비 {len(dts)} · 문서 {len(docs)}')


if __name__ == '__main__':
    main()
