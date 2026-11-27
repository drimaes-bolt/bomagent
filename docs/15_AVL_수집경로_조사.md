# 15. AVL 제품 데이터 수집 경로 조사

> 2026-11-27. AVL·공급 제품 DB([DEC-19](11_결정_미결_목록.md), `MDM-10`)에서 비어 있는 제조사×분류 조합을 웹에서 자동으로 채울 수 있는지 조사한 기록이다. BOM 연결(뿌리 원칙, DEC-18): BOM 행의 부품 카테고리·사양을 `MAT-14`가 AVL 공급 제품 DB에서 찾으므로, 이 DB를 채우는 경로를 정하는 일이다. 1~8장은 같은 날 오전 조사(수집 코드 없음)이고, 9~10장은 사용자 결정(DEC-20)에 따라 같은 날 오후 수집을 실행한 결과와 약관 확인 목록이다. 경로 추천은 [제안]이다.

---

## 1. 결론

| # | 결론 |
|---|---|
| 1 | **스크레이핑 방식의 크롤러는 권하지 않는다.** 조사한 17곳 중 TI·ADI·Würth는 사이트 약관이 데이터 마이닝·스크레이핑을 금지하는 것으로 읽히고, Infineon은 `robots.txt`가 제품 표 필터 URL(`*filter=*`, `*search*`)을 막으며, Murata·Molex·TE는 API 약관이 크롤링·저장·데이터셋 구축을 제한한다. 약관에 자동 수집 조항이 없는 곳(onsemi, Samsung EM 등)도 복제·재배포·영리 이용을 제한하는 문구가 있어 허용으로 볼 수 없다 |
| 2 | **제조사가 공식으로 주는 경로가 있는 곳이 많다.** 공식 내보내기 버튼(onsemi, Samsung EM, TE, Murata)과 공식 API(TI, Murata)를 쓰면 스크레이핑 없이 표 단위 사양을 받을 수 있다. 빈 26쌍 가운데 약 10쌍이 여기에 든다 |
| 3 | **API·내보내기로 받은 데이터는 공개 저장소에 올리지 않는 것을 권한다.** 2026-11-27 사용자 확인("공개 저장소에 제품 리스트 Excel 가능")은 제조사가 홍보용으로 공개한 Selection Guide PDF에 대한 것이다. TI API 약관 2(i)는 TI 데이터(파생·집계 포함)의 공개 호스팅·제3자 제공을 금지하는 것으로 읽힌다. OI-26 |
| 4 | **이 PC에서 막힌 곳이 있다.** ST·ADI·Molex는 응답하지 않고 TDK Product Center와 Infineon(curl)은 봇 방어에 막힌다. 우회하지 않았다. 다른 네트워크에서 다시 보거나 사람이 받아야 한다. OI-28 |
| 5 | **자동화할 만한 경로가 없는 제조사 8곳은 수동 선별·문의·상용 DB가 현실적이다.** Yageo·KEMET, TA-I, TDK, Power Integrations, MediaTek, Realtek, Molex, Yeonho다 |

## 2. 조사 방법과 한계

- 대상: [R13](../references/R13_Vendor_Guides/README.md) `coverage.csv`에서 제외 26쌍과 일부 5쌍에 걸친 제조사 17곳(TA-I는 TA-I Technology(大毅, `tai.com.tw`)다. 인덕터 제조사 TAI-TECH와 다른 회사다).
- 제조사마다 `robots.txt`, 약관, 개발자 포털 첫 페이지, 제품 선택기, 공개 PDF 몇 건만 읽었다. 대량·반복 요청과 로그인·봇 차단 우회는 하지 않았고, 문서화되지 않은 내부 엔드포인트는 찾지도 기록하지도 않았다. 확인용으로 받은 PDF 약 20건은 저장소 밖 임시 폴더에만 있다.
- 약관 인용 일부는 웹 페이지 요약을 거친 것이다. "약관상 ~로 읽힌다"로만 쓰며 법률 자문이 아니다. 원문 대조 전에는 단정하지 않는다.
- 유통사 API(Digi-Key, Mouser, Nexar)는 이번 범위가 아니다. [docs/14 4.2](14_부서기능_확장검토.md)의 판단대로 사내 DB에 쌓지 않는다. Mouser API 약관도 자체 DB 생성·캐시·일괄 다운로드를 금지하는 문구가 있다(지역 사이트별로 문구가 다르다).
- 확인하지 못한 것은 3장 각 제조사의 "미확인"에 적었다. 버튼 동작, 파일 형식, 행 수 한도는 사람이 한 번 눌러 보아야 안다.

## 3. 빈 조합별 추천 경로

경로 약칭: **내보내기** = 제조사 공식 선택기·데이터 파일, **API** = 공식 개발자 API, **PDF** = 공개 PDF 링크 자동 수집(기존 `tools/avl_db/` 파이프라인 재사용), **수동·상용** = 사람이 정리하거나 문의 또는 상용 DB.

### 3.1 제외 26쌍

| 분류 | 제조사 | 추천 경로 | 난이도 | 선결 조건·주의 |
|---|---|---|---|---|
| MCU | STMicroelectronics | 내보내기: 공식 GitHub `STM32_open_pin_data`(BSD-3-Clause, 부품별 XML 약 2,280개) | 낮음 | `github.com`은 이 PC에서 열린다. 신규 시리즈 누락 가능. 코어·RAM·Flash·패키지 수준 |
| MOSFET | onsemi | 내보내기: 선택기 `Export`(Excel·CSV) | 낮음(수동) | 소분류 페이지 5개. 버튼 범위·로그인 미확인 |
| MOSFET | STMicroelectronics | PDF(다른 네트워크) | 높음 | 전용 가이드 URL 미확정. 선택기 내보내기는 미확인 |
| Resistor | Yageo | 수동·상용 | 높음 | JS 사이트. 최신 공식 카탈로그는 없고 가이드는 2020판 |
| Resistor | Samsung EM | 내보내기: 선택기 "List Download"(Chip Resistor 102,717품목) | 낮음(수동 1회) | 파일 형식·범위·로그인 미확인. 자동 호출은 권하지 않음 |
| Resistor | TA-I Technology | 수동·상용 | 중간~높음 | 선택기는 있으나 내보내기·카탈로그 없음. 품번별 사양서 PDF만 있음 |
| Capacitor | Murata | API: PIM API v3(카테고리 전체 JSON) 또는 PIM `Part Number List` CSV 수동 | 중간 | 키 신청에 며칠. 저장·재배포 조건이 명시되지 않아 Murata 확인 필요 |
| Capacitor | Yageo·KEMET | 수동·상용 | 높음 | 최신 카탈로그 PDF 없음(브리프만), 사이트 전체가 JS |
| Inductor | Würth Elektronik | PDF: 2024/2025 제품 브로슈어(시리즈 단위, 이미 받아짐). 품번 단위는 공식 GitHub `.mdb` 검토 | 낮음 / 중간 | 웹 카탈로그 크롤링은 약관상 금지. `.mdb` 라이선스는 재배포 권리 없음으로 읽힘 |
| Inductor | TDK | 수동·상용 | 높음 | `product.tdk.com`이 이 PC에서 403. 열리는 TDK Electronics 쪽은 브리프뿐 |
| Power_IC | Texas Instruments | API: Product Information API | 중간 | 승인 필요. 분류 필터가 없어 우리 분류와의 매핑 필요. 데이터는 비공개 보관 |
| Power_IC | Analog Devices | PDF(다른 네트워크, 소량) | 중간 | 이 PC에서 접속 불가. 약관이 스크레이핑 금지로 읽힘. PDF 날짜 불명 |
| Power_IC | Power Integrations | 수동: 제품군 flyer·데이터시트 목록에서 정리 | 중간 | 통합 가이드는 2016판뿐. 약관이 "사내(internal business) 용도"로 한정 |
| Power_IC | onsemi | 내보내기 | 낮음~중간 | AC/DC 4개·DC/DC 2개 소분류 페이지 |
| Diode | onsemi | 내보내기 | 낮음 | 소분류 페이지 6~7개 |
| Driver_IC | Texas Instruments | API | 중간 | 위와 같음 |
| Driver_IC | Analog Devices | PDF(다른 네트워크) | 중간 | 게이트 드라이버 전용 가이드 없음 |
| Driver_IC | STMicroelectronics | PDF(다른 네트워크) | 중간 | STSPIN 브로셔(BR2409) 등 후보 URL만 확인 |
| Sensor | STMicroelectronics | PDF(다른 네트워크) | 중간 | MEMS 퀵 레퍼런스(2025-03 추정) 후보 |
| Sensor | Analog Devices | PDF(다른 네트워크) | 중간 | MEMS 관성 센서 표 등. 날짜 불명 |
| Sensor | Murata | API: 센서 카테고리 포함 여부를 키 발급 후 확인 | 중간 | 현재 PDF 경로 없음 |
| Wireless_IC | MediaTek | 수동: Filogic 제품 페이지 약 12~15개 | 낮음 | API·내보내기·가이드 PDF 없음. 약관이 "개인·비상업 내부용" |
| Wireless_IC | Realtek | 수동·상용 | 중간 | 제품 목록이 `robots.txt`로 막힌 동적 경로에 의존. 이용약관을 찾지 못함 |
| Connector | TE Connectivity | 내보내기: `Connectors.zip`(Excel·XML 데이터 피드) | 중간 | 로그인 불필요. curl은 403이라 브라우저로 받아야 함. 사내 DB 사용 범위는 TE에 문의 |
| Connector | Molex | 수동·상용(Molex 한국 지사·유통사 문의) | 높음 | `molex.com`이 이 PC에서 응답 없음. API는 약관상 구매·유통 목적 |
| Connector | Yeonho(연호전자) | 수동: 카탈로그 PDF·엑셀 문의 | 낮음 | 카탈로그·내보내기 없음, 약관 링크도 없음 |

### 3.2 일부 5쌍

| 분류 | 제조사 | 추천 경로 | 난이도 | 주의 |
|---|---|---|---|---|
| MCU | Texas Instruments | API 또는 선택표 `Download Excel` 수동 | 중간 | 선택표 버튼 동작·한도 미확인 |
| MOSFET | Infineon | PDF: 공개 250V 이하 범용 가이드(2025-05) | 낮음 | 이 가이드는 3개 상한 때문에 받지 않았던 문서. 고전압·SiC·GaN 2026판은 MyInfineon 로그인 필요 |
| Capacitor | TDK | 수동·상용 | 높음 | 위 TDK 항목과 같음 |
| Driver_IC | Infineon | 수동(MyInfineon 로그인)·상용 | 중간 | 공개 최신 가이드 없음. 제품 표 크롤링은 `robots.txt`에 어긋남 |
| Sensor | Texas Instruments | API 또는 `Download Excel` 수동 | 중간 | 통합 가이드 없음 |

## 4. 제조사별 조사표

각 항목은 [관측: 2026-11-27 조사] 기준이다. "미확인"은 접속 불가·로그인·문서 없음으로 확인하지 못한 것이다.

### 4.1 STMicroelectronics

- 접속: **불가**(`st.com` 타임아웃, 우회하지 않음). `github.com`은 열림.
- API: 미확인(검색에서 공개 개발자 API를 찾지 못함).
- 내보내기: 선택기 내보내기는 미확인. MCU는 [`STM32_open_pin_data`](https://github.com/STMicroelectronics/STM32_open_pin_data)(BSD-3-Clause)에 부품별 XML이 있고 `STM32CubeMX` 내부 DB의 일부다.
- 정책: `robots.txt` 미확인. 일본어판 약관에 자동화 장치·크롤러로 계정을 만들거나 접속하는 것을 금지하는 문구가 있다는 검색 요약이 있으나 영어판 원문은 못 읽었다.
- 미확인: robots.txt, 약관 영어판, 선택기 내보내기 버튼, PDF 후보 6건의 실제 날짜.

### 4.2 Texas Instruments

- 접속: 가능.
- API: **있음.** [Product Information API suite](https://www.ti.com/developer-api/product-information-api-suite.html). OAuth2, myTI 회사 계정과 TI 승인 필요("Only approved customers"). `GET /products`는 페이지 목록(1회 최대 100건), 파라메트릭은 제품 하나씩 호출. 한도 하루 3,000회·초당 5회.
- API 약관: 2(i) TI 데이터(파생·집계 포함)를 서면 동의 없이 공개 호스팅·제3자 제공 금지, 2(h) 출처 표기, 8(c) 접근 종료 시 저장한 TI 데이터 삭제. 캐시·대량 다운로드는 명시되지 않음.
- 내보내기: 제품 선택표에 "Download Excel"이 있다는 검색 근거만 있고 동작은 미확인.
- 정책: `robots.txt`는 `Crawl-delay: 1`이고 제품 표 경로 규칙은 없음. 사이트 약관 4항이 데이터 마이닝·로봇·스크레이핑을 금지하는 것으로 읽힌다.
- 미확인: 승인 소요, `ProductFamilyDescription` 값 형태, 파라메트릭 응답의 분류 정보, 사내 DB 보관 해석.

### 4.3 Infineon

- 접속: 브라우저·WebFetch는 열림, curl은 AWS WAF 챌린지(우회하지 않음).
- API·내보내기: 미확인. 제품 표 페이지에서 내보내기 버튼을 확인하지 못했다.
- 정책: `robots.txt`가 `/assets/row/public/*`은 허용하고 `/assets/row/restricted/*`, `*search*`, `*filter=*`은 막는다. 파라메트릭 필터 URL 크롤링은 어긋난다. 약관은 원문 미추출(검색 요약: 정보 제공·비상업·개인 용도로 복제·배포 한정).
- PDF: 250V 이하 범용 MOSFET 가이드(2025-05, 공개 PDF). 2026판 "Power and Sensing Selection Guide"는 MyInfineon 로그인 필요.

### 4.4 Analog Devices

- 접속: **불가**(연결 끊김, 우회하지 않음).
- API: 제품 데이터 API는 찾지 못함. [ADI API 포털](https://www.analog.com/en/support/api-suites.html)은 주문 API 중심.
- 내보내기: 미확인(파라메트릭 표 다운로드는 2차 자료 정황뿐).
- 정책: 약관 요약상 데이터 마이닝·스크레이핑·자동화 수단 금지, Content 수집·집계 권리 없음. `robots.txt` 미확인.
- PDF: 후보 7건. 모두 직접 열지 못했고 날짜 불명.

### 4.5 onsemi

- 접속: 가능(분류 페이지 하나가 12MB로 무겁다).
- API: 미확인.
- 내보내기: **있음.** 제품 선택기 페이지의 `Export` 메뉴에 Excel·CSV. 확인한 페이지는 [저·중전압 MOSFET](https://www.onsemi.com/products/discrete-power-modules/mosfets/low-medium-voltage-mosfets)(2,969 부품). 범위(필터 결과 전체인지 선택분인지), 로그인 필요 여부는 클릭하지 않아 미확인.
- 정책: `robots.txt`에 `Crawl-delay: 10`. 제품 분류 페이지는 막지 않음(`/products/inventory*`, `/search-results*`는 막음). 약관에 스크레이핑 조항은 없으나 복제 제한(Copyright 절)이 있어 재복제는 제한되는 것으로 읽힌다.
- PDF: 자체 호스팅 MOSFET·Diode 선택 가이드 못 찾음.

### 4.6 Power Integrations

- 접속: 가능. API·내보내기 없음(Solution Finder 84제품 목록은 있으나 내보내기 버튼 없음).
- 정책: `robots.txt` `Crawl-delay: 10`(AI 크롤러 일부는 15). 약관 1절이 콘텐츠를 "solely for your internal business use"로 한정한다. 공개 저장소 게시는 맞지 않는 것으로 읽힌다.
- 자료: 통합 Selection Guide는 2016판뿐. 제품군별 flyer 42종, 데이터시트 79종(날짜 없음).

### 4.7 MediaTek

- 접속: 가능. API·내보내기·Selection Guide PDF 없음. Filogic 제품 페이지(약 12~15개)에 규격이 정적 HTML로 있다.
- 정책: `robots.txt` 전체 허용. 약관이 "personal and non-commercial internal use"로 한정하는 것으로 읽힌다.

### 4.8 Realtek

- 접속: 가능. API·내보내기·PDF 없음. 제품 목록은 `robots.txt`가 막은 동적 경로(`/Product/ListProductMenu`, `/Product/ListProductHits`)에 의존하는 것으로 보인다.
- 정책: 이용약관을 찾지 못해 허용 여부를 판단할 수 없다.

### 4.9 Yageo · KEMET

- 접속: 가능하나 `kemet.com`을 포함해 모두 `yageogroup.com`으로 넘어가고 클라이언트 렌더링이라 본문을 읽지 못한다.
- API·내보내기: 없음/미확인.
- 정책: `robots.txt`가 `?search=` URL을 막는다. 약관 본문은 못 읽었다.
- PDF: Resistor 선택 가이드는 2020판(3년 초과). 그룹 개요 PDF(2026-09)는 시리즈·품번 목록이 없다. Capacitor는 브리프만 있다.

### 4.10 Samsung Electro-Mechanics

- 접속: 가능. `robots.txt` 전체 허용.
- 내보내기: **있음.** [Chip Resistor 선택기](https://product.samsungsem.com/cr/basic-search.do)의 "List Download"(Total Parts 102,717). MLCC 선택기에도 같은 버튼(9,416). 형식·범위·로그인 미확인.
- 정책: 약관에 자동 수집 조항은 없고 10(2)가 영리 목적 이용·복제·배포를 사전 동의 없이 금지하는 것으로 읽힌다.
- PDF: Chip Resistor 카탈로그는 2022-03판(3년 초과).

### 4.11 TA-I Technology

- 접속: 가능. API·내보내기 없음. 선택기 결과에 품번별 사양서 PDF 열만 있다. 다운로드 페이지에는 정책 문서뿐.
- 정책: `robots.txt` 전체 허용. 약관에 자동 수집 조항 없음(개인정보 안내 수준).

### 4.12 Murata

- 접속: 가능(`pim.murata.com`은 JS 앱).
- API: **있음.** [Product Information Management API v3](https://www.murata.com/en-global/support/api). 무료, my Murata 계정과 키 신청·승인("several days"). `GET /v3/products`(카테고리 필수, 한 번에 2,000건)와 카테고리 전체 사양 JSON 다운로드 URL(7일 유효). 73개 카테고리. 센서 카테고리 포함 여부 미확인. 한도 미확인.
- API 약관: 10.1(3)이 스크레이핑·크롤링 등 통상 범위를 넘는 접근을 금지. 5.2가 용도를 한정. DB 저장·재배포 허용 여부는 명시되지 않음.
- 내보내기: `pim.murata.com`의 Part Number List(CSV 주의문이 공식 페이지에 있음). 시리즈·검색 결과 단위로 보이고 전체 일괄 여부는 미확인.
- PDF: MLCC 카탈로그는 공식 PDF 라이브러리에 없다.

### 4.13 TDK

- 접속: `product.tdk.com`·`www.tdk.com`은 **403**(Akamai, `robots.txt`도 403, 우회하지 않음). `tdk-electronics.tdk.com`(구 EPCOS)은 열림.
- API·내보내기: 없음/미확인. TDK Electronics 제품 검색에 내보내기 언급 없음.
- 정책: TDK Electronics 약관 4.1이 콘텐츠의 복제·전송·배포·저장을 제한한다. `robots.txt`는 일반 봇의 제품 검색을 막지 않음. `product.tdk.com` 약관은 미확인.
- PDF: MLCC 카탈로그는 막힌 도메인에 있다. 열리는 쪽은 브리프·기술 안내서다.

### 4.14 Würth Elektronik

- 접속: 부분(curl 403, WebFetch 가능).
- API: 있음. REDEXPERT API와 Customer API 모두 영업 승인형. 한도·저장 조건 비공개.
- 내보내기: 표 단위 내보내기 없음. 공식 GitHub 라이브러리(Altium `.mdb`, KiCad)가 대안일 수 있으나 내용 미확인. 라이선스는 사용을 허용하되 재배포 권리를 주지 않는 것으로 읽힌다.
- 정책: 약관이 "data mining or similar data gathering or extraction methods"를 금지한다. `robots.txt`는 카탈로그 다운로드 경로 일부를 막는다.
- PDF: Electronic Components 2024/2025 브로슈어(48쪽, 시리즈 단위 표).

### 4.15 TE Connectivity

- 접속: 가능(대량 파일 HEAD는 Akamai 403).
- 내보내기: **있음.** [Product Information Files](https://www.te.com/en/services/xml-download.html)의 분류별 zip. `Connectors.zip`(Excel·XML), 로그인 안내 없음. 파일 크기·내용은 직접 열어 보지 못함.
- API: 있음(MuleSoft 포털, 승인 필요, 분당 30회·일 5,000회). 약관이 캐시·저장·대량 다운로드를 금지하는 것으로 읽혀 DB 구축에는 맞지 않는다.
- 정책: `robots.txt`가 카탈로그 경로 일부와 AI 크롤러를 막고 데이터 피드 경로는 막지 않는 것으로 보인다(원문 라인 대조 필요). 약관(2023)은 "personal use for non-commercial purposes" 다운로드로 한정한다. 데이터 피드 안내 문구와 서로 달라 TE에 문의하는 것이 안전하다.

### 4.16 Molex

- 접속: **불가**(`molex.com` 타임아웃). 개발자 포털 `developer.molex.com`은 열림.
- API: 있음(무료, 신청·검토, 분당 400회). 약관 허용 목적이 구매·관련 활동·유통으로 좁고 데이터셋 구축이 금지되는 것으로 읽힌다.
- 내보내기·PDF: 접속 불가로 미확인. 제품군별 레퍼런스 가이드 URL 후보만 있다.

### 4.17 Yeonho Electronics(연호전자)

- 접속: 가능. 카탈로그·자료실·API·내보내기 없음. 제품 화면은 자바스크립트 호출. `robots.txt` 404, 약관 링크 없음.

## 5. 경로 유형별 정리

| 경로 | 해당 제조사 | 장점 | 제약 |
|---|---|---|---|
| 내보내기 | onsemi, Samsung EM, TE, Murata, ST(MCU) | 구조화된 표, 스크레이핑 없음 | 버튼·파일 형식·범위를 사람이 한 번 확인해야 한다. 약관상 사내 DB·공개 게시 범위는 제조사별로 다르다 |
| API | TI, Murata (Würth·TE·Molex는 약관상 부적합) | 가장 깨끗한 구조화 | 승인 대기. 저장·재배포·삭제 조건. 한도 |
| PDF | Infineon, Würth, ST·ADI(다른 네트워크) | 기존 추출·검증 파이프라인 재사용, 제조사 홍보 자료라 공개 저장소 기준이 이전과 같음 | 개별 제품이 없는 문서는 계열 행에 그침 |
| 수동·상용 | Yageo·KEMET, TA-I, TDK, Power Integrations, MediaTek, Realtek, Molex, Yeonho | 약관 위험이 가장 작음 | 사람 시간 또는 라이선스 비용(docs/14 4.2 조건 8) |

## 6. 권장 착수 순서

1. **대기 시간이 긴 신청부터 한다.** TI Product Information API 접근 요청, Murata PIM API 키 신청. 승인에 며칠이 걸린다. 신청 때 사용 목적(사내 시연·사양 조회용 DB)을 적고 저장 조건을 함께 문의한다.
2. **사람이 한 번 눌러 형식과 범위를 확인한다.** onsemi 선택기 `Export`(MOSFET·Power_IC·Diode), Samsung EM `List Download`, TE `Connectors.zip`, Murata `Part Number List`. 버튼 범위·열 구성·행 수·로그인 여부를 적고 나서 자동화 여부를 정한다. 자동화한다면 onsemi는 `Crawl-delay: 10`을 지킨다.
3. **공개 PDF를 기존 파이프라인에 넣는다.** Infineon 250V 이하 범용 가이드(2025-05), Würth 2024/2025 브로슈어. 이 경로의 산출물은 이전 PDF와 같은 기준(제조사가 홍보용으로 공개한 자료, 2026-11-27 사용자 확인)을 적용한다.
4. **ST MCU는 GitHub 오픈 데이터**를 내려받아 사양 열에 맞춘다.
5. **다른 네트워크가 필요한 곳**(ST, ADI, Molex, TDK Product Center)은 접근이 되는 환경에서 PDF 후보 URL과 날짜를 먼저 확인한다.
6. **나머지**는 제조사 문의(연호전자 등)나 상용 DB 비교로 넘긴다.

## 7. 이 조사가 정하지 못한 것

[docs/11](11_결정_미결_목록.md)에 OI-26~28로 올렸다.

| 항목 | 내용 |
|---|---|
| OI-26 | 공식 API·내보내기로 받은 제조사 데이터를 사내 DB에 두는 범위와 공개 저장소 게시 여부. 제조사에 확인할지, 비공개 저장소·사내 DB로만 둘지 |
| OI-27 | 3년 기준(최근 3년 이내 문서)의 예외(예: Yageo 2020판 선택 가이드)와 상용 부품 DB 라이선스 비교 착수 여부 |
| OI-28 | 이 PC에서 막힌 제조사(ST, ADI, Molex, TDK Product Center)를 다른 네트워크에서 수집할 것인지 |

## 8. 출처

제조사 페이지는 4장에 링크했다. 약관·`robots.txt`는 각 제조사 도메인의 `/robots.txt`와 이용약관 페이지에서 2026-11-27에 읽었다. 유통사 API 약관은 [Mouser API 약관](https://www.mouser.com/en/apiterms/)과 [docs/14 9장](14_부서기능_확장검토.md) 출처를 따른다. 조사 대상 목록은 [R13 coverage.csv](../references/R13_Vendor_Guides/coverage.csv)다.

## 9. 수집 실행 결과 (2026-11-27 오후)

사용자 결정(DEC-20): 백데이터는 비공개로 두고 시연 목업의 표에 넣은 행만 공개한다. 정보가 많아지는 방향으로 수집한다. 원천 파일과 변환 결과는 `AVL_DB/_private/`(git 제외)에 있고, 실행 스크립트는 [tools/avl_db/collect/](../tools/avl_db/collect/README.md)다.

| 출처 | 방법 | 결과 | AVL 행 | 비고 |
|---|---|---|---|---|
| STMicroelectronics STM32 | 공식 GitHub `STM32_open_pin_data`(BSD-3-Clause) 복제 | 성공 | MCU 2,282 | 코어·클럭·Flash·RAM·전압·온도·패키지·주변장치 수. ST 사이트는 이 PC에서 접속 불가라 사용하지 않음 |
| onsemi | 제품 선택기 `Export > CSV`를 Chrome 자동화로 한 번씩 누름. `Crawl-delay: 10` 준수 | 소분류 페이지 20개 중 18개 성공 | 6,615 (MOSFET 2,378 · 다이오드 3,649 · 전원 IC 567 · 드라이버 IC 21) | GaN FET·LED 드라이버 페이지는 Export 버튼이 없다. 제너 다이오드는 첫 시도에서 시간 초과, 대기를 420초로 늘려 받았다. 참고 단가 열은 읽지 않았다 |
| 삼성전기 MLCC | 제품 검색 `List Download` 1회 | 품번 9,416개(중복 1 제외 9,415행) | Capacitor 9,415 | 파일에 품번만 있다. 크기·유전체·용량·허용오차·전압은 삼성전기 MLCC 카탈로그 6~8쪽의 품번 체계표로 해독했고 표에 없는 코드는 비웠다(`원문 대조` 열 = 품번 해독) |
| 삼성전기 Chip Resistor | 같은 버튼 | **실패**: `listDownload.do`가 404(전체 102,717품목, 크기 필터를 걸어도 같음) | 0 | 서버 쪽 오류로 보인다. 같은 사이트의 MLCC는 됐다. 일반 브라우저에서 사람이 한 번 눌러 보면 된다 |
| TE Connectivity | 제품 정보 파일 `Connectors.zip`(Excel 데이터 피드 64MB, 소분류 119개)을 Chrome으로 한 번 받음 | 성공 | Connector 59,839 | 파일이 inch·°F라 피치는 mm, 온도는 °C로 환산했다. 가격·재고는 파일에 없다 |
| MediaTek · Power Integrations | 제품 웹 페이지를 읽음(에이전트, 읽기 도구가 요약해서 돌려줌) | 성공 | Wireless_IC 13 · Power_IC 84 | MediaTek 값은 원문 대조를 권장. PI는 Solution Finder 목록(제품군 84개)이라 사양이 적다 |
| 새 공개 PDF 4건 | Würth 2024/2025 브로슈어, Infineon 250V 범용 MOSFET 가이드, TE InDeCo 포트폴리오, PI PowiGaN 플라이어 | 원문 대조 433행 전부 통과 | 인덕터 188 · MOSFET 169 · 커넥터 59 · 전원 IC 17 | Würth·TE·PI 문서는 개별 제품을 거의 열거하지 않아 대부분 계열 행이다 |

합계: 제품 행 52,154 → **130,835**(부품번호 95,473 · 사양 조합 33,551 · 계열 1,811), 제조사 22 → 28곳, AVL 항목(분류 × 제조사) 35 → 44개. 시연 목업 `DATA.avl`이 4.4MB에서 14MB로, HTML이 6MB에서 15.7MB로 커졌다. 13만 행에서도 필터 한 번에 0.3~0.5초, 쪽 이동·정렬은 0.05초 안쪽이다(Chrome, 2026-11-27 측정).

수집하지 못한 것

| 대상 | 이유 |
|---|---|
| TI API, Murata PIM API | 계정·승인 신청이 필요하다. 사용자가 신청한다 |
| Murata `pim.murata.com` 제품 검색 | 이용 제한(Limited Use) 동의 화면이 먼저 나온다. 동의 클릭은 대신하지 않았다 |
| ADI, Molex, ST 사이트, TDK Product Center | 이 PC에서 응답 없음·403. 우회하지 않았다 |
| Würth 공식 GitHub `.mdb` 라이브러리 | 저장소는 받았으나 `.mdb`를 읽을 파서 설치가 허용되지 않아 중단하고 받은 파일을 지웠다. 파서 설치(`pip install access-parser`) 또는 Access 드라이버 사용을 허용하면 이어갈 수 있다 |
| Yageo·KEMET, TA-I, Realtek, 연호전자 | 공식 일괄 경로 없음(4장) |
| 삼성전기 Power Inductor·Tantalum·Silicon Capacitor 목록 | 같은 `List Download`가 있으나 품번만 오고 해독표(카탈로그)가 3년 기준에 맞지 않아 이번에는 받지 않았다 |

## 10. 사용자가 판단할 항목 (약관·정책 확인)

DEC-20에 따라 수집은 막지 않고 아래를 남긴다. 시연 목업(공개)의 표에는 이 출처의 행이 이미 들어 있다. 판단 결과에 따라 해당 출처 행을 빼려면 `AVL_DB/_private/merged/`의 병합 파일에서 출처(`doc`)로 걸러 `build_data_avl.py`를 다시 돌리면 된다.

| # | 출처(행 수) | 확인할 점 | 근거 |
|---|---|---|---|
| 1 | Power Integrations 웹(84) | 약관 1절이 콘텐츠를 "solely for your internal business use"로 한정한다. 공개 표 게시와 맞지 않을 수 있다 | 4.6 |
| 2 | MediaTek 웹(13) | 약관이 "personal and non-commercial internal use"로 한정하는 것으로 읽힌다. 값은 요약 도구를 거쳐 원문 대조가 필요하다 | 4.7 |
| 3 | 삼성전기 MLCC(9,415) | 약관 10(2)가 영리 목적 이용·복제·배포를 사전 동의 없이 금지하는 것으로 읽힌다. 품번 목록은 공식 `List Download`로 받았다 | 4.10 |
| 4 | onsemi(6,615) | 약관 Copyright 절이 사이트 정보의 복제·전송을 제한한다(개인 비상업 1부·고객 주문 예외로 읽힘). 공식 `Export` 버튼으로 받았고 `robots.txt`는 지켰다 | 4.5 |
| 5 | TE(59,839) | 약관(2023)은 "personal use for non-commercial purposes" 다운로드로 한정하고, 데이터 피드 안내문은 제품 정보를 고객 사이트·조달 플랫폼에 채우는 용도로 안내한다. 둘이 어긋나 TE에 문의하는 편이 안전하다 | 4.15 |
| 6 | ST 오픈 데이터(2,282) | BSD-3-Clause라 재배포할 때 저작권·라이선스 고지를 유지해야 한다. 목업 `제조사 자료` 탭의 출처 이름에 라이선스를 적어 두었으나 별도 고지 문구가 필요한지 확인 | 4.1 |
| 7 | 새 공개 PDF 4건(433) | 기존 PDF와 같은 기준(홍보용 공개 자료, 사용자 확인 2026-11-27) | — |

수집 중에 생긴 일

- onsemi 수집 스크립트가 중복 실행되어 약 7분간 두 프로세스가 동시에 요청했다(각각 12초 간격이라 합치면 `Crawl-delay: 10`보다 촘촘했다). 발견 즉시 모두 종료하고 하나만 다시 돌렸다.
- 삼성전기 Chip Resistor `List Download`는 전체와 크기 필터 상태로 총 3번 눌렀다(안내문은 반복 실행을 권하지 않는다). 모두 404였다.
- Würth GitHub 저장소를 받는 동안 `.mdb` 읽기용 패키지 설치가 자동 승인 검사에서 거부되어 우회하지 않고 중단했다.

## 11. 부품번호 조립: 문서에 형명이 없던 행 (2026-11-28)

사용자 질문: Walsin 저항 등의 부품번호가 비어 있는 이유와, 문서로 형명을 정할 수 있으면 최대한 채우라는 지시. 이어서 Walsin 밖에도 비어 있는 제품이 있는지 확인해 같은 방식으로 채우라는 지시. 결정은 DEC-21([docs/11](11_결정_미결_목록.md)), 실행 스크립트는 Walsin이 [derive_walsin_pn.py](../tools/avl_db/collect/derive_walsin_pn.py), ROHM·Panasonic이 [derive_rohm_panasonic_pn.py](../tools/avl_db/collect/derive_rohm_panasonic_pn.py)다. 11.1~11.6은 Walsin, 11.7은 그 밖의 제조사다.

### 11.1 비어 있던 이유

- [관측 2026-11-27] 두 Walsin 카탈로그는 완성된 형명 목록을 싣지 않는다. 칩 저항 카탈로그는 시리즈별 선택표(저항 범위)와 주문 코드(How To Order, PDF 4~5쪽)만 있고, MLCC 카탈로그는 크기 × 유전체 × 정전용량 × 전압 매트릭스(칸마다 두께 기호)와 주문 코드(PDF 5쪽)만 있다.
- 1차 추출은 DEC-19의 "형명을 합성하지 않는다"를 따라 매트릭스 칸을 `사양 조합`, 범위 표를 `계열`로 풀고 부품번호를 비웠다. 공란은 MLCC 칸 32,647 · 저항 252 · 계열 행 546(칩 저항 443, 저항 제품 가이드 49, 커패시터 제품 가이드 54)이었다.
- 그 문구는 이번 지시와 맞지 않았다. 문서가 주문 코드를 직접 인쇄했으면 한 칸의 사양이 형명을 정한다. 그래서 DEC-19를 "문서의 주문 코드가 정하는 형명만 조립한다"로 좁혔다(DEC-21).

### 11.2 한 일

| 대상 | 이전 | 이후 |
|---|---|---|
| MLCC 사양 조합 칸 | 32,647칸, 부품번호 없음 | 31,880칸을 부품번호 94,905행으로 풂(허용오차마다 한 행. S2·S3의 UL/TUV 열과 CQC 열은 형명이 같아 1,134개를 합침) |
| 칩 저항 WW(저저항) 칸 | 229칸 | 부품번호 458행(허용오차 ±1%·±5%) |
| 칩 저항 WA04P(감쇠기) 칸 | 23칸 | 부품번호 23행 |
| 합계 | 제품 행 130,835 | **194,089**(+63,254) |
| 조립하지 못한 칸 | | MLCC 767칸: 크기 1825가 766칸(SH 499 · M 266 · ST 1), 허용오차가 없는 SH 1칸. 부품번호는 비우고 비고에 사유를 적었다 |
| 그대로 둔 공란 | | 계열 행 546. 저항값·정전용량 범위만 인쇄돼 있어 값을 정하기 전에는 형명이 하나로 정해지지 않는다. 표준 저항값표(E24·E96)로 풀면 시리즈마다 수백 형명, 전체 수십만 행이 되는데 문서가 제품으로 열거한 것이 아니라서 풀지 않았다(DEC-19 유지) |

조립하지 못한 칸이 생긴 이유: 시리즈 두 글자 형식(SH·M·ST)의 크기 코드 목록(PDF 5쪽: 02·03·15·11·18·21·22·31·32·42·43·52·55·56)에 1825가 없다. 코드를 짐작해 넣지 않았다. 일반·중·고압 시리즈는 크기를 인치 그대로 써서 1825도 조립된다.

### 11.3 조립 규칙(문서 근거)

| 시리즈 | 형명 순서 | 근거 |
|---|---|---|
| 일반(4V~100V) · 01R5 · 중·고압 | 크기(인치, 01005는 `01R5`) + 유전체 + 정전용량 + 허용오차 + 전압 + 단자 `C` + 포장 `T` | MLCC PDF 5쪽 How To Order, 8·14·15쪽 형명 설명 |
| 고압 표면 코팅 | 위와 같고 단자 `M` | 18쪽 |
| RF · UF · RT · HH · MT · ST · VT · MG · HT · SH · SG · TT · FT | 시리즈 두 글자 + 크기 두 자리 코드(03=0201, 15=0402, 21=0805…) + 유전체 + 정전용량 + 허용오차 + 전압 + 단자 `C` + 포장 `T` | 19~53쪽 시리즈별 형명 설명 |
| S2 · S3(안전 인증) | 위와 같고 전압 칸이 서지(임펄스) 전압 코드(5000V=`502`, 2500V=`252`), 단자 `K`(표면 코팅만 공급하는 `+` 칸은 `M`) | 38·41쪽 |
| M · V(메가 캡) | 시리즈 + 적층 수 + 크기 코드 + 유전체 + 정전용량 + 허용오차 + 전압 + 두께 기호(칸의 글자) + 제어 코드(M은 `L`, V는 `M`, 문서 예시 값) | 54·56쪽 |
| 칩 저항 WW | 시리즈명(예 `WW25A`) + 저항 코드(`R005`=5mΩ, `R0L5`=0.5mΩ, `0L75`=0.75mΩ) + 허용오차(`F`=±1%, `J`=±5%) + 포장 `T` + 단자 `L` | 저항 PDF 4쪽 |
| 칩 저항 WA04P | `WA04P` + 감쇠량 코드(`001`=1dB, `R05`=0.5dB) + 임피던스 `X` + 허용오차 `A`~`H`(0dB는 `P`) + `T` + `L` | 저항 PDF 21쪽 |

공통 코드: 정전용량·전압은 "유효숫자 두 자리 + 0의 개수, R은 소수점"(4V=`4R0`, 100V=`101`, 1250V만 범례의 `12E`). 유전체 `N`=NP0 · `G`=X8G · `B`=X7R · `A`=X7S · `T`=X7T · `S`=X6S · `X`=X5R. 허용오차 `A` ±0.05pF · `B` ±0.1pF · `C` ±0.25pF · `D` ±0.5pF · `F` ±1% · `G` ±2% · `J` ±5% · `K` ±10% · `M` ±20% · `Z` -20/+80% · `P` ±0.02pF · `Q` ±0.03pF.

### 11.4 문서가 정하지 않아 고른 값 [판단]

| 요소 | 고른 값 | 영향 |
|---|---|---|
| 포장 | `T`(7인치 릴). 문서 예시가 모두 `T`다. 같은 형명에 포장 코드만 다른 변형(`Q` 10인치, `G` 13인치)이 있다. 7인치 릴 수량이 없는 칸(2220 크기, 두께 기호 R)은 `G` | `G`는 21행 |
| 단자 | 시리즈의 문서 예시 값(`C`, 고압 표면 코팅 `M`, S2·S3 `K`) | |
| M 시리즈의 별표 없는 칸 | 허용오차 `K`(±10%)만. 문서는 별표 칸을 "M(±20%)만"이라고만 적어서 나머지는 예시값으로 정했다 | 448행 |
| FT 시리즈 매트릭스 7칸 | 허용오차 `M`(±20%). 같은 쪽 형명표 11행이 모두 ±20%다 | 7행 |
| 칩 저항 WW의 접미 코드 | 전력·TCR·AEC 코드는 넣지 않았다. 문서 예시(`WR08X4R3_JTL`)도 접미 없이 끝난다 | |

### 11.5 문서 안의 불일치와 처리

| 곳 | 불일치 | 처리 |
|---|---|---|
| HT 시리즈(36쪽) | 예시 형명의 유전체 글자가 `R`, 범례는 `G`=X8G, 매트릭스는 X8G뿐 | 범례 `G` |
| MG 시리즈(33쪽) | 예시 형명의 앞머리가 `MT` | 범례의 `MG` |
| SG 시리즈(51쪽) | 예시 형명은 `K`, 설명 칸은 `J` | 매트릭스 허용오차(K·M) |
| M·V 시리즈(54·56쪽) | 예시 형명의 `K`가 별표(M만) 칸과 맞지 않음 | 매트릭스(M) |
| 전압 600V(M 시리즈 10행), 3500V(고압 표면 코팅 4행) | 범례에 코드가 없다 | 코드 규칙으로 `601`, `352`. 600V는 630V의 오기일 수 있다 |

### 11.6 검증 [관측 2026-11-27]

- 정전용량 코드: 매트릭스 행 머리글의 `값 (코드)` 181종과 비교해 불일치 0. 행의 정전용량 140종이 모두 문서 머리글과 같은 수치·같은 코드다.
- 전압 범례 23개 코드와 저항 코드 예시 10개(`R100`·`R033`·`R560`·`R0L5`·`0L75`·`15L5`·`R2L5`·`R002`·`R005`·`R020`)가 전부 일치한다.
- FT 시리즈: 문서가 인쇄한 형명 11개를 칸의 사양에서 다시 조립해 11개 모두 일치했다.
- 문서의 시리즈별 예시 형명 22개 중 19개가 조립 결과에 있다. 없는 3개(SG·M·V)는 11.5의 불일치 때문이다.
- 시연 화면에서 Walsin `0603B104K` 검색이 0건에서 6건, Walsin 저항 `WW25A`가 56행(저항값 28 × 허용오차 2)이 되었다. 필터 개수와 낱말 검색 결과는 데이터를 직접 센 값과 일치한다.

### 11.7 Walsin 밖의 빈 부품번호 전수 확인과 조립

2026-11-28에 부품번호가 빈 행 3,134개(계열 1,811 · 사양 조합 1,323)를 제조사·문서별로 세고, 사양 조합 행 556개(Walsin 제외)의 문서를 읽어 형명 규칙이 인쇄돼 있는지 확인했다.

| 제조사 | 빈 행 | 문서의 형명 규칙 | 결과 |
|---|---|---|---|
| ROHM 제너 다이오드 | 382 | 있음. PDF 34쪽 Product No. Explanation과 22·23쪽 위쪽 예시(`EDZV` `FH` `T2R` `3.6` `B`, `YDZV` `FH` `TR` `13`). 표 주석이 "이 표는 판매 가능한 전압"이라고 적었다 | **382행 전부 조립** |
| Panasonic OS-CON SMD | 15(단일 값) | 있음. PDF 37쪽: 정격전압 코드 + 시리즈 + 정격용량 코드 + 허용오차 `M` | **9행 조립**(`16SVPG330M`, `2R5SVPC2700M` 등) |
| Panasonic 그 밖 | 140 | 용량·전압이 범위("33μF~47μF")로만 인쇄된 개요표 행. 범위 안의 어느 값이 제품인지 문서가 열거하지 않는다 | 비움 |
| Panasonic POSCAP | 6 | 41쪽에 규칙은 있으나 전압 코드가 둘(`16` 또는 `1C`, `2R5` 또는 `E`)이고 특수 코드(0~4자리)가 선택이며, 시리즈 `TC`는 규칙의 "3~4자리"와 맞지 않는다 | 비움 |
| Vishay 전류 센서 WSLT | 10 | 선택 가이드에 형명 규칙이 없다 | 비움 |
| Power Integrations · TE | 5 · 4 | 플라이어·포트폴리오에 형명 규칙이 없고 제품군 하나에 사양이 여럿이다 | 비움 |
| 계열 행 | 1,811 | 범위만 인쇄된 제품군이다. 계열명이 형명처럼 생긴 301행(Coilcraft 195, Vishay, Power Integrations 등)도 확인했으나 제품군 이름이거나(`1205POC`, `AWM1000`) 전압 등급 범위의 앞뒤 끝만 적은 것(`VS-T40HF10 ~ VS-T40HF120`)이라 형명 하나로 정해지지 않는다 | 비움 |

못 채운 행은 비고 맨 앞에 `형명 미조립: 사유`를 적었다(Walsin 767칸은 비고 끝).

ROHM 제너 규칙 [관측]:

| 요소 | 출처 |
|---|---|
| 형명 = 시리즈 + 등급 코드 + 테이핑 코드 + 제너 전압 + 세부 구분(예 `EDZV` `FH` `T2R` `3.6` `B` → `EDZVFHT2R3.6B`) | 34쪽 설명과 22쪽 위쪽 예시. 23쪽 예시는 `YDZVFHTR13`(전압 `13`, 세부 구분 없음) |
| 등급 코드: 표 머리글의 Automotive Grade Code(`FH` 또는 `TF`)를 AEC-Q101 `YES`인 행에만 붙이고 `—`인 행은 붙이지 않는다 | 22·23쪽 표 |
| 테이핑 코드: 머리글의 Taping Code(ADZ `T15R`, CDZV·EDZV `T2R`, UFZV·UDZV·UDZLV `TE-17`, TFZV·YFZV·TDZV·YDZV·KDZV·KDZLV·PDZV `TR`, BZX84 `T116`, PTZ `TE25`) | 22·23쪽 머리글. 34쪽 포장표와 패키지별로 모두 일치(SOD-923 `T2R`, SOD-323FL `TE-17`, SOD-323HE `TR`, SOT-23 `T116`, SMA `TE25`) |
| 전압·세부 구분: 표의 첫 칸(`2.0B`, `47A`, `13`) 그대로 | 22·23쪽 표 |
| `BZX84BxxLY` · `BZX84CxxLY`: 시리즈명의 `xx` 자리에 표의 전압 구분(`2V4`)을 넣고 뒤에 등급·테이핑 코드를 붙임(`BZX84C2V4LYFHT116`) | 문서에 이 시리즈의 예시는 없다. 시리즈명의 `xx`와 표의 `2V4` 열로 [판단]한 것이라 다른 시리즈보다 약하다. BZX84는 50행 |

검증 [관측 2026-11-28]: 문서 예시 `EDZVFHT2R3.6B`와 `YDZVFHTR13`이 조립 결과에 있다. 조립한 382행의 형명은 모두 유일하고 기존 형명과 겹치지 않는다. 차량용 행은 `FH` 175행 + `TF` 108행이고 나머지 99행은 등급 코드가 없다.

고른 값 [판단]: AEC-Q101 `YES`인 행은 차량용 형명(등급 코드 포함)만 만들었다. 같은 전압의 일반 형명도 있을 수 있으나 문서가 정하지 않았다. 반대로 `—`인 행은 등급 코드 없는 형명만 만들었다.

### 11.8 영향

- 시연 목업 `DATA.avl`은 130,835 → 194,089행(Walsin +63,254). ROHM·Panasonic 391행은 사양 조합 행을 부품번호 행으로 바꾼 것이라 총 행 수는 그대로다. HTML 15.7MB → 22.3MB(gzip 2.1 → 2.8MB). 19만 행에서 필터 한 번이 0.8~1.1초로 느려져 필터 계산을 고쳤다(낱말·분류 조건은 한 번만 적용, 대문자 본문 캐시, 고른 필터만 판정). 결과: 분류 선택 0.23초, 낱말 입력 0.01초, 쪽 이동 0.05초 안쪽.
- 조립 형명 행도 목업 표에 들어가므로 공개된다(DEC-20: 표에 넣은 행은 공개). 조립한 형명이라는 점은 `원문 대조`의 `주문 코드 조합`과 비고에 남는다.
- 비공개 병합 파일(`_private/merged`)과 엑셀(`_private/xlsx`)을 새 데이터로 바꿨다. 공개 `AVL_DB/AVL_Parts_*.xlsx`(1차 52,154행)는 바꾸지 않았다. 거기에는 Walsin·ROHM·Panasonic 사양 조합 행의 부품번호가 여전히 비어 있다.
- 조립한 형명은 문서 규칙상 성립하는 형명이다. 제조사가 지금 그 형명을 판매·재고한다는 보증이 아니다. 구매 전에 제조사·유통사 조회가 필요하다.

---

## 변경 이력

| 버전 | 일자 | 내용 |
|---|---|---|
| v0.1 | 2026-11-27 | 최초 작성. 빈 26쌍·일부 5쌍의 수집 경로 조사(17개 제조사), 경로 추천, 약관 위험, 착수 순서, OI-26~28 |
| v0.2 | 2026-11-27 | 9장(수집 실행 결과: ST·onsemi·삼성전기 MLCC·TE·MediaTek·Power Integrations·새 PDF 4건, 행 52,154 → 130,835)과 10장(약관 확인 항목 7건, 수집 중 일어난 일) 추가. DEC-20 |
| v0.3 | 2026-11-28 | 11장(Walsin 부품번호 조립: 공란 이유, 조립 규칙과 근거, 고른 값, 문서 안 불일치, 검증, 다른 제조사 공란) 추가. 행 130,835 → 194,089. DEC-21 |
| v0.4 | 2026-11-28 | 11.7 전면 갱신: 부품번호 공란 3,134행 전수 확인. ROHM 제너 382행·Panasonic OS-CON 9행을 문서의 형명 규칙으로 조립. 못 채운 행(Panasonic 146, Vishay 10, Power Integrations 5, TE 4, 계열 1,811)의 사유. 11.8 영향 갱신 |
