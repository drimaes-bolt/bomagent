# -*- coding: utf-8 -*-
"""목업 데이터 줄에 "avl"을 넣고 이전 [가상] 카탈로그("catalog")를 뺀다. 데이터 줄은 JSON을 읽고 다시 써도 같은 모양이다(검사함).
실행: python -I inject_avl.py <html> <avl_data.json>"""
import io
import json
import sys

path, datap = sys.argv[1], sys.argv[2]
avl = json.loads(io.open(datap, encoding='utf-8').read())
s = io.open(path, encoding='utf-8', newline='').read()
lines = s.split('\n')
idx = [k for k, l in enumerate(lines) if l.startswith('const DATA = ')]
assert len(idx) == 1, idx
line = lines[idx[0]].rstrip('\r')
assert line.endswith('};'), line[-20:]
body = line[len('const DATA = '):-1]
dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
d = json.loads(body)
assert dump(d) == body, '데이터 줄을 다시 써도 같아야 한다'
d.pop('catalog', None)
d['avl'] = avl
lines[idx[0]] = 'const DATA = ' + dump(d) + ';'
io.open(path, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('injected: keys', list(d.keys()), 'data line bytes', len(lines[idx[0]].encode('utf-8')))
