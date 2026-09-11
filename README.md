# Планирование движений и траекторий мобильных роботов

Курс из восьми лекций по 90 минут. Презентации написаны на Markdown (Marp), в
слайды встроены интерактивные модели алгоритмов. Сборка и разработка ведутся в
Docker DevContainer, публикация — на GitHub Pages.

## Структура курса

Тематический план, включая содержание ещё не переработанных лекций, —
[`lectures/PLAN.md`](lectures/PLAN.md).

| | Тема | Файлы |
| :--- | :--- | :--- |
| 01 | Постановка задачи планирования и представление среды | [презентация](lectures/lecture-01/lecture-01.md) · [план](lectures/lecture-01/timing.md) |
| 02 | Дискретное планирование на графах и сетках | [презентация](lectures/lecture-02/lecture-02.md) · [план](lectures/lecture-02/timing.md) |
| 03 | Методы планирования, основанные на выборке | [презентация](lectures/lecture-03/lecture-03.md) · [план](lectures/lecture-03/timing.md) |
| 04 | Кинематические модели и выборочные методы: DWA и MPPI | [презентация](lectures/lecture-04/lecture-04.md) · [план](lectures/lecture-04/timing.md) |
| 05 | Оптимальное управление: от принципа максимума к численным решателям | [презентация](lectures/lecture-05/lecture-05.md) · [план](lectures/lecture-05/timing.md) |
| 06 | Управление с прогнозирующей моделью (MPC) | [презентация](lectures/lecture-06/lecture-06.md) · [план](lectures/lecture-06/timing.md) |
| 07 | Динамические ограничения и профилирование скорости | [презентация](lectures/lecture-07/lecture-07.md) · [план](lectures/lecture-07/timing.md) |
| 08 | Вычислительные аспекты и инженерные компромиссы | [презентация](lectures/lecture-08/lecture-08.md) · [план](lectures/lecture-08/timing.md) |

Лекции 01 и 02 проработаны полностью. Остальные имеют актуальные названия;
их содержание перерабатывается согласно `lectures/PLAN.md`.

## Интерактивные модели

Автономные страницы на HTML5 Canvas без внешних зависимостей
([`widgets/`](widgets/)). Встраиваются в слайды через `iframe` и открываются
отдельно.

| Модель | Назначение | Лекция |
| :--- | :--- | :--- |
| [`cspace-minkowski`](widgets/cspace-minkowski/index.html) | Построение $\mathcal{C}_{obs} = \mathcal{O} \oplus (-\mathcal{A})$ при повороте несимметричного робота | 01 |
| [`dijkstra-graph`](widgets/dijkstra-graph/index.html) | Алгоритм Дейкстры по шагам на графе из 6 вершин: таблица расстояний, ослабление рёбер | 02 |
| [`graph-search-steps`](widgets/graph-search-steps/index.html) | Разбор итерации Дейкстры, $A^*$ и $\text{Theta}^*$ на сетке: очередь, псевдокод, проверка прямой видимости | 02 |
| [`astar-grid`](widgets/astar-grid/index.html) | Сравнение трёх алгоритмов на произвольной карте, рисование стен мышью | 02 |
| [`mapf-spacetime`](widgets/mapf-spacetime/index.html) | Пространственно-временной $A^*$, конфликты и действие ожидания | 02 |
| [`rrt-exploration`](widgets/rrt-exploration/index.html) | RRT и $\text{RRT}^*$, переподключение ветвей | 03 |
| [`potential-field`](widgets/potential-field/index.html) | Потенциальные поля и захват в локальный минимум | 04 |

## Иллюстрации

Схемы алгоритмов не рисуются вручную, а вычисляются:
[`scripts/generate_algorithmic_diagrams.py`](scripts/generate_algorithmic_diagrams.py)
строит их расчётом (реальная проверка прямой видимости, настоящий поиск на
сетке, аналитические кривые Дубинса, диаграмма Вороного волновым методом) и
сохраняет в `assets/images/`. Генератор запускается автоматически при каждой
сборке, поэтому рисунок не может разойтись с текстом слайда.

Фотографические иллюстрации и PDF литературы хранятся в Git LFS
(см. [`.gitattributes`](.gitattributes)).

## Команды

| Команда | Действие |
| :--- | :--- |
| `npm run widgets` | Сервер интерактивных моделей на порту `5599` — нужен для предпросмотра слайдов |
| `npm run dev` | Сервер Marp с автообновлением слайдов |
| `npm run build:html` | Сборка HTML-версий и портала курса в `dist/` |
| `npm run build` | То же, что `build:html` |
| `npm run build:pdf` | Экспорт лекций в PDF через Chromium |
| `npm run generate:diagrams` | Перегенерация схем без полной сборки |
| `npm run preview` | Сборка и локальный просмотр портала на порту `8080` |

### Предпросмотр слайдов в VS Code

Интерактивные вставки загружаются с `http://localhost:5599`, поэтому перед
открытием предпросмотра нужно выполнить `npm run widgets`. Для отображения
`iframe` в боковой панели однократно выполните команду
**Markdown: Change Preview Security Settings** и выберите **Disable**.

## Первоисточники

Литература, на которую опирается курс, — в [`references/`](references/):
монография LaValle, конспект курса ETH Zürich, лекции MIT 16.410 и статья
Karaman & Frazzoli об асимптотической оптимальности.
