const puppeteer = require('puppeteer-core'); const fs = require('fs'); const path = require('path');
const outDir = path.resolve(process.argv[2]);
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--no-sandbox'] });
  const bc = await b.target().createCDPSession();
  await bc.send('Browser.setDownloadBehavior', { behavior: 'allowAndName', downloadPath: outDir, eventsEnabled: true });
  bc.on('Browser.downloadWillBegin', e => console.log('DL begin', e.suggestedFilename, e.url.slice(0, 120)));
  let done = null; bc.on('Browser.downloadProgress', e => { if (e.state !== 'inProgress') { console.log('DL', e.state, e.receivedBytes, e.totalBytes); done = e.state; } });
  const p = await b.newPage();
  await p.setUserAgent('DabomAVLResearch/1.0 (internal product-data research; respects robots.txt)');
  p.on('response', r => { if (/datafeed/.test(r.url())) console.log('resp', r.status(), r.url(), r.headers()['content-type'], r.headers()['content-length']); });
  await p.goto('https://www.te.com/en/catalog/exceldatafeed/Connectors.zip', { waitUntil: 'load', timeout: 60000 }).catch(e => console.log('goto:', e.message.slice(0, 100)));
  for (let i = 0; i < 900 && !done; i++) { await new Promise(r => setTimeout(r, 1000)); }
  console.log('files', fs.readdirSync(outDir).map(f => f + ':' + fs.statSync(path.join(outDir, f)).size));
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
