---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 04"
footer: "Курс лекций • Лекция 04 • Слайд %PAGE% из %TOTAL%"
math: mathjax
---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 04: Реактивные и локальные методы

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Локальное планирование</span>
  <span class="badge badge-purple">ETH Zürich • Khatib • Fox (DWA)</span>
</div>

---

<!-- _header: "Лекция 04 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Блок 1: Потенциальные поля и геометрия (45 мин)</h3>
  <ul>
    <li><strong>00–15 мин:</strong> Место локального планировщика в контуре управления робота (частота 20–50 Гц).</li>
    <li><strong>15–30 мин:</strong> Искусственные потенциальные поля (Хатиб): $U_{att}$, $U_{rep}$, градиентный спуск.</li>
    <li><strong>30–45 мин:</strong> Локальные минимумы, U-ловушки и их строгое устранение через <em>Гармонические поля (ETH)</em>.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Блок 2: Пространство скоростей и оптимизация (45 мин)</h3>
  <ul>
    <li><strong>45–60 мин:</strong> <span class="badge badge-green">Интерактивный симулятор</span>: исследование сил в потенциальном поле.</li>
    <li><strong>60–75 мин:</strong> Dynamic Window Approach (DWA) и Velocity Obstacles (VO / RVO).</li>
    <li><strong>75–85 мин:</strong> Метод упругой ленты с таймингом (Timed Elastic Band — TEB).</li>
    <li><strong>85–90 мин:</strong> Итоги, контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

---

## 1. Зачем нужны локальные методы? <span class="badge badge-time">00–15 мин</span>

<div class="grid-2">

<div class="col">
  <p>Глобальный планировщик ($A^*$, RRT*) строит маршрут по статической карте помещения раз в 1–5 секунд. В реальном мире возникают проблемы:</p>
  <ul>
    <li><strong>Внезапные препятствия:</strong> люди, погрузчики, закрывающиеся двери.</li>
    <li><strong>Несовершенство приводов:</strong> пробуксовка колес одометрии (Slip) и ошибки позиционирования.</li>
    <li><strong>Жесткие требования реального времени:</strong> время реакции робота на препятствие должно составлять $\le 20\text{--}50$ мс.</li>
  </ul>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Архитектура контура управления:</h3>
    <div class="formula-box">
      $$\text{Глобальный путь } \Pi \xrightarrow[\sim 1\text{ Гц}]{} \text{Локальный планировщик} \xrightarrow[\sim 30\text{ Гц}]{(v, \omega)} \text{Контроллер приводов} \xrightarrow[\sim 500\text{ Гц}]{u}$$
    </div>
    <p>Локальный планировщик стремится отслеживать глобальный путь, динамически огибая локальные препятствия.</p>
  </div>
</div>

</div>

---

## 2. Искусственные потенциальные поля (Хатиб, 1986) <span class="badge badge-time">15–30 мин</span>

<div class="grid-2">

<div class="col">
  <p>Робот рассматривается как частица, движущаяся под действием сил искусственного поля $U(q) = U_{att}(q) + U_{rep}(q)$:</p>

  <div class="card">
    <h3>Притягивающий потенциал (к цели):</h3>
    $$U_{att}(q) = \frac{1}{2} k_{att} \|q - q_{goal}\|^2$$
    $$F_{att}(q) = -\nabla U_{att} = -k_{att} (q - q_{goal})$$
  </div>

  <div class="card card-alert">
    <h3>Отталкивающий потенциал (от препятствий):</h3>
    $$U_{rep}(q) = \begin{cases} \frac{1}{2} k_{rep} \left(\frac{1}{d(q)} - \frac{1}{d_0}\right)^2, & d(q) \le d_0 \\ 0, & d(q) > d_0 \end{cases}$$
    $$F_{rep}(q) = k_{rep} \left(\frac{1}{d(q)} - \frac{1}{d_0}\right) \frac{1}{d(q)^2} \nabla d(q)$$
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Фундаментальные проблемы APF:</h3>
    <ol>
      <li><strong>Локальные минимумы (Local Minima):</strong> робот застревает в тупиках (U-образные препятствия), где $F_{att} + F_{rep} = 0$.</li>
      <li><strong>Осцилляции в узких проходах:</strong> попеременное отталкивание от противоположных стен.</li>
      <li><strong>Недостижимость цели вблизи препятствия:</strong> отталкивание препятствия сильнее притяжения цели (проблема GNRON).</li>
    </ol>
  </div>
</div>

</div>

---

## 3. Математическое устранение локальных минимумов <span class="badge badge-time">30–45 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Гармонические потенциальные поля (ETH Zürich):</h3>
    <p>Потенциал $U$ удовлетворяет <strong>уравнению Лапласа</strong>:</p>
    $$\Delta U = \sum_{i=1}^d \frac{\partial^2 U}{\partial q_i^2} = 0$$
    <ul>
      <li>По принципу максимума гармонических функций, гармонический потенциал <strong>не имеет локальных минимумов</strong> внутри области!</li>
      <li>Граничные условия:
        - <em>Дирихле:</em> $U = 1$ на препятствиях, $U = 0$ на цели.
        - <em>Неймана:</em> $\frac{\partial U}{\partial n} = 0$ (линии тока параллельны стенам).
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Навигационные функции (Римон–Кодичек):</h3>
    <p>Функция $U: \mathcal{C}_{free} \to [0, 1]$, являющаяся гладкой функцией Морса, имеющей ровно один глобальный минимум в цели и седловые точки вместо локальных минимумов.</p>
    $$\Phi(q) = \frac{\gamma_d(q)}{(\gamma_d(q)^k + \beta(q))^{1/k}}$$
    <p class="text-sm">При достаточно большом показателе $k$ все паразитные локальные экстремумы исчезают.</p>
  </div>
</div>

</div>

---

<!-- _header: "Интерактивная практика | Потенциальные поля" -->

## Интерактивный симулятор: Потенциальные поля и ловушки <span class="badge badge-green">⏱️ 45–60 мин</span>

<div class="interactive-container">
  <div class="interactive-header">
    <span><i class="interactive-dot"></i> Интерактивный APF: Векторы сил F_att, F_rep и демонстрация U-ловушки</span>
    <span>Перетаскивайте робота и препятствия | Переключите пресет на «U-ловушка»</span>
  </div>
  <iframe src="../../widgets/potential-field/index.html" class="interactive-frame"></iframe>
</div>

---

## 4. Dynamic Window Approach (DWA) <span class="badge badge-time">60–75 мин</span>

<div class="grid-2">

<div class="col">
  <p>Алгоритм DWA (Fox, Burgard, Thrun) осуществляет поиск оптимального управления напрямую в пространстве скоростей $(v, \omega)$:</p>

  <div class="formula-box">
    $$V_r = V_s \cap V_a \cap V_d$$
  </div>

  <ul>
    <li>$V_s$ — пределы скоростей шасси: $v \in [v_{min}, v_{max}], \omega \in [\omega_{min}, \omega_{max}]$.</li>
    <li>$V_a$ — допустимые скорости, гарантирующие остановку без коллизии:
      $$v \le \sqrt{2 \cdot \operatorname{dist}(v, \omega) \cdot a_{max}}$$
    </li>
    <li>$V_d$ — динамическое окно (скорости, достижимые за время $\Delta t$ с учетом ускорений):
      $$V_d = [v_0 - a_{max}\Delta t, v_0 + a_{max}\Delta t] \times [\omega_0 - \alpha_{max}\Delta t, \omega_0 + \alpha_{max}\Delta t]$$
    </li>
  </ul>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Целевая функция DWA:</h3>
    $$\max_{(v, \omega) \in V_r} \left( \alpha \cdot \operatorname{heading}(v, \omega) + \beta \cdot \operatorname{dist}(v, \omega) + \gamma \cdot \operatorname{velocity}(v, \omega) \right)$$
    <ul>
      <li>$\operatorname{heading}$ — соответствие направлению на ближайшую точку глобального пути.</li>
      <li>$\operatorname{dist}$ — клиренс (расстояние до ближайшего препятствия по дуге).</li>
      <li>$\operatorname{velocity}$ — поощрение движения с максимальной допустимой скоростью.</li>
    </ul>
    <p class="text-sm">Основа для <code>nav2_dwb_controller</code> в ROS 2.</p>
  </div>
</div>

</div>

---

## 5. Timed Elastic Band (TEB Local Planner) <span class="badge badge-time">75–85 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Концепция упругой ленты с временем (TEB):</h3>
    <ul>
      <li>Путь представляется последовательностью поз и интервалов времени между ними:
        $$\mathcal{B} = \{s_0, \Delta t_0, s_1, \Delta t_1, \dots, s_{N-1}, \Delta t_{N-1}, s_N\}$$
      </li>
      <li>Траектория деформируется в реальном времени как упругая струна, отталкиваемая препятствиями.</li>
      <li>Позволяет явно оптимизировать время проезда (Time-optimal trajectory).</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Формулировка в виде графа факторов (g2o):</h3>
    <p>Решается задача нелинейной оптимизации методом Левенберга-Марквардта:</p>
    $$V^*(\mathcal{B}) = \sum_k \left( w_t \Delta t_k^2 + w_{path} \|s_{k+1} - s_k\|^2 + w_{obs} f_{obs}(s_k) + w_{kin} f_{kin}(s_k, s_{k+1}) \right)$$
    <ul>
      <li>Учитывает кинематику автомобиля (Ackermann) и дифференциального робота.</li>
      <li>Поддерживает объезд препятствий в различных топологических классах гомотопии (обход препятствия слева / справа).</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 04 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol>
    <li>Локальные планировщики работают с высокой частотой (20–50 Гц), преобразуя геометрический путь в динамические команды приводов $(v, \omega)$.</li>
    <li>Метод потенциальных полей прост и интуитивен, но подвержен застреванию в локальных минимумах. Гармонические поля решают эту проблему.</li>
    <li>DWA оптимизирует скорости в динамическом окне доступных ускорений.</li>
    <li>TEB строит гладкие, кинематически осуществимые траектории на основе графовой оптимизации.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы:</h3>
  <ul>
    <li>Почему локальный планировщик не может заменить глобальный планировщик?</li>
    <li>Как граничные условия Неймана в гармонических полях препятствуют столкновению с касательными поверхностями стен?</li>
    <li>В чем фундаментальное отличие пространства поиска DWA от пространства поиска TEB?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Оптимальное управление</span>
  </div>
</div>

</div>
