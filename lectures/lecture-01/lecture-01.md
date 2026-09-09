---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 01"
footer: "Курс лекций • Лекция 01 • Слайд %PAGE% из %TOTAL%"
math: mathjax
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

<!-- _header: "Лекция 01 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Понятия, C-Space и Проходимость (45 мин)</h3>
  <ul>
    <li><strong>00–15 мин:</strong> Понятийный аппарат: Motion Planning, Path vs Trajectory. Локальное и глобальное планирование.</li>
    <li><strong>15–30 мин:</strong> Конфигурационное пространство ($\mathcal{C}$-space) и сумма Минковского.</li>
    <li><strong>30–45 мин:</strong> Проходимость среды: профильная (геометрическая), опорная (сцепление/грунт) и семантическая.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Репрезентации, Теория и World Models (45 мин)</h3>
  <ul>
    <li><strong>45–60 мин:</strong> Способы представления мира: Grids, Octree, <strong>SOTA: nvblox, wavemap, elevation_mapping_cupy</strong>. SDF/ESDF и градиенты.</li>
    <li><strong>60–70 мин:</strong> Графы видимости, Вороной, Lattice, аналитическое описание для Optimal Control.</li>
    <li><strong>70–80 мин:</strong> Свойства алгоритмов: полнота, оптимальность, асимптотическая оптимальность.</li>
    <li><strong>80–90 мин:</strong> Нейросетевые методы: Latent Spaces, <strong>World Models</strong> (неявная физика) и Q&A.</li>
  </ul>
</div>

</div>

<!-- 
Примечание для лектора:
Лекция формирует панорамный ментальный каркас всего курса. Дайте студентам единую систему координат: от классической суммы Минковского и дискретных вокселей до новейших ESDF на GPU и нейросетевых моделей мира (World Models).
-->

---

## 1. Понятийный аппарат: Путь, Траектория, Движение <span class="badge badge-time">00–15 мин</span>

<div class="grid-3">

<div class="card">
  <h3>1. Путь (Path)</h3>
  <div class="formula-box" style="margin: 8px 0; padding: 6px;">
    $$\sigma: [0, 1] \to \mathcal{C}_{free}$$
  </div>
  <ul>
    <li>Чисто <strong>геометрическая кривая</strong> в пространстве.</li>
    <li>Параметризована длиной дуги $s$.</li>
    <li><strong>Не содержит времени</strong>, скоростей и ускорений.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>2. Траектория (Trajectory)</h3>
  <div class="formula-box" style="margin: 8px 0; padding: 6px;">
    $$\tau: [0, T] \to \mathcal{X}_{free}$$
  </div>
  <ul>
    <li>Путь с <strong>временной параметризацией</strong>: $x(t), v(t), a(t)$.</li>
    <li>Учитывает кинематические и динамические возможности приводов.</li>
  </ul>
</div>

<div class="card card-success">
  <h3>3. Motion Planning</h3>
  <p>Комплексная задача синтеза управлений $u(t)$ и состояний $x(t)$:</p>
  $$\dot{x}(t) = f(x(t), u(t))$$
  <p>переводящих систему из $x_0$ в $x_{goal}$ без коллизий и нарушения физических ограничений.</p>
</div>

</div>

---

## Локальное vs Глобальное планирование <span class="badge badge-time">00–15 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Глобальное планирование (Global Planner)</h3>
  <ul>
    <li><strong>Входные данные:</strong> глобальная априорная карта окружения (SLAM / CAD / OSM).</li>
    <li><strong>Горизонт:</strong> от текущей точки до финишной цели миссии (десятки/сотни метров).</li>
    <li><strong>Частота работы:</strong> низкая ($\sim 0.2\text{--}2$ Гц) или разово по запросу.</li>
    <li><strong>Результат:</strong> глобальный геометрический путь без учета микродинамики.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Локальное планирование (Local Planner / Controller)</h3>
  <ul>
    <li><strong>Входные данные:</strong> поток локальных сенсоров в реальном времени (лидары, камеры глубины, радары).</li>
    <li><strong>Горизонт:</strong> короткий горизонт безопасности ($2\text{--}8$ метров вперед, $1\text{--}3$ секунды).</li>
    <li><strong>Частота работы:</strong> высокая ($\mathbf{20\text{--}100}$ <strong>Гц</strong>).</li>
    <li><strong>Результат:</strong> команды приводов $(v, \omega)$, парирующие внезапные препятствия и снос.</li>
  </ul>
</div>

</div>

---

## 2. Конфигурационное пространство ($\mathcal{C}$-space) <span class="badge badge-time">15–30 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Конфигурация $q \in \mathcal{C}$</strong> — минимальный набор независимых координат, однозначно определяющий положение каждой точки робота $\mathcal{A}$ в рабочем пространстве $\mathcal{W} \subset \mathbb{R}^d$.</p>

  <div class="formula-box">
    $$\mathcal{C} = \mathcal{C}_{free} \cup \mathcal{C}_{obs}$$
    $$\mathcal{C}_{obs} = \{ q \in \mathcal{C} \mid \mathcal{A}(q) \cap \mathcal{O} \neq \emptyset \}$$
  </div>

  <p>В $\mathcal{C}$-space робот сложной формы сжимается в <strong>материальную точку $q$</strong>.</p>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Сумма Минковского для трансляций:</h3>
    $$\mathcal{C}_{obs} = \mathcal{O} \oplus (-\mathcal{A}(0)) = \{ p - a \mid p \in \mathcal{O}, a \in \mathcal{A}(0) \}$$
    <ul>
      <li>Для круглого робота радиуса $R$: препятствия раздуваются наружу на $R$.</li>
      <li>Для некруглого робота на плоскости: пространство трехмерно $SE(2) = \mathbb{R}^2 \times SO(2)$, $q = (x, y, \theta)^T$.</li>
      <li>При изменении угла $\theta$ срез $\mathcal{C}_{obs}(\theta)$ непрерывно деформируется!</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _header: "Интерактивная практика | Сумма Минковского" -->

## Интерактивный симулятор: Формирование $\mathcal{C}_{obs}$ <span class="badge badge-green">⏱️ 20–30 мин</span>

<div class="interactive-container">
  <div class="interactive-header">
    <span><i class="interactive-dot"></i> Интерактивная сумма Минковского: Робот A(q) + Препятствие O &rarr; C_obs</span>
    <span>Перетаскивайте робота мышью | Вращайте угол &theta; ползунком</span>
  </div>
  <iframe src="../../widgets/cspace-minkowski/index.html" class="interactive-frame"></iframe>
</div>

---

## 3. Проходимость среды (Traversability Analysis) <span class="badge badge-time">30–45 мин</span>

<p>В реальной мобильной робототехнике бинарного разделения на «свободно / занято» недостаточно. Вводится <strong>проходимость (Traversability)</strong>:</p>

<div class="grid-3">

<div class="card">
  <h3>1. Профильная (Геометрическая)</h3>
  <ul>
    <li>Клиренс шасси (высота дорожного просвета).</li>
    <li>Углы въезда, съезда и продольной проходимости (Approach / Departure / Ramp breakover angles).</li>
    <li>Предельный шаг вертикального уступа ($h \le h_{step}$).</li>
    <li>Уклон рельефа: $|\nabla z| \le \tan(\alpha_{max})$ (защита от опрокидывания).</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>2. Опорная проходимость</h3>
  <ul>
    <li>Взаимодействие движителя с грунтом (Terramechanics).</li>
    <li>Несущая способность и плотность грунта (провал колес).</li>
    <li>Коэффициент сцепления $\mu$ (лед, мокрая трава, сыпучий песок).</li>
    <li>Оценка сопротивления качению и вероятности пробуксовки (Wheel slip).</li>
  </ul>
</div>

<div class="card card-success">
  <h3>3. Семантическая</h3>
  <ul>
    <li>Придание стоимости типам поверхности через нейросети:
      - Асфальт $\to$ Cost 1.0
      - Низкая трава $\to$ Cost 1.2 (можно ехать)
      - Глубокие лужи $\to$ Cost 8.0 (риск)
      - Проезжая часть $\to$ спецправила ПДД.
    </ul>
  </div>
</div>

</div>

---

## 4. Способы декомпозиции и репрезентации среды <span class="badge badge-time">45–60 мин</span>

<p>Качество и скорость планирования на 80% определяются выбранной моделью представления пространства:</p>

<div class="grid-2">

<div class="card">
  <h3>1. Сетки занятости (Occupancy Grids)</h3>
  <ul>
    <li>2D / 2.5D / 3D регулярные воксельные массивы.</li>
    <li>Каждая ячейка хранит логарифм шанса занятости $L(m_i) = \log \frac{P(m_i)}{1 - P(m_i)}$.</li>
    <li><em>Плюсы:</em> простота, прямой маппинг с лидара.</li>
    <li><em>Минусы:</em> гигантский расход памяти $\mathcal{O}(N^3)$ на больших картах.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>2. Иерархические деревья (Octrees / VDB)</h3>
  <ul>
    <li><strong>OctoMap / OpenVDB:</strong> адаптивное разрешение.</li>
    <li>Пустые и сплошные области объединяются в крупные блоки.</li>
    <li>Разрешение детализируется только вблизи границ препятствий.</li>
    <li>Экономия ОЗУ в 10–50 раз по сравнению с регулярной 3D-сеткой.</li>
  </ul>
</div>

</div>

---

## Современные SOTA репрезентации (2024–2026) <span class="badge badge-time">45–60 мин</span>

<div class="grid-3">

<div class="card card-accent">
  <h3>nvblox (NVIDIA Isaac)</h3>
  <ul>
    <li>GPU-ускоренное построение объемных карт на воксельных блоках.</li>
    <li>Мгновенный расчет <strong>TSDF</strong> (поверхности) и <strong>ESDF</strong> (поля расстояний) в реальном времени ($\ge 60$ fps).</li>
    <li>Интегрировано в ROS 2 Nav2 для мобильных роботов.</li>
  </ul>
</div>

<div class="card card-success">
  <h3>wavemap (ETH Zürich ASL)</h3>
  <ul>
    <li>Многомасштабное картирование на основе вейвлет-преобразования Хаара.</li>
    <li>Точная интеграция лучей лидара без артефактов дискретизации.</li>
    <li>Экстремально низкое потребление памяти при миллиметровом разрешении.</li>
  </ul>
</div>

<div class="card">
  <h3>elevation_mapping_cupy (ETH RSL)</h3>
  <ul>
    <li>2.5D карты высот рельефа на базе CuPy (CUDA Python/C++).</li>
    <li>В реальном времени вычисляет слои: уклон, шероховатость, проходимость (Traversability filter).</li>
    <li>Стандарт для четвероногих роботов (ANYmal) и тяжелых колесных платформ.</li>
  </ul>
</div>

</div>

---

## Поля расстояний: SDF, TSDF и градиенты для планирования <span class="badge badge-time">50–60 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Signed Distance Field (SDF / ESDF)</strong> сопоставляет каждой точке пространства знаковое расстояние до ближайшего препятствия:</p>

  <div class="formula-box">
    $$\operatorname{SDF}(x) = \begin{cases} -d(x, \partial \mathcal{O}), & x \in \mathcal{O} \\ 0, & x \in \partial \mathcal{O} \\ +d(x, \partial \mathcal{O}), & x \in \mathcal{C}_{free} \end{cases}$$
  </div>

  <ul>
    <li><strong>TSDF (Truncated):</strong> значения обрезаются диапазоном $[-\delta, +\delta]$ для быстрой 3D-реконструкции.</li>
    <li><strong>ESDF (Euclidean):</strong> точные метрические расстояния в свободном пространстве для планировщика.</li>
  </ul>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Главная ценность SDF: Непрерывный градиент!</h3>
    <p>Градиент поля расстояний указывает направление <strong>наискорейшего удаления от препятствия</strong>:</p>
    $$\mathbf{n}(x) = \nabla \operatorname{ESDF}(x), \quad \|\nabla \operatorname{ESDF}(x)\| = 1$$
    <ul>
      <li>Позволяет формулировать гладкие силы отталкивания в оптимизаторах траекторий (CHOMP, TrajOpt, MPC).</li>
      <li>Исключает дискретный поиск при локальном уклонении.</li>
    </ul>
  </div>
</div>

</div>

---

## Другие парадигмы описания среды <span class="badge badge-time">60–70 мин</span>

<div class="grid-3">

<div class="card">
  <h3>Графы видимости и Вороной</h3>
  <ul>
    <li><strong>Visibility Graph:</strong> ребра соединяют вершины полигонов. Дает кратчайший путь.</li>
    <li><strong>Диаграмма Вороного:</strong> ребра равноудалены от препятствий (максимальный клиренс).</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Lattice & Sampling</h3>
  <ul>
    <li><strong>Lattice:</strong> граф строится из кинематически допустимых примитивов движения (Motion Primitives).</li>
    <li><strong>Sampling-based:</strong> мир опрашивается точечными запросами коллизий без построения явной геометрии.</li>
  </ul>
</div>

<div class="card card-success">
  <h3>Аналитическое описание</h3>
  <ul>
    <li>Препятствия описываются системами нелинейных неравенств:
      $$g_i(x) \le 0$$
    <li>Или выпуклыми политопами:
      $$A_k x \le b_k$$
    <li>Прямой ввод в солверы Optimal Control / QP / NLP.</li>
  </ul>
</div>

</div>

---

## 5. Свойства алгоритмов: Полнота и Оптимальность <span class="badge badge-time">70–80 мин</span>

<div class="grid-2">

<div class="card card-accent">
  <h3>Свойства полноты (Completeness)</h3>
  <ul>
    <li><strong>Полный (Complete):</strong> находит решение за конечное время, если оно существует, или корректно сообщает о его отсутствии (графы видимости, cell decomposition).</li>
    <li><strong>Вероятностно полный (Probabilistically Complete):</strong>
      $$\lim_{N \to \infty} P(\text{нахождение пути}) = 1$$
      (RRT, PRM при бесконечном сэмплинге).
    </li>
    <li><strong>Разрешающе полный (Resolution Complete):</strong> находит решение, если оно существует при данном шаге сетки $\varepsilon$ ($A^*$, Dijkstra).</li>
  </ul>
</div>

<div class="card card-success">
  <h3>Свойства оптимальности (Optimality)</h3>
  <ul>
    <li><strong>Оптимальный:</strong> находит путь с минимальной стоимостью $J^*(Path)$.</li>
    <li><strong>Асимптотически оптимальный:</strong>
      $$P\left(\lim_{N \to \infty} \operatorname{Cost}(\tau_N) = c^*\right) = 1$$
      (RRT*, PRM*, Fast Marching). Базовый RRT <em>не является</em> асимптотически оптимальным!
    </li>
    <li><strong>Критерии качества:</strong> длина пути, время проезда, расход энергии батареи, максимальная кривизна $\max |\kappa|$, клиренс до стен.</li>
  </ul>
</div>

</div>

---

## 6. Нейросетевые методы: Latent Space и World Models <span class="badge badge-time">80–90 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Энкодеры и Latent Space:</h3>
    <ul>
      <li>Вместо громадных воксельных карт нейросетевые автоэнкодеры сжимают облака точек и изображения в компактный вектор признаков $z \in \mathbb{R}^k$:
        $$z = \operatorname{Encoder}(I_{camera}, P_{lidar})$$
      </li>
      <li>Планирование ведется в <strong>скрытом пространстве (Latent Space)</strong>, где метрика отражает семантическую сложность проезда.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>World Models (Модели мира, 2024–2026):</h3>
    <p>Новейшая парадигма автономности (DreamerV3, DayDreamer, GAIA-1, Sora для робототехники):</p>
    <ul>
      <li>Сеть учится <strong>неявно предсказывать физику мира</strong>:
        $$z_{t+1} \sim p(z_{t+1} \mid z_t, a_t)$$
      </li>
      <li>Робот может «воображать» тысячи траекторий вперед в латентном пространстве без физического риска, выбирая оптимальное действие (Latent Imagination Planning).</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 01 | Заключение" -->

## Итоги вводной лекции и дорожная карта курса <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Что мы узнали сегодня:</h3>
  <ol>
    <li>Траектория отличается от пути наличием временного профиля скорости и ускорений.</li>
    <li>В $\mathcal{C}$-space робот становится точкой за счет раздутия препятствий через сумму Минковского.</li>
    <li>Проходимость делится на профильную, опорную и семантическую.</li>
    <li>SOTA-репрезентации (nvblox, wavemap) дают градиенты для гладкой оптимизации.</li>
    <li>Будущее планирования объединяет строгие гарантии безопасности с нейросетевыми World Models.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Структура следующих лекций курса:</h3>
  <ul class="text-sm">
    <li><strong>Лекция 02:</strong> Дискретное планирование на графах и сетках ($A^*$, $D^*$)</li>
    <li><strong>Лекция 03:</strong> Сэмплирующие методы (PRM, RRT, RRT*)</li>
    <li><strong>Лекция 04:</strong> Реактивные и локальные методы (APF, DWA, TEB)</li>
    <li><strong>Лекция 05:</strong> Оптимальное управление (LQR, Direct Collocation)</li>
    <li><strong>Лекция 06:</strong> Предиктивное управление (MPC / NMPC)</li>
    <li><strong>Лекция 07:</strong> Учёт ограничений (Неголономность, скобки Ли, TOPP)</li>
    <li><strong>Лекция 08:</strong> Вычислительные аспекты и инженерные компромиссы</li>
  </ul>
</div>

</div>
