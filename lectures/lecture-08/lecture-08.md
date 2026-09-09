---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 08"
footer: "Курс лекций • Лекция 08 • Слайд %PAGE% из %TOTAL%"
math: mathjax
---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 08: Вычислительные аспекты, инженерные компромиссы и архитектура Nav2

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Инженерия и архитектура</span>
  <span class="badge badge-purple">D* Lite • Multi-Rate • ROS 2 Nav2 • Behavior Trees • Sim-to-Real</span>
</div>

---

<!-- _header: "Лекция 08 | Введение и мотивация" -->

## Чему посвящена эта лекция? <span class="badge badge-blue">Инженерия и архитектура</span>

<div class="grid-2 mt-2">

<div class="card card-accent">
  <h3>🎯 От математических теорем к реальному железу</h3>
  <p class="text-sm">
    Алгоритмы $A^*$, RRT*, MPC и TVLQR безупречны на бумаге. Но когда вы запускаете их на бортовом компьютере реального робота (NVIDIA Jetson или x86 SoC), они сталкиваются с суровой инженерной реальностью: ограниченным бюджетом CPU, задержками сенсорных очередей, ложными препятствиями в облаках точек и системными сбоями.
  </p>
  <p class="text-sm">
    Эта лекция посвящена <strong>системной интеграции и вычислительной инженерии</strong>: как объединить разрозненные алгоритмы в промышленно надежный навигационный стек (ROS 2 Nav2) с гарантированным реальным временем.
  </p>
</div>

<div class="card">
  <h3>🔍 Ключевые вопросы лекции</h3>
  <ul class="text-sm">
    <li><strong>Многотактовость и задержки:</strong> Как связать контуры 1 Гц, 30 Гц и 1 кГц без рассинхронизации и отставания от датчиков?</li>
    <li><strong>Динамическое перепланирование:</strong> Алгоритм <strong>$D^*$ Lite</strong> (ETH / Koenig & Likhachev) и починка графа за миллисекунды.</li>
    <li><strong>Быстрые карты стоимости:</strong> Алгоритм Фельценшвальба для расчета Евклидова расстояния (<strong>EDT</strong>) за $\mathcal{O}(N)$ без сеточных волн.</li>
    <li><strong>Деревья поведения (Behavior Trees):</strong> Почему конечные автоматы (FSM) не масштабируются и как Nav2 управляет миссиями?</li>
    <li><strong>Отказоустойчивость:</strong> Иерархия аварийного восстановления (Recovery Behaviors) и преодоление разрыва <strong>Sim-to-Real</strong>.</li>
  </ul>
</div>

</div>

<div class="card card-success mt-2">
  <h3 style="margin-bottom: 4px;">💡 Чему вы научитесь за эти 90 минут</h3>
  <p class="text-sm" style="margin-bottom: 0;">
    Проектировать многотактовую архитектуру реального времени, настраивать слоеные карты стоимости Costmap 2D/3D с быстрым раздутием, описывать миссии автономного движения через XML Behavior Trees и строить отказоустойчивые промышленные AGV/AMR комплексы.
  </p>
</div>

---

<!-- _header: "Лекция 08 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Системы реального времени и алгоритмы (45 мин)</h3>
  <ul>
    <li><strong>00–12 мин:</strong> Инженерные компромиссы: точность vs частота, память vs скорость, распределение ядер CPU/GPU.</li>
    <li><strong>12–22 мин:</strong> Многотактовая архитектура (Multi-Rate System): компенсация аппаратной задержки сенсоров (Latency Prediction).</li>
    <li><strong>22–35 мин:</strong> Динамическое перепланирование: <strong>$D^*$ Lite</strong> (Koenig & Likhachev) — инкрементальный поиск с правыми частями $rhs(s)$.</li>
    <li><strong>35–45 мин:</strong> Быстрые алгоритмы раздутия: <strong>Euclidean Distance Transform (EDT)</strong> Фельценшвальба за $\mathcal{O}(W \times H)$.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Архитектура Nav2 и Надежность (45 мин)</h3>
  <ul>
    <li><strong>45–58 мин:</strong> Архитектура ROS 2 Nav2: асинхронные Action-серверы и <strong>Деревья Поведения (Behavior Trees)</strong>.</li>
    <li><strong>58–68 мин:</strong> Слоеные карты стоимости (Layered Costmaps): Static, Obstacle, Voxel, Inflation Layer.</li>
    <li><strong>68–78 мин:</strong> Отказоустойчивость: иерархия восстановления (Spin, Backup, Costmap Clearing, E-Stop).</li>
    <li><strong>78–90 мин:</strong> Преодоление <strong>Sim-to-Real</strong> (калибровка, задержки, шум). <strong>Итоги всего курса лекций</strong> и Q&A.</li>
  </ul>
</div>

</div>

<!--
Примечание для лектора:
Это финальная, венчающая лекция курса. Покажите студентам, как все концепции предыдущих 7 лекций (C-space, A*, RRT*, DWA, MPC, связи Ли) сходятся в единую стройную систему промышленного робота.
-->

---

## 1. Инженерные компромиссы в реальном роботе <span class="badge badge-time">00–12 мин</span>

<div class="grid-3">

<div class="card">
  <h3>1. Горизонт vs Частота</h3>
  <ul class="text-sm">
    <li><strong>Длинный горизонт:</strong> находит глобально оптимальные объезды, но требует сотен миллисекунд CPU.</li>
    <li><strong>Короткий горизонт:</strong> мгновенный пересчет ($> 50$ Гц), но риск упереться в локальный тупик.</li>
    <li><strong>Решение:</strong> разделение на глобальный ($1\text{--}2$ Гц) и локальный ($30\text{--}50$ Гц) контуры.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>2. Точность vs Память</h3>
  <ul class="text-sm">
    <li>Разрешение 1 см дает идеальную точность в дверных проемах, но взрывает память и кэш L3 процессора.</li>
    <li>Разрешение 10 см считается мгновенно, но сглаживает проходы и заставляет робота думать, что дверь заперта.</li>
    <li><strong>Решение:</strong> иерархические структуры (OctoMap, ESDF).</li>
  </ul>
</div>

<div class="card card-alert">
  <h3>3. Бюджет бортового SoC</h3>
  <ul class="text-sm">
    <li>На одноплатном компьютере (NVIDIA Jetson / x86) одновременно работают: SLAM, нейросети детекции людей и планировщик.</li>
    <li>Лимит на поток планирования: не более <strong>1–2 ядер CPU</strong> и <strong>$\le 30$ мс</strong> на цикл.</li>
    <li>Вынуждает использовать генерацию кода на C/C++ и lock-free структуры.</li>
  </ul>
</div>

</div>

---

## 2. Многотактовая архитектура и компенсация задержки <span class="badge badge-time">12–22 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Иерархия временных контуров (Multi-Rate):</h3>
    <div class="formula-box text-sm">
      $$\begin{array}{lcl}
      \text{Миссия (Behavior Tree)} &\sim 1\text{ Гц} &\Delta t = 1000\text{ мс} \\
      \text{Глобальный планировщик } (A^*) &\sim 1\text{--}2\text{ Гц} &\Delta t = 500\text{ мс} \\
      \text{Локальный планировщик / MPC} &\sim 20\text{--}50\text{ Гц} &\Delta t = 20\text{--}50\text{ мс} \\
      \text{Контроллер приводов (RTOS)} &\sim 500\text{--}1000\text{ Гц} &\Delta t = 1\text{--}2\text{ мс}
      \end{array}$$
    </div>
    <p class="text-sm">Потоки обмениваются данными асинхронно через кольцевые буферы без взаимных блокировок (Lock-free Ring Buffers).</p>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Проблема аппаратной задержки (Latency):</h3>
    <p class="text-sm">
      Пока лидар отсканировал точки ($20$ мс), фильтр SLAM обновил позу ($15$ мс), а MPC посчитал траекторию ($25$ мс), проходит суммарная задержка $\Delta t_{lat} = 60$ мс.
    </p>
    <p class="text-sm">Если робот мчится со скоростью $2$ м/с, он проезжает <strong>12 сантиметров "вслепую"</strong> до применения команды!</p>
    <div class="card-success text-sm mt-2">
      <strong>Решение (State Forward Prediction):</strong> MPC должен оптимизировать траекторию не от текущей замеренной позы $x(t)$, а от прогнозируемой позы на момент завершения расчета:
      $$x_{init}^{mpc} = x(t) + \int_{t}^{t + \Delta t_{lat}} f(x, u_{current}) dt$$
    </div>
  </div>
</div>

</div>

---

## 3. Динамическое перепланирование: Алгоритм $D^*$ Lite <span class="badge badge-time">22–35 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Идея инкрементального поиска (Koenig & Likhachev):</h3>
    <p class="text-sm">Пусть робот едет по найденному пути, и лидар обнаруживает новое препятствие. Полный перезапуск $A^*$ неэффективен!</p>
    <p class="text-sm"><strong>$D^*$ Lite</strong> выполняет поиск <em>в обратном направлении</em> (от цели к текущей позе) и поддерживает две оценки:</p>
    <ul class="text-sm">
      <li>$g(s)$ — текущая оценка стоимости пути от $s$ до $s_{goal}$.</li>
      <li>$rhs(s)$ — одношаговая упреждающая оценка через соседей:
        $$rhs(s) = \min_{s' \in \operatorname{Succ}(s)} \Big( c(s, s') + g(s') \Big)$$
      </li>
    </ul>
    <p class="text-sm">Узел называется <strong>локально согласованным</strong>, если $g(s) = rhs(s)$.</p>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Ремонт графа при обнаружении препятствия:</h3>
    <ul class="text-sm">
      <li>При обнаружении нового препятствия стоимость затронутых ребер $c(u, v)$ меняется на $\infty$.</li>
      <li>Только узлы с $g(u) \neq rhs(u)$ помещаются в приоритетную очередь <code>PriorityQueue</code> с составным ключом:
        $$k(s) = \Big[ \min(g, rhs) + h(s_{start}, s) + k_m, \;\; \min(g, rhs) \Big]$$
      </li>
      <li>Алгоритм быстро «раскручивает» только поврежденные ветви графа, не пересчитывая 95% оставшейся карты!</li>
    </ul>
    <div class="card-success text-sm mt-2">
      <strong>Скорость:</strong> $D^*$ Lite обновляет маршрут в 10–100 раз быстрее полного перезапуска $A^*$, обеспечивая бесшовное огибание внезапных препятствий.
    </div>
  </div>
</div>

</div>

---

## 4. Быстрое Евклидово Преобразование (EDT за $\mathcal{O}(N)$) <span class="badge badge-time">35–45 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-alert">
    <h3>Проблема наивного раздутия препятствий:</h3>
    <p class="text-sm">Для безопасного движения робота радиуса $R$ карту занятости нужно раздуть (Inflation). Волновой алгоритм Дейкстры (BFS) от каждого занятого пикселя работает крайне медленно:</p>
    $$\mathcal{O}(K \cdot N_{cells})$$
    <p class="text-sm">При карте склада $2000 \times 2000$ ячеек обновление занимает секунды, блокируя поток планировщика.</p>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Алгоритм Фельценшвальба (Felzenszwalb & Huttenlocher):</h3>
    <p class="text-sm">Точное преобразование евклидова расстояния (Squared Euclidean Distance Transform) вычисляется как нижняя огибающая парабол:</p>
    $$D_f(p) = \min_{q} \Big( (p - q)^2 + f(q) \Big)$$
    <ul class="text-sm">
      <li><strong>Свойство сепарабельности:</strong> 2D задача разделяется на два независимых 1D прохода — сначала по строкам матрицы, затем по столбцам!</li>
      <li>Каждый 1D проход выполняется за строго линейное время через стек пересечения парабол.</li>
      <li>Итоговая асимптотика: <strong>строго $\mathcal{O}(W \times H)$</strong>!</li>
    </ul>
    <div class="card-accent text-sm mt-2">
      Полная карта расстояний $2000 \times 2000$ рассчитывается за <strong>менее чем 5 миллисекунд</strong> на одном ядре CPU!
    </div>
  </div>
</div>

</div>

---

## 5. Архитектура ROS 2 Nav2: Деревья Поведения <span class="badge badge-time">45–58 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Почему Behavior Trees (BT) вытеснили FSM?</h3>
    <ul class="text-sm">
      <li><strong>Конечные автоматы (FSM):</strong> при росте числа состояний число переходов взрывается комбинаторно ($\mathcal{O}(N^2)$), порождая спагетти-код.</li>
      <li><strong>Behavior Trees (Nav2):</strong> дерево реактивных узлов, возвращающих <code>SUCCESS</code>, <code>FAILURE</code> или <code>RUNNING</code>. Высокая модульность и переиспользование.</li>
    </ul>
    <div class="card text-sm mt-2">
      <strong>Типы узлов:</strong>
      <ul>
        <li><code>Sequence (->)</code>: выполняет дочерние узлы по очереди, пока они успешны.</li>
        <li><code>Fallback (?)</code>: выполняет альтернативы, пока хотя бы одна не сработает (логика восстановления).</li>
      </ul>
    </div>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Пример фрагмента дерева Nav2:</h3>
    <pre><code>&lt;root main_tree_to_execute="MainTree"&gt;
  &lt;BehaviorTree ID="MainTree"&gt;
    &lt;RecoveryNode number_of_retries="3"&gt;
      &lt;PipelineSequence&gt;
        &lt;ComputePathToPose goal="{goal}" path="{path}"/&gt;
        &lt;FollowPath path="{path}" controller_id="FollowPath"/&gt;
      &lt;/PipelineSequence&gt;
      &lt;ReactiveFallback&gt;
        &lt;ClearEntireCostmap/&gt;
        &lt;Spin spin_dist="1.57"/&gt;
        &lt;BackUp backup_dist="0.3"/&gt;
      &lt;/ReactiveFallback&gt;
    &lt;/RecoveryNode&gt;
  &lt;/BehaviorTree&gt;
&lt;/root&gt;</code></pre>
  </div>
</div>

</div>

---

## 6. Слоеные карты стоимости (Layered Costmaps) <span class="badge badge-time">58–68 мин</span>

<div class="grid-2">

<div class="col">
  <p>В современных системах (Nav2 Costmap2D) карта не является плоским массивом. Она собирается из независимых <strong>плагинов-слоев</strong>:</p>

  <div class="card">
    <h3>Слои Costmap:</h3>
    <ol class="text-sm">
      <li><strong>Static Layer:</strong> постоянная карта стен здания из SLAM (черно-белая сетка).</li>
      <li><strong>Obstacle Layer / Voxel Layer:</strong> 2D/3D данные от лидаров и камер глубины (с рейкастингом для стирания исчезнувших препятствий).</li>
      <li><strong>Range Layer:</strong> конусы безопасности от сонаров и бамперов.</li>
      <li><strong>Inflation Layer:</strong> экспоненциальное раздутие стоимости вокруг препятствий:
        $$\operatorname{cost}(d) = 254 \cdot \exp\left( -\alpha (d - r_{inscribed}) \right)$$
      </li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Шкала стоимостей ячейки (0–255):</h3>
    <ul class="text-sm">
      <li><code>0 (FREE_SPACE)</code>: абсолютно свободная зона (нет штрафа).</li>
      <li><code>1–252</code>: зона градиента раздутия (поощряет планировщик держаться по центру коридора).</li>
      <li><code>253 (INSCRIBED)</code>: робот еще не касается препятствия, но вписанная окружность уже пересекает его — риск коллизии при развороте!</li>
      <li><code>254 (LETHAL)</code>: прямое геометрическое препятствие.</li>
      <li><code>255 (NO_INFORMATION)</code>: неисследованная область.</li>
    </ul>
  </div>
</div>

</div>

---

## 7. Отказоустойчивость: Иерархия восстановления <span class="badge badge-time">68–78 мин</span>

<div class="grid-2">

<div class="col">
  <p>Что делать, если глобальный путь заблокирован или локальный контроллер не может продвинуться вперед? Nav2 запускает <strong>эскалацию поведений восстановления (Recovery Behaviors)</strong>:</p>

  <div class="card">
    <h3>Каскад восстановления (Recovery Pipeline):</h3>
    <ol class="text-sm">
      <li><strong>1. Clear Stale Costmap:</strong> Очистка динамических препятствий за пределами локального радиуса (удаление артефактов призраков и шума лидара).</li>
      <li><strong>2. Wait (Пауза 1–3 с):</strong> Ожидание, пока пешеход или встречный погрузчик проедет сам.</li>
      <li><strong>3. Spin (Поворот на месте на 360°):</strong> Сенсорный осмотр окружения и обновление всех слоев карты.</li>
      <li><strong>4. BackUp (Откат назад на 30–50 см):</strong> Выезд из тупика по ранее проверенной свободной траектории.</li>
      <li><strong>5. E-Stop & Operator Alert:</strong> Если 3 попытки исчерпаны — безопасная остановка и вызов диспетчера.</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Принцип «Не навреди»:</h3>
    <ul class="text-sm">
      <li>Любое восстановительное действие (особенно BackUp) <strong>обязано производить непрерывную проверку коллизий</strong> сзади!</li>
      <li>Если сзади робота неожиданно встал человек — действие отката немедленно прерывается.</li>
    </ul>
    <div class="card-success text-sm mt-2">
      Использование Behavior Tree позволяет декларативно настраивать порядок и параметры восстановления без изменения единой строчки C++ кода.
    </div>
  </div>
</div>

</div>

---

## 8. Преодоление Sim-to-Real и Финал Курса <span class="badge badge-time">78–86 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Факторы расхождения Sim-to-Real:</h3>
    <ul class="text-sm">
      <li><strong>Террамеханика:</strong> идеальное трение в Gazebo vs переменный коэффициент $\mu$ (пыль, влажный бетон, ковры).</li>
      <li><strong>Датчики:</strong> идеальные лучи симулятора vs переотражения лидара от стекол и зеркальных поверхностей, слепые зоны камер.</li>
      <li><strong>Аппаратная задержка (Jitter):</strong> нерегулярные кванты времени операционной системы Linux без RT-Preempt патча.</li>
    </ul>
    <div class="card-success text-sm mt-2">
      <strong>Рецепт надежности:</strong> Domain Randomization (рандомизация массы и трения в симуляции), HIL-тестирование на реальном железе и аппаратный watchdog.
    </div>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Связующий мост всех 8 лекций курса:</h3>
    <div class="formula-box text-sm">
      $$\begin{array}{rcl}
      \text{Мир и проходимость} &\rightarrow &\text{Лекция 01} \\
      \text{Сетки, графы, Theta*, CBS} &\rightarrow &\text{Лекция 02} \\
      \text{Сэмплинг в C-space (RRT*)} &\rightarrow &\text{Лекция 03} \\
      \text{Реактивное уклонение (DWA)} &\rightarrow &\text{Лекция 04} \\
      \text{Оптимальное управление (LQR)} &\rightarrow &\text{Лекция 05} \\
      \text{Предиктивный горизонт (MPC)} &\rightarrow &\text{Лекция 06} \\
      \text{Связи Ли, трение и TOPP} &\rightarrow &\text{Лекция 07} \\
      \mathbf{\text{Инженерия и Nav2 BT}} &\rightarrow &\mathbf{\text{Лекция 08}}
      \end{array}$$
    </div>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 08 | Итоги и вопросы" -->

## Резюме лекции и завершение курса <span class="badge badge-time">86–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol class="text-sm">
    <li><strong>Многотактовая архитектура</strong> согласует разные частоты планирования и компенсирует сенсорные задержки упреждающим прогнозом состояния.</li>
    <li><strong>$D^*$ Lite</strong> пересчитывает только затронутые участки графа, решая задачу перепланирования за миллисекунды.</li>
    <li><strong>Алгоритм EDT</strong> строит карты расстояний за линейное время $\mathcal{O}(N)$ через разделение по осям.</li>
    <li><strong>ROS 2 Nav2 и Behavior Trees</strong> обеспечивают масштабируемость логики миссий и автоматическое восстановление при сбоях.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы курса:</h3>
  <ul class="text-sm">
    <li>Зачем локальному планировщику необходимо компенсировать аппаратную задержку (Latency Prediction)?</li>
    <li>В чем заключается ключевое отличие алгоритма $D^*$ Lite от полного перезапуска алгоритма $A^*$?</li>
    <li>Почему алгоритм вычисления EDT Фельценшвальба работает за строго линейное время $\mathcal{O}(N)$?</li>
    <li>Какую роль играют Recovery Behaviors в предотвращении тупиковых ситуаций автономного мобильного робота?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-green">Курс завершен! Желаем успехов в разработке автономных роботов! 🚀</span>
  </div>
</div>

</div>
