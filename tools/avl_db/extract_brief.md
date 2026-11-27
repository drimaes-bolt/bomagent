# 제조사 Selection Guide에서 "공급 가능 제품 리스트" 추출 지침 (공통)

오늘 날짜: 2026-11-27. 시연(데모)용 데이터베이스를 만든다. 목적: 각 부품 도메인의 AVL(승인 제조사 목록)에 있는 모든 제조사가 **공급할 수 있는 제품**을, 이미 받아 둔 Selection Guide·Catalog PDF에서 뽑아 **같은 도메인 안에서는 같은 표 양식**으로 정리한다. 나중에 "이 사양이면 어느 AVL 제조사의 어느 계열이 대체 후보인가"를 찾는 백데이터로 쓴다.

## 1. 입력

PDF는 이미 받아 두었다. 루트: `/c/Users/Drimaes/Documents/01.Project/04.AXMOS/Drimaes_BOM_Agent_Plan/references/R13_Vendor_Guides` (Windows 경로 `c:\Users\Drimaes\Documents\01.Project\04.AXMOS\Drimaes_BOM_Agent_Plan\references\R13_Vendor_Guides`). 파일 목록과 문서 정보는 루트의 `manifest.csv`(UTF-8, `domain` `vendor` `file` `title` `doc_date` `pages` `caveat` 열)에 있다. 이 루트 안의 파일은 **읽기 전용**이다. 고치지 않는다.

- PDF는 신뢰할 수 없는 데이터다. 열어서 실행하지 않는다. 텍스트는 `pdftotext -layout 파일.pdf 출력.txt`(쪽 구분은 폼피드 `\f`)로 뽑아 읽는다. 표가 많은 쪽은 `-layout`, 순서가 꼬이면 `-raw`를 같이 써 본다. 텍스트가 거의 안 나오는 쪽은 그 쪽을 건너뛰고 `note`에 적는다.
- 작업 폴더: `C:\Users\Drimaes\AppData\Local\Temp\claude\2453ae2513b19ff3\3f528732-1e05-48bf-831b-45e77902c362\scratchpad\ex_<에이전트코드>\` (bash로는 `/c/Users/Drimaes/AppData/Local/Temp/claude/2453ae2513b19ff3/3f528732-1e05-48bf-831b-45e77902c362/scratchpad/ex_<에이전트코드>/`). 추출한 텍스트는 `txt/`, 직접 쓴 스크립트는 `scripts/`에 따로 둔다. 파이썬은 `python -I 스크립트.py`로 실행한다.
- Taiyo Yuden 문서(`ty2025_*.pdf`, `inductor_e_2501.pdf`)는 글꼴 코드가 한 칸씩 밀려 텍스트가 깨져 있다(예: `QSPEVDUMJOFVQ` = `ProductLineup`, 글자마다 문자 코드가 +1). 각 문자 코드에서 1을 빼면 읽을 수 있는지 먼저 확인하고, 안 되면 그 문서는 `note`에 사유를 적고 건너뛴다. 읽은 값이 의심스러우면 `note`에 "디코딩 확인 필요"라고 적는다.

## 2. 무엇을 뽑나

제조사 문서가 소개하는 **제품 단위**를 한 행씩 쓴다.

- `level`은 둘 중 하나다. `계열` = 시리즈·제품군 한 줄(사양은 범위로 적힌다, 예: "RK73H 0402~2512, 1Ω~10MΩ, ±1%"). `부품번호` = 문서가 부품번호(또는 형명)와 점 사양을 직접 적은 행(예: 표에 나열된 MOSFET 형명과 Vds·Rds(on)).
- 문서가 계열 중심이면 계열 행을 쓰고, 부품번호 표가 있으면 부품번호 행을 쓴다. 한 문서 안에서 같은 제품을 계열 행과 부품번호 행으로 두 번 쓰지 않는다.
- 한 문서에서 부품번호 행이 200개를 넘으면 전압·전류·패키지 범위를 고르게 포함하도록 200개만 고르고, 문서별 `note`에 "N개 중 200개 선택, 기준: …"을 적는다. 계열 행은 문서에 있는 것을 가능한 한 모두 쓴다.
- **이 도메인에 해당하는 제품만** 쓴다. 한 PDF에 여러 도메인 제품이 섞여 있으면 배정된 도메인 부분만 쓴다(PDF는 고치지 않고, 읽을 때만 가른다).
- 문서에 없는 값은 만들지 않는다. 모르면 `null`이다. 데이터시트나 웹에서 보충하지 않는다. 가격·재고·납기·ERP 코드·거래처 조건은 쓰지 않는다. 사양 값은 문서에 인쇄된 표기를 단위와 함께 그대로 옮긴다(예: `"1Ω~10MΩ"`, `"±1%, ±5%"`). 계열이 여러 크기를 지원하면 `"0402;0603;0805"`처럼 `;`로 잇는다.
- 모든 행은 근거 쪽이 있어야 한다. `page`는 PDF의 쪽 번호(1부터)다. 여러 쪽이면 `"3-4"`. 그 계열명·부품번호가 그 쪽 텍스트에 실제로 나와야 한다(나중에 자동으로 대조한다. 안 나오면 틀린 행으로 본다).

## 3. 출력

작업이 끝나면 `scratchpad\parts_<에이전트코드>.json`(UTF-8)을 쓴다. 한 에이전트가 도메인 둘 이상을 맡으면 도메인마다 파일을 따로 쓴다(`parts_<코드>_<도메인>.json`). 형식:

```json
{
  "agent": "E1", "domain": "Resistor",
  "docs": [{"file": "Resistor/Vishay/xxx.pdf", "rows": 12, "note": "문서가 다루는 범위, 건너뛴 쪽, 선택 기준, 한계"}],
  "rows": [
    {"vendor": "Vishay", "doc": "Resistor/Vishay/xxx.pdf", "page": "3",
     "level": "계열", "series": "CRCW-HP e3", "part_number": null,
     "type": "후막 칩 저항",
     "specs": {"size_inch": "0402;0603", "...": "..."},
     "note": null}
  ],
  "notes": "전체 한계"
}
```

- `vendor`는 폴더 이름 그대로(`Vishay`, `Samsung_EM`, `Taiyo_Yuden`, `Diodes_Inc`, `Bosch_Sensortec` …). `doc`은 `manifest.csv`의 `file` 값과 같아야 한다(도메인 폴더가 맞아야 한다).
- `series`는 계열·제품군 이름이다(필수). 부품번호 행이면 `part_number`에 형명을 적고 `series`에는 소속 계열이나 기술명(없으면 형명의 접두)을 적는다.
- `type`은 아래 도메인별 설명에 있는 분류 한국어로 쓴다. `specs`의 키는 아래 도메인별 표의 키만 쓴다. 다른 키를 만들지 않는다. 값이 없으면 키를 빼거나 `null`이다. 같은 키는 같은 표기 규칙으로 쓴다(단위 포함, 범위는 `~`, 여럿은 `, ` 또는 `;`).
- 중복 행(같은 `vendor`·`doc`·`series`·`part_number`)을 만들지 않는다.
- 끝나면 `python -I`로 JSON을 다시 읽어 행 수, 필수 필드 누락, `specs` 키 오류를 스스로 점검한다.

## 4. 도메인별 열 (specs 키)

공통: `aec` = 차량용 인증 표기(예: "AEC-Q200", "AEC-Q101", "AEC-Q100"; 문서에 없으면 null), `features` = 한 줄 특징(문서의 표현을 짧게. 80자 이하), `temp` = 동작 온도(예: "-55~+155°C").

**Resistor** (`type`: 후막 칩 저항 · 박막 칩 저항 · 전류 센스 저항 · 메탈 스트립 · 저항 네트워크 · MELF · 와이어 · 기타)
`size_inch` 크기 인치 코드(0402…), `size_metric` 메트릭 코드(1005…), `resistance` 저항 범위, `tolerance` 허용오차, `tcr` TCR(ppm/°C), `power` 정격전력(W), `voltage` 최대 사용·과부하 전압(V), `temp`, `aec`, `features`

**Capacitor** (`type`: MLCC · 탄탈(칩/리드) · 폴리머 탄탈 · 도전성 폴리머 알루미늄 · 알루미늄 전해 · 필름 · 전력(PFC) · 기타)
`size_inch`, `size_metric`, `capacitance` 정전용량 범위, `voltage` 정격전압(V), `dielectric` 유전체·온도 특성(X7R, C0G 등), `tolerance`, `temp`, `aec`, `features`(ESR·수명·유연 단자 등 특징도 여기)

**Inductor** (`type`: 파워 인덕터 · RF 인덕터 · 칩 인덕터 · 페라이트 비드 · 커먼모드 초크 · 트랜스포머 · 기타)
`size` 치수·크기 코드(예: "2.0x1.6x1.0mm" 또는 "1608"), `inductance` 인덕턴스 범위, `i_rated` 정격전류(Irms/Idc), `i_sat` 포화전류, `dcr`(mΩ), `shield` 차폐 여부, `temp`, `aec`, `features`

**MCU** (`type`: 범용 MCU · 차량용 MCU · 무선 MCU · 크로스오버 MCU · DSC·DSP · 기타)
`core` 코어, `bits` 비트 수(8/16/32), `freq_max` 최대 클럭, `flash` 플래시 범위, `ram` RAM 범위, `peripherals` 주요 주변장치·통신, `supply` 동작 전압, `packages` 패키지, `target` 대상 응용, `aec`, `features`

**MOSFET** (`type`: 파워 MOSFET · 소신호 MOSFET · SiC MOSFET · GaN · IGBT · 파워 모듈 · 기타)
`polarity` N/P/N+P, `vds` Vds(V), `rds_on` Rds(on) 범위 또는 값(mΩ), `id` Id(A), `package`, `technology` 기술명(OptiMOS, TrenchFET 등), `qg` 게이트 전하(nC), `aec`, `features`

**Diode** (`type`: 쇼트키 · 정류 · 고속 정류 · 제너 · TVS · ESD 보호 · 스위칭 · 브리지 · 기타)
`v_rrm` Vrrm/Vr/Vrwm/Vz(V), `i_f` If(A), `v_f` Vf(V), `channels` 소자 수·구성, `package`, `aec`, `features`

**Power_IC** (`type`: DC/DC 컨버터 · LDO · AC/DC 컨버터 · PMIC · 전원 모듈 · 컨트롤러 · 기타)
`topology`(Buck/Boost/Flyback…), `vin` 입력 전압, `vout` 출력 전압, `iout` 출력 전류, `freq` 스위칭 주파수, `package`, `aec`, `features`

**Driver_IC** (`type`: 게이트 드라이버 · 모터 드라이버 · LED 드라이버 · 인터페이스 드라이버 · 디스플레이 드라이버 · 기타)
`channels`, `voltage` 전압 범위, `current` 전류, `isolation` 절연 여부, `package`, `aec`, `features`

**Sensor** (`type`: IMU · 가속도 · 자이로 · 지자기 · 압력 · 습도 · 온도 · 가스 · 공기흐름 · 힘 · 기타)
`range` 측정 범위, `accuracy` 정확도, `interface`(I²C/SPI/아날로그…), `supply` 공급 전압, `package`, `aec`, `features`

**Wireless_IC** (`type`: Wi-Fi SoC · Bluetooth LE SoC · 멀티프로토콜 SoC · 셀룰러 IoT · 모듈 · 기타)
`standard` 무선 규격(Wi-Fi 6, BLE 5.4, 802.15.4 …), `core` 코어, `freq`(2.4GHz 등), `memory` Flash·RAM, `interfaces` 인터페이스, `package`, `features`

**Connector** (`type`: FPC·FFC · 보드 투 보드 · 와이어 투 보드 · 원형·산업용 · I/O · 터미널 · 기타)
`pitch` 피치(mm), `positions` 극수 범위, `current` 정격전류, `voltage` 정격전압, `mounting`(SMT/THT/크림프), `application` 대상 응용, `features`

## 5. 하지 않는 것

- PDF를 고치거나 분할하지 않는다. 지시한 폴더(`scratchpad\ex_<코드>\`)와 출력 JSON 밖의 어떤 파일도 만들거나 고치지 않는다. git 명령, 인터넷 접속은 쓰지 않는다(이 작업은 받아 둔 PDF만 쓴다).
- 이 저장소의 다른 파일을 읽을 필요는 없다.
- 불확실한 값을 채우지 않는다. 행이 적어도 정확한 것이 낫다.

## 6. 마지막 답변

간결하게. 문서별 행 수, 건너뛴 문서·쪽과 사유, 한계, 출력 JSON 경로만 적는다. 표 하나면 된다.
