---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 02"
footer: "Курс лекций • Лекция 02 • Слайд %PAGE% из %TOTAL%"
math: mathjax
---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 02: Дискретное планирование на графах и сетках

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Графы, Сетки и MAPF</span>
  <span class="badge badge-purple">Visibility • Voronoi • A* • Theta* • Space-Time • CBS</span>
</div>

---

<!-- _header: "Лекция 02 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Дорожные карты и поиск (45 мин)</h3>
  <ul>
    <li><strong>00–15 мин:</strong> Построение графов: простейшие алгоритмы графа видимости и диаграммы Вороного.</li>
    <li><strong>15–30 мин:</strong> Классический дискретный поиск: Дейкстра и $A^*$, допустимость и монотонность эвристик.</li>
    <li><strong>30–45 мин:</strong> Сглаженный поиск без привязки к ребрам сетки: <strong>$\text{Theta}^*$ (Any-Angle Planning)</strong> + <span class="badge badge-green">Интерактивный симулятор</span>.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Пространство-время, MAPF и ML (45 мин)</h3>
  <ul>
    <li><strong>45–60 мин:</strong> Динамические препятствия и задача MAPF (Vertex & Edge коллизии).</li>
    <li><strong>60–75 мин:</strong> <strong>Space-Time $A^*$</strong> (таблица резервирования) + <span class="badge badge-green">Интерактивный симулятор MAPF</span>. Ограничения масштабирования и алгоритм <strong>CBS (Conflict-Based Search)</strong>.</li>
    <li><strong>75–85 мин:</strong> Нейросети в графовых методах: Neural Heuristics ($Neural\text{ }A^*$) и отсечение поиска.</li>
    <li><strong>85–90 мин:</strong> Резюме, контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

<!-- 
Примечание лектору:
Лекция ведет от классических геометрических графов видимости к поиску на сетках, показывает переход от ступенчатого A* к гладкому Theta*, а во второй половине раскрывает 4D-планирование во времени (Space-Time A*) и индустриальный стандарт многоагентной навигации CBS.
-->

---

## 1. Граф видимости (Visibility Graph) <span class="badge badge-time">00–10 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Граф видимости $G_{vis} = (V, E)$</strong> — классический метод непрерывной дорожной карты для полигональных препятствий в 2D:</p>
  <ul>
    <li><strong>Вершины $V$:</strong> старт $q_{start}$, цель $q_{goal}$ и все невыпуклые углы препятствий (reflex vertices).</li>
    <li><strong>Ребра $E$:</strong> отрезки между парами вершин, полностью лежащие в $\mathcal{C}_{free}$ (прямая видимость).</li>
    <li><strong>Главное свойство:</strong> кратчайший путь на графе видимости является <em>глобально кратчайшим евклидовым путем</em> в 2D!</li>
  </ul>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Алгоритмы построения:</h3>
    <ol>
      <li><strong>Наивный перебор $\mathcal{O}(N^3)$:</strong>
        Для всех $\sim N^2$ пар вершин проверяем пересечение с каждым из $N$ ребер препятствий.
      </li>
      <li><strong>Радиальное заметание (Rotational Sweep) $\mathcal{O}(N^2 \log N)$:</strong>
        Вокруг каждой вершины запускается вращающийся луч, сортирующий ребра по углу (алгоритм Ли / Lee's algorithm).
      </li>
    </ol>
    <div class="card-alert mt-2">
      <strong>Недостаток:</strong> путь проходит строго по вершинам углов. Робот задевает препятствия (требуется предварительное раздутие $\mathcal{C}_{obs}$).
    </div>
  </div>
</div>

</div>

---

## 2. Диаграмма Вороного (Voronoi Diagram) <span class="badge badge-time">10–15 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Обобщенная диаграмма Вороного (GVD):</strong> множество точек пространства, равноудаленных как минимум от двух ближайших препятствий:</p>

  <div class="formula-box">
    $$\operatorname{GVD} = \{ q \in \mathcal{C}_{free} \mid \exists p_1 \in \mathcal{O}_i, p_2 \in \mathcal{O}_j, i \neq j: \|q - p_1\| = \|q - p_2\| = d(q, \mathcal{O}) \}$$
  </div>

  <ul>
    <li><strong>Преимущество:</strong> путь обеспечивает <em>максимально возможный запас безопасности (Clearance)</em>.</li>
    <li><strong>Недостаток:</strong> траектория длиннее геометрически кратчайшего пути; чувствительна к шуму формы препятствий.</li>
  </ul>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Алгоритмы построения GVD:</h3>
    <ul>
      <li><strong>Геометрический:</strong> Алгоритм Форчуна (Fortune's sweep-line) за $\mathcal{O}(N \log N)$ для точечных центров / полигонов. Ребра состоят из отрезков и парабол.</li>
      <li><strong>Сеточный (Brushfire / Wavefront):</strong>
        Одновременное распространение волнового фронта от всех ячеек препятствий на сетке за $\mathcal{O}(W \cdot H)$ — ячейки встречи фронтов образуют скелет Вороного.
    </ul>
    <p class="text-sm mt-2">Идеально подходит для навигации мобильных роботов в узких коридорах складов.</p>
  </div>
</div>

</div>

---

## 3. Алгоритмы Дейкстры и $A^*$ на сетках <span class="badge badge-time">15–30 мин</span>

<div class="grid-2">

<div class="col">
  <p>Поиск на регулярной сетке через очередь с приоритетом (Min-Heap):</p>

  <div class="formula-box">
    $$f(n) = g(n) + h(n)$$
  </div>

  <ul>
    <li>$g(n)$ — точная стоимость от старта до текущей ячейки $n$.</li>
    <li>$h(n)$ — эвристическая оценка оставшегося расстояния до цели $g$.</li>
    <li><strong>Дейкстра:</strong> $h(n) \equiv 0$. Равномерно перебирает узлы радиальным кругом во все стороны.</li>
  </ul>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Свойства эвристики $h(n)$:</h3>
    <ul>
      <li><strong>Допустимость (Admissibility):</strong>
        $$h(n) \le h^*(n) \quad \forall n$$
        Эвристика не завышает реальную стоимость $\implies$ гарантирует нахождение строго кратчайшего пути.
      </li>
      <li><strong>Монотонность / Согласованность (Consistency):</strong>
        $$h(n) \le c(n, n') + h(n')$$
        Неравенство треугольника $\implies$ при первом извлечении вершины из Open Set ее $g(n)$ уже минимальна (нет повторных раскрытий).
      </li>
    </ul>
  </div>
</div>

</div>

---

## 4. Сглаженный поиск: Алгоритм $\text{Theta}^*$ <span class="badge badge-time">30–45 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-alert">
    <h3>Проблема классического $A^*$ на сетке:</h3>
    <ul>
      <li>Путь жестко привязан к углам $45^\circ$ и $90^\circ$ (эффект оцифровки).</li>
      <li>В открытом поле без препятствий $A^*$ строит зигзагообразную «лесенку», хотя кратчайший путь — прямая линия.</li>
      <li>Пост-сглаживание не всегда исправляет топологические ошибки сетки.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Идея $\text{Theta}^*$ (Nash & Koenig, AAAI):</h3>
    <p>При раскрытии соседа $n'$ проверяется прямая видимость с <strong>родителем текущего узла</strong>:</p>
    $$\text{если } \operatorname{LineOfSight}(parent(n), n') == \text{True:}$$
    $$parent(n') = parent(n)$$
    $$g(n') = g(parent(n)) + c(parent(n), n')$$
    <ul>
      <li>Если прямая свободна, ребро срезает угол напрямую к прародителю!</li>
      <li>Результат: абсолютно прямые траектории под любыми углами без лесенок прямо во время поиска.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _header: "Интерактивная практика | A* vs Theta*" -->

## Интерактивный симулятор: Сравнение $A^*$, Дейкстры и $\text{Theta}^*$ <span class="badge badge-green">⏱️ 35–45 мин</span>

<div class="interactive-container">
  <div class="interactive-header">
    <span><i class="interactive-dot"></i> Any-Angle Pathfinding: Переключите A* (зигзаги) на Theta* (прямые линии)</span>
    <span>Рисуйте препятствия мышью | Сравните длину пути и число поворотов</span>
  </div>
  <iframe src="../../widgets/astar-grid/index.html" class="interactive-frame"></iframe>
</div>

<!-- 
Инструкция для лектора:
1. Запустите сначала поиск с алгоритмом A* (Эвклид) на пустом поле или лабиринте. Обратите внимание студентов на изломы под 45 градусов.
2. Переключите селектор алгоритма на Theta* и нажмите "Сброс" и "Запуск".
3. Покажите, как Theta* находит идеально ровный отрезок, соединяющий старт и цель напрямую, используя LineOfSight.
-->

---

## 5. Динамические препятствия и постановка MAPF <span class="badge badge-time">45–60 мин</span>

<div class="grid-2">

<div class="col">
  <p>Когда в пространстве перемещаются другие агенты, мы переходим в <strong>пространство-время $\mathcal{C} \times \mathcal{T}$</strong> с дискретными тактами $t \in \{0, 1, 2, \dots\}$.</p>
  <p><strong>Multi-Agent Path Finding (MAPF):</strong> найти набор непересекающихся траекторий для $k$ роботов:</p>
  $$\tau_i = (s_i^0, s_i^1, s_i^2, \dots, s_i^T), \quad s_i^0 = \text{Start}_i, \quad s_i^T = \text{Goal}_i$$
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Два фундаментальных типа коллизий агентов:</h3>
    <ol>
      <li><strong>Вершинное столкновение (Vertex Collision):</strong>
        Два робота пытаются занять одну и ту же клетку в один момент времени:
        $$s_i(t) = s_j(t)$$
      </li>
      <li><strong>Реберное / обменное столкновение (Edge / Swap Collision):</strong>
        Роботы движутся навстречу и меняются смежными клетками за один шаг:
        $$s_i(t) = s_j(t+1) \quad \land \quad s_i(t+1) = s_j(t)$$
      </li>
    </ol>
  </div>
</div>

</div>

---

## 6. Решение 1: Space-Time $A^*$ (Приоритетное планирование) <span class="badge badge-time">60–70 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Принцип Space-Time $A^*$ (Prioritized Planning):</h3>
    <ul>
      <li>Каждому роботу назначается приоритет: $R_1 > R_2 > \dots > R_k$.</li>
      <li>Ведется глобальная <strong>таблица резервирования (Reservation Table)</strong>:
        $$\operatorname{Table}[x, y, t] = \text{AgentID}$$
      </li>
      <li>Робот с высоким приоритетом планирует траекторию в $(x, y, t)$ и блокирует свои ячейки во времени.</li>
      <li>Следующий робот планирует в 3D $(x, y, t)$, обходя заблокированные точки как динамические стены и используя действие <strong>WAIT</strong> (ожидание на месте).</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Почему приоритетный Space-Time $A^*$ не масштабируется?</h3>
    <ul>
      <li><strong>Неполнота (Incomplete):</strong> робот с низким приоритетом может оказаться заперт в тупике роботами с более высоким приоритетом (Deadlock).</li>
      <li><strong>Субоптимальность:</strong> последовательный выбор не находит лучший суммарный компромисс.</li>
      <li><strong>Coupled A* (совместный поиск):</strong> объединение всех роботов в единое состояние размерности $(|V|)^k$ вызывает <em>экспоненциальный взрыв</em> при $k \ge 4$.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _header: "Интерактивная практика | Space-Time A* и MAPF" -->

## Интерактивный симулятор: Коллизии и Space-Time $A^*$ <span class="badge badge-green">⏱️ 65–75 мин</span>

<div class="interactive-container">
  <div class="interactive-header">
    <span><i class="interactive-dot"></i> Интерактивный MAPF: Нескоординированный A* (Коллизия) vs Space-Time A* (Wait-действие)</span>
    <span>Переключайте режим | Управляйте ползунком времени t</span>
  </div>
  <iframe src="../../widgets/mapf-spacetime/index.html" class="interactive-frame"></iframe>
</div>

<!-- 
Инструкция для лектора:
1. Включите режим "Нескоординированный A*" и нажмите Плей: на шаге t=5 возникнет красная коллизия в узком коридоре.
2. Переключите режим на "Space-Time A* (Резервирование времени)" и запустите заново: покажите, как Робот 2 берет действие WAIT (фиолетовый маркер), пропускает Робота 1, и оба благополучно доходят до целей!
-->

---

## Масштабируемый стандарт: Conflict-Based Search (CBS) <span class="badge badge-time">70–78 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Conflict-Based Search (Sharon et al., 2015)</strong> — индустриальный стандарт оптимального MAPF для сотен роботов на складах (Kiva / Amazon):</p>

  <div class="card">
    <h3>Двухуровневая архитектура:</h3>
    <ul>
      <li><strong>Нижний уровень (Low-Level):</strong> независимый поиск кратчайшего пути для одного робота с учетом набора персональных ограничений (Constraints: «робот $i$ не должен быть в клетке $v$ в момент $t$»).</li>
      <li><strong>Верхний уровень (High-Level):</strong> поиск по дереву конфликтов (Conflict Tree — CT).</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Как CBS разрешает конфликты:</h3>
    <ol>
      <li>На нижнем уровне строятся пути для всех агентов.</li>
      <li>Если обнаружен конфликт $(a_1, a_2, v, t)$, дерево ветвится на два узла:
        - <em>Ветвь 1:</em> агенту $a_1$ запрещается быть в $v$ в момент $t$.
        - <em>Ветвь 2:</em> агенту $a_2$ запрещается быть в $v$ в момент $t$.
      <li>Каждый узел перепланирует путь <strong>только для одного затронутого агента</strong>!</li>
    </ol>
    <p class="text-sm">Гарантирует глобальную оптимальность при масштабировании на сотни агентов.</p>
  </div>
</div>

</div>

---

## 7. Нейросети в графовом планировании <span class="badge badge-time">78–85 мин</span>

<p>В графовых алгоритмах глубокие нейросети применяются <strong>не для слепой замены классического поиска</strong>, а как интеллектуальные ускорители:</p>

<div class="grid-3">

<div class="card">
  <h3>1. Выученные эвристики (Neural Heuristics)</h3>
  <ul>
    <li>CNN / GNN обучаются предсказывать реальное расстояние $h_\theta(n) \approx h^*(n)$ с учетом сложного лабиринта стен.</li>
    <li><strong>Neural A* (Yonetani, 2021):</strong> дифференцируемый поиск $A^*$, ускоряющий сходимость в $5\text{--}20$ раз.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>2. Search Space Pruning (Отсечение)</h3>
  <ul>
    <li>Сеть сегментации (U-Net) по изображению карты предсказывает маску (Heatmap) наиболее вероятного коридора пути.</li>
    <li>$A^*$ ищет только внутри узкого коридора, отсекая $90\%$ пустых узлов графа.</li>
  </ul>
</div>

<div class="card card-success">
  <h3>3. Neural MAPF (PRIMAL)</h3>
  <ul>
    <li>Комбинация обучения с подкреплением (RL) и Imitation Learning для децентрализованного движения.</li>
    <li>Роботы учатся уступать дорогу в перекрестках без центрального сервера.</li>
  </ul>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 02 | Заключение" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol>
    <li>Графы видимости минимизируют длину в 2D, а диаграммы Вороного максимизируют безопасность (клиренс).</li>
    <li>Алгоритм $\text{Theta}^*$ решает проблему сетчатых ступенек через проверку прямой видимости LineOfSight.</li>
    <li>Space-Time $A^*$ решает задачу динамических препятствий через 4D-пространство $(x, y, t)$, но не масштабируется на большие флоты.</li>
    <li>CBS — оптимальный двухуровневый метод для масштабных складских систем MAPF.</li>
    <li>Нейросети выступают мощнейшими эвристиками, направляющими поиск.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы:</h3>
  <ul>
    <li>В чем различие между вершинной коллизией (Vertex) и обменной коллизией (Swap) в MAPF?</li>
    <li>Почему $\text{Theta}^*$ работает быстрее, чем запуск $A^*$ с последующим сплайн-сглаживанием?</li>
    <li>Как алгоритм CBS гарантирует оптимальность суммарного времени движения всех агентов?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Планирование, основанное на выборке (PRM, RRT, RRT*)</span>
  </div>
</div>

</div>
