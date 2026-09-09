---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 06"
footer: "Курс лекций • Лекция 06 • Слайд %PAGE% из %TOTAL%"
math: mathjax
---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 06: Предиктивное управление (Model Predictive Control — MPC)

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Предиктивное управление</span>
  <span class="badge badge-purple">Receding Horizon • Dense vs Sparse QP • NMPC • CBF • acados</span>
</div>

---

<!-- _header: "Лекция 06 | Введение и мотивация" -->

## Чему посвящена эта лекция? <span class="badge badge-blue">Предиктивный горизонт</span>

<div class="grid-2 mt-2">

<div class="card card-accent">
  <h3>🎯 Слияние планирования и стабилизации</h3>
  <p class="text-sm">
    В классической архитектуре планировщик строит траекторию, а ПИД- или LQR-регулятор слепо пытается её отслеживать. Но когда перед роботом возникает жесткое физическое ограничение (предел тяги, стена, скользкий поворот), слепой регулятор терпит аварию.
  </p>
  <p class="text-sm">
    Эта лекция посвящена <strong>Model Predictive Control (MPC)</strong>: передовой парадигме, которая непрерывно решает задачу оптимального управления в скользящем окне времени, прямо учитывая пределы приводов и препятствия.
  </p>
</div>

<div class="card">
  <h3>🔍 Ключевые вопросы лекции</h3>
  <ul class="text-sm">
    <li><strong>Принцип скользящего горизонта:</strong> Почему решается оптимизация на $N$ шагов вперед, но выполняется только $u_0^*$?</li>
    <li><strong>Вычислительная архитектура:</strong> Плотная (Dense) vs разреженная (Sparse) квадратичная программа (QP) и сложность $\mathcal{O}(N)$.</li>
    <li><strong>Математические гарантии:</strong> Терминальные множества $\mathcal{X}_f$, функции Ляпунова и рекурсивная допустимость.</li>
    <li><strong>Нелинейный MPC (NMPC):</strong> Кинематика велосипеда, координаты Френе и обход препятствий через коридоры (SFC) и функции барьеров (<strong>CBF</strong>).</li>
    <li><strong>Инженерия реального времени:</strong> Схема <strong>Real-Time Iteration (RTI)</strong> в солвере <code>acados</code> для работы на 50 Гц.</li>
  </ul>
</div>

</div>

<div class="card card-success mt-2">
  <h3 style="margin-bottom: 4px;">💡 Чему вы научитесь за эти 90 минут</h3>
  <p class="text-sm" style="margin-bottom: 0;">
    Формулировать задачи Linear MPC и NMPC для колесных платформ, строить матрицы квадратичного программирования для солверов OSQP/qPOASES, вводить барьерные функции безопасности (CBF) и интегрировать суб-миллисекундные MPC-солверы в бортовой стек мобильного робота.
  </p>
</div>

---

<!-- _header: "Лекция 06 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Концепция и Linear MPC (45 мин)</h3>
  <ul>
    <li><strong>00–12 мин:</strong> Парадигма скользящего горизонта (Receding Horizon Principle): оптимизация, применение первого шага, сдвиг.</li>
    <li><strong>12–25 мин:</strong> Дискретный Linear MPC: матрицы состояний $(A, B)$, весовые матрицы $(Q, R, R_\Delta)$, штраф за дергание управления.</li>
    <li><strong>25–37 мин:</strong> Структура задачи: Dense QP ($\mathcal{O}(N^3)$) vs Sparse QP ($\mathcal{O}(N)$), KKT-условия и солвер <code>OSQP</code>.</li>
    <li><strong>37–45 мин:</strong> Теория устойчивости MPC: терминальная стоимость $P$ (DARE) и терминальное инвариантное множество $\mathcal{X}_f$.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: NMPC, Препятствия и Солверы (45 мин)</h3>
  <ul>
    <li><strong>45–58 мин:</strong> Нелинейный MPC (NMPC): кинематическая модель велосипеда, координаты Френе (Tracking vs Contour Error).</li>
    <li><strong>58–70 мин:</strong> Препятствия в MPC: выпуклые безопасные коридоры (Safe Flight Corridors) и Control Barrier Functions (CBF).</li>
    <li><strong>70–82 мин:</strong> Реализация в реальном времени: схема <strong>Real-Time Iteration (RTI)</strong>, солверы <code>acados</code> и <code>CasADi</code>.</li>
    <li><strong>82–90 мин:</strong> Инженерные приемы: слак-переменные (мягкие ограничения), задержки в контуре, контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

<!--
Примечание для лектора:
MPC сегодня — фактический стандарт для беспилотных автомобилей, шагающих роботов (Boston Dynamics, ANYbotics) и складских AGV. Объясните слушателям баланс между теоретической строгостью (устойчивость по Ляпунову) и численной скоростью (RTI scheme).
-->

---

## 1. Парадигма скользящего горизонта (Receding Horizon) <span class="badge badge-time">00–12 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Model Predictive Control (MPC)</strong> решает задачу оптимального управления во временном окне длиной $N$ тактов дискретизации $\Delta t$ на каждом шаге контура управления:</p>

  <div class="card">
    <h3>Четырехшаговый цикл MPC:</h3>
    <ol class="text-sm">
      <li><strong>Оценка состояния:</strong> получаем текущий вектор $x_k = x(t_k)$ (из фильтра EKF / SLAM).</li>
      <li><strong>Оптимизация на горизонте $N$:</strong> находим оптимальную последовательность управлений $\mathbf{U}^* = \{u_0^*, u_1^*, \dots, u_{N-1}^*\}$.</li>
      <li><strong>Исполнение первого шага:</strong> подаем на приводы <em>только</em> первое управление: $u(t) = u_0^*$.</li>
      <li><strong>Сдвиг горизонта (Recede):</strong> сдвигаем окно на один шаг вперед: $t_{k+1} = t_k + \Delta t$ и повторяем процедуру!</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Почему MPC превосходит PID и LQR?</h3>
    <ul class="text-sm">
      <li><strong>Явный учет жестких неравенств:</strong> физические пределы углов руления $|\delta| \le \delta_{max}$, токов моторов $|I| \le I_{max}$ и границ стен.</li>
      <li><strong>Упреждающее поведение (Feedforward Foresight):</strong> робот начинает плавно притормаживать перед закрытым поворотом <em>заранее</em>, а не после вылета с траектории.</li>
      <li><strong>Естественная обратная связь:</strong> пересчет на каждом такте компенсирует проскальзывание колес, ветер и неточности матмодели.</li>
    </ul>
  </div>
</div>

</div>

---

## 2. Дискретный Linear MPC: Математическая модель <span class="badge badge-time">12–25 мин</span>

<div class="grid-2">

<div class="col">
  <p>Рассматривается линейная дискретная система с шагом $\Delta t$:</p>
  <div class="formula-box text-sm">
    $$x_{k+1} = A x_k + B u_k$$
  </div>

  <div class="card">
    <h3>Квадратичный функционал стоимости:</h3>
    <div class="formula-box text-sm">
      $$J = \sum_{k=0}^{N-1} \left( x_k^T Q x_k + u_k^T R u_k + \Delta u_k^T R_\Delta \Delta u_k \right) + x_N^T P x_N$$
    </div>
    <ul class="text-sm">
      <li>$Q \succeq 0$ — штраф за отклонение от опорной точки.</li>
      <li>$R \succ 0$ — штраф за расход энергии / амплитуду управляющих воздействий.</li>
      <li>$R_\Delta \succ 0$ — штраф за скорость изменения управления $\Delta u_k = u_k - u_{k-1}$ (устраняет рывки моторов и механический износ).</li>
      <li>$P \succ 0$ — терминальная стоимость на конце горизонта $N$.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Множество допустимых ограничений:</h3>
    <div class="formula-box text-sm">
      $$\begin{aligned}
      u_{min} &\le u_k \le u_{max} && \text{(пределы приводов)} \\
      \Delta u_{min} &\le u_k - u_{k-1} \le \Delta u_{max} && \text{(ограничение рывка / slew-rate)} \\
      x_{min} &\le x_k \le x_{max} && \text{(безопасные зоны состояния)}
      \end{aligned}$$
    </div>
    <div class="card-alert text-sm mt-2">
      <strong>Ключевая особенность:</strong> Если на шаге $k$ решения, удовлетворяющего всем жестким ограничениям, не существует — оптимизатор выдает ошибку (Infeasible), и робот рискует потерять управление!
    </div>
  </div>
</div>

</div>

---

## 3. Структура задачи: Dense QP vs Sparse QP <span class="badge badge-time">25–37 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-alert">
    <h3>Плотная форма (Dense / Condensed QP):</h3>
    <p class="text-sm">Состояния выражаются через начальное $x_0$ и вектор управлений $\mathbf{U} = [u_0^T, \dots, u_{N-1}^T]^T$:</p>
    $$x_k = A^k x_0 + \sum_{j=0}^{k-1} A^{k-1-j} B u_j$$
    <ul class="text-sm">
      <li>Оптимизация только по $\mathbf{U} \in \mathbb{R}^{m N}$.</li>
      <li>Матрица Гессиана $H_{dense}$ <strong>полностью заполнена (плотная)</strong>.</li>
      <li>Сложность факторизации: $\mathcal{O}(m^3 N^3)$.</li>
      <li>Эффективно <em>только</em> для коротких горизонтов ($N \le 10$).</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Разреженная форма (Sparse QP):</h3>
    <p class="text-sm">И состояния $\mathbf{X}$, и управления $\mathbf{U}$ остаются переменными оптимизации. Динамика задается как равенства $x_{k+1} - A x_k - B u_k = 0$:</p>
    $$\min_{\mathbf{X}, \mathbf{U}} \frac{1}{2} \mathbf{Z}^T \mathbf{H} \mathbf{Z} \quad \text{при } \mathbf{A}_{eq} \mathbf{Z} = \mathbf{b}_{eq}, \;\; \mathbf{C} \mathbf{Z} \le \mathbf{d}$$
    <ul class="text-sm">
      <li>Гессиан $\mathbf{H}$ и матрица $\mathbf{A}_{eq}$ имеют <strong>блочно-диагональную структуру</strong>!</li>
      <li>Солверы на методе расщепления операторов (<code>OSQP</code>) или Riccati-факторизации решают задачу со сложностью <strong>$\mathcal{O}(N)$</strong>!</li>
      <li>Масштабируется до горизонтов $N = 100$ и более.</li>
    </ul>
  </div>
</div>

</div>

---

## 4. Гарантии устойчивости и рекурсивная допустимость <span class="badge badge-time">37–48 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Проблема конечного горизонта:</h3>
    <p class="text-sm">Поскольку горизонт $N$ конечен, оптимальное управление на интервале $[0, N]$ <strong>не гарантирует</strong> асимптотическую устойчивость всей замкнутой бесконечной системы!</p>
    <p class="text-sm">Робот может развить максимальную скорость к концу горизонта и физически не успеть затормозить перед стеной на шаге $N+1$.</p>
  </div>

  <div class="card">
    <h3>Рекурсивная допустимость (Recursive Feasibility):</h3>
    <p class="text-sm">Если задача имела допустимое решение в момент времени $t$, то гарантируется, что она будет иметь решение и в момент $t + \Delta t$.</p>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Теорема устойчивости (Mayne et al., 2000):</h3>
    <p class="text-sm">Система с MPC асимптотически устойчива по Ляпунову, если:</p>
    <ol class="text-sm">
      <li><strong>Терминальная стоимость $P$:</strong> матрица $P$ удовлетворяет дискретному алгебраическому уравнению Риккати (DARE) для локального LQR-регулятора $u = K_f x$.</li>
      <li><strong>Терминальное инвариантное множество $\mathcal{X}_f$:</strong> в конце горизонта $x_N \in \mathcal{X}_f$, где $\mathcal{X}_f$ является контрольно-инвариантным множеством:
        $$(A + B K_f) \mathcal{X}_f \subseteq \mathcal{X}_f \subseteq \mathcal{X}_{free}$$
      </li>
    </ol>
    <p class="text-sm">Тогда оптимальная функция стоимости $V^*(x)$ выступает строгой <strong>функцией Ляпунова</strong>: $V^*(x_{k+1}) - V^*(x_k) \le -x_k^T Q x_k < 0$.</p>
  </div>
</div>

</div>

---

## 5. Нелинейный MPC (NMPC) для мобильных роботов <span class="badge badge-time">48–60 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Кинематическая модель велосипеда (Bicycle Model):</h3>
    $$\begin{aligned}
    \dot{x} &= v \cos(\psi + \beta) \\
    \dot{y} &= v \sin(\psi + \beta) \\
    \dot{\psi} &= \frac{v}{l_r} \sin\beta, \quad \beta = \arctan\left(\frac{l_r}{l_f + l_r} \tan\delta\right) \\
    \dot{v} &= a
    \end{aligned}$$
    <p class="text-sm">где $\delta$ — угол поворота передних колес, $a$ — продольное ускорение, $\beta$ — угол увода центра масс.</p>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Координаты Френе (Contouring MPC):</h3>
    <p class="text-sm">Вместо глобальных координат $(x, y)$ состояние проецируется на осевую линию пути $\mathbf{p}(s)$:</p>
    <ul class="text-sm">
      <li>$s$ — пройденная дуговая координата вдоль пути.</li>
      <li>$e_l$ — боковая ошибка отклонения от пути (Lag Error).</li>
      <li>$e_c$ — ошибка контура (Contour Error).</li>
    </ul>
    <div class="formula-box text-sm">
      $$J = \sum_{k=0}^{N-1} \Big( w_c e_c^2(k) + w_l e_l^2(k) - w_s v_s(k) \Big)$$
    </div>
    <div class="card-success text-sm">
      <strong>Эффект:</strong> Слагаемое $-w_s v_s$ поощряет робота мчаться вперед по пути, а $w_c, w_l$ не дают ему срезать повороты и вылетать с трассы.
    </div>
  </div>
</div>

</div>

---

## 6. Препятствия в MPC: Выпуклые коридоры и CBF <span class="badge badge-time">58–70 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Safe Flight Corridors (SFC — Выпуклые коридоры):</h3>
    <p class="text-sm">Свободное пространство $\mathcal{C}_{free}$ невыпукло. Но вдоль глобального пути можно построить цепочку пересекающихся <strong>выпуклых политопов</strong>:</p>
    $$\mathcal{P}_k = \{ x \in \mathbb{R}^2 \mid \mathbf{A}_k x \le \mathbf{b}_k \}$$
    <ul class="text-sm">
      <li>Нелинейные препятствия заменяются набором линейных неравенств $\mathbf{A}_k x_k \le \mathbf{b}_k$.</li>
      <li>Задача сохраняет выпуклость (QP) и решается за доли миллисекунды!</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Control Barrier Functions (Дискретные CBF):</h3>
    <p class="text-sm">Определим безопасное множество $\mathcal{S} = \{x \mid h(x) \ge 0\}$, где $h(x) = \|x - p_{obs}\|^2 - r_{safe}^2$.</p>
    <p class="text-sm">Условие дискретной барьерной функции гарантирует инвариантность безопасности множества $\mathcal{S}$:</p>
    <div class="formula-box text-sm">
      $$\Delta h(x_k, u_k) = h(x_{k+1}) - h(x_k) \ge -\gamma h(x_k), \quad 0 < \gamma \le 1$$
    </div>
    <div class="card-success text-sm">
      <strong>Преимущество:</strong> CBF добавляется в квадратичную программу как простое линейное ограничение на $u_k$, обеспечивая 100% математическую гарантию нестолкновения!
    </div>
  </div>
</div>

</div>

---

## 7. Real-Time Iteration (RTI) и стек солверов <span class="badge badge-time">70–82 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Схема Real-Time Iteration (Diehl et al.):</h3>
    <p class="text-sm">Полное решение нелинейной программы (NMPC) методом SQP требует десятков итераций Ньютона (неприемлемо для 50 Гц). Схема RTI разделяет такт на две фазы:</p>
    <ol class="text-sm">
      <li><strong>Preparation Phase (Фоновая фаза, 80% времени):</strong> интеграция динамики, линеаризация нелинейной модели, расчет матриц KKT-системы <em>до прихода нового замера</em>.</li>
      <li><strong>Feedback Phase (Мгновенная фаза, < 1 мс):</strong> пришел свежий замер $x_0$ от SLAM $\rightarrow$ решение <strong>ровно одной</strong> задачи QP $\rightarrow$ выдача $u_0^*$ на моторы!</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Индустриальный стек солверов MPC (2026):</h3>
    <ul class="text-sm">
      <li><strong><code>acados</code>:</strong> высокопроизводительный генератор C-кода для NMPC (HPIPM QP-солвер, BLASFEO линейная алгебра). Время цикла: <strong>0.5–2 мс</strong> на ARM Cortex / NVIDIA Jetson.</li>
      <li><strong><code>CasADi</code>:</strong> символьный инструмент автоматического дифференцирования (C++/Python). Идеален для прототипирования сложных моделей.</li>
      <li><strong><code>OSQP</code>:</strong> операторное расщепление (ADMM) для разреженных Linear QP. Нечувствителен к вырождению ограничений.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 06 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">82–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol class="text-sm">
    <li><strong>MPC</strong> объединяет прогнозирование динамики, оптимизацию функционала и соблюдение физических ограничений в скользящем окне.</li>
    <li><strong>Sparse QP</strong> формулировка масштабируется линейно $\mathcal{O}(N)$, вытесняя медленный Dense QP.</li>
    <li><strong>Устойчивость по Ляпунову</strong> строго гарантируется выбором терминального веса Риккати $P$ и инвариантного множества $\mathcal{X}_f$.</li>
    <li><strong>Выпуклые коридоры (SFC)</strong> и <strong>Control Barrier Functions (CBF)</strong> переводят обход нелинейных препятствий в быстрые QP-ограничения.</li>
    <li><strong>Схема RTI (acados)</strong> обеспечивает расчет NMPC на частотах 50–100 Гц на бортовых контроллерах.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы для самопроверки:</h3>
  <ul class="text-sm">
    <li>Почему в MPC исполняется только первое вычисленное управление $u_0^*$, а не весь найденный профиль?</li>
    <li>В чем вычислительная разница между плотной (Dense) и разреженной (Sparse) постановкой QP в MPC?</li>
    <li>Зачем в целевую функцию включают штраф за скорость изменения управления $\Delta u_k^T R_\Delta \Delta u_k$?</li>
    <li>Как схема Real-Time Iteration (RTI) позволяет запускать нелинейный MPC на частотах 100 Гц?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Учёт ограничений (Неголономность, Скобки Ли, TOPP)</span>
  </div>
</div>

</div>
