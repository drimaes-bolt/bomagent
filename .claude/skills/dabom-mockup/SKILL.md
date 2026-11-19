---
name: dabom-mockup
description: 다봄 시연 목업(briefing/DaBOM_taste_skill_20261021.html 등 단일 HTML)을 읽거나 고칠 때, 목업에 새 화면·기능·미리보기 화면을 넣을 때 쓴다. 파일 구조, 코드 위치, 865KB 데이터 줄 주의, 화면 추가 절차, 판 관리 규칙을 담았다.
---

# 다봄 시연 목업 수정 가이드

목업은 서버·모델 호출·저장이 없는 프론트 전용 HTML 한 파일이다. 변환 결과는 사전 계산한 데이터(`DATA`)를 보여 준다. 기획 의도를 부서별 화면으로 보여 주는 것이 목적이다.

## 1. 판과 파일

| 파일 | 성격 |
|---|---|
| `briefing/DaBOM_taste_skill_20261021.html` | **현재 기준 판.** taste-skill 규칙으로 화면 구성을 다시 정한 판. 색·글꼴은 사내 키트(R08) |
| `briefing/index.html` | **현재 기준 판의 사본.** 기준 판과 항상 바이트 단위로 같게 유지한다(아래 판 관리). 2026-11-02 생성 |
| `briefing/DaBOM_20261020.html` | 이전 판(v0.1.1). 동작과 데이터는 같고 화면 구성만 다르다. 고치지 않는다 |
| 루트 `SS_SKPRT_EBOM.xlsx` | 연구소 화면 Import에서 고르는 시연 입력(KK16 E-BOM). 다른 PC 시연 때 HTML과 한 폴더에 둔다 |
| 루트 `SS_SKPRT_MBOM.xlsx` | 변환 결과로 보여 주는 KK16 M-BOM 1차([가상]). `DATA.mbom`의 원본 |

판 관리:
- 화면을 더하거나 구성을 바꾸는 큰 수정은 기준 판을 복사해 날짜를 붙인 새 파일(`DaBOM_<판이름>_YYYYMMDD.html`)에서 한다. 오탈자·문구 같은 작은 수정은 기준 판에서 바로 한다. 어느 쪽인지 애매하면 사용자에게 묻는다.
- 새 판을 만들면 README 문서 지도·변경 이력, 이 스킬의 1장 표, `docs/13` 머리말의 기준 판 이름을 함께 고친다.
- **`index.html` 동기화 (사용자 상시 지시, 2026-11-19. CLAUDE.md 9.1)**: 새 판을 만들면 같은 작업 안에서 `index.html`을 새 판으로 바꾼다. 묻지 않는다. 기준 판을 제자리에서 고쳤을 때도 `index.html`에 반영한다. 끝낸 뒤 `cmp`로 두 파일이 같은지 확인하고 결과를 보고한다.

```bash
cp briefing/<기준판>.html briefing/index.html && cmp briefing/<기준판>.html briefing/index.html && echo OK
```

- 이전 판은 고치지 않고 보존한다. 판마다 git 커밋을 남기면 이력도 추적된다(CLAUDE.md 9.2).

## 2. 파일 구조 (기준 판)

줄 번호는 수정하면 밀린다. 위치는 아래 명령으로 다시 뽑는다. `-o`로 일치 부분만 출력하므로 데이터 줄이 통째로 나오지 않는다.

```bash
grep -n -oE "^(const|let|function|class) [A-Za-z_\$][A-Za-z0-9_\$]*|^PAGES\['[^']+'\]" briefing/DaBOM_taste_skill_20261021.html
```

| 영역 | 위치(2026-11-19 기준) | 내용 |
|---|---|---|
| `<style>` | 10~717줄 | `:root` 색 토큰(회사 8색 + 무채색), 셸·시트·그리드·반응형 |
| 머리 주석 | 720~730줄 | 판 설명, 다른 PC 시연 방법, 화면 주소 규칙 |
| `const DATA = {...}` | **738줄 한 줄, 약 865KB** | 내장 데이터(3장). 절대 통째로 읽지 않는다 |
| 공통 스크립트 | `const $`부터 | 유틸, `ACT`(클릭 동작 표), `PAGES`(화면 등록 표), `ICONS`, `Tip`(설명 풍선), `XGrid`(엑셀형 표), xlsx 읽기(`DecompressionStream`), `INV`·`INB`(재고·입고 색인), `PRODUCTS`·`PROD`, `S`(전역 상태), `DEPT`, `FUT_DEPT`, 주소 처리(`routeFromHash`·`setHash`·`go`·`render`), `renderShell`·`renderSide`·`renderPage`·`futurePage`, 상단 검색(`gsFind`), 진입 화면(`renderLanding`) |
| `const TIPS` | 공통 뒤 | 설명 풍선 사전. 항목 형식 `{ t 제목, w 존재 이유, h 실무 쓰임, r 근거, ph 단계, id 기능 ID }` |
| `const FUT` | `TIPS` 뒤 | 미리보기 화면 정의. `{ what, why, later, prep, refs, mock: { cols: [[이름, 폭]...], rows } }` |
| 연구소 | `const R`부터 | `rnd.import`(5단계: 파일 가져오기 → E-BOM 확인 → M-BOM 변환 → 검토·수정 → 생산관리로 전송), `rnd.requests`, `rnd.search`, `rnd.sent` |
| 생산관리 | `const PM`부터 | `STAGES`(S0~S6), `ROUTE`(층별 승인 경로), `pm.products`(탭: M-BOM·개정 이력·E-BOM·ERP 코드), `pm.inbox`(구조 확정 작업대), `pm.mrp`, `pm.changes` |
| 자재/구매 | `const MP`부터 | `mp.stock`, `mp.inbound`, `mp.purchase`(탭: 매칭 검토·흡수 제안·신규 품목 등록 요청·견적 필요 품목), `mp.vendors` |

## 3. 내장 데이터 `DATA`

| 키 | 내용 | 출처 |
|---|---|---|
| `ebom` | KK16 E-BOM(시트 `DMC_SKPRT_MAIN_V20`, 131행) | `SS_SKPRT_EBOM.xlsx` |
| `mbom` | KK16 M-BOM 1차(22열, 모품번 2, 131행), 셀 표시·비고, `followS1`(행 번호별 다음 개정 값: 확인 요청 회신·NC 처리 등 55행) | `SS_SKPRT_MBOM.xlsx`, KK16 샘플 [가상] |
| `products` | KK13·KK14·KK15의 M-BOM 개정들, E-BOM, 개정 이력, ERP 코드 발번 내역 | `references/samples/KK13~15` [가상] |
| `e51k` | E51K ERP BOM(19열, 309행) | `references/samples/E51K_IVI_BOM(Amaranth-물류공통).xlsx` |
| `inventory` | 재고 701품목(코드·품명·규격·구분·제조사·수량·단가·사용 모델·MSL·거래처) | 기말재고 샘플 + 품번으로 만든 [가상] 값 |
| `pendingKK16` | KK16 신규 발번 대상 62품목 | KK16 샘플 |
| `suppliers` | 거래처 41곳(유형·취급 제조사·리드타임·표기 혼재) | E51K 이름 + [가상] 유형·조건 |
| `inbound` | 입고 예정 42건 | [가상] |
| `kk16codes` | KK16 ERP 코드 발번 내역 130행 | KK16 샘플 [가상] |

데이터를 바꿀 때는 줄을 손으로 고치지 않는다. Python으로 738줄의 `const DATA = ` 뒤 JSON을 읽어 고친 뒤 `json.dumps(d, ensure_ascii=False, separators=(',', ':'))`로 다시 써 넣는다. 스크립트는 scratchpad에 두고, 쓰기 전에 원본을 백업한다.

## 4. 읽기·검색 요령

- `Read`는 `offset`·`limit`로 739줄 이후나 740줄 이전만 읽는다. 738줄을 범위에 넣지 않는다.
- 검색은 `Grep`에 함수명·키 수준으로 좁힌 패턴을 쓰거나, Bash에서 `awk 'NR!=738' 파일 | grep -n 패턴`으로 데이터 줄을 뺀다. 결과 줄 번호는 738 이후부터 1씩 작게 나오므로 주의한다.
- `Edit`은 앱 코드 부분의 고유 문자열로 한다. 데이터 줄 안의 문자열을 `old_string`으로 쓰지 않는다.

## 5. 화면을 더하는 절차

먼저 `docs/13`에 화면 행(주소·답할 질문·주요 구성·기능 ID·단계·상태)을 쓴다. 그다음:

| 순서 | 미리보기 화면(다음 단계, 버튼 동작 없음) | 동작 화면(시연 범위) |
|---|---|---|
| 1 | `DEPT.<부서>.fut`에 `{ id: 'f-xxx', label, ph: '2단계', tip: 'f.<부서>.xxx' }` | `DEPT.<부서>.nav`에 `{ id: 'xxx', label, tip: 'nav.<부서>.xxx' }`(배지가 필요하면 `badge: () => 수`) |
| 2 | `NAV_IC`에 아이콘 키(`ICONS`에 있는 이름) | 같음 |
| 3 | `TIPS`에 `'f.<부서>.xxx'` 항목 | `TIPS`에 `'nav.<부서>.xxx'` 항목 |
| 4 | `FUT['f-xxx']`에 what·why·later·prep·refs·mock. `futurePage`가 알아서 그린다 | `PAGES['<부서>.xxx'] = el => { ... }`로 화면 함수 등록. 머리는 다른 화면처럼 `pg-head` + `h1`(관련 기능·질의를 `data-tw`에) |
| 5 | — | 클릭은 `data-act="키"` + `ACT['키'] = el => { ... }`. 표는 `new XGrid(host, { cols, pre, rows, cell, ... })` |
| 6 | 주소 `#<부서>/f-xxx`로 열리는지 확인 | 주소 `#<부서>/xxx`로 열리는지 확인 |

새 부서(회계·품질·영업·기준정보)를 동작 부서로 올리려면 `DEPT`에 부서를 더하고, `AV`(아바타 글자), `GS_PH`(상단 검색 안내), `routeFromHash`의 정규식 `(rnd|pm|mp)`, `.av-<부서>` CSS를 함께 고친다. 지금은 `FUT_DEPT`에 미리보기로만 있다.

## 6. 지킬 것

- 화면에 보이는 값 중 만든 값은 `[가상]`, 정해지지 않은 안은 `[제안]`으로 표시한다. 실제 단가·개인 이름을 넣지 않는다.
- 연구소 화면에는 단가·거래처 조건을 보이지 않는다(docs/03 7장 공개 범위 [제안]). 단가 열은 권한 표시(`비공개`)로 둔다.
- 디자인은 `DA_UI_hallmark/02_app_screens.md`와 `01_foundation.md`를 따른다. 기준 판은 hallmark 이전에 만들어 검사기에서 FAIL 2·WARN 5가 나온 기록이 있다(`DA_UI_hallmark/CHANGELOG.md`). 새 판에서는 엑셀형 표에 `data-sheet` 표시를 하고 `#A0A0A0` 글자를 쓰지 않는다.
- 1440·768·390 폭에서 깨지지 않게 한다. 빈 상태·사용 불가 상태를 만든다.
- 고친 뒤 `DA_UI_hallmark/04_checklist.md`로 점검하고 보고한다. 브라우저 검사는 사람이 `checker.html`로 한다.

## 7. 시연 흐름

진입 화면에서 부서를 고른다. 연구소 `rnd/import`에서 E-BOM을 가져와 변환·검토하고 생산관리로 보내면, 생산관리 `pm/inbox`에 구조 확정 요청이 들어오고, 자재/구매 `mp/purchase`에 매칭 검토·흡수 제안·신규 품목·견적 필요 목록이 생긴다. 부서 간 알림은 `S.notes`와 상단 종 모양 단추로 오간다. 상단의 시연 초기화 단추가 처음 상태로 되돌린다.
