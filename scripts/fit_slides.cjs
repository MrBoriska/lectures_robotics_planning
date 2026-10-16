#!/usr/bin/env node
// Подбор размера текста для слайдов (классы fs-1 … fs-4 темы robotics-minimal).
//
// Для каждого слайда лекции перебираются уровни увеличения и выбирается тот,
// при котором содержимое занимает больше всего площади кадра и при этом ничего
// не выходит за кадр, не наползает на соседний блок и схема не сжимается
// меньше 120 px. Слайды с интерактивными моделями, титульные и слайды, где
// схема уже занимает кадр до низа, не трогаются.
//
//   node scripts/fit_slides.cjs lecture-07            — отчёт
//   node scripts/fit_slides.cjs lecture-07 --write    — записать классы в .md
//
// Нужен Playwright с Chromium (в DevContainer: npx playwright или глобальная
// установка; путь к пакету можно задать переменной PLAYWRIGHT_MODULE).

const { execSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const TIERS = ['', 'fs-1', 'fs-2', 'fs-3', 'fs-4'];

function loadPlaywright() {
  for (const m of [process.env.PLAYWRIGHT_MODULE, 'playwright', '/opt/node-tools/node_modules/playwright']) {
    if (!m) continue;
    try { return require(m); } catch { /* следующий вариант */ }
  }
  console.error('Не найден Playwright: установите его или задайте PLAYWRIGHT_MODULE.');
  process.exit(1);
}

// Выполняется в странице: доля занятой площади и признак переполнения.
function measureAll([TIERS, asIs]) {
  const measure = (s) => {
    const sr = s.getBoundingClientRect();
    const sc = sr.width / 1280;
    const C = 8, W = 160;
    const grid = new Uint8Array(W * 90);
    let over = false, maxB = 0;
    const mark = (r) => {
      if (!r.width || !r.height) return;
      let x0 = (r.left - sr.left) / sc, x1 = (r.right - sr.left) / sc;
      let y0 = (r.top - sr.top) / sc, y1 = (r.bottom - sr.top) / sc;
      maxB = Math.max(maxB, y1);
      // 10 px запаса снизу: шрифты на другой машине могут переносить строки иначе
      if (y1 > 672 || x1 > 1241) over = true;
      x0 = Math.max(x0, 44); x1 = Math.min(x1, 1236); y0 = Math.max(y0, 44); y1 = Math.min(y1, 682);
      for (let y = Math.floor(y0 / C); y < Math.ceil(y1 / C); y++)
        for (let x = Math.floor(x0 / C); x < Math.ceil(x1 / C); x++) grid[y * W + x] = 1;
    };
    const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    for (let n; (n = tw.nextNode());) {
      if (!n.textContent.trim() || n.parentElement.closest('header,footer,.katex-mathml')) continue;
      const rg = document.createRange();
      rg.selectNodeContents(n);
      for (const r of rg.getClientRects()) mark(r);
    }
    for (const e of s.querySelectorAll('img,iframe,video,canvas')) mark(e.getBoundingClientRect());
    for (const e of s.querySelectorAll('.grid-2,.grid-3,.col,.card,table')) if (e.scrollHeight > e.clientHeight + 3) over = true;
    for (const im of s.querySelectorAll('.diagram-box img')) if (im.getBoundingClientRect().height / sc < 120) over = true;
    let cnt = 0, tot = 0;
    for (let y = 5; y < 85; y++) for (let x = 5; x < 155; x++) { tot++; cnt += grid[y * W + x]; }
    return { fill: cnt / tot, vfill: (maxB - 44) / 638, over };
  };
  return [...document.querySelectorAll('svg[data-marpit-svg] > foreignObject > section')].map((s) => {
    const orig = s.className;
    const base = orig.replace(/\bfs-\d\b/g, '').replace(/\s+/g, ' ').trim();
    const info = {
      title: (s.querySelector('h1,h2')?.textContent || '').trim().slice(0, 60),
      lead: /\blead\b/.test(base),
      iframe: !!s.querySelector('iframe'),
      img: !!s.querySelector('img'),
      variants: [],
    };
    if (asIs) {
      info.variants.push({ cls: orig, ...measure(s) });
      return info;
    }
    const bases = /\bcompact\b/.test(base) ? [base, base.replace(/\bcompact\b/, '').trim()] : [base];
    for (const b of bases) for (const t of TIERS) {
      s.className = [b, t].filter(Boolean).join(' ');
      info.variants.push({ cls: s.className, ...measure(s) });
    }
    s.className = orig;
    return info;
  });
}

function choose(r) {
  const v0 = r.variants[0];
  if (r.lead || r.iframe || (r.img && v0.vfill >= 0.9)) return v0;
  const ok = r.variants.filter((v) => !v.over);
  if (!ok.length) return v0;
  const best = ok.reduce((a, b) => (b.fill > a.fill + 0.005 ? b : a));
  return best.fill >= v0.fill + 0.03 ? best : v0;
}

function writeClasses(mdPath, picks) {
  const lines = fs.readFileSync(mdPath, 'utf8').split('\n');
  const starts = lines.map((l, i) => (/^---\s*$/.test(l) ? i : -1)).filter((i) => i >= 0).slice(1);
  if (starts.length !== picks.length) throw new Error(`слайдов в .md ${starts.length}, в HTML ${picks.length}`);
  const ops = [];
  starts.forEach((s, k) => {
    const e = k + 1 < starts.length ? starts[k + 1] : lines.length;
    const cls = picks[k];
    const at = lines.slice(s + 1, e).findIndex((l) => /^<!--\s*_class:.*-->$/.test(l));
    if (at >= 0) ops.push({ i: s + 1 + at, cls, replace: true });
    else if (cls) ops.push({ i: s + 1, cls, replace: false });
  });
  for (const op of ops.reverse()) {
    if (op.replace) {
      if (op.cls) lines[op.i] = `<!-- _class: ${op.cls} -->`;
      else lines.splice(op.i, lines[op.i + 1] === '' && lines[op.i - 1] === '' ? 2 : 1);
    } else {
      lines.splice(op.i, 0, '', `<!-- _class: ${op.cls} -->`);
    }
  }
  fs.writeFileSync(mdPath, lines.join('\n'));
}

async function render(mdPath, browser, asIs) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'fit-'));
  const html = path.join(tmp, 'slides.html');
  execSync(`npx marp --config-file marp.config.mjs --allow-local-files --html "${mdPath}" -o "${html}"`, { cwd: ROOT, stdio: 'ignore' });
  fs.writeFileSync(html, fs.readFileSync(html, 'utf8').replace(/\.\.\/\.\.\/assets\//g, `file://${ROOT}/assets/`));
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + html);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(2000);
  const res = await page.evaluate(measureAll, [TIERS, asIs]);
  await page.close();
  fs.rmSync(tmp, { recursive: true, force: true });
  return res;
}

const lower = (cls) => cls.split(' ').map((c) => {
  const m = /^fs-(\d)$/.exec(c);
  return m ? (m[1] > 1 ? `fs-${m[1] - 1}` : '') : c;
}).filter(Boolean).join(' ');

(async () => {
  const lecture = process.argv[2];
  const doWrite = process.argv.includes('--write');
  if (!lecture) { console.error('Укажите лекцию: node scripts/fit_slides.cjs lecture-07 [--write]'); process.exit(1); }
  const mdPath = path.join(ROOT, 'lectures', lecture, `${lecture}.md`);
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const res = await render(mdPath, browser, false);

  const picks = res.map((r, i) => {
    const v0 = r.variants[0], best = choose(r);
    const mark = best.cls !== v0.cls ? '→' : ' ';
    console.log(`${String(i + 1).padStart(2)} ${mark} ${(best.cls || '-').padEnd(14)} площадь ${v0.fill.toFixed(2)} → ${best.fill.toFixed(2)}${best.over && !r.iframe ? '  ПЕРЕПОЛНЕНИЕ' : ''}  ${r.title}`);
    return best.cls;
  });
  if (doWrite) {
    writeClasses(mdPath, picks);
    // Проверка на собранном файле: класс в разметке и класс, выставленный
    // в браузере, дают чуть разную вёрстку. Переполненные слайды — на уровень ниже.
    for (let round = 0; round < 4; round++) {
      const now = await render(mdPath, browser, true);
      const bad = now.map((r, i) => (r.variants[0].over && /\bfs-\d\b/.test(picks[i]) ? i : -1)).filter((i) => i >= 0);
      if (!bad.length) break;
      for (const i of bad) {
        console.log(`${String(i + 1).padStart(2)}   ${picks[i]} не помещается после сборки → ${lower(picks[i]) || '-'}`);
        picks[i] = lower(picks[i]);
      }
      writeClasses(mdPath, picks);
    }
    console.log(`Записано: ${path.relative(ROOT, mdPath)}`);
  }
  await browser.close();
})();
