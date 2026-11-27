# -*- coding: utf-8 -*-
"""목업 데이터 줄 끝에 "avl":{...}를 붙인다(원본 JSON은 그대로 두고 문자열로 잇는다). 실행: python -I inject_avl.py <html> <avl_data.json>"""
import io
import json
import sys

path, datap = sys.argv[1], sys.argv[2]
avl = io.open(datap, encoding='utf-8').read()
json.loads(avl)   # 유효성
s = io.open(path, encoding='utf-8', newline='').read()
lines = s.split('\n')
idx = [k for k, l in enumerate(lines) if l.startswith('const DATA = ')]
assert len(idx) == 1, idx
line = lines[idx[0]].rstrip('\r')
assert line.endswith('};'), line[-20:]
body = line[len('const DATA = '):-1]
assert body.endswith('}') and '"avl":' not in body[-200:]
d0 = json.loads(body)
assert 'avl' not in d0
lines[idx[0]] = 'const DATA = ' + body[:-1] + ',"avl":' + avl + '};'
out = '\n'.join(lines)
io.open(path, 'w', encoding='utf-8', newline='').write(out)
d1 = json.loads(lines[idx[0]][len('const DATA = '):-1])
assert all(d1[k] == d0[k] for k in d0), '기존 데이터가 바뀌었다'
print('injected: keys', list(d1.keys())[-3:], 'line bytes', len(lines[idx[0]].encode('utf-8')))
