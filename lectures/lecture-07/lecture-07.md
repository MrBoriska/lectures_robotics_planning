---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 07"
footer: "Курс лекций • Лекция 07 • Слайд %PAGE% из %TOTAL%"
math: mathjax
---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 07: Учёт ограничений в алгоритмах планирования

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Физические ограничения</span>
  <span class="badge badge-purple">LaValle (гл. 13, 14) • Скобки Ли • Chow-Rashevsky • Трение • TOPP</span>
</div>

---

<!-- _header: "Лекция 07 | Введение и мотивация" -->

## Чему посвящена эта лекция? <span class="badge badge-blue">Физика и связи</span>

<div class="grid-2 mt-2">

<div class="card card-accent">
  <h3>🎯 Робот — это физическое тело, а не точка</h3>
  <p class="text-sm">
    В теории алгоритмов часто представляют робота всемогущей точкой, способной мгновенно двигаться в любом направлении с бесконечным ускорением. На практике колеса не умеют ехать боком, приводы имеют предел момента, а шины срываются в занос на поворотах.
  </p>
  <p class="text-sm">
    Эта лекция посвящена <strong>математике и учету физических ограничений</strong>: как дифференциальная геометрия (скобки Ли) доказывает управляемость неголономных систем и как динамические пределы сцепления превращают путь в физически реализуемую траекторию.
  </p>
</div>

<div class="card">
  <h3>🔍 Ключевые вопросы лекции</h3>
  <ul class="text-sm">
    <li><strong>Голономность vs Неголономность:</strong> Форма связей Пфаффа и теорема Фробениуса об интегрируемости.</li>
    <li><strong>Магия скобок Ли (Lie Brackets):</strong> Почему автомобиль может смещаться вбок при параллельной парковке? Условие ранга алгебры Ли (<strong>LARC</strong>).</li>
    <li><strong>Дискретизация неголономных систем:</strong> Решетки состояний (<strong>State Lattices</strong>) и примитивы движения.</li>
    <li><strong>Террамеханика и пределы сцепления:</strong> Круг трения Кулона, ограничение центростремительного ускорения $a_y \le \mu g$.</li>
    <li><strong>Оптимальный профиль скорости (TOPP):</strong> Как выжать 100% мощности моторов на заданной траектории.</li>
  </ul>
</div>

</div>

<div class="card card-success mt-2">
  <h3 style="margin-bottom: 4px;">💡 Чему вы научитесь за эти 90 минут</h3>
  <p class="text-sm" style="margin-bottom: 0;">
    Проверять мобильные платформы на управляемость по теореме Чоу-Рашевского через скобки Ли, строить решетки состояний (State Lattices) с клотоидными примитивами, рассчитывать динамические ограничения по сцеплению шин с грунтом и применять алгоритм TOPP-RA для профилирования скорости.
  </p>
</div>

---

<!-- _header: "Лекция 07 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Неголономность и геометрия Ли (45 мин)</h3>
  <ul>
    <li><strong>00–12 мин:</strong> Классификация ограничений: геометрические ($q \in \mathcal{C}_{free}$), кинематические ($\dot{q}$) и динамические ($\ddot{q}, \tau$).</li>
    <li><strong>12–25 мин:</strong> Дифференциальные связи Пфаффа $A(q)\dot{q} = 0$, интегрируемость распределений и теорема Фробениуса.</li>
    <li><strong>25–37 мин:</strong> <strong>Скобки Ли (Lie Brackets)</strong> $[f_1, f_2]$: коммутатор векторных полей и физика параллельной парковки.</li>
    <li><strong>37–45 мин:</strong> Теорема Чоу-Рашевского (LARC): почему колесный робот полностью управляем в $SE(2)$.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Динамика, Трение и TOPP (45 мин)</h3>
  <ul>
    <li><strong>45–56 мин:</strong> <strong>State Lattice Planning</strong>: решетки состояний в $(x, y, \theta, \kappa)$ и библиотека примитивов на клотоидах.</li>
    <li><strong>56–68 мин:</strong> Динамика шасси и трение: круг Кулона, боковой занос ($v^2 \kappa \le \mu g$) и опрокидывание (Rollover).</li>
    <li><strong>68–80 мин:</strong> <strong>Time-Optimal Path Parameterization (TOPP / TOPP-RA)</strong>: оптимизация на фазовой плоскости $(s, \dot{s}^2)$.</li>
    <li><strong>80–90 мин:</strong> Многозвенные автопоезда (Jackknifing), контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

<!--
Примечание для лектора:
Лекция раскрывает глубокую дифференциальную геометрию (Стивен Лаваль, глава 13), объясняя скобки Ли через простой бытовой опыт водителя (параллельная парковка), после чего переходит к расчету динамических перегрузок и трения.
-->

---

## 1. Классификация ограничений в робототехнике <span class="badge badge-time">00–12 мин</span>

<div class="grid-3">

<div class="card">
  <h3>1. Геометрические</h3>
  <div class="formula-box text-sm">
    $$h(q) \le 0$$
  </div>
  <ul class="text-sm">
    <li>Стены, колонны, двери.</li>
    <li>Границы шарниров манипулятора.</li>
    <li>Зазоры безопасности (Clearance).</li>
    <li>Учитываются напрямую через вырезание $\mathcal{C}_{obs}$ из $\mathcal{C}$.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>2. Кинематические</h3>
  <div class="formula-box text-sm">
    $$A(q) \dot{q} = 0, \quad |\kappa| \le \kappa_{max}$$
  </div>
  <ul class="text-sm">
    <li>Запрет бокового проскальзывания колес (Pure Rolling).</li>
    <li>Минимальный радиус поворота колес руля ($R \ge R_{min}$).</li>
    <li>Зависимость только от скоростей и координат.</li>
  </ul>
</div>

<div class="card card-alert">
  <h3>3. Динамические</h3>
  <div class="formula-box text-sm">
    $$M(q)\ddot{q} + C\dot{q} + g = B\tau$$
  </div>
  <ul class="text-sm">
    <li>Пределы крутящих моментов моторов $|\tau| \le \tau_{max}$.</li>
    <li>Сцепление шин с полом (конус трения $\mu$).</li>
    <li>Фазовое пространство размерности $2d$: $(q, \dot{q}) \in T\mathcal{C}$.</li>
  </ul>
</div>

</div>

---

## 2. Связи Пфаффа и теорема Фробениуса (LaValle гл. 13) <span class="badge badge-time">12–25 мин</span>

<div class="grid-2">

<div class="col">
  <p>Кинематические ограничения робота записываются в <strong>дифференциальной форме Пфаффа</strong>:</p>
  <div class="formula-box text-sm">
    $$\omega_i(q) \dot{q} = \sum_{j=1}^n a_{ij}(q) \dot{q}_j = 0, \quad i = 1, \dots, k$$
  </div>
  <p class="text-sm">Допустимые скорости в каждой конфигурации $q$ образуют подпространство размерности $m = n - k$ — <strong>распределение</strong> $\Delta(q) = \operatorname{span}\{g_1(q), \dots, g_m(q)\}$.</p>
  $$\dot{q} = \sum_{j=1}^m g_j(q) u_j$$
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Теорема Фробениуса об интегрируемости:</h3>
    <p class="text-sm">
      Связь называется <strong>голономной</strong>, если она может быть проинтегрирована в форму без производных: $h(q) = 0$.
    </p>
    <p class="text-sm">
      <strong>Теорема:</strong> Распределение $\Delta$ полностью интегрируемо тогда и только тогда, когда оно <strong>инволютивно</strong> (замкнуто относительно скобок Ли):
    </p>
    $$\forall X, Y \in \Delta \implies [X, Y] \in \Delta$$
    <div class="card-success text-sm mt-2">
      Если распределение <strong>НЕ инволютивно</strong>, связь является <strong>неголономной</strong>: робот может достичь любой точки пространства конфигураций $\mathcal{C}$, несмотря на мгновенные ограничения скорости!
    </div>
  </div>
</div>

</div>

---

## 3. Скобки Ли (Lie Brackets) и маневрирование <span class="badge badge-time">25–37 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Математическое определение скобки Ли:</h3>
    <p class="text-sm">Для двух гладких векторных полей $f_1(q)$ и $f_2(q)$ их скобкой Ли (коммутатором) называется векторное поле:</p>
    <div class="formula-box text-sm">
      $$[f_1, f_2](q) = \frac{\partial f_2}{\partial q} f_1(q) - \frac{\partial f_1}{\partial q} f_2(q)$$
    </div>
    <p class="text-sm"><strong>Геометрический смысл:</strong> Движение по цепочке: вперед по $f_1$ на $\epsilon$, вперед по $f_2$ на $\epsilon$, назад по $-f_1$ на $\epsilon$, назад по $-f_2$ на $\epsilon$ дает чистое смещение:</p>
    $$\Delta q = \epsilon^2 [f_1, f_2](q) + \mathcal{O}(\epsilon^3)$$
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Физический пример: Параллельная парковка</h3>
    <p class="text-sm">Автомобиль имеет два управляющих поля:</p>
    <ul class="text-sm">
      <li>$f_1 = \cos\theta \frac{\partial}{\partial x} + \sin\theta \frac{\partial}{\partial y}$ (продольное движение).</li>
      <li>$f_2 = \frac{\partial}{\partial \theta}$ (поворот руля / рыскание).</li>
    </ul>
    <p class="text-sm">Прямое движение боком $f_3 = [f_1, f_2] = \sin\theta \frac{\partial}{\partial x} - \cos\theta \frac{\partial}{\partial y}$ запрещено механикой колес!</p>
    <div class="card-success text-sm mt-2">
      Однако чередование руления и прямого хода порождает векторное поле <strong>бокового сдвига</strong>! Именно скобка Ли позволяет заехать на парковочное место в узком зазоре.
    </div>
  </div>
</div>

</div>

---

## 4. Теорема Чоу-Рашевского и условие LARC <span class="badge badge-time">37–45 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Условие ранга алгебры Ли (LARC):</h3>
    <p class="text-sm">Пусть $\operatorname{Lie}(\Delta)$ — алгебра Ли, порожденная векторными полями управления $\{g_1, \dots, g_m\}$ и их повторными скобками Ли $[g_i, g_j]$, $[g_i, [g_j, g_k]]$ и т.д.</p>
    <p class="text-sm">Система удовлетворяет условию LARC в конфигурации $q$, если:</p>
    <div class="formula-box text-sm">
      $$\operatorname{dim}\left(\operatorname{Lie}(\Delta)(q)\right) = \operatorname{dim}(\mathcal{C}) = n$$
    </div>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Теорема Чоу-Рашевского (Chow-Rashevsky Theorem):</h3>
    <p class="text-sm">
      Если конфигурационное пространство $\mathcal{C}$ связно и система удовлетворяет условию LARC в каждой точке, то:
    </p>
    <div class="formula-box text-sm">
      $$\forall q_0, q_1 \in \mathcal{C} \quad \exists \text{ допустимая траектория } q(t), \text{ соединяющая } q_0 \text{ и } q_1!$$
    </div>
    <div class="card-alert text-sm">
      <strong>Фундаментальное следствие для робототехники:</strong> Несмотря на то, что робот с дифференциальным приводом имеет всего <strong>2 мотора</strong>, он <strong>полностью управляем в 3D пространстве $SE(2) = (x, y, \theta)$</strong>!
    </div>
  </div>
</div>

</div>

---

## 5. State Lattice Planning: Решетки состояний <span class="badge badge-time">45–56 мин</span>

<div class="grid-2">

<div class="col">
  <p>Как применить сеточный поиск ($A^*$) к неголономному роботу без нарушения кинематики? <strong>State Lattice</strong> (Pivtoraiko & Kelly 2005) дискретизирует состояние в $SE(2) \times \mathcal{K}$:</p>
  <div class="formula-box text-sm">
    $$\mathbf{s} = (x, y, \theta, \kappa) \in \text{Lattice}$$
  </div>
  <div class="card">
    <h3>Примитивы движения (Motion Primitives):</h3>
    <ul class="text-sm">
      <li>Вместо ребер 8-связной сетки вершины графа соединяются физически реализуемыми микро-траекториями.</li>
      <li>Используются <strong>клотоиды (спирали Эйлера)</strong>: кривые с линейно меняющейся кривизной $\kappa(s) = \kappa_0 + c \cdot s$.</li>
      <li>Гарантируется непрерывность кривизны $C^2$ — отсутствие рывков рулевой рейки!</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Преимущества State Lattice:</h3>
    <ol class="text-sm">
      <li><strong>Сдвиговая инвариантность (Translational Invariance):</strong> библиотека примитивов рассчитывается оффлайн один раз и копируется в каждый узел решетки.</li>
      <li><strong>Строгая реализуемость:</strong> любой путь, найденный алгоритмом $A^*$ на State Lattice, <strong>на 100% готов к исполнению контроллером</strong> без срезания углов и заносов.</li>
      <li>Используется в беспилотных автомобилях и карьерных самосвалах (Nav2 Smac Planner Lattice).</li>
    </ol>
  </div>
</div>

</div>

---

## 6. Динамика шасси: Сцепление и срыв в занос <span class="badge badge-time">56–68 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-alert">
    <h3>Круг трения Кулона (Friction Circle):</h3>
    <p class="text-sm">Суммарная сила сцепления колеса с опорной поверхностью ограничена нормальной реакцией $F_z = m g$ и коэффициентом сцепления $\mu$:</p>
    <div class="formula-box text-sm">
      $$\sqrt{F_x^2 + F_y^2} \le \mu F_z = \mu m g$$
    </div>
    <ul class="text-sm">
      <li>$F_x$ — продольная сила тяги/торможения.</li>
      <li>$F_y$ — поперечная сила удержания в повороте.</li>
      <li>Если робот экстренно тормозит ($F_x \to \mu m g$), боковая сила $F_y \to 0$ — робот становится неуправляемым (снос передней оси).</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Предел скорости по центростремительному ускорению:</h3>
    <p class="text-sm">В повороте радиуса $R = 1/|\kappa(s)|$ возникает центробежная сила:</p>
    $$a_y = v^2 |\kappa(s)| \le \mu g$$
    <p class="text-sm">Максимально допустимая скорость движения по геометрическому пути:</p>
    <div class="formula-box text-sm">
      $$v_{max}(s) = \sqrt{\frac{\mu g}{|\kappa(s)|}}$$
    </div>
    <div class="card-alert text-sm">
      <strong>Опрокидывание (Rollover):</strong> Для высоких роботов (доставка, мобильные манипуляторы) предел наступает еще раньше: $a_y \le g \frac{w}{2 h_{cog}}$, где $w$ — колея, $h_{cog}$ — высота центра тяжести.
    </div>
  </div>
</div>

</div>

---

## 7. Профилирование скорости: Алгоритм TOPP / TOPP-RA <span class="badge badge-time">68–80 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Задача Time-Optimal Path Parameterization:</h3>
    <p class="text-sm">Дана геометрическая кривая $q(s), s \in [0, S]$. Требуется найти временной закон $s(t)$, минимизирующий полное время $T = \int_0^S \frac{1}{\dot{s}} ds$ при ограничениях моторов:</p>
    $$\tau_{min} \le M(q)\ddot{q} + C(q, \dot{q})\dot{q} + g(q) \le \tau_{max}$$
    <p class="text-sm">Подстановка производных через путь: $\dot{q} = q'(s)\dot{s}$, $\ddot{q} = q'(s)\ddot{s} + q''(s)\dot{s}^2$.</p>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Выпуклая формулировка TOPP-RA (Pham, 2018):</h3>
    <p class="text-sm">Введем замену переменной $b(s) = \dot{s}^2(s)$ (удвоенная кинетическая энергия):</p>
    $$\ddot{s} = \frac{1}{2} b'(s)$$
    <ul class="text-sm">
      <li>Все нелинейные ограничения на крутящие моменты моторов, ускорения и сцепление становятся <strong>строго линейными неравенствами относительно $b(s)$ и $b'(s)$</strong>!</li>
      <li>Задача нахождения предельного профиля скорости решается через <strong>линейное программирование (LP) за миллисекунды</strong>.</li>
      <li>Гарантирует 100% выжимание динамического потенциала приводов робота.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 07 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">80–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol class="text-sm">
    <li><strong>Неголономные связи</strong> запрещают боковое смещение колес, но не ограничивают конфигурационное пространство $\mathcal{C}$.</li>
    <li><strong>Скобки Ли $[f_1, f_2]$</strong> генерируют новые направления движения за счет циклического коммутатора маневров.</li>
    <li><strong>Теорема Чоу-Рашевского</strong> гарантирует полную управляемость мобильного робота в $SE(2)$ при выполнении LARC.</li>
    <li><strong>State Lattice</strong> обеспечивает кинематически безупречный сеточный поиск на базе клотоидных примитивов.</li>
    <li><strong>Круг трения</strong> ограничивает скорость в поворотах $v \le \sqrt{\mu g / \kappa}$, а алгоритм <strong>TOPP-RA</strong> строит оптимальный профиль скорости через LP.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы для самопроверки:</h3>
  <ul class="text-sm">
    <li>В чем строгое математическое отличие голономной связи от неголономной согласно теореме Фробениуса?</li>
    <li>Как маневр параллельной парковки соотносится с формулой скобки Ли $[f_1, f_2]$?</li>
    <li>Почему в State Lattice примитивы движения строят на основе клотоид, а не дуг окружностей?</li>
    <li>Как замена переменной $b(s) = \dot{s}^2$ в алгоритме TOPP-RA позволяет свести задачу профилирования скорости к выпуклой оптимизации?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Вычислительные аспекты, инженерия и архитектура Nav2</span>
  </div>
</div>

</div>
