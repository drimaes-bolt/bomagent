# R13 제조사 Selection Guide · Catalog PDF (시연용 AVL·제품군 DB 입력)

> 2026-11-27 수집. 제조사가 공개한 Selection Guide·Product Guide·Catalog PDF를 도메인별로 모았다. 다봄 시연에서 Excel로 관리할 AVL(Approved Vendor List)과, AVL별 공급 가능 제품군 DB(docs/14 4장, `DT-12`)의 원천 문서다. PDF는 제조사 저작물이라 git에 올리지 않는다(`.gitignore`). 이 README와 `manifest.csv`·`coverage.csv`만 추적한다.

| 항목 | 내용 |
|---|---|
| 요청 쌍 | 61쌍(도메인 11 × 제조사). 요청 목록은 사용자 지시, 후보 제조사는 [R09](../R09_EP_Vendor_List_by_Category.md) |
| 결과 | 수집 30쌍 · 일부 5쌍 · 제외 26쌍 (합계 61쌍) |
| 파일 | 65개(도메인 폴더마다 복사한 것 포함), 고유 PDF 55개, 약 213 MB |
| 날짜 기준 | 문서 날짜가 2023-11-27 이후(최근 3년). 못 찾은 쌍은 제외 |
| 편집 | 없음. 내려받은 그대로 둔다. 여러 도메인 제품이 한 PDF에 있으면 통째로 두고, 같은 제조사의 해당 도메인 폴더마다 바이트가 같은 복사본을 둔다 |
| 검증 | 2026-11-27 별도 점검: 65개 모두 `%PDF` 헤더, 50 KB 이상, 텍스트 추출 가능(Taiyo Yuden 4개는 글꼴 인코딩이 깨져 있음), 날짜는 본문 인쇄 날짜 또는 PDF 메타데이터로 확인, 매니페스트와 파일·크기 일치 |

## 폴더 구조

```text
R13_Vendor_Guides/
├─ <도메인>/<제조사>/<파일>.pdf      MCU MOSFET Resistor Capacitor Inductor Power_IC Diode Driver_IC Sensor Wireless_IC Connector
├─ manifest.csv                      파일마다 제목·문서 날짜·근거·출처 URL·쪽 수·해시·한계(Excel로 열 수 있다)
├─ coverage.csv                      61쌍별 수집·일부·제외와 제외 사유
└─ README.md
```

## 도메인 × 제조사 현황

수집 = 문서를 받음 · 일부 = 받았지만 그 제조사의 다른 제품군은 받지 못함 · 제외 = 받지 못함(사유는 `coverage.csv`).

| 도메인 | 제조사 | 상태 | 파일 | 사유·한계 |
|---|---|---|---|---|
| MCU | STMicroelectronics | 제외 | 0 | st.com이 이 PC에서 응답하지 않음(PDF·HTML 요청 모두 타임아웃). 접근 제한은 우회하지 않음. 후보: STM32 패밀리 개요(날짜 미확인). 다른 네트워크에서 재시도 가능 |
| MCU | Microchip | 수집 | 3 | dsPIC33 계열 가이드 4쪽. 종합 가이드는 2023-11 이전이라 제외 / 계열별 빠른 참조 2쪽. 8·16·32비트를 아우르는 종합 가이드는 2023-11 이전이라 제외 |
| MCU | TI | 일부 | 1 | MSPM0 개요만 저장. MSP430·C2000 선택 가이드는 최근 3년 내 문서를 찾지 못함(TM4C 가이드는 2021) / MSPM0 계열만 다룬다(MSP430·C2000 제외) |
| MCU | NXP | 수집 | 3 | curl은 404, WebFetch 도구가 같은 공식 URL에서 받은 바이트를 복사. 로그인 없는 공개 문서 |
| MCU | Infineon | 수집 | 2 | infineon.com 사본은 로그인으로 넘어가서, Infineon 커뮤니티가 공개 첨부로 올린 같은 문서를 받았다 / 가전 응용 기준 가이드. 도메인별 포트폴리오 가이드가 아니다. 이 도메인에서 구한 최신 공개 문서 |
| MOSFET | Infineon | 일부 | 3 | 3개 상한으로 저장. 공개 CoolMOS 선택 가이드는 2016~2019판이라 기준 미달. 250 V 이하 범용 MOSFET 가이드(2025-05)와 전원 토폴로지 가이드(2025-03)는 받지 않음 / 가전 응용 기준 가이드. 도메인별 포트폴리오 가이드가 아니다. 이 도메인에서 구한 최신 공개 문서 |
| MOSFET | onsemi | 제외 | 0 | 공식 MOSFET 포트폴리오 가이드 중 2023-11 이후 문서를 찾지 못함. 유통사(Richardson RFPD) 사본은 403. 공식 브로셔는 2022판 |
| MOSFET | STMicroelectronics | 제외 | 0 | st.com 응답 없음(위와 같음). 후보: 전력 관리 브로셔, 디지털 전원 가이드(날짜 미확인) |
| MOSFET | Vishay | 수집 | 3 | AI 응용 중심 / 항공·군용·우주 등급 중심 |
| MOSFET | Diodes_Inc | 수집 | 2 |  |
| Resistor | Yageo | 제외 | 0 | 공식 선택 가이드의 최신판이 2020년. 자료실이 JS 앱이라 목록을 읽지 못했고 내부 API 호출은 권한 분류기가 막아 중단. 유통사(TTI) 사본 403. Rutronik 호스팅 2024-07 브로셔는 공식본인지 확인하지 못해 받지 않음 |
| Resistor | Samsung_EM | 제외 | 0 | 삼성전기 사이트의 칩 저항 카탈로그가 2022-03판이라 기준 미달 |
| Resistor | Panasonic | 수집 | 3 | 차량용(AEC-Q200) 부품만. 날짜는 PDF 메타데이터(2025-08) / 파일명은 2025, PDF 생성일은 2026-10-28이라 제조사가 갱신한 판으로 보인다 |
| Resistor | ROHM | 수집 | 1 | 2024판이 최신(2025판 URL은 404). PDF 생성일 2023-12 |
| Resistor | Walsin | 수집 | 2 | 날짜는 PDF 메타데이터(2025-01) / 날짜는 PDF 메타데이터(2026-08) |
| Resistor | TA-I | 제외 | 0 | 공식 사이트에 계열별 사양서·품질 보고서만 있고 카탈로그·라인카드가 없음 |
| Resistor | Vishay | 수집 | 3 | 군용·항공우주 등급 중심. 인덕터는 마지막 1쪽뿐. 이 도메인에서 구한 최신 영문 Vishay 문서 |
| Capacitor | Murata | 제외 | 0 | MLCC 카탈로그 PDF를 더는 공개하지 않음. 카탈로그 라이브러리에는 ECAS 단일 계열만 있고 이전 라인업은 2017~2021년 |
| Capacitor | Samsung_EM | 수집 | 2 |  |
| Capacitor | TDK | 일부 | 1 | MLCC·알루미늄·필름 카탈로그는 product.tdk.com이 403(자동 요청 차단). TDK Electronics PFC 프로필만 저장 / MLCC가 아니라 산업용 PFC·전력 커패시터 프로필. TDK의 MLCC·알루미늄·필름·인덕터 카탈로그는 product.tdk.com 403으로 받지 못했다 |
| Capacitor | Taiyo_Yuden | 수집 | 2 | 1쪽 라인업 표. 인쇄된 날짜가 없고 파일명 코드(2512)와 PDF 생성일(2025-11)로 판단. 글꼴 인코딩이 깨져 텍스트 검색이 안 된다 / 1쪽 차량용 라인업 표(MLCC·인덕터·비드). 인쇄된 날짜가 없고 파일명 코드(2512)와 PDF 생성일(2025-11)로 판단. 글꼴 인코딩이 깨져 텍스트 검색이 안 된다 |
| Capacitor | Yageo_KEMET | 제외 | 0 | kemet.com이 yageogroup.com 자료실(JS 앱)으로 넘어가 읽지 못함. KEMET 선택 가이드는 2015판(Avnet), TTI 사본은 403 |
| Capacitor | Panasonic | 수집 | 3 | 파일명은 2025, PDF 생성일은 2026-10-28이라 제조사가 갱신한 판으로 보인다 |
| Capacitor | Walsin | 수집 | 2 | 날짜는 PDF 메타데이터(2026-08) |
| Capacitor | Vishay | 수집 | 3 | 군용·항공우주 등급 중심. 인덕터는 마지막 1쪽뿐. 이 도메인에서 구한 최신 영문 Vishay 문서 |
| Inductor | Murata | 수집 | 1 | 날짜 근거는 Murata 카탈로그 라이브러리 목록(2026-02 갱신)과 PDF 생성일 2026-01. 본문에 2013년 문구가 남아 있다. 파워 인덕터·트랜스포머·커먼모드 초크 중심 |
| Inductor | Coilcraft | 수집 | 2 | 차량용(AEC-Q200) 인증 부품 목록 2쪽 |
| Inductor | Wurth_Elektronik | 제외 | 0 | we-online.com PDF는 403, HTML은 봇 확인 화면. 우회하지 않음 |
| Inductor | Vishay | 수집 | 1 | 군용·항공우주 등급 중심. 인덕터는 마지막 1쪽뿐. 이 도메인에서 구한 최신 영문 Vishay 문서 |
| Inductor | TDK | 제외 | 0 | product.tdk.com 403. 접근 가능한 TDK Electronics 인덕터 문서는 2015~2019년 |
| Inductor | Taiyo_Yuden | 수집 | 3 | 1쪽 라인업 표. 인쇄된 날짜가 없고 파일명 코드(2512)와 PDF 생성일(2025-11)로 판단. 글꼴 인코딩이 깨져 텍스트 검색이 안 된다 / 1쪽 차량용 라인업 표(MLCC·인덕터·비드). 인쇄된 날짜가 없고 파일명 코드(2512)와 PDF 생성일(2025-11)로 판단. 글꼴 인코딩이 깨져 텍스트 검색이 안 된다 |
| Power_IC | TI | 제외 | 0 | 최근 3년 내 가이드 없음. 최신은 Power Management Guide 2018, 포트폴리오 개요는 2013 |
| Power_IC | ADI | 제외 | 0 | analog.com이 이 PC에서 접속되지 않음(TLS 재협상 후 연결 끊김, 타임아웃). 문서를 받거나 확인하지 못함 |
| Power_IC | Power_Integrations | 제외 | 0 | 여러 계열을 아우르는 최근 AC-DC 셀렉터 가이드가 없음(최신은 2016-04, Mouser). power.com에는 계열별 플라이어만 있어 단일 계열 문서라 받지 않음 |
| Power_IC | MPS | 수집 | 1 |  |
| Power_IC | onsemi | 제외 | 0 | 공식 전원 관리 선택 가이드를 찾지 못함. SMPS 시스템 솔루션 가이드는 날짜 없는 응용 미리보기. 유통사 사본 403 |
| Power_IC | Diodes_Inc | 수집 | 1 |  |
| Diode | Vishay | 수집 | 3 | 응용(차량·산업) 기준 구성. 날짜는 PDF 메타데이터(2025-01) / 항공우주·방산 등급 중심 |
| Diode | onsemi | 제외 | 0 | 공식 다이오드·정류·TVS 가이드 중 2023-11 이후 문서가 없음(데이터시트·응용 노트만) |
| Diode | Nexperia | 수집 | 1 | 유통사(Paltek) 호스팅 사본. 공식 사이트가 403이라 공식본과 대조하지 못했다. 본문은 Nexperia Selection Guide 2025이고 PDF 생성일은 2025-02 |
| Diode | Diodes_Inc | 수집 | 1 |  |
| Diode | ROHM | 수집 | 1 | 2024판이 최신(2025판 URL은 404). PDF 생성일 2023-12 |
| Driver_IC | TI | 제외 | 0 | 제품군 가이드가 최근 3년 내 없음(BLDC 선택 가이드 2022-05, 게이트 드라이버 응용 노트 2023-10) |
| Driver_IC | ADI | 제외 | 0 | 위와 같은 접속 실패. RS-485 선택 가이드(2024-03)를 찾았으나 받지 못함 |
| Driver_IC | STMicroelectronics | 제외 | 0 | st.com 응답 없음. 후보: 모터 제어 레퍼런스 가이드, 전력 관리 브로셔(검증 불가) |
| Driver_IC | Infineon | 일부 | 1 | 가전 응용 가이드만 저장. EiceDRIVER 가이드는 2019·2022판, BLDC 모터 드라이버 가이드와 Power and Sensing Selection Guide 2026은 로그인 필요 / 가전 응용 기준 가이드. 도메인별 포트폴리오 가이드가 아니다. 이 도메인에서 구한 최신 공개 문서 |
| Sensor | Bosch_Sensortec | 수집 | 1 |  |
| Sensor | STMicroelectronics | 제외 | 0 | st.com 응답 없음. 후보: MEMS·센서 빠른 참조 가이드(2025-03로 표기). 받지 못함. Mouser 사본은 2020-01판 |
| Sensor | ADI | 제외 | 0 | 접속 실패. MEMS 관성 센서 선택표를 찾았으나 받지 못함(날짜 미확인) |
| Sensor | TI | 일부 | 2 | 습도·초소형 온도 센서 비교 가이드만 저장. 전류·자기·mmWave 통합 가이드를 찾지 못함(전류 센스 앰프 가이드 2021) |
| Sensor | Honeywell | 수집 | 1 | 압력·공기흐름·힘 센서 중심. 자기·위치 센서 가이드는 2023-11 이전이라 제외 |
| Sensor | Murata | 제외 | 0 | 공식 카탈로그 라이브러리에 센서 카탈로그 PDF가 없음. 제품 라인 카드는 2016년 |
| Wireless_IC | Espressif | 수집 | 1 | 날짜 근거는 PDF 메타데이터뿐(2026-08). 본문에 날짜 없음. 사이트 선택기가 쓰는 공개 API 경로에서 로그인 없이 받음 |
| Wireless_IC | Nordic | 수집 | 1 | 본문 "Issue 4 2023", PDF 생성일 2024-02. 발행 월이 적혀 있지 않아 2023-11-27 기준에 가까운 문서다 |
| Wireless_IC | Qualcomm | 수집 | 1 | IoT 연결성 칩(QCC711·730·743·744·748) 비교 1쪽. 포트폴리오 브로셔가 아니다 |
| Wireless_IC | MediaTek | 제외 | 0 | Wi-Fi·Bluetooth 연결성 칩(Filogic 등)의 공개 브로셔·셀렉션 가이드가 없음(백서, 단일 제품 브리프, 연결성 칩이 아닌 Genio IoT 브로셔만 있음) |
| Wireless_IC | Realtek | 제외 | 0 | 제품 페이지와 Ameba 사이트에 브로셔·셀렉션 가이드 PDF가 없음 |
| Connector | TE_Connectivity | 제외 | 0 | te.com 카탈로그 PDF 5건이 모두 403(Referer 재시도 포함). TTI 사본도 403. Mouser·RS·Farnell 사본은 2014년 등 기준 미달이거나 단일 계열 문서 |
| Connector | Molex | 제외 | 0 | molex.com이 이 PC에서 응답하지 않음(TLS 이후 타임아웃·SSL 오류). 기준을 충족하는 유통사 사본을 찾지 못함. 후보: Core Signal 가이드, RAST 가이드(2025-08), 2023 Heavy-Duty 카탈로그 |
| Connector | Hirose | 수집 | 3 | 응용별 추천 가이드(1~2쪽). 전체 카탈로그(Connector Selector)는 온라인 뷰어만 있어 받지 못했다 |
| Connector | Yeonho | 제외 | 0 | 공식 사이트에 카탈로그·셀렉션 가이드가 없고 부품별 사양 PDF와 피치별 목록만 있음. 제3자 사이트도 단일 계열 사양서뿐 |

## 알아 둘 점

- **막힌 사이트**: 이 PC에서 `www.st.com`·`www.analog.com`·`www.molex.com`이 응답하지 않아 STMicroelectronics 4개, ADI 3개, Molex 1개가 제외됐다. 사이트가 막힌 것이지 문서가 없는 것은 아니다. 다른 네트워크에서 다시 시도하면 받을 수 있다.
- **403 차단**: `te.com`, `product.tdk.com`, `we-online.com`, `assets.nexperia.com` 등은 자동 요청에 403을 돌려줘서, 로그인·양식·캡차 우회 없이 받을 수 있는 것만 받았다.
- **검색 한도**: 수집 중 WebSearch 한도(턴당 200회)가 모두 소진되어 TI(MCU·Driver·Sensor), Molex·TE의 대체 경로, Yageo·KEMET 최신 문서 탐색이 덜 끝났다.
- **약한 매치**: 계열 하나·응용별·1~2쪽 문서는 `manifest.csv`의 `caveat`에 적었다. 시연용으로는 쓸 수 있지만 AVL별 제품군 전체를 대표하지 않는다.
- **출처 미검증**: Nexperia 사본은 유통사(Paltek) 호스팅본이다. NXP 3개는 WebFetch 도구로 받았고, Infineon 포켓 가이드는 Infineon 커뮤니티 첨부 파일이다.
- 문서 내용·단가·재고·납기는 시연의 [가상] 값이 아니라 제조사 공개 자료다. 다봄은 이 자료를 사양 범위(제품군) 근거로만 쓰고 단가·재고·납기의 근거로 쓰지 않는다(DEC-15).

## 변경 이력

| 버전 | 일자 | 내용 |
|---|---|---|
| v0.1 | 2026-11-27 | 최초 수집. 7개 에이전트로 병렬 수집 후 별도 검증 |
