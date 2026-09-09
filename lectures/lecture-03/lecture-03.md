---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 03"
footer: "Курс лекций • Лекция 03 • Слайд %PAGE% из %TOTAL%"
math: mathjax
---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 03: Планирование, основанное на выборке (Sampling-Based Motion Planning)

<div class="mt-4">
  <span class="badge badge-blue">⏱️ 90 минут</span>
  <span class="badge badge-green">Сэмплирующие методы</span>
  <span class="badge badge-purple">LaValle (гл. 5) • Karaman & Frazzoli (MIT)</span>
</div>

---

<!-- _header: "Лекция 03 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Блок 1: От сеток к сэмплингу и RRT (45 мин)</h3>
  <ul>
    <li><strong>00–15 мин:</strong> Проклятие размерности $\mathcal{O}((1/\varepsilon)^d)$ и мотивация вероятностного сэмплинга.</li>
    <li><strong>15–30 мин:</strong> Алгоритм PRM (Probabilistic Roadmaps) для многократных запросов.</li>
    <li><strong>30–45 мин:</strong> Алгоритм RRT (Случайные деревья быстрого исследования): сэмплинг, Nearest, Steer, Collision check.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Блок 2: Оптимальность и алгоритм RRT* (45 мин)</h3>
  <ul>
    <li><strong>45–60 мин:</strong> Фундаментальная теорема Карамана–Фраццоли: неоптимальность RRT и вывод <strong>$RRT^*$</strong> (Rewiring).</li>
    <li><strong>60–75 мин:</strong> <span class="badge badge-green">Интерактивный симулятор</span>: исследование поведения RRT vs RRT* в 2D $\mathcal{C}$-space.</li>
    <li><strong>75–85 мин:</strong> Informed $RRT^*$ и структуры пространственного поиска ($k$-d tree).</li>
    <li><strong>85–90 мин:</strong> Итоги, контрольные вопросы и Q&A.</li>
  </ul>
</div>

</div>

---

## 1. Проклятие размерности (Curse of Dimensionality) <span class="badge badge-time">00–15 мин</span>

<div class="grid-2">

<div class="col">
  <p>Почему сеточные методы ($A^*$) перестают работать в пространствах высокой размерности?</p>
  <ul>
    <li>Разбиение пространства размерности $d$ с шагом $\varepsilon$ порождает число ячеек:
      $$N_{cells} \sim \left(\frac{1}{\varepsilon}\right)^d$$
    </li>
    <li>Для 2D плоскости ($d=2$): $100 \times 100 = 10^4$ ячеек (мгновенный поиск).</li>
    <li>Для робота с ориентацией и прицепом ($d=4$): $100^4 = 10^8$ ячеек (гигабайты памяти).</li>
    <li>Для мобильного манипулятора ($d \ge 7$): сеточный перебор физически невозможен.</li>
  </ul>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Идея сэмплирующих алгоритмов (Sampling-based):</h3>
    <p>Вместо дискретизации всего пространства мы выбираем случайные конфигурации $q_{rand} \in \mathcal{C}$ и проверяем их на коллизии <em>локально</em> («как черный ящик»).</p>
    <div class="card-success">
      <strong>Результат:</strong> Сложность слабо зависит от размерности $d$ и определяется только связностью свободного пространства $\mathcal{C}_{free}$.
    </div>
  </div>
</div>

</div>

---

## 2. Классический RRT (Rapidly-exploring Random Tree) <span class="badge badge-time">15–35 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Алгоритм RRT (LaValle, 1998):</h3>
    <ol>
      <li>Инициализация: дерево $\mathcal{T} = \{q_{init}\}$.</li>
      <li>Сэмплирование: $q_{rand} \sim \operatorname{Uniform}(\mathcal{C})$.</li>
      <li>Ближайший узел в дереве:
        $$q_{near} = \arg\min_{q \in \mathcal{V}} \|q - q_{rand}\|$$
      </li>
      <li>Шаг в направлении цели (Steer):
        $$q_{new} = q_{near} + \Delta q \cdot \frac{q_{rand} - q_{near}}{\|q_{rand} - q_{near}\|}$$
      </li>
      <li>Проверка на коллизии отрезка $(q_{near}, q_{new})$.</li>
      <li>Если свободен: добавить $q_{new}$ и ребро в $\mathcal{T}$.</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Свойство расширения Вороного (Voronoi Bias):</h3>
    <p>Вероятность того, что вершина дерева будет выбрана в качестве $q_{near}$, пропорциональна объему ее ячейки Вороного!</p>
    <ul>
      <li>RRT агрессивно исследует самые большие неисследованные области пространства.</li>
      <li><strong>Goal Biasing:</strong> с вероятностью $P_{bias} \approx 5\text{--}10\%$ выбираем $q_{rand} = q_{goal}$, чтобы направлять дерево к цели.</li>
    </ul>
  </div>
</div>

</div>

---

## 3. Революция оптимальности: от RRT к RRT* (MIT, 2011) <span class="badge badge-time">35–50 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-alert">
    <h3>Теорема Карамана и Фраццоли:</h3>
    <p>Классические алгоритмы PRM и RRT обладают <strong>вероятностной полнотой</strong>:</p>
    $$\lim_{N \to \infty} P(\text{путь найден} \mid \text{путь существует}) = 1$$
    <p>Но вероятность нахождения оптимального пути для RRT равна <strong>НУЛЮ</strong>:</p>
    $$P\left(\lim_{N \to \infty} \operatorname{Cost}(\mathcal{T}_N) = c^*\right) = 0$$
    <p>Причина: случайные неоптимальные начальные ветви навсегда остаются в дереве и не перестраиваются.</p>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Алгоритм RRT* (Асимптотически оптимальный):</h3>
    <p>Вводит две ключевые операции в радиусе $r_N = \gamma (\frac{\log N}{N})^{1/d}$:</p>
    <ol>
      <li><strong>Choose Best Parent:</strong> среди соседних узлов выбирается тот, путь через который до $q_{new}$ дает минимальную сумму $cost(u) + \|u - q_{new}\|$.</li>
      <li><strong>Rewiring (Переподключение):</strong> для каждого соседа $v$ в радиусе проверяется, не станет ли путь до него короче, если направить ребро через $q_{new}$. Если да — родитель $v$ меняется на $q_{new}$!</li>
    </ol>
  </div>
</div>

</div>

---

<!-- _header: "Интерактивная практика | RRT и RRT*" -->

## Интерактивный симулятор: Сравнение RRT и RRT* <span class="badge badge-green">⏱️ 50–65 мин</span>

<div class="interactive-container">
  <div class="interactive-header">
    <span><i class="interactive-dot"></i> Интерактивный сэмплинг: RRT vs RRT* с переподключением ветвей</span>
    <span>Рисуйте круглые препятствия мышью | Регулируйте шаг и Goal Bias</span>
  </div>
  <iframe src="../../widgets/rrt-exploration/index.html" class="interactive-frame"></iframe>
</div>

<!-- 
Инструкция для лектора:
1. Запустите сначала базовый RRT: обратите внимание на изломанный, зигзагообразный путь.
2. Переключите алгоритм на RRT* и сбросьте дерево: покажите, как синяя сеть переподключается, превращая траекторию в гладкую линию с минимальной длиной пути.
-->

---

## 4. Informed RRT*: Сэмплирование в эллипсоиде <span class="badge badge-time">65–75 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Проблема RRT* после нахождения первого пути:</h3>
    <ul>
      <li>После того как первый путь стоимостью $c_{best}$ найден, RRT* продолжает сэмплировать точки по всему пространству $\mathcal{C}$.</li>
      <li>Точки вдали от пути заведомо не могут улучшить решение, но отнимают вычислительное время.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Идея Informed RRT* (Gammell et al.):</h3>
    <p>Ограничиваем выборку точек эллипсоидом, фокусы которого находятся в $q_{start}$ и $q_{goal}$:</p>
    $$\mathcal{C}_{informed} = \{ q \in \mathcal{C} \mid \|q - q_{start}\| + \|q - q_{goal}\| \le c_{best} \}$$
    <ul>
      <li>По мере оптимизации пути $c_{best}$ уменьшается, и эллипсоид сжимается.</li>
      <li>Сходимость к глобальному оптимуму ускоряется на порядки!</li>
    </ul>
  </div>
</div>

</div>

---

## 5. Вычислительные оптимизации: $k$-d tree и коллизии <span class="badge badge-time">75–85 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Пространственные индексы ($k$-d Tree):</h3>
    <ul>
      <li>Наивный поиск $q_{near}$ требует перебора всех $N$ узлов: $\mathcal{O}(N)$.</li>
      <li>При $N = 10^5$ итерация занимает миллисекунды.</li>
      <li>Использование сбалансированного $k$-d tree снижает поиск до:
        $$\mathcal{O}(\log N)$$
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Collision Checking (90% времени работы):</h3>
    <ul>
      <li>Иерархии ограничивающих объемов (BVH, AABB, OBB).</li>
      <li><strong>Continuous Collision Detection (CCD):</strong> проверка капсулы заметаемого объема робота во избежание эффекта туннелирования (tunneling effect) сквозь тонкие стены на больших скоростях.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 03 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol>
    <li>Сэмплирующие методы обходят проклятие размерности, оперируя с пространством через генератор точек и детектор коллизий.</li>
    <li>RRT эффективно исследует среду благодаря расширению по ячейкам Вороного, но субоптимален.</li>
    <li>RRT* вводит переподключение соседей (Rewiring), обеспечивая асимптотическую сходимость к оптимальной траектории.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы:</h3>
  <ul>
    <li>Почему при слишком высоком Goal Bias (например, $90\%$) RRT застревает в препятствиях?</li>
    <li>За счет чего радиус окрестности $r_N$ в RRT* должен сжиматься пропорционально $(\frac{\log N}{N})^{1/d}$?</li>
    <li>В каких задачах мобильной робототехники предпочтителен PRM, а в каких RRT?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Реактивные и локальные методы (DWA, TEB, APF)</span>
  </div>
</div>

</div>
