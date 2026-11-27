# 제조사 공식 내보내기·데이터 피드 수집 (2026-11-27)

[docs/15](../../../docs/15_AVL_수집경로_조사.md)에서 고른 "공식 경로"를 브라우저(Chrome)로 실행하는 스크립트와, 받은 파일을 AVL 행으로 바꾸는 변환기다. **받은 원천 데이터와 변환 결과는 `AVL_DB/_private/`에 두고 git에 올리지 않는다**(`.gitignore`). 이 폴더에는 코드만 있다.

## 준비

```bash
cd tools/avl_db/collect && npm install   # puppeteer-core. 시스템 Chrome을 쓴다(경로는 스크립트 안)
```

## 받기

| 출처 | 스크립트 | 받는 것 | 지킨 것 |
|---|---|---|---|
| onsemi 제품 선택기 | `onsemi_export_batch.js <저장 폴더>` | 소분류 페이지마다 `Export > CSV Format`을 눌러 받은 CSV(페이지 20개 중 18개 성공. GaN FET·LED 드라이버 페이지는 Export 버튼이 없다. 제너 다이오드는 대기 420초 필요) | `robots.txt` `Crawl-delay: 10`(페이지 사이 12초), 프로세스 하나만 실행 |
| 삼성전기 제품 검색 | `samsung_list_download.js <URL> <저장 폴더>` | MLCC 품번 9,416개 xlsx. Chip Resistor는 서버가 404 | 버튼 한 번 |
| TE Connectivity | `te_datafeed_download.js <저장 폴더>` | `Connectors.zip`(Excel 데이터 피드 64MB, 소분류 119개) | 파일 하나 |
| STMicroelectronics | `git clone https://github.com/STMicroelectronics/STM32_open_pin_data` | STM32 부품별 XML 2,282개(BSD-3-Clause) | 공식 오픈 데이터 |

접속 주체는 `DabomAVLResearch/1.0`으로 밝힌다. 접속 제한·봇 확인·로그인이 나오면 우회하지 않는다.

## 바꾸기·합치기

```bash
python extract_st_mcu.py <STM32_open_pin_data> <extras>/st_mcu.json
python extract_onsemi.py <onsemi csv 폴더> <extras>/onsemi.json          # 참고 단가 열은 읽지 않는다
python extract_samsung_mlcc.py <mlcc_list.xlsx> <extras>/samsung_mlcc.json   # 품번 코드를 카탈로그 6~8쪽 표로 해독
python extract_te.py <Connectors_excel.zip> <extras>/te_connectors.json     # inch→mm, °F→°C 환산
python merge_extras.py <final_rows.json.gz> <final_docs.json> <새 PDF 폴더|-> <extras> <출력 폴더>
```

```bash
python derive_walsin_pn.py <final_rows.json.gz> <출력 final_rows.json.gz> --docs <final_docs.json.gz> <출력 final_docs.json> --report 보고서.txt
```

```bash
python derive_rohm_panasonic_pn.py <final_rows.json.gz> <출력 final_rows.json.gz> --docs <final_docs.json.gz> <출력 final_docs.json> --report 보고서.txt
```

`derive_rohm_panasonic_pn.py`는 같은 방식으로 ROHM 제너(PDF 34쪽 Product No. Explanation, 22·23쪽 머리글의 등급·테이핑 코드)와 Panasonic OS-CON SMD(PDF 37쪽)의 형명을 조립한다. Walsin 처리 결과를 입력으로 받는다. 범위로만 인쇄된 행·형명 규칙이 없는 문서의 행은 건드리지 않고 사유를 비고 앞에 적는다.

`derive_walsin_pn.py`는 Walsin 카탈로그에서 형명 없이 풀었던 사양 조합 칸에 문서의 주문 코드(How To Order) 규칙으로 부품번호를 조립해 채운다(DEC-21, 원문 대조 `주문 코드 조합`). 허용오차가 여럿인 칸은 허용오차마다 한 행, 문서의 코드표에 없는 값(예: 1825 크기 코드)은 만들지 않고 비고에 사유를 적는다. 규칙·근거·검증은 [docs/15](../../../docs/15_AVL_수집경로_조사.md) 11장이다.

`merge_extras.py`의 출력 폴더에 `avl_schema.py`를 복사해 두고 `build_data_avl.py`·`build_xlsx.py`를 그 폴더로 실행한다(두 스크립트는 같은 폴더의 `extras_docs.json`을 읽어 PDF가 아닌 출처의 제목·기준일을 쓴다).
