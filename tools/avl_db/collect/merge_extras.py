# -*- coding: utf-8 -*-
"""PDF에서 뽑은 최종 행(기존 + 새 PDF)과 공식 내보내기·오픈 데이터·웹에서 모은 행(extras)을 합친다.
실행: python merge_extras.py <기존 final_rows.json[.gz]> <기존 final_docs.json> <새 PDF 폴더(x_in, 없으면 -)> <extras 폴더> <출력 폴더>
출력: <출력>/final_rows.json, final_docs.json, extras_docs.json(PDF 아닌 문서의 제목·기준일·쪽 수), merge_report.txt
같은 (도메인, 제조사, 부품번호)는 먼저 들어온 행만 쓴다. 순서: 기존 PDF → 새 PDF → extras(파일 이름순). 부품번호가 없는 계열 행은 (도메인, 제조사, 계열, 유형)이 같으면 중복이다."""
import collections
import glob
import gzip
import io
import json
import os
import sys

BASE, BASE_DOCS, XIN, EXD, OUT = sys.argv[1:6]
os.makedirs(OUT, exist_ok=True)


def load(p):
    if p.endswith('.gz'):
        return json.load(gzip.open(p, 'rt', encoding='utf-8'))
    return json.load(io.open(p, encoding='utf-8'))


rows = load(BASE)
docs = load(BASE_DOCS)
extra_docs = []
if XIN != '-':
    for r in load(os.path.join(XIN, 'final_rows.json')):
        rows.append(r)
    docs += load(os.path.join(XIN, 'final_docs.json'))


def key(r):
    pn = (r.get('part_number') or '').strip()
    if pn:
        return (r['domain'], r['vendor'], pn.upper())
    return (r['domain'], r['vendor'], 'S', r.get('doc'), (r.get('series') or '').upper(), (r.get('type') or '').upper(), r.get('level'), json.dumps(r.get('specs') or {}, sort_keys=True, ensure_ascii=False), str(r.get('page')))


seen, out, dropped, src_count = set(), [], collections.Counter(), collections.Counter()
for r in rows:   # PDF에서 뽑은 행은 그대로 둔다(중복 제거 없음). 다른 출처 행이 이것과 겹치는지만 본다
    seen.add(key(r))
    out.append(r)
    src_count['pdf'] += 1
for p in sorted(glob.glob(os.path.join(EXD, '*.json'))):
    d = load(p)
    name = os.path.basename(p)[:-5]
    for doc in d['docs']:
        extra_docs.append(doc)
    for r in d['rows']:
        r.setdefault('page', None)
        r.setdefault('note', None)
        k = key(r)
        if k in seen:
            dropped[name + ' 중복'] += 1
            continue
        seen.add(k)
        out.append(r)
        src_count[name] += 1
cnt = collections.Counter((r['domain'], r['doc']) for r in out)
lv = collections.Counter((r['domain'], r['doc'], r['level']) for r in out)
for d in extra_docs:
    docs.append({'domain': d['domain'], 'doc': d['file'], 'vendor': d['vendor'], 'note': (d.get('policy') or '') + (' / ' + d['agent_note'] if d.get('agent_note') else ''), 'agent': 'extras',
                 'rows': cnt.get((d['domain'], d['file']), 0), 'individual': lv.get((d['domain'], d['file'], '부품번호'), 0) + lv.get((d['domain'], d['file'], '사양 조합'), 0),
                 'series_only': lv.get((d['domain'], d['file'], '계열'), 0)})
json.dump(out, io.open(os.path.join(OUT, 'final_rows.json'), 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(docs, io.open(os.path.join(OUT, 'final_docs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(extra_docs, io.open(os.path.join(OUT, 'extras_docs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
by = collections.Counter(r['domain'] for r in out)
vend = collections.Counter((r['domain'], r['vendor']) for r in out)
rep = ['merged rows %d' % len(out), 'by domain %s' % dict(by), 'sources %s' % dict(src_count), 'dropped %s' % dict(dropped), 'vendor-domain pairs %d' % len(vend)]
io.open(os.path.join(OUT, 'merge_report.txt'), 'w', encoding='utf-8').write('\n'.join(rep))
print('\n'.join(rep))
