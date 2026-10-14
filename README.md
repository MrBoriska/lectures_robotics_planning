# Планирование движений и траекторий мобильных роботов

Курс из восьми лекций по 90 минут. Презентации написаны на Markdown (Marp), в
слайды встроены интерактивные модели алгоритмов. Сборка и разработка ведутся в
Docker DevContainer, публикация — на GitHub Pages.

## Структура курса

Тематический и методический план курса — [`lectures/PLAN.md`](lectures/PLAN.md).

| | Тема | Файлы |
| :--- | :--- | :--- |
| 01 | Постановка задачи планирования и представление среды | [презентация](lectures/lecture-01/lecture-01.md) · [план](lectures/lecture-01/timing.md) |
| 02 | Дискретное планирование на графах и сетках | [презентация](lectures/lecture-02/lecture-02.md) · [план](lectures/lecture-02/timing.md) |
| 03 | Методы планирования, основанные на выборке | [презентация](lectures/lecture-03/lecture-03.md) · [план](lectures/lecture-03/timing.md) |
| 04 | Учёт модели движения: кинодинамическое планирование, DWA и MPPI | [презентация](lectures/lecture-04/lecture-04.md) · [план](lectures/lecture-04/timing.md) |
| 05 | Оптимальное управление: от принципа максимума Понтрягина к численному решению и MPC | [презентация](lectures/lecture-05/lecture-05.md) · [план](lectures/lecture-05/timing.md) |
| 06 | Обучение с подкреплением в робототехнике: от марковских процессов к переносу политик на реальных роботов | [презентация](lectures/lecture-06/lecture-06.md) · [план](lectures/lecture-06/timing.md) |
| 07 | Продвинутые алгоритмы: планирование в координатах Френе, диффузионные политики и NoMaD | [презентация](lectures/lecture-07/lecture-07.md) · [план](lectures/lecture-07/timing.md) |
| 08 | Антропоморфные роботы: от точки нулевого момента до моделей «зрение–язык–действие» | [презентация](lectures/lecture-08/lecture-08.md) · [план](lectures/lecture-08/timing.md) |

Все 8 лекций курса полностью разработаны, снабжены подробными методическими планами (тайминг 90 минут), математически строгими диаграммами и интерактивными симуляторами.

## Интерактивные модели

Автономные страницы на HTML5 Canvas без внешних зависимостей ([`widgets/`](widgets/)). Встраиваются в слайды через `iframe` и открываются отдельно.

| Модель | Назначение | Лекция |
| :--- | :--- | :--- |
| [`cspace-minkowski`](widgets/cspace-minkowski/index.html) | Построение $\mathcal{C}_{obs} = \mathcal{O} \oplus (-\mathcal{A})$ при повороте несимметричного робота | 01 |
| [`dijkstra-graph`](widgets/dijkstra-graph/index.html) | Алгоритм Дейкстры по шагам на графе из 6 вершин: таблица расстояний, ослабление рёбер | 02 |
| [`graph-search-steps`](widgets/graph-search-steps/index.html) | Разбор итерации Дейкстры, $A^*$ и $\text{Theta}^*$ на сетке: очередь, псевдокод, проверка прямой видимости | 02 |
| [`astar-grid`](widgets/astar-grid/index.html) | Сравнение Дейкстры и $A^*$ на произвольной карте, рисование стен мышью | 02 |
| [`mapf-spacetime`](widgets/mapf-spacetime/index.html) | Пространственно-временной $A^*$, конфликты вершин/рёбер и действие ожидания | 02 |
| [`prm-roadmap`](widgets/prm-roadmap/index.html) | Вероятностные дорожные карты: построение графа (Learning), $k$-NN, фаза запроса (Query) и Lazy PRM | 03 |
| [`rrt-exploration`](widgets/rrt-exploration/index.html) | Деревья RRT, RRT-Connect, $\text{RRT}^*$ и Informed $\text{RRT}^*$: смещение Вороного, сжатый эллипсоид, rewire | 03 |
| [`narrow-passage`](widgets/narrow-passage/index.html) | Проблема узких коридоров и Bridge Test (мостовой сэмплинг) | 03 |
| [`bit-star`](widgets/bit-star/index.html) | Batch Informed Trees ($\text{BIT}^*$): пакетная выборка и неявный случайный геометрический граф | 03 |
| [`potential-field`](widgets/potential-field/index.html) | Искусственные потенциальные поля (APF) Хатиба и захват в локальный минимум | 04 |
| [`dwa-planner`](widgets/dwa-planner/index.html) | Dynamic Window Approach (DWA): допустимые скорости $(v, \omega)$, торможение, выбор траектории | 04 |
| [`mppi-planner`](widgets/mppi-planner/index.html) | Model Predictive Path Integral (MPPI): стохастические rollouts траекторий на GPU | 04 |
| [`hybrid-astar`](widgets/hybrid-astar/index.html) | Hybrid $A^*$: планирование для шасси с кинематикой Ридса–Шеппа / Дубинса | 04 |
| [`kinodynamic-rrt`](widgets/kinodynamic-rrt/index.html) | Кинодинамический RRT: прямое интегрирование ODE с динамическими ограничениями | 04 |
| [`bang-bang-simulator`](widgets/bang-bang-simulator/index.html) | Тележка на фазовой плоскости: релейное управление (быстродействие), минимум энергии и LQR на одной задаче; толчок, дребезг | 05 |
| [`shooting-collocation-simulator`](widgets/shooting-collocation-simulator/index.html) | Одиночная и многократная стрельба, коллокация: настоящий SQP по шагам, дефекты и невязки; неустойчивая система | 05 |
| [`mpc-interactive-solver`](widgets/mpc-interactive-solver/index.html) | MPC для робота на плоскости: скользящий горизонт, короткий горизонт, неточная модель и толчок, локальный минимум | 05 |
| [`rl-policy-shaping`](widgets/rl-policy-shaping/index.html) | Табличный Q-learning на клеточном поле и точное решение; исследование, дисконт, скольжение; разреженная, потенциальная награда и взлом награды | 06 |
| [`velocity-profile`](widgets/velocity-profile/index.html) | Профиль скорости по пути: предел по кривизне, прямой и обратный проходы, ломаная против сплайна, сравнение с постоянной скоростью | 02 |
| [`frenet-planner`](widgets/frenet-planner/index.html) | Планирование в координатах Френе: веер полиномов, стоимость, проверка столкновений с движущимися машинами, пересчёт 10 раз в секунду | 07 |
| [`diffusion-policy-interactive`](widgets/diffusion-policy-interactive/index.html) | Объезд препятствия по демонстрациям: регрессия MSE, диффузия (DDPM) и согласование потоков на точной модели данных; наведение по стоимости | 07 |
| [`lipm-capture-point`](widgets/lipm-capture-point/index.html) | Модель перевёрнутого маятника: толчок, удержание голеностопом, шаг в точку захвата, фиксированный шаг | 08 |

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

Интерактивные вставки раздаются локальным сервером на порту `5599`. В `.devcontainer` и VS Code сервер запускается **автоматически в фоновом режиме** при открытии проекта (через `postStartCommand` и фоновую задачу `.vscode/tasks.json`). Ручной запуск обычно не требуется (но доступен через `npm run widgets`).

При сборке для GitHub Pages (`npm run build:html`) скрипт сборки автоматически транслирует пути в относительные (`../../widgets/...`), поэтому публикация работает на 100% статически.

Для корректного отображения интерактивных вставок (`iframe`) в боковой панели Marp:
1. Откройте любой файл лекции (например, `lectures/lecture-03/lecture-03.md`).
2. Нажмите иконку Marp **«Open Preview to the Side»** (или сочетание `Ctrl+K V`).
3. Если превью сообщает о блокировке небезопасного контента, нажмите `Ctrl+Shift+P`, выполните команду **Markdown: Change Preview Security Settings** и выберите **Disable** (или **Allow insecure local content**).

## Первоисточники

Литература, на которую опирается курс, — в [`references/`](references/):
монография LaValle, конспект курса ETH Zürich, лекции MIT 16.410 и статья
Karaman & Frazzoli об асимптотической оптимальности.
