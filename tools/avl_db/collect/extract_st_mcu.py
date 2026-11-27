# -*- coding: utf-8 -*-
"""STMicroelectronics 공식 GitHub 오픈 데이터(STM32_open_pin_data, BSD-3-Clause)의 mcu/*.xml → AVL 행.
실행: python extract_st_mcu.py <STM32_open_pin_data 폴더> <출력 json>
한 파일 = 한 RefName(ST 데이터베이스의 부품 이름). RefName의 괄호 (E-G)는 메모리 용량 코드 범위, 끝의 x는 온도·포장 접미를 뜻한다.
번호를 풀어 새로 만들지 않고 RefName 그대로 쓴다."""
import collections
import glob
import io
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

SRC, OUT = sys.argv[1], sys.argv[2]
NS = '{http://dummy.com}'
KEY = ['USART', 'UART', 'LPUART', 'SPI', 'I2C', 'I3C', 'I2S', 'SAI', 'ADC', 'DAC', 'COMP', 'OPAMP', 'CAN', 'FDCAN', 'ETH', 'USB', 'USB_OTG_FS', 'USB_OTG_HS',
       'SDMMC', 'SDIO', 'QUADSPI', 'OCTOSPI', 'FMC', 'FSMC', 'DCMI', 'LTDC', 'DMA2D', 'DSI', 'UCPD', 'TSC', 'LCD', 'CRYP', 'AES', 'HASH', 'PKA', 'RNG', 'MDF', 'DFSDM']


def num(v):
    f = float(v)
    return str(int(f)) if f == int(f) else str(f)


def rng(vals, unit):
    v = sorted({float(x) for x in vals})
    if not v:
        return None
    return (num(v[0]) + unit) if len(v) == 1 else (num(v[0]) + '~' + num(v[-1]) + unit)


rows = []
for p in sorted(glob.glob(os.path.join(SRC, 'mcu', '*.xml'))):
    r = ET.parse(p).getroot()
    ref, fam, line, pkg = r.get('RefName'), r.get('Family'), r.get('Line'), r.get('Package')
    t = lambda tag: [e for e in r.findall(NS + tag)]
    core = (t('Core')[0].text if t('Core') else '') or ''
    core = core.strip().replace('ARM ', 'Arm ')
    bits = '64' if 'A35' in core or 'A55' in core else '32'
    freq = [e.text for e in t('Frequency') if e.text]
    flash = [e.text for e in t('Flash') if e.text]
    ram = [e.text for e in t('Ram') if e.text]
    ccm = [e.text for e in t('CCMRam') if e.text]
    io_nb = t('IONb')[0].text if t('IONb') else None
    volt = t('Voltage')[0] if t('Voltage') else None
    temp = t('Temperature')[0] if t('Temperature') else None
    ips = collections.defaultdict(set)
    for e in t('IP'):
        n = e.get('Name')
        if n in KEY:
            ips[n].add(e.get('InstanceName') or n)
    per = ', '.join((n + ('×' + str(len(ips[n])) if len(ips[n]) > 1 else '')) for n in KEY if n in ips)
    tim = {e.get('InstanceName') for e in t('IP') if (e.get('Name') or '').startswith('TIM') and e.get('InstanceName')}
    if tim:
        per = (per + ', ' if per else '') + 'TIM×' + str(len(tim))
    trust = ' · TrustZone' if t('TrustZone') else ''
    sp = {
        'core': core or None,
        'bits': bits,
        'freq_max': (num(max(float(x) for x in freq)) + 'MHz') if freq else None,
        'flash': rng(flash, 'KB'),
        'ram': (rng(ram, 'KB') or '') + ((' + CCM ' + rng(ccm, 'KB')) if ccm else '') or None,
        'peripherals': per or None,
        'supply': (num(volt.get('Min')) + '~' + num(volt.get('Max')) + 'V') if volt is not None and volt.get('Min') and volt.get('Max') else None,
        'packages': pkg,
        'target': line,
        'temp': (num(temp.get('Min')) + '~' + num(temp.get('Max')) + '°C') if temp is not None and temp.get('Min') and temp.get('Max') else None,
        'features': ('I/O ' + io_nb if io_nb else '') + trust or None,
    }
    sp = {k: v for k, v in sp.items() if v}
    rows.append({'domain': 'MCU', 'agent': 'private:st-open-pin-data', 'vendor': 'STMicroelectronics', 'doc': 'MCU/STMicroelectronics/STM32_open_pin_data',
                 'page': None, 'level': '부품번호', 'series': line or fam, 'part_number': ref, 'type': fam, 'specs': sp,
                 'note': 'RefName: (E-G)=용량 코드 범위, x=온도·포장 접미', 'verify': '오픈 데이터'})
doc = {'domain': 'MCU', 'vendor': 'STMicroelectronics', 'file': 'MCU/STMicroelectronics/STM32_open_pin_data',
       'title': 'STM32_open_pin_data (STMicroelectronics 공식 GitHub, BSD-3-Clause)', 'doc_type': 'Open data (GitHub)', 'doc_date': '2026-11',
       'pages': 0, 'source_url': 'https://github.com/STMicroelectronics/STM32_open_pin_data', 'policy': '오픈 데이터(BSD-3-Clause)', 'agent_note': 'STM32CubeMX 내부 DB의 일부. 최신 시리즈가 모두 있지는 않을 수 있다'}
io.open(OUT, 'w', encoding='utf-8').write(json.dumps({'docs': [doc], 'rows': rows}, ensure_ascii=False))
print('rows', len(rows), 'families', len({r['type'] for r in rows}))
print(json.dumps(rows[0], ensure_ascii=False)[:600])
