#!/usr/bin/env node
import { existsSync, mkdirSync, cpSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve, join, dirname, basename } from 'node:path';
import { execSync } from 'node:child_process';

const ROOT_DIR = resolve(process.cwd());
const DIST_DIR = join(ROOT_DIR, 'dist');
const LECTURES_DIR = join(ROOT_DIR, 'lectures');
const THEMES_DIR = join(ROOT_DIR, 'themes');
const WIDGETS_DIR = join(ROOT_DIR, 'widgets');
const ASSETS_DIR = join(ROOT_DIR, 'assets');

const args = process.argv.slice(2);
const buildPdf = args.includes('--pdf');
const isHtmlOnly = args.includes('--html-only') || !buildPdf;

console.log('🚀 [Build] Начало сборки курса лекций...');
console.log(`📦 [Config] PDF экспорт: ${buildPdf ? 'Включен' : 'Отключен (HTML only)'}`);

// Ensure dist directory exists
if (!existsSync(DIST_DIR)) {
  mkdirSync(DIST_DIR, { recursive: true });
}

// 0. Generate algorithmic diagrams
const algoScript = join(ROOT_DIR, 'scripts', 'generate_algorithmic_diagrams.py');
if (existsSync(algoScript)) {
  console.log('📐 [Diagrams] Генерация математически строгих диаграмм алгоритмов...');
  try {
    execSync(`python3 "${algoScript}"`, { stdio: 'inherit' });
  } catch (err) {
    console.warn('⚠️ [Diagrams Warning] Не удалось сгенерировать диаграммы:', err.message);
  }
}

// 1. Copy themes, widgets & assets
console.log('🎨 [Assets] Копирование тем оформления, интерактивных виджетов и иллюстраций...');
mkdirSync(join(DIST_DIR, 'themes'), { recursive: true });
cpSync(THEMES_DIR, join(DIST_DIR, 'themes'), { recursive: true });

mkdirSync(join(DIST_DIR, 'widgets'), { recursive: true });
cpSync(WIDGETS_DIR, join(DIST_DIR, 'widgets'), { recursive: true });

if (existsSync(ASSETS_DIR)) {
  mkdirSync(join(DIST_DIR, 'assets'), { recursive: true });
  cpSync(ASSETS_DIR, join(DIST_DIR, 'assets'), { recursive: true });
}

// `serve` rewrites /widgets/<name>/index.html -> /widgets/<name> by default.
// Dropping the trailing segment re-bases every relative URL inside the widget,
// so `../common/widget-base.css` resolved to /common/... and 404'd — the
// simulators then rendered as an unstyled (visually blank) page inside their
// iframe. Turning clean URLs off keeps the widget's own base path intact.
writeFileSync(
  join(DIST_DIR, 'serve.json'),
  JSON.stringify({ cleanUrls: false, trailingSlash: true }, null, 2),
  'utf-8'
);

// 2. Discover lectures
const lectureDirs = readdirSync(LECTURES_DIR, { withFileTypes: true })
  .filter(d => d.isDirectory() && d.name.startsWith('lecture-'))
  .map(d => d.name)
  .sort();

console.log(`📚 [Lectures] Найдено лекций: ${lectureDirs.length}`);

const lectureMetadata = [];

for (const dirName of lectureDirs) {
  const lecturePath = join(LECTURES_DIR, dirName);
  const mdFile = join(lecturePath, `${dirName}.md`);
  if (!existsSync(mdFile)) continue;

  const content = readFileSync(mdFile, 'utf-8');

  // Extract title and subtitle
  const titleMatch = content.match(/# \*\*(.*?)\*\*/);
  const subtitleMatch = content.match(/## (.*?)\n/);
  const title = titleMatch ? titleMatch[1] : `Планирование для мобильных роботов`;
  const subtitle = subtitleMatch ? subtitleMatch[1] : dirName;

  const outLectureDir = join(DIST_DIR, 'lectures', dirName);
  mkdirSync(outLectureDir, { recursive: true });

  const outHtmlPath = join(outLectureDir, 'index.html');
  const outPdfPath = join(outLectureDir, `${dirName}.pdf`);

  console.log(`\n⚙️ [Marp] Компиляция ${dirName} в HTML...`);
  const marpCommandHtml = `npx marp "${mdFile}" --config-file "${join(ROOT_DIR, 'marp.config.mjs')}" --html --allow-local-files -o "${outHtmlPath}"`;
  execSync(marpCommandHtml, { stdio: 'inherit', env: { ...process.env, MARP_NO_SANDBOX: 'true' } });

  // Normalize localhost widget paths to relative paths for production dist
  if (existsSync(outHtmlPath)) {
    let htmlContent = readFileSync(outHtmlPath, 'utf-8');
    // 5599 is the dev port served by `npm run widgets`; 5500 is kept so decks
    // that still point at a Live Server instance keep building correctly.
    htmlContent = htmlContent.replace(/http:\/\/(localhost|127\.0\.0\.1):(5599|5500)\/widgets\//g, '../../widgets/');
    writeFileSync(outHtmlPath, htmlContent, 'utf-8');
  }

  if (buildPdf) {
    console.log(`📄 [Marp] Экспорт ${dirName} в PDF...`);
    try {
      const marpCommandPdf = `npx marp "${mdFile}" --config-file "${join(ROOT_DIR, 'marp.config.mjs')}" --pdf --pdf-outlines --allow-local-files -o "${outPdfPath}"`;
      execSync(marpCommandPdf, { stdio: 'inherit', env: { ...process.env, MARP_NO_SANDBOX: 'true' } });
    } catch (err) {
      console.warn(`⚠️ [Marp PDF Warning] Не удалось экспортировать PDF для ${dirName}:`, err.message);
    }
  }

  lectureMetadata.push({
    id: dirName,
    num: dirName.replace('lecture-', ''),
    title,
    subtitle,
    htmlUrl: `lectures/${dirName}/index.html`,
    pdfUrl: `lectures/${dirName}/${dirName}.pdf`,
    hasPdf: buildPdf && existsSync(outPdfPath)
  });
}

// 3. Generate Landing Portal (index.html)
console.log('\n🌐 [Portal] Генерация главной страницы портала курса (index.html)...');

const portalHtml = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Планирование траекторий и движений мобильных роботов | Курс лекций</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card-bg: #111827;
      --card-hover: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #0284c7;
      --accent-glow: #38bdf8;
      --border: #1f2937;
      --font: 'Inter', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 40px 20px;
    }

    .container {
      max-width: 1180px;
      margin: 0 auto;
    }

    header.course-header {
      margin-bottom: 48px;
      padding-bottom: 32px;
      border-bottom: 1px solid var(--border);
    }

    .badges-top {
      display: flex;
      gap: 10px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      font-weight: 600;
      padding: 4px 12px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .badge-primary { background: rgba(2, 132, 199, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-secondary { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }
    .badge-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }

    h1 {
      font-size: 38px;
      font-weight: 800;
      letter-spacing: -0.025em;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #ffffff 30%, #38bdf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    p.lead {
      font-size: 18px;
      color: var(--text-muted);
      max-width: 780px;
    }

    .section-title {
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Lectures Grid */
    .lectures-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 24px;
      margin-bottom: 56px;
    }

    .lecture-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      transition: all 0.2s ease;
      position: relative;
      overflow: hidden;
    }

    .lecture-card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 12px 24px -10px rgba(2, 132, 199, 0.25);
    }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }

    .lecture-num {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--accent-glow);
      background: rgba(2, 132, 199, 0.15);
      padding: 2px 8px;
      border-radius: 4px;
    }

    .duration {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-muted);
    }

    h3.lecture-title {
      font-size: 18px;
      font-weight: 600;
      line-height: 1.4;
      margin-bottom: 16px;
      flex: 1;
      color: #ffffff;
    }

    .card-actions {
      display: flex;
      gap: 10px;
      margin-top: 16px;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 9px 16px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.15s ease;
      flex: 1;
    }

    .btn-primary {
      background: #0284c7;
      color: #ffffff;
    }
    .btn-primary:hover {
      background: #0369a1;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }

    .btn-secondary {
      background: #1f2937;
      color: #e2e8f0;
      border: 1px solid #374151;
    }
    .btn-secondary:hover {
      background: #374151;
      color: #ffffff;
    }

    /* Widgets Section */
    .widgets-banner {
      background: linear-gradient(180deg, #111827 0%, #0c1220 100%);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 32px;
      margin-bottom: 56px;
    }

    .widgets-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }

    .widget-link-card {
      background: #090d16;
      border: 1px solid #1f2937;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      text-decoration: none;
      color: var(--text);
      transition: border 0.15s;
    }

    .widget-link-card:hover {
      border-color: #38bdf8;
    }

    .widget-link-card h4 {
      font-size: 16px;
      color: #38bdf8;
      margin-bottom: 8px;
    }

    .widget-link-card p {
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 12px;
      flex: 1;
    }

    footer.portal-footer {
      text-align: center;
      padding-top: 32px;
      border-top: 1px solid var(--border);
      font-size: 14px;
      color: var(--text-muted);
    }

    footer a {
      color: #38bdf8;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="course-header">
      <div class="badges-top">
        <span class="badge badge-primary">Robotics & Autonomous Systems</span>
        <span class="badge badge-secondary">8 лекций по 90 минут</span>
        <span class="badge badge-amber">Marp Presentation Ecosystem</span>
      </div>
      <h1>Планирование движений и траекторий мобильных роботов</h1>
      <p class="lead">Полный курс лекций с интерактивными визуализаторами алгоритмов (A*, RRT, APF), строгой математической базой и учетом физических ограничений мобильных платформ.</p>
    </header>

    <main>
      <h2 class="section-title">📚 Материалы курса (8 лекций)</h2>
      <div class="lectures-grid">
        ${lectureMetadata.map(l => `
          <div class="lecture-card">
            <div class="card-top">
              <span class="lecture-num">Лекция ${l.num}</span>
              <span class="duration">⏱️ 90 минут</span>
            </div>
            <h3 class="lecture-title">${l.subtitle.replace(/^Лекция \d+:\s*/, '')}</h3>
            <div class="card-actions">
              <a href="${l.htmlUrl}" class="btn btn-primary" target="_blank">▶ Презентация</a>
              ${l.hasPdf ? `<a href="${l.pdfUrl}" class="btn btn-secondary" download>📄 PDF</a>` : ''}
            </div>
          </div>
        `).join('')}
      </div>

      <div class="widgets-banner">
        <h2 class="section-title">🕹️ Интерактивные симуляторы алгоритмов</h2>
        <p style="color: var(--text-muted);">Интерактивные виджеты встроены прямо в презентации Marp, а также доступны в полноэкранном режиме:</p>
        <div class="widgets-grid">
          <a href="widgets/cspace-minkowski/index.html" class="widget-link-card" target="_blank">
            <h4>C-Space & Minkowski Sum</h4>
            <p>Конфигурационное пространство, поворот робота $\theta$, вычисление сечения {obs} = O \oplus (-A)$ и проверка коллизий.</p>
            <span class="lecture-num">Открыть симулятор →</span>
          </a>
          <a href="widgets/mapf-spacetime/index.html" class="widget-link-card" target="_blank">
            <h4>Space-Time A* & MAPF</h4>
            <p>Многоагентное планирование, предотвращение Vertex и Swap коллизий с помощью действий ожидания (WAIT) и таблицы резервирования.</p>
            <span class="lecture-num">Открыть симулятор →</span>
          </a>
          <a href="widgets/graph-search-steps/index.html" class="widget-link-card" target="_blank">
            <h4>Пошаговый разбор: Dijkstra / A* / Theta*</h4>
            <p>Одна итерация за клик: извлечение из OPEN, релаксация ребра, проверка LineOfSight. Очередь с приоритетом и псевдокод синхронны с сеткой.</p>
            <span class="lecture-num">Открыть симулятор →</span>
          </a>
          <a href="widgets/astar-grid/index.html" class="widget-link-card" target="_blank">
            <h4>A* & Dijkstra Grid Search</h4>
            <p>Дискретный поиск кратчайшего пути на 2D-сетке, динамическое рисование препятствий, сравнение эвристик.</p>
            <span class="lecture-num">Открыть симулятор →</span>
          </a>
          <a href="widgets/rrt-exploration/index.html" class="widget-link-card" target="_blank">
            <h4>RRT / RRT* Tree Planner</h4>
            <p>Случайные деревья быстрого исследования в непрерывном пространстве $C_{space}$, пошаговый сэмплинг и rewiring.</p>
            <span class="lecture-num">Открыть симулятор →</span>
          </a>
          <a href="widgets/potential-field/index.html" class="widget-link-card" target="_blank">
            <h4>Artificial Potential Fields (APF)</h4>
            <p>Искусственные потенциальные поля: векторы притяжения/отталкивания и наглядный захват робота в локальный минимум.</p>
            <span class="lecture-num">Открыть симулятор →</span>
          </a>
        </div>
      </div>
    </main>

    <footer class="portal-footer">
      <p>Курс «Планирование для мобильных роботов» • Сгенерировано с помощью <a href="https://marp.app" target="_blank">Marp</a> & GitHub Pages</p>
    </footer>
  </div>
</body>
</html>
`;

writeFileSync(join(DIST_DIR, 'index.html'), portalHtml, 'utf-8');
console.log('✅ [Portal] Файл dist/index.html успешно создан!');
console.log('🎉 [Success] Сборка завершена успешно!');
