# 04 넘기기 전 점검 · 보고

DA UI hallmark v1.0. 결과물을 넘기기 전에 이 문서를 따른다.

검사는 세 단계다. 앞의 둘은 AI가, 마지막은 사람이 한다.

| 단계 | 누가 | 방법 | 이 문서 |
|---|---|---|---|
| 1. 자가 점검 | AI | 아래 항목을 하나씩 확인 | 1~3장 |
| 2. 금지 패턴 검색 | AI (코드 실행을 쓸 수 있을 때) | 4장의 스크립트를 임시 위치에서 실행 | 4장 |
| 3. 브라우저 검사 | 사람 | `checker.html`을 Edge로 열고 결과 파일을 끌어다 놓음 | 6장 |

---

## 1. 공통 점검

- [ ] `<html lang="ko" data-hm-profile="…">`, `<meta name="viewport">`, `<title>`이 있다.
- [ ] HTML 한 파일이다. 다른 파일(이미지·CSS·JS)을 상대 경로로 불러오지 않는다.
- [ ] `:root` 기준값을 바꾸지 않았다. 색은 회사 8색과 무채색만 쓴다. 빨강·주황·노랑·보라·분홍이 없다.
- [ ] 글자는 바탕과 4.5:1 이상이다. `#A0A0A0` 글자가 없다. `--ink-3`를 `--hover`·`--active`·`--b50` 위에 쓰지 않았다.
- [ ] 네이비는 로고, 주 버튼 하나, 선택 표시, 주 데이터, 강조 면에만 있다.
- [ ] 그라데이션, 반투명 흐림, 글로우가 없다. 그림자는 떠 있는 요소에만 `--float`로 있다.
- [ ] 마우스를 올렸을 때 떠오르는 효과가 없다. 등장 애니메이션과 반복 장식이 없다.
- [ ] eyebrow, 장식 번호(01/02), 고정폭 라벨, 대문자 변환, 이모지가 없다.
- [ ] 화면(또는 장)마다 `h1`이 하나이고, 모든 제목이 1440·768·390 폭에서 2줄 이내다.
- [ ] 버튼 이름이 동작을 말한다. 광고 문구, 줄표(—) 습관, 느낌표가 없다.
- [ ] 지어낸 근거가 없다. 시연용 값에 `[가상]` 또는 "예시 값" 표시가 있다. 사람 이름 대신 역할을 썼다.
- [ ] 390px에서 페이지가 옆으로 밀리지 않는다. 누르는 곳이 40px 이상이다.
- [ ] 키보드로 모든 조작이 되고 초점 표시가 보인다. 아이콘 버튼에 `aria-label`이 있다.
- [ ] `prefers-reduced-motion`과 인쇄 스타일이 있다.

## 2. 업무 화면 점검 (`app`)

- [ ] 화면마다 답할 질문이 하나이고, 가장 큰 블록이 그 질문에 답한다.
- [ ] 제품 이름과 범위가 셸에 보인다. 주 업무 동작이 한 번에 닿는다.
- [ ] 회색 틀 + 흰 시트(r16, 1px `--edge`, 그림자 없음)다. 사이드바는 `--frame`이다.
- [ ] 선택된 메뉴는 회색 채움 + 굵게다. 막대·점·글로우가 없다.
- [ ] 지표는 한 상자를 1px로 나눴다. 아이콘·색 원·미니 차트가 없다. 숫자는 48px 미만이다.
- [ ] 표 머리글에 띠·대문자가 없다(엑셀형 표 `data-sheet`만 예외). 줄무늬가 없다. 숫자는 오른쪽 정렬 `tabular-nums`다.
- [ ] 행마다 상태 꼬리표가 하나다. 채운 꼬리표는 보이는 행의 1/5 이하다.
- [ ] 합계는 행에서 계산했고 화면의 숫자끼리 맞는다.
- [ ] 빈 상태, 불러오는 중, 오류, 사용 불가 상태가 있다.
- [ ] 1100px에서 사이드바가 접히고, 640px에서 시트가 화면 전체가 되고 표가 두 줄 목록이 된다.
- [ ] `data-hm-view`와 `window.hmShow`로 모든 화면을 열 수 있다.

## 3. 발표·문서 점검 (`slides`·`doc`)

- [ ] 장(절)마다 주장이 하나다. 둘째 장(첫 절)이 요약이다.
- [ ] 숫자마다 근거가 있다. `[가상]`·`[가안]`·`[제안]` 표시가 빠지지 않았다. 결정 필요 사항을 따로 모았다.
- [ ] 장 제목은 주장 문장이다. 34~38px이고 2줄 이내다. 표지 제목은 52~56px, 2줄 이내다.
- [ ] 1440×900에서 한 장이 한 화면에 들어간다(`slides`).
- [ ] 절 사이 가는 선, 1px 테두리 상자 셋 이상, 같은 모양 카드 격자가 없다.
- [ ] 같은 구성(표·흐름·비교·지표)이 세 장 연속되지 않는다.
- [ ] 쪽 넘김 막대가 시트 아래 평범한 막대이고 쪽수에 0을 채우지 않았다(`slides`).
- [ ] 본문은 16px 이상, 13px 미만 글자가 없다.
- [ ] 인쇄하면 한 장이 한 쪽(`slides`), 문서는 목차·막대가 숨는다.

---

## 4. 금지 패턴 검색

코드 실행을 쓸 수 있으면 아래 스크립트를 **코드 실행 환경의 임시 위치**에 저장해 결과 파일에 돌린다. 사용자 폴더에 스크립트를 남기지 않는다. 파이썬 표준 라이브러리만 쓴다.

```python
# hallmark_scan.py  ·  python hallmark_scan.py 결과.html
import re, sys, colorsys
KEEP = {'000000','555555','a0a0a0','dedede','7dead5','1bbbcc','4383af','06438c'}
LINE_RULES = [
 ('FAIL','그라데이션', r'(linear|radial|conic)-gradient\(|bg-gradient-|background-clip\s*:\s*text|bg-clip-text'),
 ('FAIL','반투명 흐림', r'backdrop-filter\s*:\s*(?!none)|backdrop-blur'),
 ('FAIL','#A0A0A0 글자', r'(?<![-\w])color\s*:\s*#a0a0a0'),
 ('FAIL','대문자 변환', r'text-transform\s*:\s*uppercase|\buppercase\b'),
 ('FAIL','장식 번호', r'>\s*0[1-9]\s*<|decimal-leading-zero|STEP\s*0\d'),
 ('FAIL','eyebrow', r'class\s*=\s*"[^"]*\b(eyebrow|kicker|overline)\b'),
 ('FAIL','자리채움 글', r'lorem ipsum|dolor sit amet|홍길동|김철수|텍스트를 입력|샘플 텍스트|○○○'),
 ('FAIL','이모지', '[\U0001F300-\U0001FAFF\u2600-\u27BF]'),
 ('WARN','고정폭 글꼴(코드 블록이면 무시)', r'font-family\s*:[^;{}]*(monospace|Consolas|Courier|Menlo|D2Coding)|\bfont-mono\b'),
 ('WARN','그림자(떠 있는 요소인지 확인)', r'box-shadow\s*:\s*(?!none|inset)'),
 ('WARN','자간 넓힘', r'letter-spacing\s*:\s*0?\.(0[6-9]|[1-9])\d*em'),
 ('WARN','반복 애니메이션(불러오는 중 표시만 허용)', r'\binfinite\b'),
 ('WARN','줄무늬 표 의심', r'nth-(child|of-type)\((even|odd|2n)'),
 ('WARN','다른 파일을 불러옴', r'(src|href)\s*=\s*"(?!https?:|data:|#|mailto:|javascript:)[^"]+\.(png|jpe?g|gif|svg|webp|css|js)"'),
]
def sat_bad(h):
    r,g,b = (int(h[i:i+2],16)/255 for i in (0,2,4))
    hh,l,s = colorsys.rgb_to_hls(r,g,b)
    return s >= .25 and .12 <= l <= .95 and not (150 <= hh*360 <= 225)
for path in sys.argv[1:]:
    text = open(path, encoding='utf-8').read(); out = []
    for n, line in enumerate(text.splitlines(), 1):
        if len(line) > 2000 or 'hallmark-ignore' in line or 'taste-skill-ignore' in line: continue
        for lv, name, rx in LINE_RULES:
            if re.search(rx, line, re.I): out.append((lv, name, n, line.strip()[:90]))
    for m in re.finditer(r'#([0-9a-fA-F]{6})\b', text):
        h = m.group(1).lower()
        if h not in KEEP and sat_bad(h): out.append(('FAIL','회사 색이 아닌 색', text.count('\n',0,m.start())+1, '#'+h))
    for m in re.finditer(r'box-shadow\s*:[^;{}]*rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\)', text, re.I):
        r,g,b,a = int(m.group(1)),int(m.group(2)),int(m.group(3)),float(m.group(4))
        if 'inset' in m.group(0): continue
        if a > .08 or max(r,g,b)-min(r,g,b) > 30: out.append(('FAIL','진한 그림자·색 그림자', text.count('\n',0,m.start())+1, m.group(0)[:90]))
    if re.search(r':hover[^{]*\{[^}]*transform\s*:\s*(translate|scale)', text, re.I): out.append(('FAIL','마우스 올리면 떠오름', 0, ':hover transform'))
    if 'stroke-dashoffset' in text and 'infinite' in text: out.append(('FAIL','흐르는 점선 애니메이션 의심', 0, 'stroke-dashoffset + infinite'))
    if len(re.findall('—', re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', '', text))) > 2: out.append(('WARN','줄표(—) 3개 이상', 0, ''))
    for need, lv, name in [(r'<html[^>]*lang="ko"', 'FAIL', 'lang="ko" 없음'), (r'name="viewport"', 'FAIL', 'viewport 없음'), (r'<title>', 'WARN', 'title 없음'), (r'data-hm-profile=', 'WARN', 'data-hm-profile 없음')]:
        if not re.search(need, text, re.I): out.append((lv, name, 0, ''))
    out.sort(key=lambda x: (x[0] != 'FAIL', x[2]))
    print(f'== {path}: FAIL {sum(o[0]=="FAIL" for o in out)} · WARN {sum(o[0]=="WARN" for o in out)}')
    for lv, name, n, s in out: print(f'{lv} [{name}] {n}행  {s}')
```

결과를 보고 고친다. 걸린 줄이 `01_foundation.md` 8장의 예외(떠 있는 요소의 그림자 등)라면 그 줄에 `hallmark-ignore: 이유` 주석을 달고, 보고서에 적는다. 이 스크립트는 코드만 본다. 실제로 그려진 화면(제목 줄 수, 넘침, 대비)은 6장의 검사기가 본다.

---

## 5. 보고 양식

결과물을 넘길 때 이 양식으로 쓴다. 하지 않은 검사를 했다고 쓰지 않는다.

```
[hallmark 보고]
- 적용: DA UI hallmark v1.0 · 프로필 app | slides | doc
- 만든 파일: 파일명.html (화면/장 n개: 이름 나열)
- 화면별 질문 또는 장별 주장: 한 줄씩
- 자가 점검(1~3장): 통과 n개, 못 지킨 항목과 이유
- 금지 패턴 검색(4장): 실행함(FAIL n · WARN n, 남긴 것과 이유) | 실행 못 함(이유)
- 브라우저 검사: 아직 안 함. checker.html로 검사해 보고서를 붙여 주세요 | n회차 반영 완료
- 규칙과 다르게 한 것: 사용자 지시, 예외 주석, 외부 라이브러리
- 바꿔야 할 가상 값: [가상]·[가안] 표시한 값 목록
```

---

## 6. 검사기 보고서를 받았을 때

사용자가 `checker.html`의 "보고서 복사" 내용을 붙여 넣으면:

1. FAIL부터 고친다. 같은 원인의 항목은 한 번에 고친다.
2. 다음으로 WARN을 본다. 남길 WARN은 이유를 한 줄로 쓴다(예: "엑셀형 표의 가로 스크롤은 의도").
3. 고친 내용을 5장 양식으로 보고하고 다시 검사해 달라고 한다.
4. 최대 3회 반복한다. 3회 뒤에도 FAIL이 남으면 남은 항목과 이유를 그대로 보고한다.

보고서의 각 항목은 `[규칙 ID] 한국어 이름 · 폭 · 화면`과 측정값, 고칠 방법으로 되어 있다. `hm-`로 시작하는 ID는 hallmark 규칙, 나머지는 taste-skill 규칙이다.

## 7. 화면 캡처를 받았을 때

사용자가 검사기 화면이나 결과물 캡처를 붙여 넣으면, 코드가 아니라 그림만 보고 판단한다.

```
[캡처 검토]
- 1초에 보이는 것: 하나만 (없으면 "없음")
- 가장 큰 것이 화면의 질문(장의 주장)에 답하는가: 예 | 아니오
- 고칠 곳 세 군데 (잘 보이는 순서, 어디에 무엇을 어떻게):
  1. …
  2. …
  3. …
```

고칠 순서: 위계(가장 중요한 것을 가장 크게) → 배치(가장자리 맞춤, 빈 구멍) → 글자(크기 차이, 줄바꿈) → 색(네이비 사용처) → 세부(상태, 휴대폰). 한 번에 세 가지만 고친다.

---

## 변경 이력

| 버전 | 일자 | 내용 |
|---|---|---|
| v1.0 | 2026-10-21 | 최초 작성 |
