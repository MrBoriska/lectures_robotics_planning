---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 01"
footer: "Планирование для мобильных роботов | Лекция 01"
math: katex

---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 01: Постановка задачи планирования, репрезентация среды и ландшафт методов

<div class="mt-4">

<span class="badge badge-blue">⏱️ 90 минут</span>
<span class="badge badge-green">Фундаментальный обзор</span>
<span class="badge badge-purple">LaValle • ETH Zürich • MIT • SOTA 2026</span>

</div>

---

<!-- _header: "Лекция 01 | Введение и мотивация" -->

## Чему посвящена эта лекция ? <span class="badge badge-blue">Контекст и цели</span>

<div class="grid-2 mt-2">

<div class="card card-accent">

### 🎯 Роль планирования в робототехнике

Автономный мобильный робот решает классическую триаду задач:
**«Где я?»** (локализация) $\rightarrow$ **«Что вокруг?»** (восприятие) $\rightarrow$ **«Как достигнуть цели?» (планирование)**.

Планирование — это ключевая задача автономного мобильного робота, связывающая сенсорное восприятие пространства с низкоуровневым управлением двигателями исходя из вышестоящей задачи.



**💡 Результат занятия:** Строго формулировать задачу планирования в $\mathcal{C}$-space, выбирать оптимальную репрезентацию среды под физику робота (колеса, гусеницы, шагающая платформа) и ориентироваться в современных индустриальных фреймворках восприятия и моделирования мира.

</div>

<div class="card">

### 🔍 Ключевые вопросы лекции

- **В чем разница** между планированием движения, геометрическим путем и динамической траекторией?
- **Как сжать робота в точку?** Конфигурационное пространство ($\mathcal{C}$-space) и сумма Минковского.
- **Почему геометрии мало?** Профильная, опорная (террамеханика) и семантическая проходимость.
- **Как оцифровать среду?** Сетки, октадеревья, GPU ESDF (`nvblox`, `wavemap`) и World Models.

</div>

</div>

---

<!-- _header: "Лекция 01 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-2">

<div class="card card-accent">

### Часть 1: Понятия, C-Space и Проходимость (45 мин)

- **00–15 мин:** Понятийный аппарат: Motion Planning, Path vs Trajectory. Локальное и глобальное планирование.
- **15–30 мин:** Конфигурационное пространство ($\mathcal{C}$-space) и сумма Минковского.
- **30–45 мин:** Проходимость среды: профильная (геометрическая), опорная (сцепление/грунт) и семантическая.

</div>

<div class="card card-accent">

### Часть 2: Репрезентации, Теория и World Models (45 мин)

- **45–60 мин:** Способы представления мира: Grids, Octree, **SOTA: nvblox, wavemap, elevation_mapping_cupy**. SDF/ESDF и градиенты.
- **60–70 мин:** Графы видимости, Вороной, Lattice, аналитическое описание для Optimal Control.
- **70–80 мин:** Свойства алгоритмов: полнота, оптимальность, асимптотическая оптимальность.
- **80–90 мин:** Нейросетевые методы: Latent Spaces, **World Models** (неявная физика) и Q&A.

</div>

</div>

---

## 1. Понятийный аппарат: Путь, Траектория, Движение <span class="badge badge-time">00–15 мин</span>

<div class="grid-3">

<div class="card">

### 1. Путь (Path)

$$\sigma: [0, 1] \to \mathcal{C}_{free}$$

- Чисто **геометрическая кривая** в пространстве конфигураций.
- Параметризована длиной дуги $s \in [0, 1]$.
- **Не содержит времени**, скоростей и ускорений.

</div>

<div class="card card-accent">

### 2. Траектория (Trajectory)

$$\tau: [0, T] \to \mathcal{X}_{free}$$

- Путь с **временной параметризацией**: $x(t), v(t), a(t)$.
- Учитывает кинематические и динамические возможности приводов шасси.

</div>

<div class="card card-success">

### 3. Motion Planning

Комплексная задача синтеза управлений $u(t)$ и состояний $x(t)$:

$$\dot{x}(t) = f(x(t), u(t))$$

переводящих систему из $x_0$ в $x_{goal}$ без столкновений и сбоев приводов.

</div>

</div>

---

## Локальное vs Глобальное планирование <span class="badge badge-time">00–15 мин</span>

<div class="grid-2">

<div class="card">

### Глобальное планирование (Global Planner)

- **Входные данные:** глобальная статическая карта окружения (SLAM / CAD / OSM).
- **Горизонт:** от текущей точки до финишной цели миссии (десятки/сотни метров).
- **Частота работы:** низкая ($\sim 0.2\text{--}2$ Гц) или разово по запросу.
- **Результат:** глобальный опорный путь $\sigma(s)$ без учета мгновенной динамики.

</div>

<div class="card card-accent">

### Локальное планирование (Local Planner / Controller)

- **Входные данные:** поток локальных сенсоров в реальном времени (лидары, камеры глубины).
- **Горизонт:** короткий горизонт безопасности ($2\text{--}8$ метров вперед, $1\text{--}3$ секунды).
- **Частота работы:** высокая ($\mathbf{20\text{--}50}$ Гц).
- **Результат:** команды приводов $(v, \omega)$, парирующие внезапные препятствия и снос.

</div>

</div>

---

## 2. Конфигурационное пространство ($\mathcal{C}$-space) <span class="badge badge-time">15–30 мин</span>

<div class="grid-2">

<div class="col">

<div class="card">

### Редукция робота к материальной точке

Конфигурация $q \in \mathcal{C}$ — минимальный вектор координат, однозначно определяющий положение каждой точки робота $\mathcal{A}(q)$ в рабочем пространстве $\mathcal{W} \subset \mathbb{R}^d$.

$$\mathcal{C}_{obs} = \{ q \in \mathcal{C} \mid \mathcal{A}(q) \cap \mathcal{O} \neq \emptyset \}$$
$$\mathcal{C}_{free} = \mathcal{C} \setminus \mathcal{C}_{obs}$$

В $\mathcal{C}$-space робот сложной формы сжимается в точку, а препятствия $\mathcal{O}$ раздуваются на геометрию робота.

</div>

</div>

<div class="col">

<div class="diagram-box">

<img src="../../assets/images/lecture-01/minkowski_cspace.svg" alt="Сумма Минковского и C-space" />

</div>

<div class="formula-box text-sm">

$$\mathcal{C}_{obs} = \mathcal{O} \oplus (-\mathcal{A}(0)) = \{ p - a \mid p \in \mathcal{O}, a \in \mathcal{A}(0) \}$$

</div>

</div>

</div>

---

<!-- _header: "Интерактивная практика | Сумма Минковского" -->

## Интерактивный симулятор: Формирование $\mathcal{C}_{obs}$ <span class="badge badge-green">⏱️ 20–30 мин</span>

<div class="interactive-container">

<div class="interactive-header">

<span><i class="interactive-dot"></i> Интерактивная сумма Минковского: Робот $\mathcal{A}(q)$ + Препятствие $\mathcal{O} \rightarrow \mathcal{C}_{obs}$</span>
<span>Перетаскивайте робота мышью | Вращайте угол $\theta$ ползунком</span>

</div>
<iframe src="http://localhost:5500/widgets/cspace-minkowski/index.html" class="interactive-frame"></iframe>

</div>

---

## 3. Проходимость среды (Traversability Analysis) <span class="badge badge-time">30–34 мин</span>

<div class="grid-3">

<div class="card card-accent">

### 1. Профильная (Геометрия)
- **Клиренс:** дорожный просвет днища
- **Углы свесов:** въезд $\alpha_{\text{app}}$ и съезд $\alpha_{\text{dep}}$
- **Предельный уклон:** $\theta \le \theta_{\max}$
- **Предельный шаг ступени:** $h \le h_{\text{step}}$
- **Сенсоры:** 3D LiDAR, TSDF / ESDF
- **Критерий:** корпус и днище не касаются препятствий

</div>
<div class="card card-alert">

### 2. Опорная (Террамеханика)
- **Коэффициент трения $\mu$:** лед, мокрая глина, сырой песок
- **Несущая способность грунта:** провал колес (*sinkage* $z$)
- **Проскальзывание:** *wheel slip* $s$
- **Модель:** Беккера–Вонга
- **Критерий:** передача тяги приводов без пробуксовки и посадки

</div>
<div class="card card-success">

### 3. Семантическая (ИИ)
- **Классификация поверхности:**
  - Асфальт / бетон: $\text{Cost} = 1.0$ (норма)
  - Трава / гравий: $\text{Cost} = 1.3$ (безопасно)
  - Лужи / песок / кусты: $\text{Cost} = 8.0$ (риск)
- Разметка, зоны пешеходов, ПДД
- **Критерий:** штрафы в целевой функции стоимости $J$

</div>

</div>

<div class="card" style="margin-top: 4px; padding: 10px 16px; background: #f8fafc; border-left: 4px solid #0284c7;">

💡 **Фундаментальный вывод:** Бинарного $\mathcal{C}_{\text{free}} / \mathcal{C}_{\text{obs}}$ недостаточно: геометрия допускает проезд, но террамеханика гарантирует пробуксовку колес, а семантика налагает запреты безопасности.

</div>

---

## 1. Профильная проходимость: Клиренс, углы и ступени <span class="badge badge-time">34–38 мин</span>

<div class="grid-2">

<div class="col">

<div class="card card-accent">

### Геометрические пороги проходимости:
- **Дорожный просвет ($h_{\text{clear}}$):** минимальный зазор между грунтом и нижней точкой шасси/дифференциала.
- **Угол въезда ($\alpha_{\text{app}}$) и съезда ($\alpha_{\text{dep}}$):** предельный наклон рампы без удара бампером или оборудованием.
- **Угол переката ($\beta_{\text{ramp}}$):** порог преодоления гребня без посадки на «брюхо» (*high-centering*).
- **Предельный вертикальный шаг:** $h \le h_{\text{step}} \approx 0.5 \cdot D_{\text{wheel}}$.
- **Сенсорный стек:** 3D LiDAR, стереокамеры $\rightarrow$ 2.5D Elevation Map (`elevation_mapping_cupy`) и GPU ESDF.

</div>

<div class="card" style="margin-top: 4px; padding: 8px 12px; background: #eff6ff; border-left: 3px solid #0284c7;">

💡 **Критерий:** ни одна точка шасси не входит в контакт с рельефом $\operatorname{dist}(p_{\text{robot}}, \mathcal{O}_{\text{terrain}}) > 0$.

</div>

</div>

<div class="col">

<div class="diagram-box">

<img src="../../assets/images/lecture-01/traversability_geometry.jpg" alt="Геометрическая проходимость планетохода" />

</div>

</div>

</div>

---

## 2. Опорная проходимость: Террамеханика Беккера–Вонга <span class="badge badge-time">38–41 мин</span>

<div class="grid-2">

<div class="col">

<div class="card card-alert">

### Взаимодействие колеса с грунтом:
- **Уравнение осадки Беккера ($z$ — глубина колеи):**
$$p(z) = \left( \frac{k_c}{b} + k_\phi \right) z^n$$
$b$ — ширина протектора, $k_c, k_\phi, n$ — модули грунта.
- **Сдвиговые напряжения Яна–Беккера:**
$$\tau(j) = (c + p \tan \phi)\left(1 - e^{-j/K}\right)$$
- **Буксование колеса (Slip ratio $s$):**
$$s = 1 - \frac{v_x}{r \cdot \omega}$$
При $s > 0.25$ колесо зарывается, сопротивление качению $R_c$ растет, вызывая застревание даже на ровном месте.

</div>

</div>

<div class="col">

<div class="diagram-box">

<img src="../../assets/images/lecture-01/traversability_terramechanics.jpg" alt="Террамеханика колесо-грунт" />

</div>

</div>

</div>

---

## 3. Семантическая проходимость: ИИ-сегментация и Costmap <span class="badge badge-time">41–45 мин</span>

<div class="grid-2">

<div class="col">

<div class="card card-success">

### Оценка проходимости нейросетями:
- **Семантическая сегментация (RGB + LiDAR):**
  - Асфальт / ровный бетон: $C_{\text{surf}} = 1.0$ (оптимально)
  - Стриженый газон / гравий: $C_{\text{surf}} = 1.3$ (допустимо)
  - Рыхлый песок / грязь / лужи: $C_{\text{surf}} = 8.0$ (высокий риск)
  - Разметка, зоны пешеходов, ПДД
- **Штрафы в целевой функции планирования:**
$$J = \int_0^T \left( C_{\text{semantic}}(x(t)) + \|\mathbf{u}(t)\|_R^2 \right) dt$$
- **SOTA подходы:** Self-Supervised Traversability (Wayve, ETH Zurich Rüegg et al., DINOv2 visual features).

</div>

</div>

<div class="col">

<div class="diagram-box">

<img src="../../assets/images/lecture-01/traversability_semantics.jpg" alt="Семантическая проходимость и разметка" />

</div>

</div>

</div>

---

## 4. Способы декомпозиции и репрезентации среды <span class="badge badge-time">45–60 мин</span>

<div class="grid-2">

<div class="card">

### 1. Сетки занятости (Occupancy Grids)

- 2D / 2.5D / 3D регулярные воксельные массивы.
- Каждая ячейка хранит логарифм шанса занятости:
$$L(m_i) = \log \frac{P(m_i)}{1 - P(m_i)}$$
- **Плюсы:** простота, прямой маппинг с лидара.
- **Минусы:** гигантский расход памяти $\mathcal{O}(N^3)$ на больших картах.

</div>

<div class="card card-accent">

### 2. Иерархические деревья (Octrees / VDB)

- **OctoMap / OpenVDB:** адаптивное разрешение.
- Пустые и сплошные области объединяются в крупные блоки.
- Разрешение детализируется только вблизи границ препятствий.
- **Экономия ОЗУ:** в 10–50 раз по сравнению с регулярной 3D-сеткой.

</div>

</div>

---

## Современные SOTA репрезентации (2024–2026) <span class="badge badge-time">45–60 мин</span>

<div class="grid-3">

<div class="card card-accent">

### nvblox (NVIDIA Isaac)

- GPU-ускоренное построение объемных карт на воксельных блоках.
- Мгновенный расчет TSDF (поверхности) и ESDF (поля расстояний) в реальном времени ($\ge 60$ fps).
- Интегрировано в ROS 2 Nav2.

</div>

<div class="card">

### wavemap (ETH Zürich ASL)

- Многомасштабное картирование на основе вейвлет-преобразования Хаара.
- Точная интеграция лучей лидара без артефактов дискретизации.
- Экстремально низкое потребление памяти при миллиметровом разрешении.

</div>

<div class="card card-success">

### elevation_mapping_cupy (ETH RSL)

- 2.5D карты высот рельефа на базе CuPy (CUDA C++).
- В реальном времени вычисляет слои: уклон, шероховатость, проходимость.
- Стандарт для шагающих роботов ANYmal.

</div>

</div>

---

## Поля расстояний: SDF, ESDF и градиенты <span class="badge badge-time">50–60 мин</span>

<div class="grid-2">

<div class="col">

<div class="card">

### Евклидово знаковое поле (ESDF)

Сопоставляет каждой точке пространства знаковое расстояние до ближайшего препятствия:

$$\operatorname{SDF}(x) = \begin{cases} -d(x, \partial \mathcal{O}), & x \in \mathcal{O} \\ +d(x, \partial \mathcal{O}), & x \in \mathcal{C}_{free} \end{cases}$$

**TSDF (Truncated):** обрезка диапазоном $[-\delta, +\delta]$ для быстрой 3D-реконструкции поверхностей.

</div>

</div>

<div class="col">

<div class="diagram-box">

<img src="../../assets/images/lecture-01/sdf_gradient.svg" alt="SDF и градиенты" />

</div>

<div class="card card-accent text-sm">

Градиент $\mathbf{n}(x) = \nabla \operatorname{ESDF}(x)$ задает направление наискорейшего удаления от стен, позволяя строить гладкие траектории в оптимизаторах CHOMP, TrajOpt и MPC.

</div>

</div>

</div>

---

## 5. Свойства алгоритмов: Полнота и Оптимальность <span class="badge badge-time">70–80 мин</span>

<div class="grid-2">

<div class="card">

### Свойства полноты (Completeness)

- **Полный (Complete):** находит решение за конечное время, если оно существует, или сообщает об отсутствии (графы видимости).
- **Вероятностно полный:**
$$\lim_{N \to \infty} P(\text{путь найден}) = 1$$
(RRT, PRM при бесконечном числе сэмплов).
- **Разрешающе полный:** находит решение при данном дискретном шаге сетки $\varepsilon$ ($A^*$, Дейкстра).

</div>

<div class="card card-accent">

### Свойства оптимальности (Optimality)

- **Оптимальный:** находит путь с минимальной стоимостью $J^*(Path)$.
- **Асимптотически оптимальный:**
$$P\left(\lim_{N \to \infty} \operatorname{Cost}(\tau_N) = c^*\right) = 1$$
($RRT^*$, $PRM^*$, Fast Marching). Базовый RRT не является асимптотически оптимальным!
- **Критерии качества:** длина пути, время проезда, расход батареи, максимальная кривизна $\max |\kappa|$.

</div>

</div>

---

## 6. Нейросетевые методы: Latent Space и World Models <span class="badge badge-time">80–90 мин</span>

<div class="grid-2">

<div class="card card-accent">

### Энкодеры и Latent Space

- Вместо вокселей нейросетевые автоэнкодеры сжимают лидарные облака и камеры в компактный вектор $z \in \mathbb{R}^k$:
$$z = \operatorname{Encoder}(I_{camera}, P_{lidar})$$
- Планирование ведется в латентном пространстве, где расстояние отражает семантическую проходимость.

</div>

<div class="card card-success">

### World Models (Модели мира, 2024–2026)

- Новейшая парадигма автономности (DreamerV3, GAIA-1, Sora для робототехники):
$$z_{t+1} \sim p(z_{t+1} \mid z_t, a_t)$$
- Робот «воображает» тысячи траекторий вперед в скрытом пространстве без физического риска (Latent Imagination Planning).

</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 01 | Заключение" -->

## Итоги вводной лекции и дорожная карта курса <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">

### Что мы узнали сегодня:

1. **Траектория** отличается от пути наличием временного профиля скорости и ускорений.
2. В $\mathcal{C}$-space робот становится точкой за счет раздутия препятствий через **сумму Минковского**.
3. **Проходимость** делится на профильную, опорную и семантическую.
4. **SOTA-репрезентации** (`nvblox`, `wavemap`) дают градиенты расстояний $\nabla \operatorname{ESDF}$ для гладкой оптимизации.

</div>

<div class="card card-accent">

### Программа следующих лекций:

- **Лекция 02:** Дискретное планирование на графах и сетках ($A^*$, $\text{Theta}^*$, CBS)
- **Лекция 03:** Сэмплирующие методы (PRM, RRT, $RRT^*$)
- **Лекция 04:** Реактивные и локальные методы (DWA, VO, TEB)
- **Лекция 05:** Оптимальное управление (ПМП, LQR, Коллокация)
- **Лекция 06:** Предиктивное управление (Linear MPC, NMPC, CBF)
- **Лекция 07:** Учёт ограничений (Неголономность, Скобки Ли, TOPP)
- **Лекция 08:** Вычислительные аспекты и архитектура Nav2

</div>

</div>
