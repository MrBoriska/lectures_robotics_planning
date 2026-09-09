# 🤖 Курс лекций: Планирование движений и траекторий мобильных роботов

[![Marp](https://img.shields.io/badge/Presented_with-Marp-0284c7.svg)](https://marp.app/)
[![DevContainer](https://img.shields.io/badge/VS_Code-DevContainer-2563eb.svg)](https://code.visualstudio.com/docs/devcontainers/containers)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub_Pages-10b981.svg)](https://pages.github.com/)
[![Lectures](https://img.shields.io/badge/Lectures-8_%C3%97_90_min-f59e0b.svg)](#структура-курса)

Современный учебно-методический комплекс презентаций для 90-минутных лекций по планированию траекторий мобильных колесных роботов. Написан на **Markdown (Marp)** со встроенными интерактивными симуляторами алгоритмов, строгой математической формализацией ($\mathcal{C}$-space, суммы Минковского, неголономные связи), минималистичным дизайном и готовым **Docker DevContainer** для разработки.

---

## 🚀 Быстрый старт через VS Code DevContainer (Рекомендуется)

Проект полностью изолирован в легковесном Docker-контейнере на базе `node:22-bookworm-slim` с предустановленным Chromium, Marp CLI и плагинами VS Code. Ничего на хост-систему устанавливать не нужно!

1. Откройте директорию проекта в **VS Code**.
2. Установите расширение **Dev Containers** (`ms-vscode-remote.remote-containers`), если оно еще не установлено.
3. Нажмите `F1` (или `Ctrl+Shift+P` / `Cmd+Shift+P`) и выберите:  
   👉 **`Dev Containers: Reopen in Container`**
4. VS Code автоматически соберет легковесный контейнер, установит все экстеншены и настроит рабочую среду.

### Предустановленные расширения VS Code:
* 📽️ **Marp for VS Code** (`marp-team.marp-vscode`) — рендеринг слайдов, live-preview и экспорт.
* ✍️ **Markdown All in One** (`yzhang.markdown-all-in-one`) — шорткаты форматирования, оглавление.
* 📊 **Markdown Mermaid** (`bierner.markdown-mermaid`) — диаграммы и графы.
* 🌐 **Live Server** (`ritwickdey.liveserver`) — локальный предпросмотр интерактивных виджетов.
* 💅 **Prettier** (`esbenp.prettier-vscode`) — автоформатирование.
* 🔤 **Code Spell Checker + Russian** — проверка орфографии русского и английского языка.

---

## 📚 Структура курса (8 лекций по 90 минут)

Каждая лекция выстроена по строгому педагогическому регламенту:
* `00–15 мин`: Введение, мотивация, контекст физического робота.
* `15–35 мин`: Математический фундамент ($\mathcal{C}$-space, целевые функции, ограничения).
* `35–55 мин`: Алгоритмическое ядро, псевдокод и структуры данных.
* `55–70 мин`: **Интерактивная практика** с живым симулятором алгоритма.
* `70–85 мин`: Учет кинематики и неголономности, перенос в ROS 2 (Nav2).
* `85–90 мин`: Резюме, контрольные вопросы и дискуссия.

| Лекция | Файл презентации | План и тайминг | Статус темы |
| :--- | :--- | :--- | :--- |
| **Лекция 01** | [`lectures/lecture-01/lecture-01.md`](lectures/lecture-01/lecture-01.md) | [timing.md](lectures/lecture-01/timing.md) | Введение, $\mathcal{C}$-space, дискретный поиск ($A^*$, Dijkstra) |
| **Лекция 02** | [`lectures/lecture-02/lecture-02.md`](lectures/lecture-02/lecture-02.md) | [timing.md](lectures/lecture-02/timing.md) | [Тема будет заполнена] |
| **Лекция 03** | [`lectures/lecture-03/lecture-03.md`](lectures/lecture-03/lecture-03.md) | [timing.md](lectures/lecture-03/timing.md) | [Тема будет заполнена] |
| **Лекция 04** | [`lectures/lecture-04/lecture-04.md`](lectures/lecture-04/lecture-04.md) | [timing.md](lectures/lecture-04/timing.md) | [Тема будет заполнена] |
| **Лекция 05** | [`lectures/lecture-05/lecture-05.md`](lectures/lecture-05/lecture-05.md) | [timing.md](lectures/lecture-05/timing.md) | [Тема будет заполнена] |
| **Лекция 06** | [`lectures/lecture-06/lecture-06.md`](lectures/lecture-06/lecture-06.md) | [timing.md](lectures/lecture-06/timing.md) | [Тема будет заполнена] |
| **Лекция 07** | [`lectures/lecture-07/lecture-07.md`](lectures/lecture-07/lecture-07.md) | [timing.md](lectures/lecture-07/timing.md) | [Тема будет заполнена] |
| **Лекция 08** | [`lectures/lecture-08/lecture-08.md`](lectures/lecture-08/lecture-08.md) | [timing.md](lectures/lecture-08/timing.md) | [Тема будет заполнена] |

---

## 🕹️ Интерактивные симуляторы алгоритмов (`widgets/`)

В слайды можно встраивать интерактивные симуляторы через тег `<iframe>`. Они работают автономно в браузере без внешних библиотек и CDN:

1. **A\* & Dijkstra Grid Search** (`widgets/astar-grid/index.html`):
   - Динамическое рисование стен/препятствий мышью.
   - Перетаскивание точек Start и Goal.
   - Сравнение эвристик (Манхэттен, Евклид, Дейкстра $h=0$).
   - Пошаговый запуск и статистика исследованных узлов.
2. **RRT / RRT\* Sampling Planner** (`widgets/rrt-exploration/index.html`):
   - Случайные деревья в непрерывном 2D конфигурационном пространстве.
   - Визуализация выборки $q_{rand}$, ближайшего соседа $q_{near}$, шага $q_{new}$.
   - Сравнение классического RRT и оптимизирующего RRT\* (переподключение ветвей).
3. **Artificial Potential Fields** (`widgets/potential-field/index.html`):
   - Силы притяжения к цели и отталкивания от препятствий.
   - Наглядная демонстрация проблемы **локального минимума (U-ловушки)**.

---

## 🎨 Минималистичный и стильный дизайн (`themes/robotics-minimal.css`)

Кастомная тема для Marp создана специально для презентаций по робототехнике:
* Соотношение сторон 16:9 (`size: 16:9`).
* Поддержка математических формул $\LaTeX$ через MathJax/KaTeX.
* Готовые классы верстки:
  - `.grid-2`, `.grid-3` — адаптивные колонки для сравнения алгоритмов.
  - `.card`, `.card-accent`, `.card-alert`, `.card-success` — информационные блоки.
  - `.badge`, `.badge-blue`, `.badge-green`, `.badge-time` — маркеры тайминга и сложности.
  - `.formula-box` — акцентные блоки под математические формулы.
  - `<!-- _class: invert -->` — глубокий темный режим для титульных и итоговых слайдов.

---

## 🛠️ Скрипты и команды (внутри DevContainer)

| Команда | Описание |
| :--- | :--- |
| `npm run dev` | Запуск сервера Marp с автообновлением при сохранении `.md` файлов |
| `npm run build` | Полная сборка всех презентаций в HTML, копирование тем, виджетов и генерация портала |
| `npm run build:html` | Быстрая сборка только HTML-версий |
| `npm run build:pdf` | Экспорт всех лекций в формат PDF (через Chromium) |
| `npm run preview` | Сборка и запуск локального веб-сервера портала на порту `8080` |

---

## 🌐 Публикация на GitHub Pages

В репозитории настроен GitHub Actions Workflow ([`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)):
1. При любом `git push` в ветку `main` автоматически запускается сборка.
2. Генерируется портал курса `dist/index.html`, презентации лекций и интерактивные симуляторы.
3. Результат автоматически развертывается на **GitHub Pages**.
