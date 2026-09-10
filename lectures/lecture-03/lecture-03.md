---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 03"
footer: "Курс лекций • Лекция 03"
math: katex

---

<!-- _class: lead -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 03: Планирование, основанное на выборке (Sampling-Based Motion Planning)

<div class="mt-4">

<span class="badge badge-blue">⏱️ 90 минут</span>
<span class="badge badge-green">Сэмплирующие методы</span>
<span class="badge badge-purple">LaValle (гл. 5, 6) • Karaman & Frazzoli (MIT) • PRM • RRT • RRT*</span>

</div>

---

<!-- _header: "Лекция 03 | Введение и мотивация" -->

## Чему посвящена эта лекция? <span class="badge badge-blue">Сэмплирующий базис</span>

<div class="grid-2 mt-2">

<div class="card card-accent">

### 🎯 Преодоление проклятия размерности

В Лекции 02 мы исследовали поиск на сетках ($A^*$, $\text{Theta}^*$). Но что делать, когда робот движется не на плоской сетке $\mathbb{R}^2$, а имеет размерность состояния $d \ge 4$ (ориентация, прицеп, манипулятор, скорость)?

Эта лекция посвящена <strong>методам случайной выборки</strong> (Sampling-Based Planning): как исследовать непрерывное конфигурационное пространство без его явного геометрического построения, используя только генератор случайных точек и локальный детектор коллизий.



**💡 Результат занятия:** Проектировать и реализовывать сэмплирующие планировщики (PRM, RRT, RRT*), настраивать метрики расстояния и эвристики смещения (Goal Bias), применять сжатие выборки в Informed $RRT^*$ и понимать границы применимости вероятностных методов для роботов с дифференциальными ограничениями.

</div>

<div class="card">

### 🔍 Ключевые вопросы лекции

- <strong>Почему сетки взрываются?</strong> Проклятие размерности $\mathcal{O}((1/\varepsilon)^d)$ и альтернатива «черного ящика».
- <strong>Многократные vs однократные запросы:</strong> Архитектура PRM (Probabilistic Roadmaps) vs деревья RRT.
- <strong>Проблема узких проходов:</strong> Почему случайные точки не попадают в узкие двери и как это лечить?
- <strong>Революция оптимальности MIT:</strong> Доказательство неоптимальности RRT и вывод асимптотически оптимального $RRT^*$.
- <strong>Ускорения:</strong> Informed $RRT^*$ (эллипсоидный сэмплинг), $k$-d tree и кинодинамическое расширение.

</div>

</div>

---

<!-- _header: "Лекция 03 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">

### Часть 1: От сеток к PRM и RRT (45 мин)

- <strong>00–12 мин:</strong> Проклятие размерности $\mathcal{O}((1/\varepsilon)^d)$, непрерывный $\mathcal{C}$-space и парадигма Collision Checking Black-box.
- <strong>12–22 мин:</strong> Probabilistic Roadmaps (PRM): фаза построения (Learning) и фаза запроса (Query). Multi-query парадигма.
- <strong>22–32 мин:</strong> Проблема узких проходов (Narrow Passages) и эвристики сэмплинга (Bridge Test, Gaussian Sampling).
- <strong>32–45 мин:</strong> Классический RRT (LaValle 1998): свойство расширения Вороного (Voronoi Bias), шаги Nearest и Steer. Двунаправленный <strong>RRT-Connect</strong>.

</div>

<div class="card card-accent">

### Часть 2: Оптимальность, RRT* и Инженерия (45 мин)

- <strong>45–58 мин:</strong> Теорема Карамана–Фраццоли (MIT): почему $P(\text{cost}(RRT) = c^*) = 0$. Алгоритм <strong>$RRT^*$</strong>: ChooseParent и Rewiring.
- <strong>58–72 мин:</strong> <span class="badge badge-green">Интерактивный симулятор</span>: исследование поведения RRT vs RRT* в реальном времени.
- <strong>72–82 мин:</strong> <strong>Informed $RRT^*$</strong>: эллипсоидное ограничение $\mathcal{C}_{informed}$. Пространственные индексы ($k$-d tree) и CCD.
- <strong>82–90 мин:</strong> Введение в Kinodynamic RRT (учет $\dot{x}=f(x,u)$). Итоги, контрольные вопросы и Q&A.

</div>

</div>

<!-- 
Примечание для лектора:
Подчеркните фундаментальный сдвиг парадигмы: мы отказываемся от аналитического вычисления границ преград C_obs. Единственное, что умеет робот — проверить точку или отрезок на коллизию (Collision Checker as a Black Box).
-->
---

## 1. Проклятие размерности и философия сэмплинга <span class="badge badge-time">00–12 мин</span>

<div class="grid-2">

<div class="col">

Почему сеточные методы ($A^*$, Дейкстра) перестают работать при росте степеней свободы робота?

- Дискретизация пространства размерности $d$ с шагом $\varepsilon$ порождает число ячеек:
$$N_{cells} \sim \mathcal{O}\left(\left(\frac{1}{\varepsilon}\right)^d\right)$$


- Для плоскости ($d=2$, сетка $1000 \times 1000$): $10^6$ ячеек (поиск за доли секунды).
- Для робота с ориентацией и прицепом ($d=4$): $10^{12}$ ячеек (терабайты оперативной памяти).
- Для манипулятора на колесной базе ($d \ge 7$): сеточный перебор физически невозможен.

</div>

<div class="col">

<div class="card card-accent">

### Сдвиг парадигмы: Collision Checking as Black-Box

Вместо точного вычисления границ $\partial \mathcal{C}_{obs}$ (что экспоненциально сложно в $\mathbb{R}^d$) алгоритм использует только <strong>предикат коллизии</strong>:

<div class="formula-box">

$$\operatorname{Clear}(q) = \begin{cases} 1, & q \in \mathcal{C}_{free} \\ 0, & q \in \mathcal{C}_{obs} \end{cases}$$

</div>
<div class="card-success text-sm">

<strong>Результат:</strong> Сложность слабо зависит от размерности $d$ и определяется топологической связностью и "толщиной" свободного пространства $\mathcal{C}_{free}$.

</div>

</div>

</div>

</div>

---

## 2. Probabilistic Roadmaps (PRM): Многократные запросы <span class="badge badge-time">12–22 мин</span>

<div class="grid-2">

<div class="col">

<div class="card">

### Фаза построения дорожной карты (Learning Phase):

- Генерируем $N$ случайных конфигураций $q \sim \operatorname{Uniform}(\mathcal{C})$.
- Отфильтровываем коллизии: оставляем вершины $\mathcal{V} \subset \mathcal{C}_{free}$.
- Для каждой вершины $q \in \mathcal{V}$ находим $k$ ближайших соседей (или в радиусе $r$).
- Пытаемся соединить ребро $(q, q_{neighbor})$ локальным планировщиком (прямой отрезок с шагом $\delta$).
- Если отрезок свободен от препятствий — добавляем ребро в $\mathcal{E}$.

</div>

</div>

<div class="col">

<div class="card card-accent">

### Фаза запроса (Query Phase) и свойства:

- <strong>Подключение:</strong> Соединяем $q_{init}$ и $q_{goal}$ с ближайшими видимыми вершинами дорожной карты $\mathcal{G} = (\mathcal{V}, \mathcal{E})$.
- <strong>Поиск:</strong> Запускаем $A^*$ или Дейкстру по готовому графу за миллисекунды.

<div class="card-alert text-sm mt-2">

<strong>Multi-Query парадигма:</strong> граф строится <em>один раз</em> для статической карты (цех завода, терминал) и затем мгновенно обслуживает тысячи маршрутных запросов.

</div>

</div>

</div>

</div>

---

## 3. Проблема узких проходов (Narrow Passages) <span class="badge badge-time">22–32 мин</span>

<div class="grid-2">

<div class="col">

<div class="card card-alert">

### В чем фундаментальная уязвимость сэмплинга?

Пусть свободный проход $\mathcal{C}_{narrow}$ (дверной проем, щель) имеет объем $\mu(\mathcal{C}_{narrow})$, а все пространство — $\mu(\mathcal{C})$.

Вероятность попадания случайной точки в проход при равномерном сэмплинге:

$$P(q \in \mathcal{C}_{narrow}) = \frac{\mu(\mathcal{C}_{narrow})}{\mu(\mathcal{C})} \ll 1$$

Чтобы хотя бы одна точка попала в узкий проем, требуются миллионы сэмплов!

</div>

</div>

<div class="col">

<div class="card card-accent">

### Интеллектуальные стратегии сэмплинга:

- <strong>Bridge Test (Мостовой тест):</strong> выбираем точку $q_1 \in \mathcal{C}_{obs}$. Выбираем случайный шаг в случайном направлении $q_2 \in \mathcal{C}_{obs}$. Если середина отрезка $q_{mid} = \frac{q_1 + q_2}{2} \in \mathcal{C}_{free}$, значит, мы нашли узкий мост между двумя препятствиями! Сохраняем $q_{mid}$.
- <strong>Gaussian Sampling:</strong> генерируем пару точек с гауссовым смещением. Сохраняем точку, только если одна в препятствии, а вторая свободна (сэмплинг вдоль границ $\partial \mathcal{C}_{obs}$).
- <strong>Medial Axis Sampling:</strong> смещение точек к скелету пространства (максимальный клиренс).

</div>

</div>

</div>

---

## 4. Классический RRT (Rapidly-exploring Random Tree) <span class="badge badge-time">32–45 мин</span>

<div class="grid-2">

<div class="col">

<div class="card">

### Алгоритм RRT (LaValle, 1998):

- Инициализация: дерево $\mathcal{T} = (\{q_{init}\}, \emptyset)$.
- Сэмплирование: $q_{rand} \sim \operatorname{Uniform}(\mathcal{C})$.
- Поиск ближайшего узла дерева:
$$q_{near} = \arg\min_{q \in \mathcal{V}} \|q - q_{rand}\|$$


- Продвижение на шаг $\Delta q$ (Steer):
$$q_{new} = q_{near} + \min(\Delta q, \|q_{rand} - q_{near}\|) \frac{q_{rand} - q_{near}}{\|q_{rand} - q_{near}\|}$$


- Проверка на коллизии сегмента $(q_{near}, q_{new})$.
- Если свободен: $\mathcal{V} \leftarrow \mathcal{V} \cup \{q_{new}\}$, $\mathcal{E} \leftarrow \mathcal{E} \cup \{(q_{near}, q_{new})\}$.

</div>

</div>

<div class="col">

<div class="card card-accent">

### Свойство Voronoi Bias (Смещение Вороного):

Вероятность того, что вершина дерева $q \in \mathcal{V}$ будет выбрана в качестве $q_{near}$, <strong>строго пропорциональна объему ее ячейки Вороного</strong> $\operatorname{Vol}(\operatorname{Vor}(q))$!

<div class="card-success text-sm mt-2">

<strong>Эффект:</strong> Дерево стремительно прорастает в самые крупные неисследованные пустоты пространства, не застревая в уже исследованных зонах.

</div>
<div class="card-alert text-sm mt-2">

<strong>Goal Biasing:</strong> с вероятностью $P_{bias} \approx 5\text{--}10\%$ выбираем $q_{rand} = q_{goal}$. При $P_{bias} > 20\%$ дерево теряет исследовательскую силу и втыкается в препятствия перед целью.

</div>

</div>

</div>

</div>

---

## 5. Двунаправленный поиск: RRT-Connect <span class="badge badge-time">42–50 мин</span>

<div class="grid-2">

<div class="col">

Для ускорения сходимости в задачах с одним запросом Kuffner & LaValle (2000) предложили строить <strong>два дерева одновременно</strong>: $\mathcal{T}_a$ от старта и $\mathcal{T}_b$ от цели.

<div class="card card-accent">

### Операция CONNECT:

В отличие от стандартного шага `EXTEND` (продвижение на один шаг $\Delta q$), операция `CONNECT` повторяет шаги к точке $q_{target}$ до тех пор, пока:

- Либо дерево не упрется в препятствие (коллизия),
- Либо не достигнет $q_{target}$ вплотную!

</div>

</div>

<div class="col">

<div class="card">

### Псевдокод итерации RRT-Connect:

- Выбираем $q_{rand} \sim \operatorname{Uniform}(\mathcal{C})$.
- Делаем шаг `EXTEND` в дереве $\mathcal{T}_a \rightarrow q_{new}$.
- Пытаемся соединить второе дерево $\mathcal{T}_b$ с только что добавленным узлом: `CONNECT`$(\mathcal{T}_b, q_{new})$.
- Если деревья соединились — <strong>путь найден!</strong>
- Меняем деревья местами: $\operatorname{Swap}(\mathcal{T}_a, \mathcal{T}_b)$ для сбалансированного роста.

<div class="card-success text-sm mt-2">

<strong>Практический эффект:</strong> RRT-Connect находит первый путь в 10–50 раз быстрее базового RRT в сложных лабиринтах.

</div>

</div>

</div>

</div>

---

## 6. Теорема Карамана–Фраццоли: Неоптимальность RRT <span class="badge badge-time">50–60 мин</span>

<div class="grid-2">

<div class="col">

<div class="card card-alert">

### Теорема (Karaman & Frazzoli, MIT / IJRR 2011):

Классические алгоритмы PRM и RRT обладают свойством <strong>вероятностной полноты</strong>:

$$\lim_{N \to \infty} P(\text{путь найден} \mid \text{путь существует}) = 1$$

Однако вероятность того, что стоимость найденного решения сходится к оптимальной $c^*$, <strong>тождественно равна нулю</strong>:

$$P\left(\lim_{N \to \infty} \operatorname{Cost}(\mathcal{T}_N) = c^*\right) = 0$$

</div>

</div>

<div class="col">

<div class="card card-accent">

### Почему RRT фундаментально неоптимален?

- <strong>Случайная фиксация топологии:</strong> ранние ветви дерева, возникшие случайно, навсегда остаются родителями своих потомков.
- <strong>Отсутствие памяти о стоимости:</strong> шаг `EXTEND` выбирает геометрически ближайший узел $q_{near}$, полностью игнорируя накопленную стоимость пути от корня $cost(q_{near})$.
- Сколько бы миллионов узлов мы ни добавляли в RRT, траектория навсегда останется изломанной и субоптимальной.

<div class="card-success text-sm mt-2">

<strong>Решение:</strong> переподключение ветвей дерева — алгоритм <strong>$RRT^*$</strong>.

</div>

</div>

</div>

</div>

---

## 7. Алгоритм RRT*: ChooseParent и Rewiring <span class="badge badge-time">60–68 мин</span>

<div class="grid-2">

<div class="col">

При добавлении нового узла $q_{new}$ алгоритм $RRT^*$ рассматривает окрестность радиуса $r_N = \gamma \left(\frac{\log N}{N}\right)^{1/d}$:

<div class="card">

### 1. Выбор лучшего родителя (ChooseParent):

Среди соседей $u \in \operatorname{Near}(q_{new}, r_N)$ выбирается узел с минимальной накопленной стоимостью:

$$q_{parent} = \arg\min_{u} \left( \operatorname{cost}(u) + \|u - q_{new}\| \right)$$

</div>

<div class="card card-success mt-2">

### 2. Переподключение ветвей (Rewiring):

Для каждого соседа $v \in \operatorname{Near}(q_{new}, r_N)$, если путь через $q_{new}$ короче:

$$\operatorname{cost}(q_{new}) + \|q_{new} - v\| < \operatorname{cost}(v)$$

Старое ребро к $v$ удаляется, а $q_{new}$ назначается новым родителем вершины $v$!

</div>

</div>

<div class="col">

<div class="diagram-box">

<img src="../../assets/images/lecture-03/rrt_star_rewire.svg" alt="RRT* Rewiring" />

</div>

</div>

</div>

---

<!-- _header: "Интерактивная практика | RRT и RRT*" -->

## Интерактивный симулятор: Сравнение RRT и RRT* <span class="badge badge-green">⏱️ 68–78 мин</span>

<div class="interactive-container">

<div class="interactive-header">

<span><i class="interactive-dot"></i> Интерактивный сэмплинг: RRT vs RRT* с переподключением ветвей (Rewiring)</span>
<span>Рисуйте препятствия мышью | Регулируйте шаг и радиус окрестности</span>

</div>
<iframe src="http://localhost:5599/widgets/rrt-exploration/index.html" class="interactive-frame"></iframe>

</div>

<!-- 
Методические указания лектору:
1. Запустите сначала базовый RRT: обратите внимание аудитории на угловатый, зигзагообразный путь с лишними петлями.
2. Переключите режим на RRT* и сбросьте дерево: покажите, как синяя сеть переподключается, превращая ломаную в гладкую линию с минимальной длиной пути.
-->
---

## 8. Informed RRT*: Сжатие выборки в эллипсоид <span class="badge badge-time">78–83 мин</span>

<div class="grid-2">

<div class="col">

<div class="card card-accent">

### Проблема RRT* после первого решения:

Как только первый путь стоимостью $c_{best}$ найден, RRT* продолжает генерировать сэмплы по всему $\mathcal{C}$. Точки вне эллипсоида с суммой расстояний $> c_{best}$ бесполезны!

</div>

<div class="card card-success mt-2">

### Informed RRT* (Gammell et al., 2014):

Сэмплируем строго внутри гиперэллипсоида:

$$\mathcal{C}_{inf} = \{ q \in \mathcal{C} \mid \|q - q_{init}\| + \|q - q_{goal}\| \le c_{best} \}$$

По мере нахождения лучших путей $c_{best} \downarrow$ эллипсоид сжимается, концентрируя 100% вычислений в зоне оптимума!

</div>

</div>

<div class="col">

<div class="diagram-box">

<img src="../../assets/images/lecture-03/informed_rrt_ellipse.svg" alt="Informed RRT* Ellipsoid" />

</div>

</div>

</div>

---

## 9. Инженерия сэмплинга: $k$-d tree, CCD и Kinodynamic RRT <span class="badge badge-time">83–88 мин</span>

<div class="grid-2">

<div class="col">

<div class="card">

### Ускорение поиска соседей ($k$-d Tree):

Наивный поиск $q_{near}$ среди $N$ вершин дерева требует $\mathcal{O}(N)$ операций.

При $N = 10^5$ итерация занимает сотни миллисекунд. Использование сбалансированных структур ($k$-d tree, nanoflann) снижает сложность до:


$$\mathcal{O}(\log N)$$
<div class="card-alert text-sm mt-2">

<strong>Continuous Collision Detection (CCD):</strong> проверка заметаемого объема (Swept Volume / GJK) исключает туннелирование робота сквозь тонкие стены на высокой скорости.

</div>

</div>

</div>

<div class="col">

<div class="card card-accent">

### Kinodynamic RRT (Дифференциальные связи):

Если робот неголономен ($\dot{x} = f(x, u)$), мы не можем соединять узлы прямой линией!

- Выбираем $q_{rand}$.
- Находим ближайший узел по <em>квазиметрике достижимости</em>.
- Сэмплируем управление $u \sim \operatorname{Uniform}(\mathcal{U})$ и длительность $\Delta t$.
- Численно интегрируем систему: $x(t + \Delta t) = x(t) + \int f(x, u) dt$.
- Если отрезок свободен — добавляем траекторный примитив в дерево.

</div>

</div>

</div>

---

<!-- _class: accent -->
<!-- _header: "Лекция 03 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">88–90 мин</span>

<div class="grid-2">

<div class="card">

### Главные выводы:

- <strong>Сэмплирующие методы</strong> преодолевают проклятие размерности, заменяя аналитическое построение $\mathcal{C}_{obs}$ локальным детектором коллизий.
- <strong>RRT</strong> агрессивно исследует пространство за счет Voronoi Bias, но фундаментально субоптимален.
- <strong>RRT*</strong> вводит ChooseParent и Rewiring, обеспечивая асимптотическую оптимальность решения.
- <strong>Informed RRT*</strong> концентрирует выборку внутри эллипсоида, ускоряя сходимость в десятки раз.

</div>

<div class="card card-accent">

### Контрольные вопросы для самопроверки:

- Почему при Goal Bias $> 50\%$ алгоритм RRT часто работает медленнее, чем при $5\%$?
- В чем заключается теорема Карамана–Фраццоли и почему классический RRT не сходится к оптимуму?
- Как алгоритм Bridge Test помогает обнаружить узкие проходы между препятствиями?
- Почему в неголономном пространстве евклидово расстояние $\|q_1 - q_2\|$ не отражает реальную сложность перехода?

<div class="mt-4 text-center">

<span class="badge badge-blue">Следующая лекция: Реактивные и локальные методы (DWA, TEB, APF)</span>

</div>

</div>

</div>
