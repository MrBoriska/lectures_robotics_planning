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
## Лекция 06: Предиктивное управление (Model Predictive Control)

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Современное управление</span>
  <span class="badge badge-purple">Receding Horizon • QP / SQP • CasADi</span>
</div>

---

<!-- _header: "Лекция 06 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Блок 1: Концепция и линейный MPC (45 мин)</h3>
  <ul>
    <li><strong>00–15 мин:</strong> Принцип скользящего горизонта (Receding Horizon) и архитектура MPC.</li>
    <li><strong>15–30 мин:</strong> Формулировка дискретной оптимизации: горизонт $N$, матрицы весов $Q, R$, ограничения.</li>
    <li><strong>30–45 мин:</strong> Сведение задачи к квадратичному программированию (Quadratic Programming — QP).</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Блок 2: NMPC и препятствия (45 мин)</h3>
  <ul>
    <li><strong>45–60 мин:</strong> Нелинейный MPC (NMPC) для кинематической модели велосипеда и дифференциального шасси.</li>
    <li><strong>60–75 мин:</strong> Включение препятствий: функции барьеров (Control Barrier Functions) и выпуклые коридоры.</li>
    <li><strong>75–85 мин:</strong> Схема Real-Time Iteration (RTI), солверы (acados, CasADi, OSQP) и задержки в контуре.</li>
    <li><strong>85–90 мин:</strong> Итоги, контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

---

## 1. Принцип скользящего горизонта (Receding Horizon) <span class="badge badge-time">00–15 мин</span>

<div class="grid-2">

<div class="col">
  <p><strong>Model Predictive Control (MPC)</strong> объединяет планирование траектории и стабилизирующее управление в единый процесс, выполняемый на каждом цикле управления:</p>

  <div class="card">
    <h3>Циклический алгоритм MPC:</h3>
    <ol>
      <li><strong>Измерение:</strong> оцениваем текущее состояние $x_k = x(t_k)$ робота через EKF / SLAM.</li>
      <li><strong>Прогноз и оптимизация:</strong> решаем задачу оптимального управления на горизонте прогноза $N$: $\{u_k, u_{k+1}, \dots, u_{k+N-1}\}$.</li>
      <li><strong>Применение:</strong> подаем на приводы <em>только первое воздействие</em> $u^*(t) = u_k$.</li>
      <li><strong>Сдвиг:</strong> сдвигаем временное окно на шаг вперед $\Delta t$ и повторяем с пункта 1.</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>В чем преимущество перед LQR и PID?</h3>
    <ul>
      <li><strong>Явный учет жестких ограничений:</strong> пределы углов колес $|\delta| \le \delta_{max}$, токи моторов $|u| \le u_{max}$, стены и препятствия.</li>
      <li><strong>Взгляд в будущее:</strong> робот начинает плавно притормаживать перед поворотом <em>заранее</em>, а не по факту ошибки.</li>
      <li><strong>Компенсация возмущений:</strong> перерасчет на каждом шаге естественным образом компенсирует скольжение и неточности модели.</li>
    </ul>
  </div>
</div>

</div>

---

## 2. Математическая постановка Linear MPC <span class="badge badge-time">15–30 мин</span>

<div class="grid-2">

<div class="col">
  <p>Дискретная линейная модель системы и целевая функция на горизонте $N$:</p>

  <div class="formula-box">
    $$x_{k+1} = A x_k + B u_k$$
    $$\min_{u_0, \dots, u_{N-1}} J = \sum_{k=0}^{N-1} \left( x_k^T Q x_k + u_k^T R u_k + \Delta u_k^T R_\Delta \Delta u_k \right) + x_N^T P x_N$$
  </div>

  <ul>
    <li>$Q \ge 0$ — штраф за отклонение от желаемой траектории.</li>
    <li>$R > 0$ — штраф за величину управляющего воздействия.</li>
    <li>$R_\Delta$ — штраф за рывок (smoothness / rate of change): $\Delta u_k = u_k - u_{k-1}$.</li>
    <li>$P$ — терминальный штраф из уравнения Риккати.</li>
  </ul>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Ограничения (Constraints):</h3>
    <p>Все ограничения формулируются в виде политопов:</p>
    $$u_{min} \le u_k \le u_{max}$$
    $$\Delta u_{min} \le u_k - u_{k-1} \le \Delta u_{max}$$
    $$x_{min} \le x_k \le x_{max}$$
    <p class="text-sm">Если ограничения совместны, задача решается детерминированно за микросекунды.</p>
  </div>
</div>

</div>

---

## 3. Сведение к задаче Quadratic Programming (QP) <span class="badge badge-time">30–45 мин</span>

<div class="grid-2">

<div class="col">
  <p>Выражая будущие состояния через начальное $x_0$ и вектор управлений $U = (u_0^T, u_1^T, \dots, u_{N-1}^T)^T$:</p>
  $$X = \mathcal{S}_x x_0 + \mathcal{S}_u U$$
  
  <p>Подстановка в критерий $J$ сводит задачу к <strong>каноническому квадратичному программированию (QP)</strong>:</p>

  <div class="formula-box">
    $$\min_{U} \frac{1}{2} U^T H U + g^T U$$
    $$\text{s.t.} \quad A_{in} U \le b_{in}$$
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Свойства матрицы Гессиана $H$:</h3>
    <ul>
      <li>$H = \mathcal{S}_u^T \bar{Q} \mathcal{S}_u + \bar{R}$.</li>
      <li>Если $R > 0$, матрица $H$ строго <strong>симметрична и положительно определена ($H \succ 0$)</strong>.</li>
      <li>Критерий строго выпуклый $\implies$ любой локальный минимум является <em>глобальным оптимумом</em>!</li>
      <li>Современные решатели (OSQP, qpOASES, DAQP) находят решение за $< 1$ мс на процессоре микроконтроллера.</li>
    </ul>
  </div>
</div>

</div>

---

## 4. Нелинейный MPC (NMPC) для мобильных роботов <span class="badge badge-time">45–65 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Кинематическая модель велосипеда (Bicycle Model):</h3>
    $$\begin{pmatrix} \dot{x} \\ \dot{y} \\ \dot{\psi} \\ \dot{v} \end{pmatrix} = \begin{pmatrix} v \cos(\psi + \beta) \\ v \sin(\psi + \beta) \\ \frac{v}{L} \tan(\delta) \cos\beta \\ a \end{pmatrix}, \quad \beta = \arctan\left(\frac{l_r}{L}\tan\delta\right)$$
    <ul>
      <li>Управление: продольное ускорение $a$ и угол поворота передних колес $\delta$.</li>
      <li>Система существенно <strong>нелинейна</strong> из-за тригонометрических связей.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Решение в реальном времени: Real-Time Iteration (RTI)</h3>
    <ul>
      <li><strong>Sequential Quadratic Programming (SQP):</strong> на каждом шаге нелинейная динамика линеаризуется вокруг текущей траектории, решаясь как цепочка QP.</li>
      <li><strong>RTI Scheme (Diehl et al.):</strong> за цикл управления выполняется всего <em>одна</em> итерация SQP, разделенная на фазу подготовки (Preparation phase) и фазу быстрой обратной связи (Feedback phase).</li>
      <li>Инструменты генерации кода C/C++: <strong>acados</strong>, <strong>CasADi</strong>.</li>
    </ul>
  </div>
</div>

</div>

---

## 5. Препятствия в MPC: Выпуклые коридоры и барьеры <span class="badge badge-time">65–85 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-alert">
    <h3>Проблема невыпуклости препятствий:</h3>
    <p>Условие избежания коллизии с круглым препятствием радиуса $R_{obs}$:</p>
    $$\|p_k - p_{obs}\|^2 \ge (R_{rob} + R_{obs})^2$$
    <ul>
      <li>Знак $\ge$ делает допустимое множество невыпуклым!</li>
      <li>Прямая подача такого ограничения в солвер порождает множество локальных минимумов.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Инженерные решения в MPC:</h3>
    <ol>
      <li><strong>Безопасные коридоры полета/движения (Safe Flight Corridors — SFC):</strong>
        Глобальный путь декомпозируется на пересекающиеся выпуклые многогранники (Convex Polytopes) $A_i p_k \le b_i$. Внутри каждого политопа ограничение выпукло!</li>
      <li><strong>Control Barrier Functions (CBF):</strong>
        Мягкие или жесткие барьерные ограничения, гарантирующие прямое невыходное множество (Forward Invariance) безопасной зоны.</li>
    </ol>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 06 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol>
    <li>MPC объединяет планирование траектории и замкнутое управление с явным учетом физических ограничений.</li>
    <li>Принцип скользящего горизонта обеспечивает естественную компенсацию внешних возмущений и динамических препятствий.</li>
    <li>Линейный MPC сводится к строго выпуклой задаче QP, решаемой за доли миллисекунды.</li>
    <li>Для нелинейных платформ связка NMPC + RTI (acados) является де-факто стандартом в беспилотных автомобилях и AMR.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы:</h3>
  <ul>
    <li>Почему в MPC на реальном шасси применяется только первое вычисленное управляющее воздействие $u_k$, а остальные отбрасываются?</li>
    <li>Что произойдет с задачей QP в MPC при возникновении взаимно противоречивых ограничений (infeasibility)?</li>
    <li>В чем разница между задачами Trajectory Tracking (отслеживание траектории во времени) и Path Following (следование по геометрическому пути)?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Учёт ограничений в алгоритмах планирования</span>
  </div>
</div>

</div>
