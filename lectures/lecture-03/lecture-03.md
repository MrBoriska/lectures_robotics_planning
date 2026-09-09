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
  <span class="badge badge-purple">LaValle (гл. 5, 6) • Karaman & Frazzoli (MIT) • PRM • RRT • RRT*</span>
</div>

---

<!-- _header: "Лекция 03 | Введение и мотивация" -->

## Чему посвящена эта лекция? <span class="badge badge-blue">Сэмплирующий базис</span>

<div class="grid-2 mt-2">

<div class="card card-accent">
  <h3>🎯 Преодоление проклятия размерности</h3>
  <p class="text-sm">
    В Лекции 02 мы исследовали поиск на сетках ($A^*$, $\text{Theta}^*$). Но что делать, когда робот движется не на плоской сетке $\mathbb{R}^2$, а имеет размерность состояния $d \ge 4$ (ориентация, прицеп, манипулятор, скорость)?
  </p>
  <p class="text-sm">
    Эта лекция посвящена <strong>методам случайной выборки</strong> (Sampling-Based Planning): как исследовать непрерывное конфигурационное пространство без его явного геометрического построения, используя только генератор случайных точек и локальный детектор коллизий.
  </p>
</div>

<div class="card">
  <h3>🔍 Ключевые вопросы лекции</h3>
  <ul class="text-sm">
    <li><strong>Почему сетки взрываются?</strong> Проклятие размерности $\mathcal{O}((1/\varepsilon)^d)$ и альтернатива «черного ящика».</li>
    <li><strong>Многократные vs однократные запросы:</strong> Архитектура PRM (Probabilistic Roadmaps) vs деревья RRT.</li>
    <li><strong>Проблема узких проходов:</strong> Почему случайные точки не попадают в узкие двери и как это лечить?</li>
    <li><strong>Революция оптимальности MIT:</strong> Доказательство неоптимальности RRT и вывод асимптотически оптимального $RRT^*$.</li>
    <li><strong>Ускорения:</strong> Informed $RRT^*$ (эллипсоидный сэмплинг), $k$-d tree и кинодинамическое расширение.</li>
  </ul>
</div>

</div>

<div class="card card-success mt-2">
  <h3 style="margin-bottom: 4px;">💡 Чему вы научитесь за эти 90 минут</h3>
  <p class="text-sm" style="margin-bottom: 0;">
    Проектировать и реализовывать сэмплирующие планировщики (PRM, RRT, RRT*), настраивать метрики расстояния и эвристики смещения (Goal Bias), применять сжатие выборки в Informed $RRT^*$ и понимать границы применимости вероятностных методов для роботов с дифференциальными ограничениями.
  </p>
</div>

---

<!-- _header: "Лекция 03 | Структура занятия" -->

## План лекции на 90 минут <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: От сеток к PRM и RRT (45 мин)</h3>
  <ul>
    <li><strong>00–12 мин:</strong> Проклятие размерности $\mathcal{O}((1/\varepsilon)^d)$, непрерывный $\mathcal{C}$-space и парадигма Collision Checking Black-box.</li>
    <li><strong>12–22 мин:</strong> Probabilistic Roadmaps (PRM): фаза построения (Learning) и фаза запроса (Query). Multi-query парадигма.</li>
    <li><strong>22–32 мин:</strong> Проблема узких проходов (Narrow Passages) и эвристики сэмплинга (Bridge Test, Gaussian Sampling).</li>
    <li><strong>32–45 мин:</strong> Классический RRT (LaValle 1998): свойство расширения Вороного (Voronoi Bias), шаги Nearest и Steer. Двунаправленный <strong>RRT-Connect</strong>.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Оптимальность, RRT* и Инженерия (45 мин)</h3>
  <ul>
    <li><strong>45–58 мин:</strong> Теорема Карамана–Фраццоли (MIT): почему $P(\text{cost}(RRT) = c^*) = 0$. Алгоритм <strong>$RRT^*$</strong>: ChooseParent и Rewiring.</li>
    <li><strong>58–72 мин:</strong> <span class="badge badge-green">Интерактивный симулятор</span>: исследование поведения RRT vs RRT* в реальном времени.</li>
    <li><strong>72–82 мин:</strong> <strong>Informed $RRT^*$</strong>: эллипсоидное ограничение $\mathcal{C}_{informed}$. Пространственные индексы ($k$-d tree) и CCD.</li>
    <li><strong>82–90 мин:</strong> Введение в Kinodynamic RRT (учет $\dot{x}=f(x,u)$). Итоги, контрольные вопросы и Q&A.</li>
  </ul>
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
  <p>Почему сеточные методы ($A^*$, Дейкстра) перестают работать при росте степеней свободы робота?</p>
  <ul>
    <li>Дискретизация пространства размерности $d$ с шагом $\varepsilon$ порождает число ячеек:
      $$N_{cells} \sim \mathcal{O}\left(\left(\frac{1}{\varepsilon}\right)^d\right)$$
    </li>
    <li>Для плоскости ($d=2$, сетка $1000 \times 1000$): $10^6$ ячеек (поиск за доли секунды).</li>
    <li>Для робота с ориентацией и прицепом ($d=4$): $10^{12}$ ячеек (терабайты оперативной памяти).</li>
    <li>Для манипулятора на колесной базе ($d \ge 7$): сеточный перебор физически невозможен.</li>
  </ul>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Сдвиг парадигмы: Collision Checking as Black-Box</h3>
    <p class="text-sm">
      Вместо точного вычисления границ $\partial \mathcal{C}_{obs}$ (что экспоненциально сложно в $\mathbb{R}^d$) алгоритм использует только <strong>предикат коллизии</strong>:
    </p>
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
    <h3>Фаза построения дорожной карты (Learning Phase):</h3>
    <ol class="text-sm">
      <li>Генерируем $N$ случайных конфигураций $q \sim \operatorname{Uniform}(\mathcal{C})$.</li>
      <li>Отфильтровываем коллизии: оставляем вершины $\mathcal{V} \subset \mathcal{C}_{free}$.</li>
      <li>Для каждой вершины $q \in \mathcal{V}$ находим $k$ ближайших соседей (или в радиусе $r$).</li>
      <li>Пытаемся соединить ребро $(q, q_{neighbor})$ локальным планировщиком (прямой отрезок с шагом $\delta$).</li>
      <li>Если отрезок свободен от препятствий — добавляем ребро в $\mathcal{E}$.</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Фаза запроса (Query Phase) и свойства:</h3>
    <ul class="text-sm">
      <li><strong>Подключение:</strong> Соединяем $q_{init}$ и $q_{goal}$ с ближайшими видимыми вершинами дорожной карты $\mathcal{G} = (\mathcal{V}, \mathcal{E})$.</li>
      <li><strong>Поиск:</strong> Запускаем $A^*$ или Дейкстру по готовому графу за миллисекунды.</li>
    </ul>
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
    <h3>В чем фундаментальная уязвимость сэмплинга?</h3>
    <p class="text-sm">
      Пусть свободный проход $\mathcal{C}_{narrow}$ (дверной проем, щель) имеет объем $\mu(\mathcal{C}_{narrow})$, а все пространство — $\mu(\mathcal{C})$.
    </p>
    <p class="text-sm">
      Вероятность попадания случайной точки в проход при равномерном сэмплинге:
    </p>
    $$P(q \in \mathcal{C}_{narrow}) = \frac{\mu(\mathcal{C}_{narrow})}{\mu(\mathcal{C})} \ll 1$$
    <p class="text-sm">
      Чтобы хотя бы одна точка попала в узкий проем, требуются миллионы сэмплов!
    </p>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Интеллектуальные стратегии сэмплинга:</h3>
    <ul class="text-sm">
      <li><strong>Bridge Test (Мостовой тест):</strong> выбираем точку $q_1 \in \mathcal{C}_{obs}$. Выбираем случайный шаг в случайном направлении $q_2 \in \mathcal{C}_{obs}$. Если середина отрезка $q_{mid} = \frac{q_1 + q_2}{2} \in \mathcal{C}_{free}$, значит, мы нашли узкий мост между двумя препятствиями! Сохраняем $q_{mid}$.</li>
      <li><strong>Gaussian Sampling:</strong> генерируем пару точек с гауссовым смещением. Сохраняем точку, только если одна в препятствии, а вторая свободна (сэмплинг вдоль границ $\partial \mathcal{C}_{obs}$).</li>
      <li><strong>Medial Axis Sampling:</strong> смещение точек к скелету пространства (максимальный клиренс).</li>
    </ul>
  </div>
</div>

</div>

---

## 4. Классический RRT (Rapidly-exploring Random Tree) <span class="badge badge-time">32–45 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Алгоритм RRT (LaValle, 1998):</h3>
    <ol class="text-sm">
      <li>Инициализация: дерево $\mathcal{T} = (\{q_{init}\}, \emptyset)$.</li>
      <li>Сэмплирование: $q_{rand} \sim \operatorname{Uniform}(\mathcal{C})$.</li>
      <li>Поиск ближайшего узла дерева:
        $$q_{near} = \arg\min_{q \in \mathcal{V}} \|q - q_{rand}\|$$
      </li>
      <li>Продвижение на шаг $\Delta q$ (Steer):
        $$q_{new} = q_{near} + \min(\Delta q, \|q_{rand} - q_{near}\|) \frac{q_{rand} - q_{near}}{\|q_{rand} - q_{near}\|}$$
      </li>
      <li>Проверка на коллизии сегмента $(q_{near}, q_{new})$.</li>
      <li>Если свободен: $\mathcal{V} \leftarrow \mathcal{V} \cup \{q_{new}\}$, $\mathcal{E} \leftarrow \mathcal{E} \cup \{(q_{near}, q_{new})\}$.</li>
    </ol>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Свойство Voronoi Bias (Смещение Вороного):</h3>
    <p class="text-sm">
      Вероятность того, что вершина дерева $q \in \mathcal{V}$ будет выбрана в качестве $q_{near}$, <strong>строго пропорциональна объему ее ячейки Вороного</strong> $\operatorname{Vol}(\operatorname{Vor}(q))$!
    </p>
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
  <p>Для ускорения сходимости в задачах с одним запросом Kuffner & LaValle (2000) предложили строить <strong>два дерева одновременно</strong>: $\mathcal{T}_a$ от старта и $\mathcal{T}_b$ от цели.</p>

  <div class="card card-accent">
    <h3>Операция CONNECT:</h3>
    <p class="text-sm">
      В отличие от стандартного шага `EXTEND` (продвижение на один шаг $\Delta q$), операция `CONNECT` повторяет шаги к точке $q_{target}$ до тех пор, пока:
    </p>
    <ul class="text-sm">
      <li>Либо дерево не упрется в препятствие (коллизия),</li>
      <li>Либо не достигнет $q_{target}$ вплотную!</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Псевдокод итерации RRT-Connect:</h3>
    <ol class="text-sm">
      <li>Выбираем $q_{rand} \sim \operatorname{Uniform}(\mathcal{C})$.</li>
      <li>Делаем шаг `EXTEND` в дереве $\mathcal{T}_a \rightarrow q_{new}$.</li>
      <li>Пытаемся соединить второе дерево $\mathcal{T}_b$ с только что добавленным узлом: `CONNECT`$(\mathcal{T}_b, q_{new})$.</li>
      <li>Если деревья соединились — <strong>путь найден!</strong></li>
      <li>Меняем деревья местами: $\operatorname{Swap}(\mathcal{T}_a, \mathcal{T}_b)$ для сбалансированного роста.</li>
    </ol>
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
    <h3>Теорема (Karaman & Frazzoli, MIT / IJRR 2011):</h3>
    <p class="text-sm">
      Классические алгоритмы PRM и RRT обладают свойством <strong>вероятностной полноты</strong>:
    </p>
    $$\lim_{N \to \infty} P(\text{путь найден} \mid \text{путь существует}) = 1$$
    <p class="text-sm">
      Однако вероятность того, что стоимость найденного решения сходится к оптимальной $c^*$, <strong>тождественно равна нулю</strong>:
    </p>
    $$P\left(\lim_{N \to \infty} \operatorname{Cost}(\mathcal{T}_N) = c^*\right) = 0$$
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Почему RRT фундаментально неоптимален?</h3>
    <ul class="text-sm">
      <li><strong>Случайная фиксация топологии:</strong> ранние ветви дерева, возникшие случайно, навсегда остаются родителями своих потомков.</li>
      <li><strong>Отсутствие памяти о стоимости:</strong> шаг `EXTEND` выбирает геометрически ближайший узел $q_{near}$, полностью игнорируя накопленную стоимость пути от корня $cost(q_{near})$.</li>
      <li>Сколько бы миллионов узлов мы ни добавляли в RRT, траектория навсегда останется изломанной и субоптимальной.</li>
    </ul>
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
  <p>При добавлении нового узла $q_{new}$ алгоритм $RRT^*$ рассматривает окрестность радиуса $r_N = \gamma \left(\frac{\log N}{N}\right)^{1/d}$:</p>

  <div class="card">
    <h3>1. Выбор лучшего родителя (ChooseParent):</h3>
    <p class="text-sm">Среди всех соседей $u \in \operatorname{Near}(q_{new}, r_N)$ выбирается узел с минимальной суммарной стоимостью до старта:</p>
    $$q_{parent} = \arg\min_{u} \left( \operatorname{cost}(u) + \|u - q_{new}\| \right)$$
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>2. Переподключение ветвей (Rewiring):</h3>
    <p class="text-sm">Для каждого соседа $v \in \operatorname{Near}(q_{new}, r_N)$ проверяем условие улучшения:</p>
    $$\text{Если } \operatorname{cost}(q_{new}) + \|q_{new} - v\| < \operatorname{cost}(v):$$
    <ol class="text-sm">
      <li>Проверяем отрезок $(q_{new}, v)$ на коллизии.</li>
      <li>Если свободен — удаляем старое входящее ребро в $v$.</li>
      <li>Назначаем $q_{new}$ новым родителем вершины $v$!</li>
      <li>Рекурсивно обновляем стоимость поддерева узла $v$.</li>
    </ol>
  </div>
  <div class="card-alert text-sm">
    <strong>Гарантия:</strong> $RRT^*$ асимптотически сходится к глобальному оптимуму почти наверное: $P(\lim \operatorname{Cost} = c^*) = 1$.
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
  <iframe src="../../widgets/rrt-exploration/index.html" class="interactive-frame"></iframe>
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
    <h3>Проблема RRT* после первого решения:</h3>
    <ul>
      <li>Как только первый путь стоимостью $c_{best}$ найден, RRT* продолжает генерировать сэмплы по всему конфигурационному пространству $\mathcal{C}$.</li>
      <li>Точки, сумма расстояний от которых до старта и цели больше $c_{best}$, <strong>физически не способны улучшить решение</strong>!</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Informed RRT* (Gammell et al., 2014):</h3>
    <p class="text-sm">Сэмплируем строго внутри гиперэллипсоида (Prolate Hyperspheroid):</p>
    $$\mathcal{C}_{informed} = \{ q \in \mathcal{C} \mid \|q - q_{init}\| + \|q - q_{goal}\| \le c_{best} \}$$
    <ul class="text-sm">
      <li>Фокусы эллипсоида — $q_{init}$ и $q_{goal}$. Длина главной полуоси равна $c_{best}/2$.</li>
      <li>Сэмплинг выполняется отображением из единичной гиперсферы через матрицу поворота $C$ и масштабирования $L$: $q = C L x_{ball} + q_{center}$.</li>
      <li>По мере нахождения лучших путей $c_{best} \downarrow$, эллипсоид сжимается, концентрируя 100% вычислений в перспективной зоне!</li>
    </ul>
  </div>
</div>

</div>

---

## 9. Инженерия сэмплинга: $k$-d tree, CCD и Kinodynamic RRT <span class="badge badge-time">83–88 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Ускорение поиска соседей ($k$-d Tree):</h3>
    <p class="text-sm">Наивный поиск $q_{near}$ среди $N$ вершин дерева требует $\mathcal{O}(N)$ операций.</p>
    <p class="text-sm">При $N = 10^5$ итерация занимает сотни миллисекунд. Использование сбалансированных структур ($k$-d tree, nanoflann) снижает сложность до:</p>
    $$\mathcal{O}(\log N)$$
    <div class="card-alert text-sm mt-2">
      <strong>Continuous Collision Detection (CCD):</strong> проверка заметаемого объема (Swept Volume / GJK) исключает туннелирование робота сквозь тонкие стены на высокой скорости.
    </div>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Kinodynamic RRT (Дифференциальные связи):</h3>
    <p class="text-sm">
      Если робот неголономен ($\dot{x} = f(x, u)$), мы не можем соединять узлы прямой линией!
    </p>
    <ol class="text-sm">
      <li>Выбираем $q_{rand}$.</li>
      <li>Находим ближайший узел по <em>квазиметрике достижимости</em>.</li>
      <li>Сэмплируем управление $u \sim \operatorname{Uniform}(\mathcal{U})$ и длительность $\Delta t$.</li>
      <li>Численно интегрируем систему: $x(t + \Delta t) = x(t) + \int f(x, u) dt$.</li>
      <li>Если отрезок свободен — добавляем траекторный примитив в дерево.</li>
    </ol>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 03 | Итоги и вопросы" -->

## Резюме лекции и контрольные вопросы <span class="badge badge-time">88–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы:</h3>
  <ol class="text-sm">
    <li><strong>Сэмплирующие методы</strong> преодолевают проклятие размерности, заменяя аналитическое построение $\mathcal{C}_{obs}$ локальным детектором коллизий.</li>
    <li><strong>RRT</strong> агрессивно исследует пространство за счет Voronoi Bias, но фундаментально субоптимален.</li>
    <li><strong>RRT*</strong> вводит ChooseParent и Rewiring, обеспечивая асимптотическую оптимальность решения.</li>
    <li><strong>Informed RRT*</strong> концентрирует выборку внутри эллипсоида, ускоряя сходимость в десятки раз.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы для самопроверки:</h3>
  <ul class="text-sm">
    <li>Почему при Goal Bias $> 50\%$ алгоритм RRT часто работает медленнее, чем при $5\%$?</li>
    <li>В чем заключается теорема Карамана–Фраццоли и почему классический RRT не сходится к оптимуму?</li>
    <li>Как алгоритм Bridge Test помогает обнаружить узкие проходы между препятствиями?</li>
    <li>Почему в неголономном пространстве евклидово расстояние $\|q_1 - q_2\|$ не отражает реальную сложность перехода?</li>
  </ul>
  <div class="mt-4 text-center">
    <span class="badge badge-blue">Следующая лекция: Реактивные и локальные методы (DWA, TEB, APF)</span>
  </div>
</div>

</div>
