# 🤖 Курс лекций: Планирование движений и траекторий мобильных роботов

[![Marp](https://img.shields.io/badge/Presented_with-Marp-0284c7.svg)](https://marp.app/)
[![DevContainer](https://img.shields.io/badge/VS_Code-DevContainer-2563eb.svg)](https://code.visualstudio.com/docs/devcontainers/containers)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub_Pages-10b981.svg)](https://pages.github.com/)
[![Lectures](https://img.shields.io/badge/Lectures-8_%C3%97_90_min-f59e0b.svg)](#структура-курса)

Современный учебно-методический комплекс презентаций для 90-минутных лекций по планированию движений мобильных колесных роботов. Написан на **Markdown (Marp)** со встроенными интерактивными симуляторами алгоритмов, строгой математической формализацией ($\mathcal{C}$-space, суммы Минковского, неголономные связи, LQR, MPC, World Models), минималистичным дизайном и готовым **Docker DevContainer** для изолированной разработки.

---

## 📚 Структура курса (8 лекций по 90 минут)

Каждая лекция выстроена по строгому педагогическому регламенту: теория (45 мин), интерактивный симулятор (15 мин), прикладная робототехника / ROS 2 (20 мин) и Q&A (10 мин).

| Лекция | Файл презентации | План и тайминг | Ключевые темы и концепции |
| :--- | :--- | :--- | :--- |
| **Лекция 01** | [`lecture-01.md`](lectures/lecture-01/lecture-01.md) | [timing.md](lectures/lecture-01/timing.md) | **Постановка задачи планирования, репрезентация среды и ландшафт методов:** Path vs Trajectory, $\mathcal{C}$-space, сумма Минковского, профильная, опорная и семантическая проходимость, SOTA (nvblox, wavemap, elevation_mapping_cupy), SDF/ESDF, World Models. |
| **Лекция 02** | [`lecture-02.md`](lectures/lecture-02/lecture-02.md) | [timing.md](lectures/lecture-02/timing.md) | **Дискретное планирование на графах и сетках:** 4/8-связные сетки, граф видимости, диаграммы Вороного, Dijkstra, $A^*$, допустимые и монотонные эвристики (Octile, Manhattan, Euclid), $D^*$ Lite, сглаживание траекторий. |
| **Лекция 03** | [`lecture-03.md`](lectures/lecture-03/lecture-03.md) | [timing.md](lectures/lecture-03/timing.md) | **Планирование, основанное на выборке:** Проклятие размерности, PRM, RRT, доказательство неоптимальности базового RRT (Караман–Фраццоли), асимптотически оптимальный $RRT^*$ (Rewiring), Informed $RRT^*$, $k$-d tree, BVH. |
| **Лекция 04** | [`lecture-04.md`](lectures/lecture-04/lecture-04.md) | [timing.md](lectures/lecture-04/timing.md) | **Реактивные и локальные методы:** Искусственные потенциальные поля (APF), гармонические поля (уравнение Лапласа $\Delta U = 0$), устранение U-ловушек, Dynamic Window Approach (DWA), Timed Elastic Band (TEB), Velocity Obstacles (VO/RVO). |
| **Лекция 05** | [`lecture-05.md`](lectures/lecture-05/lecture-05.md) | [timing.md](lectures/lecture-05/timing.md) | **Оптимальное управление:** Вариационное исчисление, принцип максимума Понтрягина (Bang-Bang управление), уравнение HJB, LQR регулятор и уравнение Риккати, Direct Shooting vs Direct Collocation, кривые Дубинса и Ридса-Шеппа. |
| **Лекция 06** | [`lecture-06.md`](lectures/lecture-06/lecture-06.md) | [timing.md](lectures/lecture-06/timing.md) | **Предиктивное управление (Model Predictive Control):** Принцип скользящего горизонта (Receding Horizon), линейный MPC (задача QP), нелинейный NMPC (Bicycle model, SQP, RTI, acados), Control Barrier Functions (CBF), Safe Flight Corridors. |
| **Лекция 07** | [`lecture-07.md`](lectures/lecture-07/lecture-07.md) | [timing.md](lectures/lecture-07/timing.md) | **Учёт ограничений в алгоритмах планирования:** Геометрические, кинематические и динамические связи, неголономность (Пфафф $\omega \dot{q} = 0$), скобки Ли (Lie brackets), теорема Чоу–Рашевского, State Lattice, Kinodynamic RRT, конус трения шин, профилирование TOPP-RA. |
| **Лекция 08** | [`lecture-08.md`](lectures/lecture-08/lecture-08.md) | [timing.md](lectures/lecture-08/timing.md) | **Вычислительные аспекты и инженерные компромиссы:** Многотактовая архитектура (1 Гц $\to$ 30 Гц $\to$ 1 кГц), компенсация задержки (Latency), алгоритм линейного EDT Фельзеншвальба, ROS 2 Nav2, Деревья поведения (Behavior Trees), восстановительные сценарии, Sim-to-Real. |

---

## 🕹️ Интерактивные алгоритмические симуляторы (`widgets/`)

В слайды интегрированы полнофункциональные автономные симуляторы (чистый HTML5 Canvas/JS):
1. [**C-Space & Minkowski Sum**](widgets/cspace-minkowski/index.html) — визуализация формирования среза $\mathcal{C}_{obs} = \mathcal{O} \oplus (-\mathcal{A})$ при вращении некруглого робота $\theta$.
2. [**A\* & Dijkstra Grid Search**](widgets/astar-grid/index.html) — интерактивная сетка, динамическое рисование стен, сравнение эвристик (Манхэттен, Евклид, Дейкстра $h=0$), анимация фронта волны.
3. [**RRT / RRT\* Tree Exploration**](widgets/rrt-exploration/index.html) — случайный сэмплинг в непрерывном $\mathcal{C}$-space, демонстрация переподключения ребер (Rewiring) в $RRT^*$.
4. [**Artificial Potential Fields (APF)**](widgets/potential-field/index.html) — векторы сил притяжения/отталкивания и наглядный захват робота в U-ловушку (локальный минимум).

---

## 📖 Первоисточники в репозитории (`references/`)

* **Стивен М. Лаваль:** «Planning Algorithms» ([`references/lavalle_planning_algorithms/`](references/lavalle_planning_algorithms/)).
* **ETH Zürich:** «Autonomous Mobile Robots» ([`references/eth_zurich/`](references/eth_zurich/)).
* **MIT:** «Principles of Autonomy and Decision Making» + статья Karaman & Frazzoli по $RRT^*$ ([`references/mit/`](references/mit/)).
* **Сводный анализ:** [`references/README.md`](references/README.md).

---

## 🛠️ Скрипты и команды (внутри Docker / DevContainer)

| Команда | Описание |
| :--- | :--- |
| `npm run dev` | Запуск сервера Marp с автообновлением слайдов на лету |
| `npm run build` | Полная сборка всех 8 презентаций в HTML, PDF и генерация портала курса |
| `npm run build:html` | Быстрая сборка только HTML-версий |
| `npm run build:pdf` | Экспорт всех лекций в PDF через Chromium |
| `npm run preview` | Локальный сервер портала курса на порту `8080` |
