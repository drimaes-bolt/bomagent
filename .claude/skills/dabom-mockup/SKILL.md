---
name: dabom-mockup
description: 다봄 시연 목업(briefing/DaBOM_avl_20261127.html 등 단일 HTML)을 읽거나 고칠 때, 목업에 새 화면·기능·미리보기 화면을 넣을 때 쓴다. 파일 구조, 코드 위치, 1MB 넘는 데이터 줄 주의, 화면 추가 절차, 판 관리 규칙을 담았다.
---

# 다봄 시연 목업 수정 가이드

목업은 서버·모델 호출·저장이 없는 프론트 전용 HTML 한 파일이다. 변환 결과는 사전 계산한 데이터(`DATA`)를 보여 준다. 기획 의도를 부서별 화면으로 보여 주는 것이 목적이다.

## 1. 판과 파일

| 파일 | 성격 |
|---|---|
| `briefing/DaBOM_avl_20261127.html` | **현재 기준 판(AVL 판).** 뿌리 판을 복사해 `DATA.avl`(AVL 제조사와 개별 제품 52,154행, HTML 약 6MB)과 기준정보 동작 화면 `mdm/avl`을 더했다. 거래처 카탈로그 `mp/catalog`(카탈로그 제품 탭)와 연구소 검색 `rnd/search`(거래처 카탈로그 탭)도 같은 제품 표(`avlBrowser`)를 쓴다. 옛 [가상] `DATA.catalog`는 없앴다. 코드는 3장 아래 "AVL 판에서 더한 장치"에 정리했다. 근거 DEC-19, MDM-10, MAT-14 |
| `briefing/DaBOM_root_20261124.html` | 이전 기준 판(뿌리 판). 진입 화면에 "시작도 뿌리도 BOM이다"와 뿌리·줄기·가지 지도(`BOM_ROOT`·`TRUNK`·`renderLanding`), 미리보기 화면의 `FUT_BOM` 띠. 근거 DEC-18. 고치지 않는다 |
| `briefing/DaBOM_expand_20261123.html` | 그 이전 판(확장 판). taste-skill 판을 복사해 재고(Inventory.xlsx)·사용 이력·분류 필터·거래처 카탈로그·미리보기 부서(생산기술·회계·품질·기준정보)를 더했다. 근거 docs/14. 고치지 않는다 |
| `briefing/index.html` | **현재 기준 판의 사본.** 기준 판과 항상 바이트 단위로 같게 유지한다(아래 판 관리). 2026-11-02 생성, 2026-11-23 확장 판으로, 2026-11-24 뿌리 판으로, 2026-11-27 AVL 판으로 교체 |
| `briefing/DaBOM_taste_skill_20261021.html` | 더 이전 기준 판. taste-skill 규칙으로 화면 구성을 다시 정한 판. 고치지 않는다 |
| `briefing/DaBOM_20261020.html` | 그 이전 판(v0.1.1). 고치지 않는다 |
| `briefing/DaBOM_plan_board_20261123.html` | 목업이 아니라 기획 현황판. `tools/build_plan_board.py`가 docs/에서 만든다. 목업 진입 화면 아래 안내문에서 링크한다 |
| 루트 `SS_SKPRT_EBOM.xlsx` | 연구소 화면 Import에서 고르는 시연 입력(KK16 E-BOM). 다른 PC 시연 때 HTML과 한 폴더에 둔다 |
| 루트 `SS_SKPRT_MBOM.xlsx` | 변환 결과로 보여 주는 KK16 M-BOM 1차([가상]). `DATA.mbom`의 원본 |
| 루트 `Inventory.xlsx` · `PartHistory.xlsx` | `DATA.inventory`의 원본(재고 1,048 · 사용 이력 356). 2025 기말 실제 품목의 단가는 넣지 않고 [가상] 단가를 쓴다 |

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
grep -n -oE "^(const|let|function|class) [A-Za-z_\$][A-Za-z0-9_\$]*|^PAGES\['[^']+'\]" briefing/DaBOM_avl_20261127.html
```

| 영역 | 위치(AVL 판, 2026-11-27 기준) | 내용 |
|---|---|---|
| `<style>` | 10~821줄 | `:root` 색 토큰(회사 8색 + 무채색), 셸·시트·그리드·반응형 |
| 머리 주석 | 824~853줄 | 판 설명, 다른 PC 시연 방법, 화면 주소 규칙 |
| `const DATA = {...}` | **861줄 한 줄, 약 548만 자**(AVL 판. 뿌리 판은 836줄·약 112만 자, 확장 판은 791줄, taste-skill 판은 738줄) | 내장 데이터(3장). 절대 통째로 읽지 않는다 |
| 공통 스크립트 | `const $`부터 | 유틸, `ACT`(클릭 동작 표), `PAGES`(화면 등록 표), `ICONS`, `Tip`(설명 풍선), `XGrid`(엑셀형 표), xlsx 읽기(`DecompressionStream`), `INV`·`INB`(재고·입고 색인), `PRODUCTS`·`PROD`, `S`(전역 상태), `DEPT`, `FUT_DEPT`, 주소 처리(`routeFromHash`·`setHash`·`go`·`render`), `renderShell`·`renderSide`·`renderPage`·`futurePage`, 상단 검색(`gsFind`), 진입 화면(`BOM_ROOT`·`TRUNK`·`renderLanding`) |
| `const TIPS` | 공통 뒤 | 설명 풍선 사전. 항목 형식 `{ t 제목, w 존재 이유, h 실무 쓰임, r 근거, ph 단계, id 기능 ID }` |
| `const FUT` | `TIPS` 뒤 | 미리보기 화면 정의. `{ what, why, later, prep, refs, mock: { cols: [[이름, 폭]...], rows } }` |
| 연구소 | `const R`부터 | `rnd.import`(5단계: 파일 가져오기 → E-BOM 확인 → M-BOM 변환 → 검토·수정 → 생산관리로 전송), `rnd.requests`, `rnd.search`, `rnd.sent` |
| 생산관리 | `const PM`부터 | `STAGES`(S0~S6), `ROUTE`(층별 승인 경로), `pm.products`(탭: M-BOM·개정 이력·E-BOM·ERP 코드), `pm.inbox`(구조 확정 작업대), `pm.mrp`, `pm.changes` |
| 자재/구매 | `const MP`부터 | `mp.stock`(재고 목록·사용 이력), `mp.catalog`(거래처 카탈로그), `mp.inbound`, `mp.purchase`(탭: 매칭 검토·흡수 제안·신규 품목 등록 요청·견적 필요 품목), `mp.vendors` |
| 회계 | `S.acc`부터 | `acc.rollup`(모델별 자재비). 생산기술·품질·기준정보는 미리보기 화면만 있어 코드는 `FUT` 정의뿐이다 |

## 3. 내장 데이터 `DATA`

| 키 | 내용 | 출처 |
|---|---|---|
| `ebom` | KK16 E-BOM(시트 `DMC_SKPRT_MAIN_V20`, 131행) | `SS_SKPRT_EBOM.xlsx` |
| `mbom` | KK16 M-BOM 1차(22열, 모품번 2, 131행), 셀 표시·비고, `followS1`(행 번호별 다음 개정 값: 확인 요청 회신·NC 처리 등 55행) | `SS_SKPRT_MBOM.xlsx`, KK16 샘플 [가상] |
| `products` | KK13·KK14·KK15의 M-BOM 개정들, E-BOM, 개정 이력, ERP 코드 발번 내역 | `references/samples/KK13~15` [가상] |
| `e51k` | E51K ERP BOM(19열, 309행) | `references/samples/E51K_IVI_BOM(Amaranth-물류공통).xlsx` |
| `inventory` | 1,394행 = 재고 목록 1,048(`src:'INV'`, Inventory.xlsx) + 재고 목록 밖 사용 이력 346(`src`=KK13·KK14·KK15·E51K). 행 배열 18칸: 품번·품명·규격·계정·제조업체·추정(mi)·단가·수량·할당·사용 모델·MSL·주거래처·라이프사이클·출처(src)·구분(org: 실제·가상·BOM)·속성(a: c 분류, t 세부유형, s 크기, v 값, tl 허용오차, vr 정격전압, dl 유전체, th 두께)·MOQ·사용 이력(hist: k zero·bom, st 재구매 가능·확인 필요, why) | Inventory.xlsx(수량·규격) + 기존 목업 [가상] 단가·할당·거래처 + PartHistory.xlsx |
| `avl` | 부품 카테고리별 AVL과 공급 제품. `asOf`, `cats[]`(id·ko·`cols`(사양 열 [키, 머리글, 너비])·`vendors`(k·name·short·country·fab·biz·rank·docs·n)·`docs`(t 제목·d 기준일·p 쪽 수·f 파일·v 제조사 번호)·`S`(문자열 사전)·`rows`). 행 배열: [제조사 번호, 구분 번호(0 계열·1 부품번호·2 사양 조합), `S` 번호들(계열, 부품번호, 유형), 문서 번호, `S` 번호들(쪽, 비고, 원문 대조, ...사양)]. 앱이 읽을 때 `AVL` 안에서 `S` 번호를 문자열로 풀어 쓴다(행 앞 9칸 `AVL_OFF = 9`, 이후가 사양). 제품에 ERP 코드 없음. 옛 `catalog` 키는 없앴다 | `AVL_DB/_source/final_rows.json.gz` → `tools/avl_db/build_data_avl.py` → `inject_avl.py`. R13 제조사 PDF에서 추출(공개 사양, 가상 아님) |
| `pendingKK16` | KK16 신규 발번 대상 62품목 | KK16 샘플 |
| `suppliers` | 거래처 41곳(유형·취급 제조사·리드타임·표기 혼재) | E51K 이름 + [가상] 유형·조건 |
| `inbound` | 입고 예정 42건 | [가상] |
| `kk16codes` | KK16 ERP 코드 발번 내역 130행 | KK16 샘플 [가상] |

데이터를 바꿀 때는 줄을 손으로 고치지 않는다. Python으로 데이터 줄(AVL 판 861줄)의 `const DATA = ` 뒤 JSON을 읽어 고친 뒤 `json.dumps(d, ensure_ascii=False, separators=(',', ':'))`로 다시 써 넣는다. 스크립트는 scratchpad에 두고, 쓰기 전에 원본을 백업한다.

## 4. 읽기·검색 요령

- `Read`는 `offset`·`limit`로 데이터 줄(AVL 판 861줄)을 범위에 넣지 않는다.
- 검색은 `Grep`에 함수명·키 수준으로 좁힌 패턴을 쓰거나, Bash에서 `awk 'NR!=861' 파일 | grep -n 패턴`으로 데이터 줄을 뺀다. 결과 줄 번호는 데이터 줄 이후부터 1씩 작게 나오므로 주의한다. 데이터 줄 번호는 `grep -n -m1 '^const DATA = ' 파일 | cut -c1-20`으로 먼저 확인한다.
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

부서는 `DEPT` 한 곳에 정의한다(확장 판). 미리보기 부서는 `preview: true`, `nav: []`(동작 화면이 없으면 비움), `fut: [...]`로 둔다. 첫 화면은 `firstPage(d)`(동작 화면이 없으면 첫 미리보기)이고, 주소 정규식은 `DEPT_KEYS`로 만들어 새 부서를 더해도 고칠 곳이 없다. 새 부서를 더할 때 같이 고칠 것: `AV`(아바타 글자), `.av-<부서>` CSS, `NAV_IC`, **`BOM_ROOT`**(그 부서가 BOM의 어디를 보는지 한 줄. 뿌리 원칙 DEC-18. 없으면 진입 화면의 가지 목록에 `undefined`가 나온다. 같은 내용을 docs/03 0.1에도 적는다). `GS_PH`는 없으면 기본 문구가 붙는다. 진입 화면의 가지 목록(부서 선택)과 부서 전환 메뉴는 `preview` 표시로 동작 부서 → 미리보기 부서 순서로 저절로 나뉜다. `FUT_DEPT`에는 화면이 전혀 없는 참여 부서(영업)만 남았다.

확장 판에서 더한 공통 장치(위치는 2장 명령으로 찾는다):

| 장치 | 내용 |
|---|---|
| `INV_STOCK` · `INV_HIST` | 재고 목록(1,048) · 사용 이력 품목(356). `equivStock(it)`는 같은 사양 재고 보유 품목 |
| 분류 필터 `pdbMount(id, host, st, cfg)` | `PDB_FACETS.part`(대분류 → 크기·값·허용오차·유전체·정격전압 → 제조업체·상태·사용 모델·출처)와 `.avl`(분류 11개 → 제조사 전부 → 분류마다 다른 메뉴). 상태 객체 `st = { q, sel, more, open, fopen }`는 화면을 다시 열어도 남는다. `cfg = { kind, list, text, body, grid, ph, unit, extra }`(`extra`는 사양 폼 같은 추가 조건 함수). 다른 화면에서 넘길 때는 `pdbQuery(st, q, it)` |
| 화면 | `mp.stock`(재고 목록·사용 이력 전환), `rnd.search`(재고·사용 이력·거래처 카탈로그 탭), `mp.catalog`(라인카드·제조사 문서·카탈로그 제품 탭), `mdm.avl`(AVL 목록·공급 제품 탭), `acc.rollup`(모델별 자재비) |
| 맞추기 | `reuse0(m)` = 재사용인데 재고 0. `FILTERS`·`LADDER`에 `l-reuse0`, 견적 필요 목록(`rfqItems`)에 재구매 행 |
| 설명·미리보기 | 확장 판의 `TIPS`·`FUT` 추가분은 `S.rnd = {` 바로 앞의 `Object.assign(TIPS, …)`·`Object.assign(FUT, …)` 블록에 모았다 |

AVL 판에서 더한 장치(`AVL` 앞부분 위치는 2장 명령으로 찾는다):

| 장치 | 내용 |
|---|---|
| `AVL` · `AVL_ITEMS` | `DATA.avl`을 읽을 때 문자열 사전(`S`)을 풀어 행 배열로 만든다. `AVL_ITEMS` = `{ c(분류), ci, v(제조사), r(행) }` 전체 52,154개. `AVL_OFF = 9`는 행에서 사양이 시작하는 칸 |
| `AVL_FAC` | 분류마다 다른 필터 메뉴 정의 `[사양 열 키, 머리글, 'size'면 숫자 순서]`. 첫 항목이 크기·패키지. 새 분류 열을 더하면 여기도 고친다 |
| `PDB_FACETS.avl` · `avlExtra` | 분류(11) → 제조사(전부) → `AVL_FAC`의 메뉴. 분류를 정확히 하나 골랐을 때만 그 분류의 메뉴와 사양 폼이 나온다(`when`). `AVL_FORMS`(저항·커패시터·인덕터 사양 폼)는 `avlTest`로 범위 표기·크기·전압·허용오차를 비교하고 읽지 못한 칸은 건너뛴 개수를 알린다 |
| `AVL_STD` · `avlSizeTok` | `0402~2512`처럼 범위로 적힌 칩 크기를 표준 크기로 풀어 필터·사양 폼에만 쓴다(표에는 원문 표기). 인치 코드가 기본이고 `m`을 붙이면 메트릭 |
| `avlBrowser(host)` · `avlGrid` | 제품 표 화면 한 벌. 정렬 선택 `#avlb-sk`(SI 접두어·숫자 인식 `avlSortVal`), 쪽 이동(페이지네이션): `AVLB.page`·`AVLB.ps`(쪽당 행 수, `AVL_PS = [25, 50, 100, 200]`, 기본 50), 표 위 `avlPager(total, true)`(이전·쪽 번호·다음·쪽 번호 입력 `#avlb-pj`), 정렬 줄의 `#avlb-ps`, 표 아래 `avlPager(total, false)`(`#avlb-more2`). 필터·낱말·사양 조건 `sig`가 바뀌거나 정렬을 바꾸면 1쪽으로 돌아간다. 640px 이하에서는 쪽 번호를 숨기고 단추를 40px로 키운다. `mdm.avl`·`mp.catalog`·`rnd.search`가 같이 쓴다. 행 상세 `avlDetail` |
| `avlDocs` · `avlMakerRows` · `AVL_MK` | 제조사 문서 목록(같은 PDF를 여러 분류에 둔 것은 한 문서)과 라인카드 제조사 이름을 `AVL` 제조사로 잇는 대응표 |
| `PAGES['mdm.avl']` | 탭 AVL 목록(`AVLP.tab = 'list'`) · 공급 제품(`'items'`). 목록 행을 누르면 그 제조사의 제품으로 간다 |

검증: 목업을 고친 뒤 스크립트 부분을 뽑아 `node --check`로 문법을 보고, Chrome 헤드리스(`"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless --dump-dom --virtual-time-budget=…`. 2026-11-27에 Edge 헤드리스가 출력을 내지 않아 Chrome으로 바꿈)로 오류 수집용 스크립트를 넣은 사본을 열어 모든 `#부서/화면`을 돌려 본다(2026-11-23 확장 판에서 67개 점검·오류 0. 2026-11-24 뿌리 판에서는 부서별 화면 47개와 진입 화면을 순회해 오류 0. 2026-11-27 AVL 판은 화면 48개(`mdm/avl` 포함) 순회 오류 0, 분류 11개·제조사 22개 필터 표시, 분류 선택 시 분류별 메뉴 전환(저항: 크기·유형·허용오차·정격전력, MOSFET: 패키지·극성·Vds 등), 정렬·더 보기, 사양 폼(저항 10k·0603·허용오차 1%, 커패시터 100n·16V·X7R) 동작을 확인, 설명 풍선 키 누락 0). hallmark 점검은 FAIL 0·WARN 1(기존 로딩 스피너). 헤드리스 Edge의 창 폭은 약 492px보다 좁아지지 않으므로 390px 확인은 사람이 `checker.html`로 한다.

## 6. 지킬 것

- 화면에 보이는 값 중 만든 값은 `[가상]`, 정해지지 않은 안은 `[제안]`으로 표시한다. 실제 단가·개인 이름을 넣지 않는다.
- 연구소 화면에는 단가·거래처 조건을 보이지 않는다(docs/03 7장 공개 범위 [제안]). 단가 열은 권한 표시(`비공개`)로 둔다.
- 디자인은 `DA_UI_hallmark/02_app_screens.md`와 `01_foundation.md`를 따른다. 기준 판은 hallmark 이전에 만들어 검사기에서 FAIL 2·WARN 5가 나온 기록이 있다(`DA_UI_hallmark/CHANGELOG.md`). 새 판에서는 엑셀형 표에 `data-sheet` 표시를 하고 `#A0A0A0` 글자를 쓰지 않는다.
- 1440·768·390 폭에서 깨지지 않게 한다. 빈 상태·사용 불가 상태를 만든다.
- **뿌리 원칙(사용자 지시 2026-11-24, DEC-18)**: 진입 화면 첫머리의 "시작도 뿌리도 BOM이다"와 뿌리·줄기·가지 지도를 지운 채 다른 구성으로 바꾸지 않는다. 새 화면·부서·기능을 넣을 때는 BOM의 무엇을 읽고 무엇을 돌려주는지 한 줄을 먼저 적는다(docs/04 1.1, 부서는 `BOM_ROOT`). 한 줄로 적을 수 없는 화면은 넣지 않고 docs/11 미결로 올린다. 새 미리보기 화면은 `FUT_BOM`에 항목을 더하고 docs/13 12장 표에도 같은 줄을 적는다(없으면 띠가 나오지 않는다).
- 고친 뒤 `DA_UI_hallmark/04_checklist.md`로 점검하고 보고한다. 브라우저 검사는 사람이 `checker.html`로 한다.

## 7. 시연 흐름

진입 화면은 먼저 "시작도 뿌리도 BOM이다"와 뿌리·줄기·가지 지도를 보여 주고, 그 안의 가지 목록에서 부서를 고른다. 연구소 `rnd/import`에서 E-BOM을 가져와 변환·검토하고 생산관리로 보내면, 생산관리 `pm/inbox`에 구조 확정 요청이 들어오고, 자재/구매 `mp/purchase`에 매칭 검토·흡수 제안·신규 품목·견적 필요 목록이 생긴다. 부서 간 알림은 `S.notes`와 상단 종 모양 단추로 오간다. 상단의 시연 초기화 단추가 처음 상태로 되돌린다.
