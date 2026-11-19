# CHANGELOG · DA UI hallmark

새 버전을 받으면 이 표부터 본다. 바꾸는 방법은 `GUIDE.html`의 "새 버전으로 바꾸기"에 있다.

| 버전 | 일자 | 내용 |
|---|---|---|
| v1.0 | 2026-10-21 | 최초 배포. 규칙 문서 5개(00~04), 시작 틀 3개(업무 화면·발표·문서), 브라우저 검사기 `checker.html`, 안내 `GUIDE.html`. 사내 웹 키트(`DA_WEBUI_KIT.md` v1.0)보다 우선한다 |

## v1.0 검증 기록 [관측]

v1.0 제작 때 Edge(헤드리스)에서 `checker.html`로 확인했다. 폭은 1440·768·390이다.

| 대상 | 결과 |
|---|---|
| `10_template_app.html` (화면 4개) | FAIL 0 · WARN 0 |
| `11_template_slides.html` (장 9개) | FAIL 0 · WARN 0 |
| `12_template_doc.html` | FAIL 0 · WARN 0 |
| `GUIDE.html` | FAIL 0 · WARN 0 |
| `checker.html` 자체 | 화면 검사 FAIL 0 · WARN 0. 코드 검사는 검사 규칙 문자열("lorem ipsum" 같은 찾을 패턴)을 파일 안에 담고 있어 걸린다. 검사 대상이 아니다 |
| taste 판 다봄 시연 목업 | FAIL 2 · WARN 5. 엑셀형 표에 `data-sheet` 표시가 없어 머리글 띠로 걸리고, 시트 탭의 ◀ ▶ 화살표가 `#A0A0A0`이다. taste-skill 규칙에서 걸린 것은 없다 |
| 사내 키트로 만든 기존 화면 1종 | FAIL 20 · WARN 15 (그라데이션 글자, `#A0A0A0` 글자, 글로우, 카드 그림자, 반투명 흐림, 떠오름 효과, 흐르는 점선, STEP 번호, eyebrow 등을 잡음) |
