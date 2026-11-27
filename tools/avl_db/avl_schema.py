# -*- coding: utf-8 -*-
"""AVL·공급 제품 DB 공통 정의. 엑셀 생성기와 목업 데이터 생성기가 함께 쓴다."""

# 도메인 순서와 이름. (코드, 한국어 이름, R09 절 제목 키워드)
DOMAINS = [
    ('MCU', 'MCU', '2. MCU'),
    ('MOSFET', 'MOSFET', '3. MOSFET'),
    ('Resistor', '저항', '4. Resistor'),
    ('Capacitor', '커패시터', '5. Capacitor'),
    ('Inductor', '인덕터', '6. Inductor'),
    ('Power_IC', 'AC/DC·DC/DC 전원 IC', '7. AC/DC'),
    ('Diode', '다이오드', '8. Diode'),
    ('Driver_IC', '드라이버 IC', '9. 각종 Driver'),
    ('Sensor', '센서', '12. Sensor'),
    ('Wireless_IC', '무선·연결 IC', '13. Wireless'),
    ('Connector', '커넥터', '15. Connector'),
]
DOMAIN_KO = {d[0]: d[1] for d in DOMAINS}

# 제조사 폴더 이름 → (표시 이름, R09 표의 Vendor Name)
VENDORS = {
    'STMicroelectronics': ('STMicroelectronics', 'STMicroelectronics'),
    'Microchip': ('Microchip Technology', 'Microchip Technology'),
    'TI': ('Texas Instruments (TI)', 'Texas Instruments (TI)'),
    'NXP': ('NXP Semiconductors', 'NXP Semiconductors'),
    'Infineon': ('Infineon Technologies', 'Infineon Technologies'),
    'onsemi': ('onsemi (ON Semiconductor)', 'ON Semiconductor (onsemi)'),
    'Vishay': ('Vishay Intertechnology', 'Vishay Intertechnology'),
    'Diodes_Inc': ('Diodes Incorporated', 'Diodes Incorporated'),
    'Yageo': ('Yageo', 'Yageo'),
    'Yageo_KEMET': ('Yageo / KEMET', 'Yageo / KEMET'),
    'Samsung_EM': ('Samsung Electro-Mechanics', 'Samsung Electro-Mechanics'),
    'Panasonic': ('Panasonic', 'Panasonic'),
    'ROHM': ('ROHM Semiconductor', 'ROHM Semiconductor'),
    'Walsin': ('Walsin Technology', 'Walsin Technology'),
    'TA-I': ('TA-I Technology', 'TA-I Technology'),
    'Murata': ('Murata Manufacturing', 'Murata Manufacturing'),
    'TDK': ('TDK Corporation', 'TDK Corporation'),
    'Taiyo_Yuden': ('Taiyo Yuden', 'Taiyo Yuden'),
    'Coilcraft': ('Coilcraft', 'Coilcraft'),
    'Wurth_Elektronik': ('Würth Elektronik', 'Würth Elektronik'),
    'ADI': ('Analog Devices (ADI)', 'Analog Devices (ADI)'),
    'Power_Integrations': ('Power Integrations', 'Power Integrations'),
    'MPS': ('Monolithic Power Systems (MPS)', 'Monolithic Power (MPS)'),
    'Nexperia': ('Nexperia', 'Nexperia'),
    'Bosch_Sensortec': ('Bosch Sensortec', 'Bosch Sensortec'),
    'Honeywell': ('Honeywell', 'Honeywell'),
    'Espressif': ('Espressif Systems', 'Espressif Systems'),
    'Nordic': ('Nordic Semiconductor', 'Nordic Semiconductor'),
    'Qualcomm': ('Qualcomm', 'Qualcomm'),
    'MediaTek': ('MediaTek', 'MediaTek'),
    'Realtek': ('Realtek Semiconductor', 'Realtek Semiconductor'),
    'TE_Connectivity': ('TE Connectivity', 'TE Connectivity'),
    'Molex': ('Molex', 'Molex'),
    'Hirose': ('Hirose Electric (HRS)', 'Hirose Electric (HRS)'),
    'Yeonho': ('Yeonho Electronics', 'Yeonho Electronics'),
}

COMMON = {
    'aec': ('차량용 인증', 12),
    'features': ('특징', 34),
    'temp': ('동작 온도', 14),
}

# 도메인별 사양 열: (키, 머리글, 너비)
SPECS = {
    'Resistor': [('size_inch', '크기(인치)', 10), ('size_metric', '크기(메트릭)', 11), ('resistance', '저항 범위', 18), ('tolerance', '허용오차', 14),
                 ('tcr', 'TCR(ppm/°C)', 14), ('power', '정격전력(W)', 12), ('voltage', '최대 전압(V)', 12), ('temp', '동작 온도', 14), ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'Capacitor': [('size_inch', '크기(인치)', 10), ('size_metric', '크기(메트릭)', 11), ('capacitance', '정전용량 범위', 18), ('voltage', '정격전압(V)', 14),
                  ('dielectric', '유전체·온도특성', 16), ('tolerance', '허용오차', 12), ('temp', '동작 온도', 14), ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'Inductor': [('size', '크기', 16), ('inductance', '인덕턴스 범위', 18), ('i_rated', '정격전류', 14), ('i_sat', '포화전류', 14), ('dcr', 'DCR(mΩ)', 12),
                 ('shield', '차폐', 10), ('temp', '동작 온도', 14), ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'MCU': [('core', '코어', 18), ('bits', '비트', 7), ('freq_max', '최대 클럭', 12), ('flash', '플래시', 14), ('ram', 'RAM', 12), ('peripherals', '주변장치·통신', 28),
            ('supply', '동작 전압', 12), ('packages', '패키지', 20), ('target', '대상 응용', 22), ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'MOSFET': [('polarity', '극성', 8), ('vds', 'Vds(V)', 12), ('rds_on', 'Rds(on)(mΩ)', 14), ('id', 'Id(A)', 10), ('package', '패키지', 16),
               ('technology', '기술', 16), ('qg', 'Qg(nC)', 10), ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'Diode': [('v_rrm', 'Vr(V)', 12), ('i_f', 'If(A)', 10), ('v_f', 'Vf(V)', 10), ('channels', '소자 구성', 14), ('package', '패키지', 16),
              ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'Power_IC': [('topology', '토폴로지', 14), ('vin', '입력 전압', 14), ('vout', '출력 전압', 14), ('iout', '출력 전류', 12), ('freq', '스위칭 주파수', 14),
                 ('package', '패키지', 16), ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'Driver_IC': [('channels', '채널', 10), ('voltage', '전압', 14), ('current', '전류', 14), ('isolation', '절연', 10), ('package', '패키지', 16),
                  ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'Sensor': [('range', '측정 범위', 20), ('accuracy', '정확도', 14), ('interface', '인터페이스', 14), ('supply', '공급 전압', 12), ('package', '패키지', 16),
               ('aec', '차량용 인증', 12), ('features', '특징', 34)],
    'Wireless_IC': [('standard', '무선 규격', 22), ('core', '코어', 18), ('freq', '주파수', 12), ('memory', '메모리', 18), ('interfaces', '인터페이스', 22),
                    ('package', '패키지', 16), ('features', '특징', 34)],
    'Connector': [('pitch', '피치(mm)', 10), ('positions', '극수', 12), ('current', '정격전류', 12), ('voltage', '정격전압', 12), ('mounting', '실장', 10),
                  ('application', '대상 응용', 24), ('features', '특징', 34)],
}

HEAD_COLS = [('vendor', '제조사', 16), ('level', '구분', 8), ('series', '계열(Series)', 26), ('part_number', '부품번호', 22), ('type', '제품 유형', 18)]
TAIL_COLS = [('note', '비고', 24), ('doc_title', '출처 문서', 36), ('page', '쪽', 7), ('doc_date', '문서 기준일', 11), ('verify', '원문 대조', 12)]


# 공통 키 temp(동작 온도)는 모든 도메인에서 쓴다. 도메인에 없으면 aec 앞에 넣는다.
for _d, _cols in SPECS.items():
    if not any(k == 'temp' for k, _, _ in _cols):
        _i = next((n for n, (k, _, _) in enumerate(_cols) if k in ('aec', 'features')), len(_cols))
        _cols.insert(_i, ('temp', '동작 온도', 14))
