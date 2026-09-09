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
## Лекция 04: Реактивные и локальные методы планирования

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Локальное планирование</span>
  <span class="badge badge-purple">Khatib • ETH Zürich (Harmonic Fields) • Fox (DWA) • VO / RVO • TEB</span>
</div>

---

<!-- _header: "Лекция 04 | Введение и мотивация" -->

## Чему посвящена эта лекция? <span class="badge badge-blue">Локальный контур</span>

<div class="grid-2 mt-2">

<div class="card card-accent">
  <h3>🎯 Разрыв между глобальным планом и реальностью</h3>
  <p class="text-sm">
    Глобальные алгоритмы ($A^*$, RRT*) строят идеальный маршрут по статической карте. Но в реальном мире перед колесами робота внезапно появляются пешеходы, погрузчики, закрываются двери, а колеса проскальзывают по гладкому бетону.
  </p>
  <p class="text-sm">
    Эта лекция посвящена <strong>высокочастотному локальному планированию (20–50 Гц)</strong>: как за миллисекунды реагировать на динамические препятствия, гарантировать торможение без столкновений и плавно удерживать робота на глобальной траектории.
  </p>
</div>

<div class="card">
  <h3>🔍 Ключевые вопросы лекции</h3>
  <ul class="text-sm">
    <li><strong>Физические аналогии:</strong> Искусственные потенциальные поля Хатиба и почему робот «застревает» в U-образных ловушках?</li>
    <li><strong>Математическое устранение ловушек:</strong> Гармонические поля (ETH Zürich), уравнение Лапласа $\Delta U = 0$ и принцип максимума.</li>
    <li><strong>Учет динамики приводов:</strong> Как алгоритм <code>DWA</code> ищет допустимые скорости в окне ускорений?</li>
    <li><strong>Движущиеся препятствия:</strong> Препятствия в пространстве скоростей (Velocity Obstacles, VO) и устранение «зеркального танца» через RVO/ORCA.</li>
    <li><strong>Эластичная деформация:</strong> Метод упругой ленты с таймингом (<code>TEB</code>) на факторных графах.</li>
  </ul>
</div>

</div>

<div class="card card-success mt-2">
  <h3 style="margin-bottom: 4px;">💡 Чему вы научитесь за эти 90 минут</h3>
  <p class="text-sm" style="margin-bottom: 0;">
    Проектировать локальные контуры управления, решать проблему застревания в потенциальных полях через гармонические функции, реализовывать алгоритм DWA с динамическими окнами и настраивать многоагентное избегание столкновений на базе Velocity Obstacles.
  </p>
</div>

---

<!-- _header: "Лекция 04 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Потенциальные поля и геометрия (45 мин)</h3>
  <ul>
    <li><strong>00–12 мин:</strong> Иерархия управления: глобальный планировщик ($\sim 1$ Гц) vs локальный ($\sim 30$ Гц) vs контроллер моторов ($\sim 1$ кГц).</li>
    <li><strong>12–22 мин:</strong> Метод искусственных потенциальных полей (Хатиб 1986): силы притяжения $F_{att}$ и отталкивания $F_{rep}$.</li>
    <li><strong>22–32 мин:</strong> Патологии полей: локальные минимумы, колебания в узких коридорах (Oscillations) и проблема близких целей (GNRON).</li>
    <li><strong>32–45 мин:</strong> <strong>Гармонические потенциальные поля (ETH Zürich)</strong>: уравнение Лапласа $\Delta U = 0$, краевые условия Дирихле/Неймана.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Пространство скоростей и оптимизация (45 мин)</h3>
  <ul>
    <li><strong>45–55 мин:</strong> <span class="badge badge-green">Интерактивный симулятор</span>: исследование сил в искусственном потенциальном поле и U-ловушках.</li>
    <li><strong>55–67 мин:</strong> <strong>Dynamic Window Approach (DWA)</strong>: пространство скоростей $(v, \omega)$, окно динамики $V_d$, безопасное торможение $V_a$.</li>
    <li><strong>67–76 мин:</strong> <strong>Velocity Obstacles (VO)</strong>: конус коллизий, относительная скорость, запаздывание реакции.</li>
    <li><strong>76–84 мин:</strong> Взаимное избегание: <strong>RVO</strong> и <strong>ORCA</strong>. Метод <strong>Timed Elastic Band (TEB)</strong> на фактор-графах $g2o$.</li>
    <li><strong>84–90 мин:</strong> Итоги, контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

<!--
Примечание для лектора:
Лекция показывает эволюцию мысли от непрерывных силовых моделей (потенциалы 1986 г.) к чистому кинематическому пространству скоростей (DWA 1997 г., VO 1998 г.) и современной нелинейной оптимизации траекторий во времени (TEB).
-->

---

## 1. Зачем нужны локальные методы? Иерархия контуров <span class="badge badge-time">00–12 мин</span>

<div class="grid-2">

<div class="col">
  <p>Глобальный планировщик ($A^*$, RRT*) строит маршрут по статической глобальной карте медленно ($1\text{--}5$ с). В реальной эксплуатации возникают три вызова:</p>
  <ul>
    <li><strong>Динамические препятствия:</strong> люди, погрузчики, открывающиеся ворота, которых нет на исходной карте.</li>
    <li><strong>Погрешности приводов и датчиков:</strong> проскальзывание колес (Wheel Slip), дрейф одометрии и задержка передачи команд.</li>
    <li><strong>Жесткий дедлайн реального времени:</strong> время реакции на появившееся препятствие должно составлять <strong>не более 20–50 мс</strong>.</li>
  </ul>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Трехуровневая архитектура управления:</h3>
    <div class="formula-box text-sm">
      $$\begin{aligned}
      \text{Миссия / BT} &\xrightarrow{0.1\text{--}1\text{ Гц}} \text{Глобальный путь } \Pi(s) \\
      &\xrightarrow{1\text{--}2\text{ Гц}} \mathbf{\text{Локальный планировщик}} \\
      &\xrightarrow{20\text{--}50\text{ Гц}} \text{Команды } (v, \omega) \text{ на контроллер} \\
      &\xrightarrow{500\text{--}1000\text{ Гц}} \text{Токи/ШИМ моторов } \tau
      \end{aligned}$$
    </div>
    <p class="text-sm">Локальный планировщик совмещает <strong>следование глобальному плану</strong> с <strong>реактивным уклонением</strong> от локальных сенсорных препятствий (LiDAR Costmap).</p>
  </div>
</div>

</div>

---

## 2. Искусственные потенциальные поля (Хатиб, 1986) <span class="badge badge-time">12–22 мин</span>

<div class="grid-2">

<div class="col">
  <p>Робот моделируется как материальная точка в потенциальном поле $U(q) = U_{att}(q) + U_{rep}(q)$ под действием результирующей силы $F(q) = -\nabla U(q)$:</p>

  <div class="card">
    <h3>Притягивающий потенциал цели:</h3>
    $$U_{att}(q) = \frac{1}{2} k_{att} \|q - q_{goal}\|^2$$
    $$F_{att}(q) = -\nabla U_{att} = -k_{att} (q - q_{goal})$$
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Отталкивающий потенциал препятствий:</h3>
    <p class="text-sm">Действует только в зоне влияния $d_0$ вокруг препятствий:</p>
    $$U_{rep}(q) = \begin{cases} \frac{1}{2} k_{rep} \left(\frac{1}{d(q)} - \frac{1}{d_0}\right)^2, & d(q) \le d_0 \\ 0, & d(q) > d_0 \end{cases}$$
    $$F_{rep}(q) = k_{rep} \left(\frac{1}{d(q)} - \frac{1}{d_0}\right) \frac{1}{d^2(q)} \nabla d(q)$$
    <p class="text-sm">где $d(q) = \min_{c \in \mathcal{O}} \|q - c\|$ — кратчайшее евклидово расстояние до препятствия, а $\nabla d(q)$ — вектор нормали от препятствия.</p>
  </div>
</div>

</div>

---

## 3. Патологии классических полей Хатиба <span class="badge badge-time">22–32 мин</span>

<div class="grid-3">

<div class="card card-alert">
  <h3>1. Локальные минимумы</h3>
  <p class="text-sm">В U-образных тупиках и между двумя препятствиями силы взаимно компенсируются:</p>
  $$F_{att}(q) + F_{rep}(q) = 0$$
  <p class="text-sm">при $q \neq q_{goal}$. Робот полностью останавливается, не доехав до цели.</p>
</div>

<div class="card card-alert">
  <h3>2. Колебания в коридорах</h3>
  <p class="text-sm">В узких проходах робот отталкивается от левой стены, перелетает к правой, отталкивается от нее — возникает незатухающий автоколебательный процесс (chattering).</p>
</div>

<div class="card card-alert">
  <h3>3. Проблема GNRON</h3>
  <p class="text-sm"><strong>Goal Non-Reachable with Obstacle Nearby:</strong> если цель лежит вблизи препятствия ($d(q_{goal}) < d_0$), отталкивающая сила выталкивает робота из цели!</p>
</div>

</div>

<div class="card card-accent mt-2 text-sm">
  <strong>Вывод:</strong> Классический метод Хатиба интуитивен и быстр ($\mathcal{O}(1)$ на шаг), но математически несостоятелен в сложных средах без фундаментальных модификаций.
</div>

---

## 4. Гармонические поля: Ликвидация минимумов (ETH Zürich) <span class="badge badge-time">32–45 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Уравнение Лапласа и принцип максимума:</h3>
    <p class="text-sm">Потенциал $U(q)$ называют <strong>гармоническим</strong>, если он удовлетворяет дифференциальному уравнению Лапласа во всей свободной области $\mathcal{C}_{free}$:</p>
    $$\nabla^2 U(q) = \Delta U(q) = \sum_{i=1}^d \frac{\partial^2 U}{\partial q_i^2} = 0$$
    <div class="card-success text-sm mt-2">
      <strong>Теорема о максимуме/минимуме:</strong> Неконстантная гармоническая функция на замкнутой области достигает своих экстремумов <em>строго на границах области</em>! Внутри $\mathcal{C}_{free}$ <strong>локальные минимумы отсутствуют в принципе</strong>.
    </div>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Граничные условия и численное решение:</h3>
    <ul class="text-sm">
      <li><strong>Цель (сток):</strong> $U(q_{goal}) = 0$ (глобальный минимум).</li>
      <li><strong>Препятствия:</strong> $U(q_{obs}) = 1$ (условие Дирихле) либо $\frac{\partial U}{\partial n} = 0$ (условие Неймана — непроницаемый поток).</li>
    </ul>
    <p class="text-sm">На 2D сетке решается релаксацией Гаусса–Зейделя за несколько итераций:</p>
    <div class="formula-box text-sm">
      $$U(i, j) = \frac{1}{4} \Big( U(i+1, j) + U(i-1, j) + U(i, j+1) + U(i, j-1) \Big)$$
    </div>
    <p class="text-sm">Траектория робота строится градиентным спуском $\dot{q} = -\nabla U(q)$ с гарантией достижения цели!</p>
  </div>
</div>

</div>

---

<!-- _header: "Интерактивная практика | Потенциальные поля" -->

## Интерактивный симулятор: Потенциальные поля и ловушки <span class="badge badge-green">⏱️ 45–55 мин</span>

<div class="interactive-container">
  <div class="interactive-header">
    <span><i class="interactive-dot"></i> Векторные силы: $F_{att}$ (синий), $F_{rep}$ (красный) и суммарный вектор $F_{net}$ (зеленый)</span>
    <span>Перетаскивайте препятствия | Создайте U-ловушку и наблюдайте застревание</span>
  </div>
  <iframe src="../../widgets/potential-field/index.html" class="interactive-frame"></iframe>
</div>

<!-- 
Методические указания лектору:
1. Запустите движение робота по прямой: покажите, как растет сила притяжения Fatt к цели.
2. Поставьте препятствие между стартом и целью: покажите возникновение отталкивающего вектора Frep.
3. Постройте дугу из 3-4 препятствий в виде буквы U (тупик): продемонстрируйте полное зануление зеленой силы Fnet и остановку робота в локальном минимуме.
-->

---

## 5. Dynamic Window Approach (DWA) (Fox et al., 1997) <span class="badge badge-time">55–67 мин</span>

<div class="grid-2">

<div class="col">
  <p>В отличие от полей, <strong>DWA</strong> оптимизирует траекторию непосредственно в <strong>пространстве скоростей</strong> $(v, \omega)$ робота с учетом его тормозной динамики.</p>

  <div class="card">
    <h3>Пересечение трех пространств скоростей:</h3>
    <ol class="text-sm">
      <li><strong>Допустимые скорости $V_s$:</strong> конструктивные пределы шасси: $V_s = [v_{min}, v_{max}] \times [-\omega_{max}, \omega_{max}]$.</li>
      <li><strong>Динамическое окно $V_d$:</strong> скорости, достижимые за квант времени $\tau$ с учетом ускорений $(\dot{v}_{max}, \dot{\omega}_{max})$:
        $$V_d = [v - \dot{v}_{max}\tau, v + \dot{v}_{max}\tau] \times [\omega - \dot{\omega}_{max}\tau, \omega + \dot{\omega}_{max}\tau]$$
      </li>
      <li><strong>Безопасные скорости $V_a$:</strong> скорости, с которых робот гарантированно успеет затормозить до препятствия:
        $$V_a = \left\{(v, \omega) \;\middle|\; v \le \sqrt{2 \cdot \operatorname{dist}(v,\omega) \cdot \dot{v}_{max}}\right\}$$
      </li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Целевая функция выбора скорости $(v^*, \omega^*)$:</h3>
    <div class="formula-box text-sm">
      $$G(v, \omega) = \alpha \cdot \operatorname{heading}(v, \omega) + \beta \cdot \operatorname{dist}(v, \omega) + \gamma \cdot \operatorname{velocity}(v, \omega)$$
    </div>
    <ul class="text-sm">
      <li>$\operatorname{heading}(v, \omega)$ — выравнивание по направлению к следующей целевой точке глобального пути.</li>
      <li>$\operatorname{dist}(v, \omega)$ — клиренс (расстояние до ближайшего препятствия по круговой дуге движения).</li>
      <li>$\operatorname{velocity}(v, \omega)$ — поощрение поддержания высокой крейсерской скорости.</li>
    </ul>
    <div class="card-success text-sm mt-2">
      Поиск оптимума в результирующем окне $V_r = V_s \cap V_d \cap V_a$ выполняется дискретным перебором на сетке $(v, \omega)$ за доли миллисекунды.
    </div>
  </div>
</div>

</div>

---

## 6. Движущиеся препятствия: Velocity Obstacles (VO) <span class="badge badge-time">67–76 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Идея Fiorini & Shiller (1998):</h3>
    <p class="text-sm">Пусть робот $A$ движется со скоростью $v_A$, а препятствие $B$ — со скоростью $v_B$. Относительная скорость сближения: $v_{rel} = v_A - v_B$.</p>
    <p class="text-sm">Построим <strong>конус столкновений</strong> $CC_{A|B}$ как множество лучей из центра $A$, пересекающих раздутое препятствие $B \oplus (-A)$:</p>
    <div class="formula-box text-sm">
      $$VO_{A|B} = \{ v_A \mid v_A - v_B \in CC_{A|B} \} = v_B \oplus CC_{A|B}$$
    </div>
    <div class="card-alert text-sm">
      <strong>Критерий безопасности:</strong> Если $v_A \in VO_{A|B}$, то при сохранении текущих скоростей столкновение неизбежно. Любая скорость $v_A \notin VO_{A|B}$ гарантирует безопасность!
    </div>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Проблема «зеркального танца» (Reciprocal Dance):</h3>
    <p class="text-sm">
      Если препятствие $B$ — это <em>другой разумный робот</em>, использующий тот же алгоритм VO:
    </p>
    <ul class="text-sm">
      <li>Робот $A$ предполагает, что $B$ движется с постоянной скоростью $v_B$, и уклоняется вправо.</li>
      <li>Робот $B$ одновременно предполагает, что $A$ летит прямо, и тоже уклоняется вправо (навстречу $A$!).</li>
      <li>На следующем шаге оба шарахаются влево.</li>
      <li><strong>Результат:</strong> бесконечные колебания и ступор посреди коридора.</li>
    </ul>
    <div class="card-success text-sm mt-2">
      <strong>Решение:</strong> взаимные алгоритмы <strong>RVO</strong> (Reciprocal VO) и <strong>ORCA</strong> (Optimal Reciprocal Collision Avoidance).
    </div>
  </div>
</div>

</div>

---

## 7. Взаимное избегание: RVO, ORCA и Timed Elastic Band <span class="badge badge-time">76–84 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>RVO и ORCA (van den Berg et al.):</h3>
    <ul class="text-sm">
      <li><strong>RVO:</strong> Каждый робот берет на себя ровно <strong>50% ответственности</strong> за маневр уклонения:
        $$v_A \leftarrow \frac{v_A + v_{A}^{cand}}{2}$$
      </li>
      <li><strong>ORCA:</strong> Преобразует нелинейный конус столкновений в <strong>линейное полупространство</strong> допустимых скоростей для каждого соседа:
        $$\mathbf{n}^T (v_A - (v_A^{pref} + \frac{1}{2}\mathbf{u})) \ge 0$$
      </li>
      <li>Задача нахождения оптимальной скорости для сотен роботов решается <strong>2D Линейным Программированием (2D LP) за $\mathcal{O}(k)$ микросекунд</strong>!</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Timed Elastic Band (TEB — Rösmann et al.):</h3>
    <p class="text-sm">Локальная траектория представляется эластичной лентой из поз $s_i = (x_i, y_i, \theta_i)$ и временных интервалов $\Delta T_i$:</p>
    $$\mathcal{B} = \{ s_1, \Delta T_1, s_2, \Delta T_2, \dots, s_{n-1}, \Delta T_{n-1}, s_n \}$$
    <ul class="text-sm">
      <li>Формулируется задача нелинейной оптимизации на гиперграфе (фреймворк $g2o$):
        $$\min_{\mathcal{B}} \sum_k \left( w_t \Delta T_k^2 + w_{obs} f_{obs}(s_k) + w_{kin} f_{kin}(s_k, s_{k+1}, \Delta T_k) \right)$$
      </li>
      <li>Учитывает минимальный радиус поворота, пределы ускорений и обход препятствий в едином графе оптимизации.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 04 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">84–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol class="text-sm">
    <li><strong>Локальные методы</strong> работают на частотах 20–50 Гц, обеспечивая безопасность в динамической среде.</li>
    <li><strong>Поля Хатиба</strong> подвержены локальным минимумам в U-ловушках. <strong>Гармонические поля (ETH)</strong> устраняют ловушки благодаря уравнению Лапласа $\Delta U = 0$.</li>
    <li><strong>DWA</strong> производит поиск непосредственно в динамическом окне достижимых скоростей $(v, \omega)$.</li>
    <li><strong>VO и ORCA</strong> решают задачу уклонения от движущихся агентов через 2D линейное программирование.</li>
    <li><strong>TEB</strong> деформирует траекторию во времени на гиперграфах с учетом неголономных связей.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы для самопроверки:</h3>
  <ul class="text-sm">
    <li>Какое свойство решений уравнения Лапласа гарантирует отсутствие локальных минимумов внутри области?</li>
    <li>Из каких трех подпространств скоростей формируется результирующее окно $V_r$ в алгоритме DWA?</li>
    <li>Почему алгоритм Velocity Obstacles вызывает «зеркальный танец», если оба робота являются автономными агентами?</li>
    <li>Какую роль в алгоритме TEB играют переменные временных интервалов $\Delta T_i$?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Оптимальное управление (ПМП, LQR, Коллокация)</span>
  </div>
</div>

</div>
