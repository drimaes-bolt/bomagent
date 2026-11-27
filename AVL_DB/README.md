# AVL_DB — AVL(제조사 목록)과 공급 제품 DB (시연용)

> 2026-11-27 작성. 부품 카테고리별 AVL(Approved Vendor List)과, AVL 제조사가 Selection Guide에서 공급 가능하다고 밝힌 제품을 엑셀로 정리했다. 추후 대체품 추천의 백데이터이고 시연 목업(`briefing/index.html`)이 같은 데이터를 쓴다. 출처 PDF는 [R13](../references/R13_Vendor_Guides/README.md), 결정은 DEC-19(docs/11)다. **제품에는 ERP 코드를 붙이지 않았다.** ERP 코드는 연구소가 설계에 부품을 적용할 때 사내 기존 품목을 먼저 찾고 없을 때 처음 채번한다(docs/08).

## 파일

| 파일 | 내용 |
|---|---|
| `AVL_List.xlsx` | 카테고리별 AVL. 시트: 요약 · 전체 AVL · 카테고리 11개. 열: 카테고리 · 제조사 · 국가·생산 위치·사업분야·순위(R09) · 출처 문서 수 · 공급 제품 행 수 · 제품 유형 · 대표 문서 · 기준일 · 한계 |
| `AVL_Parts_<도메인>.xlsx` × 11 | 도메인별 공급 제품 리스트. 한 파일 안에서는 모든 제조사가 같은 표 양식이다. 시트: 제품 리스트 · 문서 목록 · 읽는 법 |
| `_source/` | 이 엑셀과 목업 데이터의 원천. `final_rows.json`(검증을 거친 제품 행), `final_docs.json`(문서별 추출 메모), `raw/`(에이전트가 뽑은 원본 JSON) |

엑셀 양식은 루트 `Inventory.xlsx`를 따랐다(1행 제목, 2행 설명, 3행 연두색 머리글, Tahoma 10, 틀 고정, 자동 필터).

## 규모

| 도메인 | AVL 제조사 | 제품 행 | 계열 | 부품번호 | 확인 필요 |
|---|---|---|---|---|---|
| MCU | 4곳: Infineon Technologies, Microchip Technology, NXP Semiconductors, Texas Instruments (TI) | 316 | 200 | 116 | 4 |
| MOSFET | 3곳: Diodes Incorporated, Infineon Technologies, Vishay Intertechnology | 873 | 27 | 846 | 2 |
| 저항 | 4곳: Panasonic, ROHM Semiconductor, Vishay Intertechnology, Walsin Technology | 1,028 | 770 | 258 | 4 |
| 커패시터 | 6곳: Panasonic, Samsung Electro-Mechanics, TDK Corporation, Taiyo Yuden, Vishay Intertechnology, Walsin Technology | 525 | 427 | 98 | 5 |
| 인덕터 | 4곳: Coilcraft, Murata Manufacturing, Taiyo Yuden, Vishay Intertechnology | 748 | 730 | 18 | 0 |
| AC/DC·DC/DC 전원 IC | 2곳: Diodes Incorporated, Monolithic Power Systems (MPS) | 251 | 51 | 200 | 0 |
| 다이오드 | 4곳: Diodes Incorporated, Nexperia, ROHM Semiconductor, Vishay Intertechnology | 919 | 135 | 784 | 4 |
| 드라이버 IC | 1곳: Infineon Technologies | 44 | 6 | 38 | 0 |
| 센서 | 3곳: Bosch Sensortec, Honeywell, Texas Instruments (TI) | 93 | 41 | 52 | 3 |
| 무선·연결 IC | 3곳: Espressif Systems, Nordic Semiconductor, Qualcomm | 32 | 0 | 32 | 0 |
| 커넥터 | 1곳: Hirose Electric (HRS) | 93 | 93 | 0 | 0 |
| **합계** | 35곳(카테고리별 합) | **4,922** | 2,480 | 2,442 | 22 |

출처 문서는 도메인 폴더 기준 64건이다(여러 도메인에 걸친 PDF는 도메인마다 따로 센 것). 제품 행이 나오지 않은 문서 1건(Taiyo Yuden 1쪽 마케팅 소개)은 `문서 목록`에만 있다.

## 도메인별 사양 열

같은 도메인 안에서는 열이 같고, 저항·커패시터처럼 사양 항목이 다른 도메인은 열이 다르다. 모든 파일의 앞쪽 열은 제조사 · 구분(계열/부품번호) · 계열(Series) · 부품번호 · 제품 유형이고, 뒤쪽 열은 비고 · 출처 문서 · 쪽 · 문서 기준일 · 원문 대조다.

| 도메인 | 사양 열 |
|---|---|
| MCU | 코어 · 비트 · 최대 클럭 · 플래시 · RAM · 주변장치·통신 · 동작 전압 · 패키지 · 대상 응용 · 동작 온도 · 차량용 인증 · 특징 |
| MOSFET | 극성 · Vds(V) · Rds(on)(mΩ) · Id(A) · 패키지 · 기술 · Qg(nC) · 동작 온도 · 차량용 인증 · 특징 |
| 저항 | 크기(인치) · 크기(메트릭) · 저항 범위 · 허용오차 · TCR(ppm/°C) · 정격전력(W) · 최대 전압(V) · 동작 온도 · 차량용 인증 · 특징 |
| 커패시터 | 크기(인치) · 크기(메트릭) · 정전용량 범위 · 정격전압(V) · 유전체·온도특성 · 허용오차 · 동작 온도 · 차량용 인증 · 특징 |
| 인덕터 | 크기 · 인덕턴스 범위 · 정격전류 · 포화전류 · DCR(mΩ) · 차폐 · 동작 온도 · 차량용 인증 · 특징 |
| AC/DC·DC/DC 전원 IC | 토폴로지 · 입력 전압 · 출력 전압 · 출력 전류 · 스위칭 주파수 · 패키지 · 동작 온도 · 차량용 인증 · 특징 |
| 다이오드 | Vr(V) · If(A) · Vf(V) · 소자 구성 · 패키지 · 동작 온도 · 차량용 인증 · 특징 |
| 드라이버 IC | 채널 · 전압 · 전류 · 절연 · 패키지 · 동작 온도 · 차량용 인증 · 특징 |
| 센서 | 측정 범위 · 정확도 · 인터페이스 · 공급 전압 · 패키지 · 동작 온도 · 차량용 인증 · 특징 |
| 무선·연결 IC | 무선 규격 · 코어 · 주파수 · 메모리 · 인터페이스 · 패키지 · 동작 온도 · 특징 |
| 커넥터 | 피치(mm) · 극수 · 정격전류 · 정격전압 · 실장 · 대상 응용 · 동작 온도 · 특징 |

## 만든 방법과 검증

1. 제조사 Selection Guide PDF를 [R13](../references/R13_Vendor_Guides/README.md)에 모았다. 문서를 확보하지 못한 제조사·카테고리 26쌍은 AVL에서도 뺐다(사용자 결정).
2. 도메인별로 PDF 텍스트를 읽어 제품 행을 뽑았다(`tools/avl_db/extract_brief.md`의 지침, 에이전트 9개). 문서에 없는 값은 비웠고 단가·재고·납기·ERP 코드는 넣지 않았다. 문서가 소개한 제품 단위 그대로 쓰고(`구분` 열), 부품번호 표가 큰 문서는 문서당 200행을 범위가 고르게 되도록 골랐다.
3. 원문 대조(`tools/avl_db/verify_rows.py`, `finalize.py`): 모든 행의 계열명·부품번호가 지정한 쪽 텍스트에 있는지 자동으로 확인했다. 통과하지 못한 2건은 직접 확인했다. 사양 숫자도 같은 줄·같은 쪽에서 찾아 행마다 `원문 대조` 수준을 적었다.
4. 글꼴이 깨진 Taiyo Yuden 문서(4개, 행 46개)는 쪽을 그림으로 그려 직접 대조했다. 이 과정에서 마케팅 소개 4행과, 비드를 커패시터로 잘못 넣은 1행을 빼냈다.

| 원문 대조 | 뜻 | 행 수 |
|---|---|---|
| 행 일치 | 부품번호가 있는 줄 근처(±2줄)에서 사양 숫자를 찾음 | 1,417 |
| 쪽 일치 | 같은 쪽에서 사양 숫자를 찾음(계열 행의 범위 표기, 표 배치가 복잡한 쪽) | 3,275 |
| 이름·쪽 일치 | 이름과 쪽만 일치. 사양 숫자가 없는 행 | 162 |
| 그림 확인 | 쪽 그림을 직접 대조(Taiyo Yuden) | 46 |
| 확인 필요 | 사양 숫자를 찾지 못함. 열이 밀렸거나 단위를 바꾸었을 수 있다. 원문을 열어 확인한다 | 22 |

## 알아 둘 점

- **범위**: 확보한 문서에 나온 제품만 담았다. 한 제조사의 전 제품이 아니다. 제조사별 범위와 한계는 `AVL_Parts_*.xlsx`의 `문서 목록` 시트와 `references/R13_Vendor_Guides/manifest.csv`의 `caveat`에 있다. 응용별 1~2쪽 가이드(Hirose), 계열 하나(TI MSPM0), 군용 중심(Vishay) 같은 약한 매치가 있다.
- **판**: 문서 날짜가 2023-11-27 이후인 것만 썼다. 최신판이 아닐 수 있다.
- **부품번호 행은 샘플**: 부품번호 표가 큰 문서(MPS·Nexperia·ROHM·Vishay·Infineon·Diodes)는 문서당 200행으로 줄였다. 계열 행은 문서에 있는 만큼 모두 적었다.
- **사양은 문서 표기 그대로**: 같은 값이어도 문서마다 표기가 다르다(예: `4.7µF`, `4u7`). 목업의 "사양으로 찾기"는 범위 표기를 읽어 비교하고, 읽지 못한 칸은 제외하고 개수를 알린다.
- **AVL의 뜻**: 시연용 목록이다. 실제 승인 절차를 거친 목록이 아니다. 제조사 속성(국가·생산 위치·사업분야·순위)은 R09(EP_Vendor_List_by_Category)에서 왔다.
- **저작권**: 사양 값은 제조사가 홍보 목적으로 공개한 문서에서 사실만 옮긴 것이다. 이 엑셀과 `_source/`는 공개 저장소에 올려도 된다는 사용자 확인을 받았다(2026-11-27). 원본 PDF는 저작물이라 올리지 않는다(`.gitignore`).

## 다시 만들기 · 문서를 더할 때

새 제조사 문서를 R13에 더했거나 판이 바뀌었을 때의 순서다. 스크립트는 `tools/avl_db/`에 있고 모두 표준 라이브러리와 `openpyxl`, `pdftotext`(poppler)만 쓴다.

1. 새 문서를 R13 폴더에 넣고 `manifest.csv`에 행을 더한다.
2. `tools/avl_db/extract_brief.md`의 지침으로 그 문서의 제품 행을 `parts_<코드>.json` 형식으로 뽑는다(AI 에이전트 또는 사람). 기존 raw JSON은 `AVL_DB/_source/raw/`에 있다.
3. 작업 폴더 `W`에 raw JSON을 모으고 `python tools/avl_db/verify_rows.py W references/R13_Vendor_Guides` → `finalize.py`(같은 인자)로 원문 대조와 `final_rows.json`·`final_docs.json`을 만든다.
4. `python tools/avl_db/build_xlsx.py W references/R13_Vendor_Guides references/R09_EP_Vendor_List_by_Category.md AVL_DB`로 엑셀을 만든다.
5. `python tools/avl_db/build_data_avl.py W references/R13_Vendor_Guides references/R09_EP_Vendor_List_by_Category.md`로 목업 데이터를 만들고, 새 판 HTML에 `inject_avl.py`로 `DATA.avl`을 넣는다(`.claude/skills/dabom-mockup`).
6. 기획 문서의 숫자(README, docs/05 DT-16)를 갱신하고 `python tools/build_plan_board.py`로 현황판을 다시 만든다.

## 변경 이력

| 버전 | 일자 | 내용 |
|---|---|---|
| v0.1 | 2026-11-27 | 최초 작성. R13 PDF에서 제품 행 4,922개와 AVL 35곳 |
