---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 05"
footer: "Курс лекций • Лекция 05"
math: katex
---

---

<!-- _class: lead -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 05: Оптимальное управление: от принципа максимума Понтрягина к численному OCP и MPC

<div class="mt-4">

<span class="badge badge-blue">⏱️ 90 минут</span>
<span class="badge badge-green">Фундаментальные основы и прикладной стек</span>
<span class="badge badge-purple">ПМП • Bang-Bang • LQR • Direct Collocation • SQP • IPOPT • MPC</span>

</div>

---

## Введение: Переход от эвристического планирования к вариационной оптимизации

<div class="grid-2">
<div class="col">
<div class="card card-accent">
  <strong>Ограничения методов поиска ($A^*$, RRT)</strong>
  <ul>
    <li>Генерируемые пути представляют собой геометрические кривые, игнорирующие дифференциальные связи.</li>
    <li>Дискретизация фазового пространства вносит существенную вычислительную сложность при росте размерности (Curse of Dimensionality).</li>
    <li>Отсутствие строгого учета ограничений на управляющие воздействия (моменты, силы).</li>
  </ul>
</div>
</div>
<div class="col">
<div class="card card-success">
  <strong>Вариационная постановка (OCP)</strong>
  <ul>
    <li>Переход от дискретного графа к непрерывному функциональному пространству $\mathcal{H}$.</li>
    <li>Управление рассматривается как непрерывная функция времени $u(t)$, формирующая траекторию состояния $x(t)$.</li>
    <li>Обеспечение строгой оптимальности в смысле заданного функционала при соблюдении уравнений динамики.</li>
  </ul>
</div>
</div>
</div>

---

## План лекции (90 минут)

<div class="grid-2">
<div class="col">
<div class="card card-accent">
  <strong>Часть 1: Аналитический синтез и ПМП (40 мин)</strong>
  <ul>
    <li>Постановка задачи оптимального управления (OCP).</li>
    <li>Неприменимость классического вариационного исчисления.</li>
    <li>Принцип максимума Понтрягина (ПМП) и функция Гамильтона.</li>
    <li>Аналитический синтез задачи быстродействия для двойного интегратора.</li>
    <li>Сопоставление законов Bang-Bang и LQR.</li>
  </ul>
</div>
</div>
<div class="col">
<div class="card card-success">
  <strong>Часть 2: Численный OCP и MPC (50 мин)</strong>
  <ul>
    <li>Пределы аналитического синтеза в робототехнике.</li>
    <li>Парадигма прямой транскрипции (Direct Transcription).</li>
    <li>Методы дискретизации динамики (Shooting, Collocation).</li>
    <li>Алгоритмы нелинейного программирования (NLP).</li>
    <li>Управление с прогнозирующей моделью (MPC) и Real-Time Iteration (RTI).</li>
  </ul>
</div>
</div>
</div>

---

## 1. Постановка задачи оптимального управления (OCP)

<div class="grid-2">
<div class="col">
  <p>Форма Больца для функционала стоимости:</p>
  $$ J(x(\cdot), u(\cdot)) = \Phi(x(t_f), t_f) + \int_{t_0}^{t_f} L(x(t), u(t), t) dt \to \min_{u(\cdot)} $$
  <p>где $\Phi$ — терминальный штраф (штраф Майера), $L$ — интегральный штраф (штраф Лагранжа).</p>
</div>
<div class="col">
<div class="card card-accent">
  <strong>Динамические и алгебраические ограничения</strong>
  <ul>
    <li>Уравнения динамики в форме Коши:
      $$ \dot{x}(t) = f(x(t), u(t), t), \quad x(t_0) = x_0 $$
    </li>
    <li>Компактное множество допустимых управлений:
      $$ u(t) \in \mathcal{U} \subset \mathbb{R}^m $$
      <em>(Например, $|u_i(t)| \le U_{max}$)</em>
    </li>
    <li>Терминальные условия: $\Psi(x(t_f)) = 0$.</li>
  </ul>
</div>
</div>
</div>

---

## 2. Неприменимость классического вариационного исчисления

<div class="grid-2">
<div class="col">
<div class="card card-alert">
  <strong>Проблема границ компакта $\mathcal{U}$</strong>
  <ul>
    <li>Классическое вариационное исчисление (уравнения Эйлера-Лагранжа) предполагает открытость множества допустимых вариаций.</li>
    <li>Необходимое условие $\nabla_u \mathcal{L} = 0$ невыполнимо, если глобальный экстремум достигается на границе замкнутого компакта $\mathcal{U}$.</li>
  </ul>
</div>
</div>
<div class="col">
<div class="card card-accent">
  <strong>Метод игольчатых вариаций</strong>
  <ul>
    <li>Динамика механических систем часто аффинна по управлению: $f(x, u) = a(x) + B(x)u$.</li>
    <li>Л. С. Понтрягин предложил класс «игольчатых» вариаций: сильные возмущения управления на бесконечно малом интервале времени $\Delta t \to 0$.</li>
  </ul>
</div>
</div>
</div>

---

## Поиск экстремума: Классический подход vs ПМП

<div class=\"diagram-box\">

<img src=\"../../assets/images/lecture-05/calculus_of_variations_vs_pmp.svg\" alt=\"Вариационное исчисление и ПМП\" />

</div>

---

## 3. Принцип максимума Понтрягина (ПМП)

Определим <strong>функцию Гамильтона-Понтрягина</strong> (Гамильтониан):
$$ \mathcal{H}(x, u, \lambda, t) = -L(x, u, t) + \lambda^T f(x, u, t) $$
<em>(В русскоязычной литературе часто используется форма без минуса при $L$, тогда говорят о «Принципе минимума», но физический смысл не меняется).</em>

<div class="card card-success">
  <strong>Формулировка теоремы (ПМП)</strong>
  <p>Пусть $u^*(t)$ — оптимальное управление, а $x^*(t)$ — соответствующая ему оптимальная траектория. Тогда существует ненулевая непрерывная вектор-функция сопряженных переменных $\lambda(t)$, такая что для почти всех $t \in [t_0, t_f]$ функция Гамильтона достигает <strong>глобального максимума</strong> по $u$ на множестве $\mathcal{U}$:</p>
  $$ \mathcal{H}(x^*(t), u^*(t), \lambda(t), t) = \max_{u \in \mathcal{U}} \mathcal{H}(x^*(t), u, \lambda(t), t) $$
</div>

---

## 4. Сопряженные переменные $\lambda(t)$ как теневые цены

<div class="grid-2">
<div class="col">
  <strong>Экономическая и физическая интерпретация</strong>
  <ul>
    <li>Сопряженный вектор $\lambda(t)$ формализует чувствительность оптимального функционала стоимости $J^*$ к возмущениям фазового состояния $x(t)$:
      $$ \lambda_i(t) = -\frac{\partial J^*}{\partial x_i} $$
    </li>
    <li>Это аналог «множителей Лагранжа» для динамических ограничений $\dot{x} = f(x,u)$.</li>
  </ul>
</div>
<div class="col">
<div class="card card-accent">
  <strong>Функция переключения $\sigma(t)$</strong>
  <ul>
    <li>При аффинной динамике Гамильтониан линеен по $u$: $\mathcal{H} = \dots + \sigma(t)^T u$.</li>
    <li>Вектор $\sigma(t) = B(x)^T \lambda$ называется функцией переключения. Он однозначно определяет знак и структуру оптимального управления на границе $\mathcal{U}$.</li>
  </ul>
</div>
</div>
</div>

---

## 5. Каноническая система условий оптимальности

<div class="card card-success">
  Оптимальная траектория $(x^*, \lambda^*)$ удовлетворяет системе Гамильтоновых дифференциальных уравнений (краевая задача):
</div>

<div class="grid-2">
<div class="col">
  <strong>1. Уравнения состояния:</strong>
  $$ \dot{x} = \frac{\partial \mathcal{H}}{\partial \lambda} = f(x, u) $$
  <strong>2. Сопряженные уравнения:</strong>
  $$ \dot{\lambda} = -\frac{\partial \mathcal{H}}{\partial x} = \frac{\partial L}{\partial x} - \left( \frac{\partial f}{\partial x} \right)^T \lambda $$
</div>
<div class="col">
  <strong>3. Условия трансверсальности</strong> (при свободном правом конце):
  $$ \lambda(t_f) = -\frac{\partial \Phi}{\partial x}(x(t_f)) $$
  <strong>4. Условие максимума:</strong>
  $$ u^* = \arg\max_{u \in \mathcal{U}} \mathcal{H}(x, u, \lambda) $$
</div>
</div>
<p style="margin-top: 1rem;"><em>Данная система образует двухточечную краевую задачу (Two-Point Boundary Value Problem, TPBVP), аналитическое решение которой возможно лишь для узкого класса систем.</em></p>

---

## 6. Аналитический синтез: Задача быстродействия

<div class="grid-2">
<div class="col">
  <strong>Объект: Двойной интегратор</strong>
  <p>Модель материальной точки массы $m=1$, управляемой ограниченной силой:</p>
  $$ \ddot{x} = u, \quad |u| \le 1 $$
  <p>Переход к пространству состояний ($x_1 = x, x_2 = \dot{x}$):</p>
  $$ \begin{cases} \dot{x}_1 = x_2 \\ \dot{x}_2 = u \end{cases} $$
</div>
<div class="col">
<div class="card card-accent">
  <strong>Постановка задачи</strong>
  <p>Перевести систему из начального состояния $(x_{10}, x_{20})$ в начало координат $(0, 0)$ за <strong>минимальное время</strong>:</p>
  $$ J = \int_{0}^{t_f} 1 dt = t_f \to \min $$
  <p>Здесь $L \equiv 1$, $\Phi \equiv 0$.</p>
</div>
</div>
</div>

---

## 7. Вывод релейного закона управления (Bang-Bang)

<div class="grid-2">
<div class="col">
  <p>Формируем функцию Гамильтона:</p>
  $$ \mathcal{H} = -1 + \lambda_1 x_2 + \lambda_2 u $$
  <p>Применяем условие максимума ПМП по $u \in [-1, 1]$:</p>
  $$ \max_{|u| \le 1} (\lambda_2 u) $$
</div>
<div class="col">
<div class="card card-success">
  <strong>Закон Bang-Bang</strong>
  <p>Максимум линейной функции на отрезке всегда достигается на его границах (при $\lambda_2 \neq 0$):</p>
  $$ u^*(t) = \operatorname{sign}(\lambda_2(t)) $$
  <p>Оптимальное управление является кусочно-постоянным, принимая лишь предельные значения $+1$ и $-1$.</p>
</div>
</div>
</div>

---

## 8. Теорема Фельдбаума об $n$ интервалах

<div class="grid-2">
<div class="col">
  <strong>Анализ сопряженной системы</strong>
  $$ \dot{\lambda}_1 = -\frac{\partial \mathcal{H}}{\partial x_1} = 0 \implies \lambda_1(t) = C_1 $$
  $$ \dot{\lambda}_2 = -\frac{\partial \mathcal{H}}{\partial x_2} = -\lambda_1 \implies \lambda_2(t) = -C_1 t + C_2 $$
  <p>Функция переключения $\lambda_2(t)$ является <em>линейной (аффинной)</em>.</p>
</div>
<div class="col">
<div class="card card-alert">
  <strong>Число переключений</strong>
  <ul>
    <li>Линейная функция $\lambda_2(t) = -C_1 t + C_2$ имеет <strong>не более одного корня</strong> на $(0, \infty)$.</li>
    <li>Следовательно, управление $u^*(t) = \operatorname{sign}(\lambda_2(t))$ меняет знак не более 1 раза.</li>
    <li>Траектория состоит максимум из 2 участков: разгон и интенсивное торможение.</li>
  </ul>
</div>
</div>
</div>

---

## 9. Фазовая плоскость и кривая переключения $\Gamma$

<div class="grid-2">
<div class="col">
  <p>Интегрируя систему при $u = \pm 1$, получаем семейства парабол в фазовой плоскости $(x_1, x_2)$:</p>
  $$ x_1 - \frac{1}{2u} x_2^2 = C $$
  <p>Траектории, ведущие точно в начало координат, образуют кривую переключения $\Gamma = \Gamma_+ \cup \Gamma_-$:</p>
  $$ \Gamma: x_1 + \frac{1}{2} x_2 |x_2| = 0 $$
</div>
<div class="col">
<div class="card card-accent">
  <strong>Синтез позиционного управления</strong>
  <p>Обратная связь по состоянию $u(x_1, x_2)$:</p>
  $$ u^*(x_1, x_2) = \begin{cases} -1, & x_1 > -\frac{1}{2} x_2 |x_2| \\ +1, & x_1 < -\frac{1}{2} x_2 |x_2| \\ -\operatorname{sign}(x_2), & (x_1, x_2) \in \Gamma \end{cases} $$
  <p>На кривой $\Gamma$ управление удерживает систему в скользящем режиме до достижения начала координат.</p>
</div>
</div>
</div>

---

## Фазовая плоскость задачи быстродействия

<div class=\"diagram-box\">

<img src=\"../../assets/images/lecture-05/bang_bang_phase_plane.svg\" alt=\"Фазовая плоскость Bang-Bang\" />

</div>

---

## 10. Квадратичный критерий и регулятор LQR

<div class="grid-2">
<div class="col">
  <strong>Линейно-Квадратичный Регулятор</strong>
  <p>Отсутствие жестких границ $\mathcal{U}$, интегральный штраф на энергию:</p>
  $$ J_{LQR} = \frac{1}{2}\int_0^\infty (x^T Q x + u^T R u) dt $$
  <p>Гамильтониан строго вогнут по $u$:</p>
  $$ \frac{\partial \mathcal{H}}{\partial u} = -R u + B^T \lambda = 0 $$
  <p>Решение Риккати дает: $u = -K x$.</p>
</div>
<div class="col">
<div class="card card-accent">
  <strong>Bang-Bang vs LQR</strong>
  <ul>
    <li><strong>Bang-Bang:</strong> Строго минимальное время, разрывная функция $u(t)$, ударные нагрузки на редуктор, риск <em>chattering</em> (высокочастотных переключений) при шумах.</li>
    <li><strong>LQR:</strong> Гладкий ПД-закон, бесконечное время сходимости (асимптотическая устойчивость), минимум энергетических затрат.</li>
  </ul>
</div>
</div>
</div>

---

## Интерактивный симулятор: Фазовая плоскость

<div class="interactive-container">

<div class="interactive-header">

<span><i class="interactive-dot"></i> Интерактивная симуляция контура управления</span>
<span>Исследование фазовых портретов и параметров оптимизации</span>

</div>
<iframe src="http://localhost:5599/widgets/bang-bang-simulator/index.html" class="interactive-frame"></iframe>

</div>

---

## 11. Пределы аналитического синтеза в робототехнике

<div class="grid-2">
<div class="col">
<div class="card card-alert">
  <strong>Барьеры размерности и нелинейности</strong>
  <ul>
    <li>Аналитический синтез (TPBVP) разрешим лишь для систем размерности $n \le 3$. Для роботов $n \ge 4$ (напр., квадрокоптер $n=12$) замкнутых решений нет.</li>
    <li>Нелинейные эффекты Кориолиса и гироскопические моменты делают $\dot{\lambda}$ неинтегрируемым в квадратурах.</li>
  </ul>
</div>
</div>
<div class="col">
<div class="card card-alert">
  <strong>Ограничения фазового пространства (Препятствия)</strong>
  <ul>
    <li>Наличие невыпуклых препятствий $h(x) \le 0$ требует введения разрывных множителей Лагранжа в точках входа на границу.</li>
    <li>Количество и порядок точек переключения становятся a priori неизвестными.</li>
    <li><strong>Необходим переход к численным методам оптимизации.</strong></li>
  </ul>
</div>
</div>
</div>

---

## 12. Парадигма прямой транскрипции (Direct Transcription)

<div class="grid-2">
<div class="col">
  <strong>Непрямые методы (Indirect)</strong>
  <ul>
    <li>«First Optimize, then Discretize».</li>
    <li>Основаны на ПМП: составляется TPBVP, которая затем решается численно.</li>
    <li>Крайне узкая область сходимости из-за высокой чувствительности к начальному приближению $\lambda(0)$ (которое не имеет интуитивного физического смысла).</li>
  </ul>
</div>
<div class="col">
<div class="card card-success">
  <strong>Прямые методы (Direct)</strong>
  <ul>
    <li>«First Discretize, then Optimize».</li>
    <li>Бесконечномерная задача вариационного исчисления сводится к конечномерной задаче нелинейного программирования (NLP).</li>
    <li>Оптимизация ведется непосредственно в пространстве состояний $X$ и управлений $U$, что упрощает задание начального приближения (warm-start).</li>
  </ul>
</div>
</div>
</div>

---

## 13. Методы дискретизации динамики

<div class="grid-2">
<div class="col">
  <strong>1. Single Shooting (Однократная стрельба)</strong>
  <ul>
    <li>$U$ дискретизируется, $X$ вычисляется интегратором (напр. RK4) как функция $X(U)$.</li>
    <li>Мало переменных NLP, но высокая плотность Якобиана. Сильно подвержен экспоненциальной неустойчивости интегрирования.</li>
  </ul>
  <strong>2. Multiple Shooting (Многократная стрельба)</strong>
  <ul>
    <li>Горизонт бьется на узлы. В каждом узле свое начальное состояние $x_k$ и управление $u_k$.</li>
    <li>Вводятся <em>дефекты неразрывности</em>: $x_{k+1} - F(x_k, u_k) = 0$.</li>
    <li>Высокая робастность к неустойчивости динамики.</li>
  </ul>
</div>
<div class="col">
<div class="card card-accent">
  <strong>3. Direct Collocation (Прямая коллокация)</strong>
  <ul>
    <li>Траектории $X(t)$ и $U(t)$ аппроксимируются полиномами (часто полиномами Лагранжа).</li>
    <li>Производная аппроксимации приравнивается к функции динамики в точках коллокации (корни ортогональных полиномов).</li>
    <li>Максимальное количество переменных, но предельно разреженная структура матриц (Sparsity).</li>
  </ul>
</div>
</div>
</div>

---

## 14. Численные алгоритмы NLP

Стандартная форма NLP: $\min_{w} F(w) \quad \text{s.t.} \quad G(w) = 0, \quad H(w) \le 0$

<div class="grid-2">
<div class="col">
  <strong>Методы внутренней точки (Interior Point)</strong>
  <ul>
    <li>Неравенства $H(w) \le 0$ заменяются логарифмическими барьерами в целевой функции $\mu \sum \ln(-H_i(w))$.</li>
    <li>Барьерный параметр $\mu \to 0$ последовательно уменьшается.</li>
    <li>Примеры: <strong>IPOPT</strong>, <strong>FATROP</strong>. Отлично работают для задач огромной размерности, но не поддерживают warm-start для активного набора (active set).</li>
  </ul>
</div>
<div class="col">
<div class="card card-accent">
  <strong>Последовательное квадратичное программирование (SQP)</strong>
  <ul>
    <li>На каждом шаге NLP локально аппроксимируется квадратичной задачей (QP) с линеаризацией ограничений.</li>
    <li>Решение QP дает шаг Ньютона $\Delta w$.</li>
    <li>Примеры: <strong>SNOPT</strong>, <strong>acados (SQP-RTI)</strong>. Идеально подходят для MPC благодаря эффективному использованию warm-start.</li>
  </ul>
</div>
</div>
</div>

---

## 15. Программный стек дифференцируемой оптимизации

<div class="grid-2">
<div class="col">
<div class="card card-accent">
  <strong>Символьные градиенты и AD</strong>
  <ul>
    <li>Современные NLP-солверы (на основе метода Ньютона) требуют точного вычисления Якобианов $\nabla G(w)$ и Гессианов $\nabla^2 \mathcal{L}_{NLP}$.</li>
    <li>Численное дифференцирование (конечные разности) неприемлемо из-за вычислительных затрат $\mathcal{O}(N^2)$ и потери точности.</li>
    <li>Используется Алгоритмическое Дифференцирование (AD).</li>
  </ul>
</div>
</div>
<div class="col">
  <strong>CasADi (Символьный фреймворк)</strong>
  <ul>
    <li>Граф вычислений строится на основе символьных примитивов (SX, MX).</li>
    <li>Реализует прямое (Forward AD) и обратное (Reverse AD) дифференцирование.</li>
    <li>Экспортирует графы в оптимизированный C-код для компиляции в реальном времени.</li>
    <li><strong>L4CasADi:</strong> Интеграция нейросетевых моделей PyTorch/JAX непосредственно в OCP пайплайн CasADi.</li>
  </ul>
</div>
</div>

---

## 16. Управление с прогнозирующей моделью (MPC)

<div class="card card-success">
  <strong>Принцип скользящего горизонта (Receding Horizon Control)</strong>
  <p>Решение OCP в реальном времени используется для замыкания контура обратной связи:</p>
  <ol>
    <li>Измерение текущего состояния робота $x(t)$.</li>
    <li>Решение локальной задачи NLP на конечном горизонте прогноза $T_p$. Учет локальных препятствий (напр. через Safe Flight Corridors, SFC).</li>
    <li>Из полученной оптимальной траектории управления $u^*(t)$ к объекту применяется только <strong>первое значение</strong> $u^*(t_0)$.</li>
    <li>Сдвиг горизонта на шаг дискретизации $\Delta t$ и повторение цикла.</li>
  </ol>
</div>
<p style="margin-top: 1rem;">MPC объединяет преимущества оптимального планирования с робастностью обратной связи к неконтролируемым возмущениям.</p>

---

## 17. Реализация в реальном времени: RTI (Real-Time Iteration)

<div class="grid-2">
<div class="col">
<div class="card card-alert">
  <strong>Проблема задержки вычислений</strong>
  <ul>
    <li>Решение полного NLP на борту робота (до сходимости критериев KKT) требует слишком много времени, что недопустимо для частот контура 50–100 Гц.</li>
    <li>Отставание фазы приводит к потере устойчивости системы.</li>
  </ul>
</div>
</div>
<div class="col">
<div class="card card-accent">
  <strong>Схема RTI (Диль, 2001)</strong>
  <ul>
    <li>Выполнение лишь <strong>одной итерации SQP</strong> на каждом такте управления (без ожидания сходимости).</li>
    <li><strong>Фаза подготовки:</strong> Линеаризация динамики и ограничений вдоль предыдущей траектории (до получения нового измерения $x(t)$). Выполняется асинхронно.</li>
    <li><strong>Фаза обратной связи:</strong> Моментальное решение QP после получения $x(t)$.</li>
  </ul>
</div>
</div>
</div>

---

## Интерактивный симулятор: Нелинейный предиктивный контур (NMPC)

<div class="interactive-container">

<div class="interactive-header">

<span><i class="interactive-dot"></i> Интерактивная симуляция контура управления</span>
<span>Исследование фазовых портретов и параметров оптимизации</span>

</div>
<iframe src="http://localhost:5599/widgets/mpc-interactive-solver/index.html" class="interactive-frame"></iframe>

</div>

---

## Резюме лекции: Системная иерархия планирования

<div class="card card-success" style="text-align: center;">
  <strong>Современная архитектура автономности</strong>
</div>

<div class="grid-2">
<div class="col">
  <ul>
    <li><strong>Глобальный поиск (Global Planner):</strong> $A^*$, RRT*, Lattice. Решает задачу навигации в лабиринте, игнорируя точную динамику. Выход: грубый путь или набор коридоров (SFC).</li>
    <li><strong>Локальное планирование (NMPC / OCP):</strong> Оптимизирует траекторию внутри коридоров, учитывая строгие ограничения на кинематику, динамику и предельные возможности приводов (напр. CasADi + acados).</li>
  </ul>
</div>
<div class="col">
  <ul>
    <li><strong>Исполнительный уровень (Low-Level Control):</strong> Высокочастотные контроллеры (PID, LQR, WBC - Whole-Body Control), стабилизирующие робота вокруг траектории NMPC, подавляя высокочастотные шумы сенсоров и модельные неопределенности.</li>
  </ul>
</div>
</div>

---

## Рекомендуемая академическая литература

<div class="grid-2">
<div class="col">
  <strong>Фундаментальная теория (Аналитика)</strong>
  <ul>
    <li>Понтрягин Л. С., Болтянский В. Г. и др. <em>«Математическая теория оптимальных процессов»</em>.</li>
    <li>Черноусько Ф. Л., Баничук Н. В. <em>«Вариационные задачи механики и управления»</em>.</li>
    <li>Kirk, D. E. <em>«Optimal Control Theory: An Introduction»</em> (Dover Books).</li>
  </ul>
</div>
<div class="col">
  <strong>Современные численные методы и MPC</strong>
  <ul>
    <li>Rawlings, J. B., Mayne, D. Q., Diehl, M. <em>«Model Predictive Control: Theory, Computation, and Design»</em>.</li>
    <li>Tedrake, R. <em>«Underactuated Robotics»</em> (MIT Course Notes).</li>
    <li>Документация и статьи по фреймворкам: <strong>CasADi</strong>, <strong>acados</strong>, <strong>Crocoddyl</strong>.</li>
  </ul>
</div>
</div>
