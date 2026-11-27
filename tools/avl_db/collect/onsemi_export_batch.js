const puppeteer = require('puppeteer-core'); const fs = require('fs'); const path = require('path');
const outDir = path.resolve(process.argv[2]);
const list = [
  ['mosfet-high-voltage', 'discrete-power-modules/mosfets/high-voltage-mosfets'],
  ['mosfet-small-signal', 'discrete-power-modules/mosfets/small-signal-mosfets'],
  ['mosfet-sic', 'silicon-carbide-sic-power/elitesic-mosfets/sic-mosfets'],
  ['mosfet-gan', 'discrete-power-modules/gallium-nitride-gan-fets'],
  ['pic-offline-controllers', 'power-management/ac-dc-power-conversion/offline-controllers'],
  ['pic-offline-regulators', 'power-management/ac-dc-power-conversion/offline-regulators'],
  ['pic-pfc', 'power-management/ac-dc-power-conversion/power-factor-controllers'],
  ['pic-secondary-side', 'power-management/ac-dc-power-conversion/secondary-side-controllers'],
  ['pic-dcdc-controllers', 'power-management/dc-dc-power-conversion/controllers'],
  ['pic-dcdc-converters', 'power-management/dc-dc-power-conversion/converters'],
  ['pic-led-drivers', 'power-management/led-drivers'],
  ['drv-integrated-driver-mosfet', 'power-management/integrated-driver-mosfet'],
  ['diode-rectifiers', 'discrete-power-modules/rectifiers'],
  ['diode-schottky', 'discrete-power-modules/schottky-diodes-schottky-rectifiers'],
  ['diode-zener', 'discrete-power-modules/zener-diodes'],
  ['diode-small-signal-switching', 'discrete-power-modules/small-signal-switching-diodes'],
  ['diode-esd', 'discrete-power-modules/esd-protection-diodes'],
  ['diode-rf', 'discrete-power-modules/rf-diodes'],
  ['diode-sic', 'silicon-carbide-sic-power/elitesic-diodes'],
];
(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--no-sandbox'] });
  for (const [label, rel] of list) {
    if (fs.existsSync(path.join(outDir, label + '.csv'))) { console.log(label, 'skip(exists)'); continue; }
    const p = await b.newPage();
    try {
      await p.setUserAgent('DabomAVLResearch/1.0 (internal product-data research; respects robots.txt)');
      const cdp = await p.createCDPSession();
      const dl = path.join(outDir, '_dl_' + label); fs.mkdirSync(dl, { recursive: true });
      await cdp.send('Page.setDownloadBehavior', { behavior: 'allow', downloadPath: dl });
      const resp = await p.goto('https://www.onsemi.com/products/' + rel, { waitUntil: 'networkidle2', timeout: 120000 });
      if (!resp || resp.status() !== 200) { console.log(label, 'HTTP', resp && resp.status()); await p.close(); await new Promise(r => setTimeout(r, 12000)); continue; }
      await new Promise(r => setTimeout(r, 3000));
      const before = new Set(fs.readdirSync(dl));
      const total = await p.evaluate(() => { const e = document.querySelector('[data-table-size]'); return e ? e.getAttribute('data-table-size') : null; });
      const clicked = await p.evaluate(() => {
        const btn = document.querySelector('button.btn-export'); if (!btn) return 'no-export-btn';
        btn.click();
        const opt = [...document.querySelectorAll('p,div,a,button')].find(e => e.children.length < 2 && e.textContent.trim() === 'CSV Format');
        if (!opt) return 'no-option';
        (opt.closest('a,button,[role=button],div.row') || opt).click(); return 'ok';
      });
      let f = null;
      if (clicked === 'ok') for (let i = 0; i < 120; i++) { await new Promise(r => setTimeout(r, 1000)); const now = fs.readdirSync(dl).filter(x => !before.has(x) && !x.endsWith('.crdownload')); if (now.length) { f = now[0]; break; } }
      if (f) { const dst = path.join(outDir, label + '.csv'); fs.renameSync(path.join(dl, f), dst); fs.rmdirSync(dl); console.log(label, 'total', total, 'saved', fs.statSync(dst).size); }
      else console.log(label, 'total', total, 'click', clicked, 'NO DOWNLOAD');
    } catch (e) { console.log(label, 'ERR', e.message); }
    await p.close();
    await new Promise(r => setTimeout(r, 12000));   // robots.txt Crawl-delay: 10
  }
  await b.close(); console.log('DONE');
})();
