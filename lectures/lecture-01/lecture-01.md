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
## Лекция 01: Введение, конфигурационное пространство и дискретный поиск пути

<div class="mt-4">
  <span class="badge badge-blue">⏱️ Продолжительность: 90 минут</span>
  <span class="badge badge-green">Курс: Мобильная робототехника</span>
  <span class="badge badge-purple">Marp + Interactive Engine</span>
</div>

---

<!-- _header: "Лекция 01 | Структура занятия" -->

## Тайминг и структура лекции <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Теория и концепции (45 мин)</h3>
  <ul>
    <li><strong>00–15 мин:</strong> Мотивация, постановка задачи Motion Planning, иерархия стека навигации.</li>
    <li><strong>15–35 мин:</strong> Конфигурационное пространство ($\mathcal{C}$-space), Minkowski sum, препятствия.</li>
    <li><strong>35–45 мин:</strong> Дискретизация среды: сетки занятости (Occupancy Grid) и графы.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Алгоритмы и практика (45 мин)</h3>
  <ul>
    <li><strong>45–65 мин:</strong> Алгоритмы дискретного поиска: BFS, Dijkstra, $A^*$ и эвристики.</li>
    <li><strong>65–75 мин:</strong> <span class="badge badge-green">Интерактивный разбор</span> работы $A^*$ и сравнение эвристик.</li>
    <li><strong>75–85 мин:</strong> Практические ограничения: кинематика, углы поворота, сглаживание.</li>
    <li><strong>85–90 мин:</strong> Резюме, контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

<!-- 
Примечание для лектора (Speaker Note):
Держите темп! Первые 15 минут — погружение и мотивация, чтобы студенты поняли, почему просто "ехать по прямой" в робототехнике невозможно.
-->

---

## Проблема планирования движения в робототехнике <span class="badge badge-time">00–15 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Motion Planning</strong> — это фундаментальная задача нахождения допустимой траектории из начального состояния $q_{start}$ в целевое $q_{goal}$ в пространстве состояний при наличии препятствий и динамических ограничений.</p>

  <div class="card">
    <h3>Иерархия навигационного стека:</h3>
    <ol>
      <li><strong>Глобальный планировщик (Global Planner):</strong> находит геометрический путь на глобальной карте (A*, Dijkstra, RRT*).</li>
      <li><strong>Локальный планировщик (Local Planner / Trajectory Rollout):</strong> генерирует управляющие воздействия $(v, \omega)$ с учетом динамики и препятствий (DWA, TEB, MPC).</li>
      <li><strong>Контроллер приводов:</strong> отслеживание скоростей колес (PID).</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Ключевые вызовы для мобильных роботов:</h3>
    <ul>
      <li><strong>Неголономные связи:</strong> дифференциальный привод или модель Аккермана не могут двигаться боком:
        $$\dot{x} \sin\theta - \dot{y} \cos\theta = 0$$
      </li>
      <li><strong>Неполная информация:</strong> лидары и камеры имеют шум и ограниченную дальность.</li>
      <li><strong>Динамические препятствия:</strong> люди, другие роботы.</li>
      <li><strong>Требования реального времени:</strong> время цикла планирования $\le 50$ мс.</li>
    </ul>
  </div>
</div>

</div>

---

## Конфигурационное пространство ($\mathcal{C}$-space) <span class="badge badge-time">15–35 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Конфигурация $q$</strong> — минимальный набор независимых параметров, однозначно определяющий положение каждой точки робота $\mathcal{A}$ в пространстве $\mathcal{W} \subset \mathbb{R}^2$.</p>

  <div class="formula-box">
    $$\mathcal{C} = \mathcal{C}_{free} \cup \mathcal{C}_{obs}$$
    $$\mathcal{C}_{obs} = \{ q \in \mathcal{C} \mid \mathcal{A}(q) \cap \mathcal{O} \neq \emptyset \}$$
  </div>

  <p>Преобразование робота конечных размеров в <em>материальную точку</em> в $\mathcal{C}$-space достигается через <strong>сумму Минковского</strong>:</p>
  
  <div class="card">
    $$\mathcal{C}_{obs} = \mathcal{O} \oplus (-\mathcal{A}(0)) = \{ p + r \mid p \in \mathcal{O}, r \in -\mathcal{A}(0) \}$$
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Размерность $\mathcal{C}$-space для мобильных платформ:</h3>
    <ul>
      <li><strong>Круглый омни-робот:</strong> $\mathbb{R}^2$ — конфигурация $q = (x, y)^T$. Препятствия просто "раздуваются" на радиус робота $R$.</li>
      <li><strong>Дифференциальный робот прямоугольной формы:</strong> $SE(2) = \mathbb{R}^2 \times SO(2)$ — конфигурация $q = (x, y, \theta)^T$. Трехмерное пространство!</li>
      <li><strong>Робот с прицепом:</strong> $\mathbb{R}^2 \times S^1 \times S^1$ (4 измерения).</li>
    </ul>
  </div>

  <div class="card card-success">
    <strong>Инсайт:</strong> Раздувание карты (Inflation Layer в ROS Costmap2D) — это дискретное приближение суммы Минковского для круглого описанного радиуса.
  </div>
</div>

</div>

---

## Дискретизация пространства и графы поиска <span class="badge badge-time">35–45 мин</span>

<p>Для применения алгоритмов поиска непрерывное пространство $\mathcal{C}_{free}$ преобразуется в дискретный граф $G = (V, E)$:</p>

<div class="grid-3">

<div class="card">
  <h3>1. Регулярная сетка (Grid)</h3>
  <p>Пространство разбивается на ячейки (4- или 8-связность).</p>
  <ul>
    <li>Просто строить по данным лидара.</li>
    <li>Метрическая точность ограничена размером ячейки.</li>
    <li>Размер графа растет экспоненциально с размерностью $\mathcal{O}(N^d)$.</li>
  </ul>
</div>

<div class="card">
  <h3>2. Граф видимости (Visibility)</h3>
  <p>Вершины — вершины многоугольных препятствий.</p>
  <ul>
    <li>Гарантирует кратчайший путь в 2D.</li>
    <li>Путь проходит в опасной близости от углов (требует clearance margin).</li>
  </ul>
</div>

<div class="card">
  <h3>3. Диаграмма Вороного</h3>
  <p>Ребра равноудалены от ближайших препятствий.</p>
  <ul>
    <li>Максимально безопасный зазор (High Clearance).</li>
    <li>Путь длиннее оптимального по расстоянию.</li>
  </ul>
</div>

</div>

---

## Алгоритм $A^*$: Формулировка и Эвристики <span class="badge badge-time">45–65 мин</span>

<div class="grid-2">

<div class="col">
  <p>Алгоритм $A^*$ вычисляет функцию приоритета для каждой вершины $n \in V$:</p>

  <div class="formula-box">
    $$f(n) = g(n) + h(n)$$
  </div>

  <ul>
    <li>$g(n)$ — точная стоимость пути от стартовой вершины $s$ до $n$.</li>
    <li>$h(n)$ — эвристическая оценка оставшейся стоимости от $n$ до цели $g$.</li>
  </ul>

  <div class="card card-alert">
    <h3>Свойства эвристики $h(n)$:</h3>
    <ul>
      <li><strong>Допустимость (Admissibility):</strong> $h(n) \le h^*(n)$. Гарантирует нахождение оптимального пути!</li>
      <li><strong>Монотонность (Consistency):</strong> $h(n) \le c(n, n') + h(n')$. Устраняет необходимость повторного раскрытия вершин.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Выбор метрики эвристики на сетке:</h3>
    <ul>
      <li><strong>Манхэттенская (4-связность):</strong>
        $$h(n) = |x_n - x_g| + |y_n - y_g|$$
      </li>
      <li><strong>Диагональная / Octile (8-связность):</strong>
        $$h(n) = \Delta x + \Delta y + (\sqrt{2} - 2)\min(\Delta x, \Delta y)$$
      </li>
      <li><strong>Евклидова (для непрерывных переходов):</strong>
        $$h(n) = \sqrt{(x_n - x_g)^2 + (y_n - y_g)^2}$$
      </li>
      <li><strong>При $h(n) \equiv 0$:</strong> алгоритм вырождается в классический алгоритм Дейкстры (Uniform Cost Search).</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _header: "Интерактивная практика | Алгоритм A*" -->

## Интерактивная демонстрация: Дискретный поиск пути <span class="badge badge-green">⏱️ 65–75 мин</span>

<div class="interactive-container">
  <div class="interactive-header">
    <span><i class="interactive-dot"></i> Интерактивный симулятор: Сравнение A* и Дейкстры на 2D-сетке</span>
    <span>Кликните мышью для добавления препятствий | Перетаскивайте S и G</span>
  </div>
  <iframe src="../../widgets/astar-grid/index.html" class="interactive-frame"></iframe>
</div>

<!-- 
Инструкция для лектора:
1. Запустите сначала поиск с алгоритмом Дейкстры (h=0) и обратите внимание студентов на круговой фронт открытых вершин (Open Set).
2. Переключите на A* (Эвклид) и покажите направленный эллипсоидальный фронт к цели.
3. Нарисуйте U-образную стену и покажите, как A* упирается в тупик и возвращается к обходу.
-->

---

## От геометрического пути к реальному роботу <span class="badge badge-time">75–85 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Проблема кусочно-линейных траекторий:</h3>
    <ul>
      <li>Сетка $A^*$ генерирует изломы с углами $45^\circ$ и $90^\circ$.</li>
      <li>В точках излома кривизна $\kappa \to \infty$.</li>
      <li>Робот с неголономным шасси (или с ограничением на ускорение) вынужден полностью остановиться для смены курса.</li>
    </ul>
  </div>

  <div class="card">
    <h3>Методы сглаживания (Path Smoothing):</h3>
    <ol>
      <li><strong>Градиентная оптимизация (Gradient Descent):</strong>
        $$\min \sum w_s \|p_i - p_{orig}\|^2 + w_k \|p_{i-1} - 2p_i + p_{i+1}\|^2$$
      </li>
      <li><strong>Сплайны и кривые Безье:</strong> генерация траекторий с гладкостью $C^1$ или $C^2$.</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Кривые Дубинса и Ридса-Шеппа:</h3>
    <p>Для колесных роботов с минимальным радиусом поворота $R_{min}$ (модель автомобиля Car-like Robot):</p>
    <ul>
      <li>Траектории состоят из дуг окружностей максимальной кривизны ($L, R$) и прямолинейных отрезков ($S$).</li>
      <li><strong>Дубинс (только вперед):</strong> 6 базовых типов слов $\{LSL, RSR, LSR, RSL, LRL, RLR\}$.</li>
      <li><strong>Ридс-Шепп:</strong> допускает реверсивное движение (задний ход).</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 01 | Заключение" -->

## Итоги лекции и контрольные вопросы <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol>
    <li>Конфигурационное пространство ($\mathcal{C}$-space) превращает геометрию робота в точку, упрощая планирование.</li>
    <li>Сумма Минковского формализует процедуру раздутия препятствий.</li>
    <li>$A^*$ с допустимой и монотонной эвристикой гарантирует оптимальность при существенно меньшем числе раскрытых узлов, чем Дейкстра.</li>
    <li>Путь на сетке требует обязательного сглаживания и кинематической адаптации.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Вопросы для самопроверки:</h3>
  <ul>
    <li>Что произойдет с алгоритмом $A^*$, если эвристика $h(n)$ переоценивает реальную стоимость пути ($h(n) > h^*(n)$)?</li>
    <li>Почему для робота прямоугольной формы с дифференциальным приводом нельзя обойтись двумерным $\mathcal{C}$-space $(x, y)$?</li>
    <li>В чем различие между допустимой и согласованной (монотонной) эвристикой?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Выборочные алгоритмы (RRT, RRT*, PRM)</span>
  </div>
</div>

</div>
