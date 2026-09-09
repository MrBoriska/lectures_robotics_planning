---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 05"
footer: "Курс лекций • Лекция 05 • Слайд %PAGE% из %TOTAL%"
math: mathjax
---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 05: Оптимальное управление в планировании траекторий

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Теория оптимального управления</span>
  <span class="badge badge-purple">LaValle (гл. 15) • Pontryagin • Bellman • LQR • Direct Collocation</span>
</div>

---

<!-- _header: "Лекция 05 | Введение и мотивация" -->

## Чему посвящена эта лекция? <span class="badge badge-blue">Оптимальное управление</span>

<div class="grid-2 mt-2">

<div class="card card-accent">
  <h3>🎯 От геометрии к силам, энергиям и времени</h3>
  <p class="text-sm">
    Геометрический путь $\sigma(s)$ указывает, <em>куда</em> ехать, но ничего не говорит о том, <em>с какими ускорениями</em>, <em>напряжениями на моторах</em> и <em>минимальным временем</em> робот способен его преодолеть без заноса.
  </p>
  <p class="text-sm">
    Эта лекция посвящена <strong>теории оптимального управления (Optimal Control)</strong>: как превратить абстрактную задачу движения в строгую оптимизацию функционала качества $J(u)$ с учетом дифференциальной физики $\dot{x} = f(x, u)$ и ограничений приводов.
  </p>
</div>

<div class="card">
  <h3>🔍 Ключевые вопросы лекции</h3>
  <ul class="text-sm">
    <li><strong>Математический базис:</strong> Принцип максимума Понтрягина (ПМП), Гамильтониан $H$ и сопряженные переменные $\lambda(t)$.</li>
    <li><strong>Аналитические экстремали:</strong> Почему повороты на пределе сцепления порождают Bang-Bang управление и кривые <strong>Дубинса и Ридса-Шеппа</strong>?</li>
    <li><strong>Динамическое программирование:</strong> Уравнение Гамильтона–Якоби–Беллмана (HJB) и линейно-квадратичный регулятор (<strong>LQR</strong>).</li>
    <li><strong>Численная транскрипция:</strong> Почему прямая стрельба (Shooting) нестабильна и как <strong>Direct Collocation</strong> решает задачу через разреженные NLP?</li>
    <li><strong>Стабилизация:</strong> Отслеживание траектории через нестационарный <strong>TVLQR</strong>.</li>
  </ul>
</div>

</div>

<div class="card card-success mt-2">
  <h3 style="margin-bottom: 4px;">💡 Чему вы научитесь за эти 90 минут</h3>
  <p class="text-sm" style="margin-bottom: 0;">
    Формулировать задачи оптимального управления в форме Лагранжа и Больца, находить аналитические кратчайшие пути с ограниченным радиусом кривизны (кривые Дубинса), проектировать оптимальные LQR/TVLQR регуляторы для мобильных роботов и транскрибировать траектории методом прямой коллокации.
  </p>
</div>

---

<!-- _header: "Лекция 05 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Аналитическая теория (45 мин)</h3>
  <ul>
    <li><strong>00–12 мин:</strong> Постановка задачи Больца: состояние $x \in \mathcal{X}$, управление $u \in \mathcal{U}$, интегрант потерь $L(x, u)$ и терминальные затраты $\Phi(x_T)$.</li>
    <li><strong>12–25 мин:</strong> Принцип максимума Понтрягина (ПМП): функция Гамильтона $H(x, u, \lambda)$, сопряженная система $\dot{\lambda} = -\nabla_x H$.</li>
    <li><strong>25–35 мин:</strong> Релейное управление (Bang-Bang Control): функция переключения и задачи быстродействия.</li>
    <li><strong>35–45 мин:</strong> Аналитические экстремали для колесных систем: кривые Дубинса (LSL, RSR, LSR...) и Ридса-Шеппа (реверс).</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Численная оптимизация и слежение (45 мин)</h3>
  <ul>
    <li><strong>45–60 мин:</strong> Принцип оптимальности Беллмана, уравнение HJB и вывод LQR (алгебраическое уравнение Риккати CARE).</li>
    <li><strong>60–72 мин:</strong> Численная оптимизация траекторий: Single/Multiple Shooting vs <strong>Direct Collocation (Эрмит–Симпсон)</strong>. Разреженные NLP (IPOPT).</li>
    <li><strong>72–82 мин:</strong> Практика слежения за траекторией: линеаризация шасси и нестационарный регулятор <strong>TVLQR</strong>.</li>
    <li><strong>82–90 мин:</strong> Сравнение аналитики и численных солверов, контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

<!--
Примечание для лектора:
Лекция соединяет золотой классический фонд советской и мировой математики (Понтрягин, Беллман) с современной вычислительной робототехникой (разреженные нелинейные программы и Direct Collocation на базе IPOPT).
-->

---

## 1. Постановка задачи оптимального управления <span class="badge badge-time">00–12 мин</span>

<div class="grid-2">

<div class="col">
  <p>В отличие от чисто геометрического пути, в оптимальном управлении мы ищем непрерывную функцию управления $u(t)$ и порождаемую траекторию состояния $x(t)$:</p>

  <div class="formula-box text-sm">
    $$\min_{u(t) \in \mathcal{U}} J = \int_{0}^{T} L(x(t), u(t)) \, dt + \Phi(x(T))$$
    $$\text{при ограничениях:} \quad \dot{x}(t) = f(x(t), u(t)), \quad x(0) = x_0$$
    $$g(x(t), u(t)) \le 0, \quad \psi(x(T)) = 0$$
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Компоненты функционала Больца:</h3>
    <ul class="text-sm">
      <li>$L(x, u)$ — текущие затраты (Running Cost / Lagrangian): расход энергии моторов $\int u^2 dt$, квадрат ошибки слежения $\|x - x_{ref}\|^2$, штраф за время.</li>
      <li>$\Phi(x(T))$ — терминальные затраты (Terminal Cost): точность достижения целевой точки $q_{goal}$ в момент $T$.</li>
      <li>$\dot{x} = f(x, u)$ — уравнения движения (неголономная кинематика или динамика шасси).</li>
      <li>$g(x, u) \le 0$ — ограничения на угол поворота колес $|\delta| \le \delta_{max}$, токи моторов, стены коридора.</li>
    </ul>
  </div>
</div>

</div>

---

## 2. Принцип максимума Понтрягина (ПМП) <span class="badge badge-time">12–25 мин</span>

<div class="grid-2">

<div class="col">
  <p>Для оптимизации вводится <strong>функция Гамильтона (Гамильтониан)</strong> с вектором сопряженных переменных $\lambda(t) \in \mathbb{R}^n$ (множители Лагранжа к динамике):</p>

  <div class="formula-box text-sm">
    $$H(x, u, \lambda) = L(x, u) + \lambda^T f(x, u)$$
  </div>

  <div class="card card-alert text-sm">
    <strong>Физический смысл $\lambda(t)$ (Costate):</strong> сопряженная переменная показывает чувствительность минимальной стоимости к возмущению состояния: $\lambda(t) = \nabla_x J^*(x, t)$.
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Необходимые условия экстремума (ПМП):</h3>
    <ol class="text-sm">
      <li><strong>Уравнения состояния:</strong> $\dot{x}(t) = \frac{\partial H}{\partial \lambda} = f(x(t), u(t))$.</li>
      <li><strong>Сопряженная система:</strong> $\dot{\lambda}(t) = -\frac{\partial H}{\partial x} = -\frac{\partial L}{\partial x} - \left(\frac{\partial f}{\partial x}\right)^T \lambda(t)$.</li>
      <li><strong>Условие минимума по управлению:</strong> оптимальное управление в каждый момент времени доставляет абсолютный минимум Гамильтониану:
        $$u^*(t) = \arg\min_{u \in \mathcal{U}} H(x^*(t), u, \lambda^*(t))$$
      </li>
      <li><strong>Условие трансверсальности:</strong> $\lambda(T) = \nabla_x \Phi(x(T))$.</li>
    </ol>
  </div>
</div>

</div>

---

## 3. Релейное управление (Bang-Bang Control) <span class="badge badge-time">25–35 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Линейность по управлению (Control-Affine Systems):</h3>
    <p class="text-sm">В большинстве мобильных роботов управление входит линейно: $\dot{x} = f_0(x) + f_1(x) u$, а цель — минимизация времени $L(x, u) = 1$ при $|u| \le u_{max}$.</p>
    <p class="text-sm">Тогда Гамильтониан имеет вид:</p>
    $$H = 1 + \lambda^T f_0(x) + \underbrace{\left(\lambda^T f_1(x)\right)}_{\sigma(t)} u$$
    <p class="text-sm">где $\sigma(t) = \lambda(t)^T f_1(x(t))$ называется <strong>функцией переключения (Switching Function)</strong>.</p>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Релейный закон оптимального управления:</h3>
    <p class="text-sm">Чтобы минимизировать $H$, управление должно мгновенно принимать экстремальные граничные значения в зависимости от знака $\sigma(t)$:</p>
    $$u^*(t) = -u_{max} \operatorname{sign}(\sigma(t)) = \begin{cases} +u_{max}, & \sigma(t) < 0 \\ -u_{max}, & \sigma(t) > 0 \end{cases}$$
    <div class="card-success text-sm mt-2">
      <strong>Вывод быстродействия:</strong> Самое быстрое перемещение робота — это всегда <em>предельный разгон</em> на максимум тяги с последующим <em>предельным торможением</em> «в пол» (Bang-Bang маневр).
    </div>
  </div>
</div>

</div>

---

## 4. Кривые Дубинса и Ридса-Шеппа (LaValle гл. 15) <span class="badge badge-time">35–48 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Автомобиль Дубинса (Dubins, 1957):</h3>
    <p class="text-sm">Модель движения только вперед ($v = 1$) с ограниченной кривизной $|\dot{\theta}| \le u_{max} = 1/\rho_{min}$:</p>
    $$\dot{x} = \cos\theta, \quad \dot{y} = \sin\theta, \quad \dot{\theta} = u, \quad u \in [-u_{max}, u_{max}]$$
    <p class="text-sm">Из ПМП доказано (Sussmann & Tang 1991): кратчайший путь между любыми двумя позами $(x, y, \theta)$ состоит ровно из <strong>3 сегментов</strong> из набора $\{L, R, S\}$:</p>
    <ul class="text-sm">
      <li><strong>Круговой поворот влево $L$:</strong> $u = +u_{max}$ (дуга окружности).</li>
      <li><strong>Круговой поворот вправо $R$:</strong> $u = -u_{max}$ (дуга окружности).</li>
      <li><strong>Прямолинейный отрезок $S$:</strong> $u = 0$ (прямая линия).</li>
    </ul>
    <p class="text-sm">Существует ровно 6 оптимальных семейств: <strong>$LSL, RSR, LSR, RSL, LRL, RLR$</strong>.</p>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Кривые Ридса-Шеппа (Reeds & Shepp, 1990):</h3>
    <p class="text-sm">Разрешено движение вперед и назад: $v \in \{-1, +1\}$.</p>
    <ul class="text-sm">
      <li>Оптимальные слова содержат смену направления (Cusp): $L^+ S^- R^+$.</li>
      <li>Всего выделено <strong>46 оптимальных комбинаций</strong> в 9 семействах.</li>
      <li>Используются в парковочных автопилотах и складских AGV.</li>
    </ul>
    <div class="formula-box text-sm">
      $$\text{Слова RS: } \{ C|C|C, \;\; CC|C, \;\; CSC, \;\; C|CSC, \dots \}$$
    </div>
    <div class="card-success text-sm">
      <strong>Применение:</strong> Аналитический вызов функции Дубинса/Ридса-Шеппа работает за <strong>$< 1$ микросекунды</strong> и служит идеальным локальным планировщиком для RRT* и Hybrid $A^*$.
    </div>
  </div>
</div>

</div>

---

## 5. Динамическое программирование и LQR <span class="badge badge-time">48–60 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Уравнение Гамильтона–Якоби–Беллмана (HJB):</h3>
    <p class="text-sm">Функция оптимальных затрат (Value function) $V(x, t) = \min_u \int_t^T L dt + \Phi$ удовлетворяет дифференциальному уравнению в частных производных:</p>
    $$-\frac{\partial V}{\partial t} = \min_{u \in \mathcal{U}} \left( L(x, u) + \nabla_x V(x, t)^T f(x, u) \right)$$
    <p class="text-sm">Для бесконечного горизонта $\partial V / \partial t = 0$.</p>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Линейно-квадратичный регулятор (LQR):</h3>
    <p class="text-sm">Для линейной системы $\dot{x} = A x + B u$ и квадратичного функционала $L = x^T Q x + u^T R u$ решение HJB ищется в виде $V(x) = x^T P x$:</p>
    <div class="formula-box text-sm">
      $$A^T P + P A - P B R^{-1} B^T P + Q = 0 \quad \text{(CARE)}$$
    </div>
    <p class="text-sm">Решив матричное алгебраическое уравнение Риккати относительно матрицы $P \succ 0$, получаем <strong>оптимальную линейную обратную связь</strong>:</p>
    $$u^*(t) = -K x(t), \quad K = R^{-1} B^T P$$
  </div>
</div>

</div>

---

## 6. Численная оптимизация: Shooting vs Direct Collocation <span class="badge badge-time">60–72 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-alert">
    <h3>Прямая стрельба (Single Shooting):</h3>
    <p class="text-sm">Оптимизируются только управляющие воздействия $u_0, u_1, \dots, u_{N-1}$. Состояния $x_k$ вычисляются прямым интегрированием вперед.</p>
    <ul class="text-sm">
      <li><strong>Плюс:</strong> малое число оптимизационных переменных ($m \times N$).</li>
      <li><strong>Минус:</strong> крайняя неустойчивость: малое изменение $u_0$ вызывает экспоненциальное отклонение $x_N$ в конце траектории. Градиенты в нелинейных системах «взрываются».</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Прямая коллокация (Direct Collocation):</h3>
    <p class="text-sm">И состояния $x_k$, и управления $u_k$ объявляются переменными оптимизации в узлах сетки (Метод Эрмита–Симпсона):</p>
    $$\dot{x}_{col} = f\left(x_{k+1/2}, u_{k+1/2}\right) = \frac{x_{k+1} - x_k}{\Delta t_k}$$
    <ul class="text-sm">
      <li><strong>Плюс:</strong> динамика системы формулируется как локальные алгебраические равенства.</li>
      <li><strong>Ключевое свойство:</strong> Якобиан и Гессиан задачи имеют <strong>блочно-диагональную разреженную структуру</strong>!</li>
      <li>Решается за десятки миллисекунд методами внутренней точки (Interior Point, солвер <code>IPOPT</code>).</li>
    </ul>
  </div>
</div>

</div>

---

## 7. Слежение за траекторией: Time-Varying LQR (TVLQR) <span class="badge badge-time">72–82 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Линеаризация вдоль опорной траектории:</h3>
    <p class="text-sm">Пусть Direct Collocation вернул номинальную пару $\left(x_{nom}(t), u_{nom}(t)\right)$. Определим отклонения (ошибки слежения):</p>
    $$\delta x(t) = x(t) - x_{nom}(t), \quad \delta u(t) = u(t) - u_{nom}(t)$$
    <p class="text-sm">Линеаризованная динамика в отклонениях становится нестационарной:</p>
    $$\delta \dot{x}(t) = A(t) \delta x(t) + B(t) \delta u(t)$$
    $$A(t) = \left.\frac{\partial f}{\partial x}\right|_{(x_{nom}, u_{nom})}, \quad B(t) = \left.\frac{\partial f}{\partial u}\right|_{(x_{nom}, u_{nom})}$$
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Дифференциальное уравнение Риккати (DRE):</h3>
    <p class="text-sm">Интегрируется <em>назад во времени</em> от $t = T$ до $t = 0$ с условием $P(T) = Q_f$:</p>
    $$-\dot{P}(t) = A^T(t) P(t) + P(t) A(t) - P(t) B(t) R^{-1} B^T(t) P(t) + Q$$
    <p class="text-sm">Результирующее управление на борту мобильного робота:</p>
    <div class="formula-box text-sm">
      $$u^*(t) = u_{nom}(t) - K(t) \left(x(t) - x_{nom}(t)\right)$$
    </div>
    <div class="card-success text-sm">
      <strong>Гарантия:</strong> TVLQR обеспечивает локальную асимптотическую устойчивость и удерживает шасси в безопасной трубке вокруг траектории даже при возмущениях.
    </div>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 05 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">82–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol class="text-sm">
    <li><strong>Оптимальное управление</strong> минимизирует функционал потерь $J$ при строгом соблюдении дифференциальных ограничений робота $\dot{x} = f(x, u)$.</li>
    <li><strong>ПМП Понтрягина</strong> связывает динамику состояния с сопряженной системой через Гамильтониан $H$.</li>
    <li><strong>Кривые Дубинса и Ридса-Шеппа</strong> представляют аналитическое решение задачи быстродействия для колесного шасси.</li>
    <li><strong>Direct Collocation</strong> транскрибирует непрерывную задачу в разреженную NLP, решаемую солвером IPOPT.</li>
    <li><strong>TVLQR</strong> стабилизирует движение вокруг найденной оптимальной траектории.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы для самопроверки:</h3>
  <ul class="text-sm">
    <li>Какой физический смысл имеют сопряженные переменные $\lambda(t)$ в принципе максимума Понтрягина?</li>
    <li>Почему в задаче быстродействия с линейным входом управление всегда является кусочно-постоянным (Bang-Bang)?</li>
    <li>Почему кривая Дубинса не всегда является кратчайшим путем, если роботу разрешено сдавать назад?</li>
    <li>В чем фундаментальное преимущество Direct Collocation перед Single Shooting при численной оптимизации нелинейных траекторий?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Предиктивное управление (Model Predictive Control — MPC)</span>
  </div>
</div>

</div>
