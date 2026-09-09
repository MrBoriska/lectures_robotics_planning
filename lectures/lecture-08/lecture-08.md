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
## Лекция 08: Вычислительные аспекты и инженерные компромиссы

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Инженерия и архитектура</span>
  <span class="badge badge-purple">Real-Time • Nav2 • Behavior Trees • Sim-to-Real</span>
</div>

---

<!-- _header: "Лекция 08 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Блок 1: Real-Time и структуры данных (45 мин)</h3>
  <ul>
    <li><strong>00–15 мин:</strong> Инженерные компромиссы: горизонт vs частота, бюджет вычислений на бортовом компьютере (SoC).</li>
    <li><strong>15–30 мин:</strong> Многотактовая архитектура (Multi-rate): планирование на 1 Гц, 30 Гц и 1 кГц. Компенсация задержки (Latency).</li>
    <li><strong>30–45 мин:</strong> Пространственные структуры данных: $k$-d tree, BVH, быстрое преобразование евклидова расстояния (EDT).</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Блок 2: Навигационный стек и надежность (45 мин)</h3>
  <ul>
    <li><strong>45–65 мин:</strong> Архитектура ROS 2 Nav2: Деревья поведения (Behavior Trees) и отказоустойчивость.</li>
    <li><strong>65–75 мин:</strong> Восстановительные поведения (Recovery Behaviors: Spin, Backup, Costmap clearing).</li>
    <li><strong>75–85 мин:</strong> Sim-to-Real перенос, валидация безопасности и физические аварийные контуры.</li>
    <li><strong>85–90 мин:</strong> Итоги курса, будущее мобильной автономности и Q&A.</li>
  </ul>
</div>

</div>

---

## 1. Инженерные компромиссы в реальном роботе <span class="badge badge-time">00–15 мин</span>

<div class="grid-3">

<div class="card">
  <h3>Горизонт vs Частота</h3>
  <ul>
    <li><strong>Длинный горизонт:</strong> позволяет находить глобально оптимальные маневры, но требует экспоненциально больше CPU.</li>
    <li><strong>Короткий горизонт:</strong> быстрый пересчет, но риск застрять в локальной ловушке.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Точность vs Скорость</h3>
  <ul>
    <li>Сеточные воксели 1 см дают ювелирную точность, но перегружают память.</li>
    <li>Воксели 10 см считаются мгновенно, но робот не помещается в узкие дверные проемы.</li>
  </ul>
</div>

<div class="card card-alert">
  <h3>Бюджет бортового SoC</h3>
  <ul>
    <li>SLAM, нейросети детекции людей и планировщик делят одну плату (NVIDIA Jetson / x86).</li>
    <li>Лимит на поток планирования: не более <strong>1–2 ядер CPU</strong> и <strong>$\le 30$ мс</strong> на цикл.</li>
  </ul>
</div>

</div>

---

## 2. Многотактовая архитектура (Multi-Rate System) <span class="badge badge-time">15–30 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Иерархия временных масштабов:</h3>
    <ol>
      <li><strong>Уровень миссии ($\sim 0.1\text{--}1$ Гц):</strong> логика поведения, выбор целей (Behavior Tree).</li>
      <li><strong>Глобальный планировщик ($\sim 1\text{--}2$ Гц):</strong> геометрический путь в глобальной статической карте.</li>
      <li><strong>Локальный планировщик / MPC ($\sim 20\text{--}50$ Гц):</strong> оптимизация траектории и обход динамических препятствий.</li>
      <li><strong>Контроллер приводов ($\sim 500\text{--}1000$ Гц):</strong> контур токов и скоростей двигателей в реальном времени (RTOS / Microcontroller).</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Компенсация задержки (Latency Compensation):</h3>
    <p>Время от момента съемки кадра сенсором до подачи тока на мотор составляет $\tau_{delay} \approx 40\text{--}100$ мс!</p>
    <ul>
      <li>За это время на скорости $2$ м/с робот проезжает $20$ см «вслепую».</li>
      <li><strong>Решение:</strong> планирование стартует не из текущего положения $x(t)$, а из <em>прогнозируемого состояния</em> на шаг вперед:
        $$\hat{x}(t + \tau_{delay}) = x(t) + \int_t^{t+\tau_{delay}} f(x(\tau), u(\tau)) \, d\tau$$
      </li>
    </ul>
  </div>
</div>

</div>

---

## 3. Быстрые алгоритмы для карт: Алгоритм EDT <span class="badge badge-time">30–45 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Евклидово преобразование расстояний (EDT):</h3>
    <ul>
      <li>Вычисляет расстояние до ближайшего препятствия для всех ячеек сетки $N \times M$.</li>
      <li>Наивный перебор: $\mathcal{O}((N \cdot M)^2)$ — недопустимо медленно.</li>
      <li><strong>Алгоритм Фельзеншвальба (Felzenszwalb & Huttenlocher):</strong>
        Разделение по осям $X$ и $Y$ с поиском нижней огибающей парабол за <strong>$\mathcal{O}(N \cdot M)$ — строго линейное время!</strong>
      </li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Пространственные индексы (Spatial Query):</h3>
    <table>
      <thead>
        <tr>
          <th>Структура</th>
          <th>Поиск соседа</th>
          <th>Динамическое обновление</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Массив (Brute-force)</strong></td>
          <td>$\mathcal{O}(N)$</td>
          <td>$\mathcal{O}(1)$</td>
        </tr>
        <tr>
          <td><strong>$k$-d Tree</strong></td>
          <td>$\mathcal{O}(\log N)$</td>
          <td>$\mathcal{O}(N \log N)$ перебалансировка</td>
        </tr>
        <tr>
          <td><strong>Voxel Hashing / BVH</strong></td>
          <td>$\mathcal{O}(1)$ среднее</td>
          <td>$\mathcal{O}(1)$</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

</div>

---

## 4. Архитектура ROS 2 Nav2 и Деревья поведения (BT) <span class="badge badge-time">45–65 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Behavior Trees (Деревья поведения):</h3>
    <p>Пришли на смену конечным автоматам (FSM) благодаря модульности, реактивности и масштабируемости.</p>
    <ul>
      <li>Узлы: <code>Sequence</code> $\to$, <code>Fallback</code> ?, <code>Parallel</code> $\rightrightarrows$, <code>Decorator</code>.</li>
      <li>Состояния возврата: <code>SUCCESS</code>, <code>FAILURE</code>, <code>RUNNING</code>.</li>
      <li>Позволяют описывать сложные протоколы: «Спланируй глобальный путь $\to$ если контроллер застрял $\to$ запусти расчистку карты $\to$ повтори попытку».</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Пайплайн Nav2 в ROS 2:</h3>
    <ul>
      <li><code>nav2_bt_navigator</code> — центральный дирижер навигационной задачи.</li>
      <li><code>nav2_planner</code> — плагины глобального пути (Smac Planner, NavFn).</li>
      <li><code>nav2_controller</code> — локальные плагины траекторий (DWB, TEB, MPPI).</li>
      <li><code>nav2_costmap_2d</code> — многослойные карты занятости на базе плагинов.</li>
    </ul>
  </div>
</div>

</div>

---

## 5. Восстановительные поведения (Recovery Behaviors) <span class="badge badge-time">65–75 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-alert">
    <h3>Когда алгоритмы планирования пасуют:</h3>
    <ul>
      <li>Внезапное препятствие окружило робота со всех сторон (лифт, толпа).</li>
      <li>Одометрия накопила ошибку, и робот «по карте» оказался внутри стены.</li>
      <li>Планировщик возвращает статус <code>NO_PATH_FOUND</code>.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Каскад восстановления (Recovery Pipeline):</h3>
    <ol>
      <li><strong>Очистка временных слоев карты (Clear Costmap):</strong> удаление фантомных препятствий, зафиксированных лидаром из-за шума или пыли.</li>
      <li><strong>Вращение на месте (Spin Recovery):</strong> поворот на $360^\circ$ для актуализации 3D-данных вокруг робота.</li>
      <li><strong>Откат назад (Wait & Back-up):</strong> отъезд по своей же безопасной колее на 0.5–1.0 м назад.</li>
      <li><strong>Аварийный вызов оператора:</strong> безопасная остановка и запрос помощи.</li>
    </ol>
  </div>
</div>

</div>

---

## 6. Sim-to-Real перенос и безопасность <span class="badge badge-time">75–85 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Преодоление разрыва реальности (Sim-to-Real Gap):</h3>
    <ul>
      <li><strong>Рандомизация домена (Domain Randomization):</strong> рандомизация коэффициентов трения колес ($\mu \in [0.4, 0.9]$), массы груза и задержек в Isaac Sim.</li>
      <li><strong>Моделирование шума сенсоров:</strong> добавление гауссова шума дальностей и выпадения лучей лидара.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Аппаратные барьеры безопасности (Safety Interlocks):</h3>
    <ul>
      <li>Планировщик — это программный код, который может зависнуть.</li>
      <li><strong>Watchdog Timer:</strong> если за 100 мс новая команда <code>/cmd_vel</code> не пришла, моторный драйвер мгновенно сбрасывает скорости в 0.</li>
      <li><strong>Аппаратный лазерный сканер безопасности (Safety SICK / Pepperl+Fuchs):</strong> физически разрывает цепь питания моторов при появлении объекта в опасной зоне 30 см.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Курс завершен! | Финальные выводы" -->

## Итоги курса: Систематизация знаний <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Фундаментальный стек инженера по планированию:</h3>
  <ol class="text-sm">
    <li><strong>Пространство состояний ($\mathcal{C}$-space):</strong> геометрия и сумма Минковского.</li>
    <li><strong>Дискретный глобальный поиск:</strong> $A^*$, $D^*$ Lite, графы видимости.</li>
    <li><strong>Сэмплирующие методы:</strong> RRT, асимптотическая оптимальность RRT*.</li>
    <li><strong>Локальная реактивность:</strong> DWA, потенциальные поля, TEB.</li>
    <li><strong>Теория управления:</strong> LQR, Direct Collocation, аналитический Дубинс.</li>
    <li><strong>Предиктивность:</strong> MPC, квадратичное программирование (QP).</li>
    <li><strong>Физические связи:</strong> неголономность, скобки Ли, сцепление колес.</li>
    <li><strong>Промышленная надежность:</strong> ROS 2 Nav2, Behavior Trees, Safety Watchdogs.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Куда двигаться дальше?</h3>
  <p>Современный фронтир робототехники объединяет доказанную безопасность классических алгоритмов с гибкостью нейросетей:</p>
  <ul>
    <li>Диффузионные политики управления (Diffusion Policy).</li>
    <li>Модели мира (World Models) для планирования в латентном пространстве.</li>
    <li>Аппаратно-ускоренные поля расстояний (nvblox на GPU).</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-green">Спасибо за внимание! Успешных траекторий! 🚀</span>
  </div>
</div>

</div>
