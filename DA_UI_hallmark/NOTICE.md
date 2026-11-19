# NOTICE · 출처와 라이선스

DA UI hallmark v1.0은 드림에이스 사내 디자인 규칙이다. 아래 자료를 바탕으로 만들었다.

| 자료 | 쓴 곳 | 라이선스 |
|---|---|---|
| `DA_WEBUI_KIT.md` v1.0 (사내 웹 라이트 키트) | 회사 8색, 네이비 강조, 바탕·면 위계, Pretendard, So-What 바, 알림 상자 | 사내 자료 |
| taste-skill v2.1.4 (Leonxlnx/taste-skill) | 규칙 문서의 "AI가 만든 티" 목록·업무 화면 관례·문구 규칙을 한국어로 다시 정리했다. `checker.html`에 검사 코드를 옮겨 넣었다 | MIT (아래 전문) |
| Pretendard (orioncactus/pretendard) | 템플릿과 검사기가 CDN으로 불러오는 글꼴. 이 폴더에 글꼴 파일은 넣지 않았다 | SIL Open Font License 1.1 |

## checker.html에 옮겨 넣은 taste-skill 코드

- `skills/taste-skill/scripts/lib/probe.mjs`: `probe`, `frame`, `layout`, `app` 등 화면 측정 함수
- `skills/taste-skill/scripts/lib/rules.mjs`: `judge`, `judgeLayout`, `judgeApp`, `APP_SKIP` 등 판정 규칙
- `skills/taste-skill/scripts/lint.mjs`: 코드 검사 규칙 표(`R`, `APP_LEVEL`)
- `skills/taste-skill/scripts/inspect.mjs`: 제목이 늦게 보이는지 보는 `TITLE_SEEN`, 가려진 글·잘린 글·빈 화면 판정 방식

고친 곳은 한 가지다. 화면 여러 개를 한 파일에 두고 숨겨 두는 경우를 위해, 제목(`h1`)을 찾을 때 숨긴 화면의 `h1`을 건너뛰고 보이는 첫 `h1`을 쓰게 했다(`probe`, `app`, `TITLE_SEEN` 세 곳). `hm-`로 시작하는 규칙과 화면 구성은 DA UI hallmark가 새로 만들었다.

## taste-skill 라이선스 전문

```
MIT License

Copyright (c) 2026 Leonxlnx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 예시 값

템플릿의 요청·품목·수치·일정은 모두 설명용 예시다([가상]·[가안]·[제안]). 품목 예시의 제조사 이름(Murata, Samsung EM, Yageo, TDK, Epson, JST, ST)은 공개된 회사 이름을 예시로 쓴 것이고, 거래 조건이나 실적이 아니다.
