// 삼성전기 제품 검색의 "List Download" 버튼을 한 번 눌러 목록 파일을 받는다.
// 사용: node samsung_list_download.js <선택기 URL, 예 https://product.samsungsem.com/mlcc/basic-search.do> <저장 폴더>
// MLCC는 품번 9,416개 xlsx가 내려온다(2026-11-27). Chip Resistor(102,717품목)는 서버가 listDownload.do에서 404를 돌려주어 받지 못했다(필터를 걸어도 같았다).
// 버튼 안내문이 "반복 실행하면 더 느려진다"고 하므로 한 번만 누른다.
const puppeteer = require('puppeteer-core'); const fs = require('fs'); const path = require('path');
const url = process.argv[2], outDir = path.resolve(process.argv[3]);
(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--no-sandbox'] });
  const bc = await b.target().createCDPSession();
  await bc.send('Browser.setDownloadBehavior', { behavior: 'allowAndName', downloadPath: outDir, eventsEnabled: true });
  let done = null;
  bc.on('Browser.downloadWillBegin', e => console.log('DL begin', e.suggestedFilename, e.url.slice(0, 120)));
  bc.on('Browser.downloadProgress', e => { if (e.state !== 'inProgress') { console.log('DL', e.state, e.totalBytes); done = e.state; } });
  const p = await b.newPage();
  await p.setUserAgent('DabomAVLResearch/1.0 (internal product-data research; respects robots.txt)');
  p.on('response', r => { if (/listDownload/.test(r.url())) console.log('listDownload', r.status(), r.headers()['content-disposition'] || ''); });
  await p.goto(url, { waitUntil: 'networkidle2', timeout: 120000 });
  await new Promise(r => setTimeout(r, 2000));
  await p.evaluate(() => { const e = [...document.querySelectorAll('a')].find(e => /list\s*download/i.test(e.textContent)); if (e) e.click(); });
  for (let i = 0; i < 300 && !done; i++) await new Promise(r => setTimeout(r, 1000));
  console.log('files', fs.readdirSync(outDir));   // 파일 이름은 GUID로 저장된다. xlsx로 이름을 바꿔 쓴다
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
