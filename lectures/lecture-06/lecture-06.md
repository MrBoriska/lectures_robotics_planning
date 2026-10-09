---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
math: katex
header: "Планирование для мобильных роботов | Лекция 06"
footer: "Курс лекций • Лекция 06"
---

<!-- Slide 1 -->
<!-- _class: lead -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 06: Обучение с подкреплением (Reinforcement Learning) и его применение в робототехнике

<div class="mt-4">

<span class="badge badge-blue">⏱️ 90 минут</span>
<span class="badge badge-green">Фундаментальные основы и Sim-to-Real</span>
<span class="badge badge-purple">MDP • Уравнения Беллмана • DQN • Actor-Critic • PPO • SAC • Isaac Sim</span>

</div>

<div class="mt-4" style="font-size: 14px; color: #475569; max-width: 820px; margin: 0 auto; line-height: 1.5;">

Введение в парадигму последовательного принятия решений. Отказ от аналитических уравнений контактов в пользу обучения во взаимодействии со средой. Преодоление барьера переноса из симуляции в физический мир.

</div>

---

<!-- Slide 2 -->
## Место RL в машинном обучении <span class="badge badge-time">05–10 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🎯 Парадигма принятия решений (Kevin Murphy, 2023)
- **Supervised Learning ($y \approx f(x)$):** Требует разметки эксперта; при выходе робота за распределение обучающих данных (Out-of-Distribution) ошибка катастрофически накапливается.
- **Unsupervised Learning ($p(x)$):** Выявляет структуру и латентные представления без целевого сигнала управления.
- **Reinforcement Learning:** Агент оптимизирует долгосрочную отдачу $\mathbb{E}[\sum \gamma^t R_t]$ через активное исследование среды (Trial and Error). Обучающий сигнал — скалярная награда, которая может быть отложенной.

</div>

<div class="card card-success mt-2">

### 🚀 Почему RL критически важен в робототехнике?
- Контакты с грунтом, трение и сыпучие среды не имеют строгих гладких аналитических моделей для классического MPC.
- Инференс обученной нейросети занимает $<1$ мс на бортовом GPU/TPU.

</div>
</div>

<div class="col">
<div class="card" style="padding: 6px;">

![Taxonomy](../../assets/images/lecture-06/rl_taxonomy_murphy.svg)

</div>
</div>
</div>

---

<!-- Slide 3 -->
## Марковский процесс принятия решений (MDP) <span class="badge badge-time">10–15 мин</span>

<div class="grid-2">
<div class="col">
<div class="card">

### 📐 Формальное определение кортежа $\mathcal{M}$
Марковский процесс принятия решений задается пятеркой:

<div class="math-block">

$$ \mathcal{M} = \langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle $$

</div>

- **Пространство состояний $\mathcal{S}$:** Положение, скорости, углы суставов робота $s_t \in \mathbb{R}^n$.
- **Пространство действий $\mathcal{A}$:** Управляющие моменты $\tau_t$ или целевые положения сервоприводов $a_t \in \mathbb{R}^m$.
- **Вероятность переходов $\mathcal{P}$:** Динамика среды
  $$\mathcal{P}(s' \mid s, a) = \mathbb{P}(S_{t+1} = s' \mid S_t = s, A_t = a)$$
- **Функция вознаграждения $\mathcal{R}$:** Скалярное поощрение
  $$\mathcal{R}(s, a) = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a]$$
- **Фактор дисконтирования $\gamma \in [0, 1)$:** Приоритет сиюминутной выгоды над далеким будущим.

</div>
</div>

<div class="col">
<div class="card card-alert">

### 🔄 Свойство Маркова (Markov Property)
Будущее состояние зависит исключительно от текущего состояния и действия, но не от предыстории:

<div class="math-block">

$$ \mathbb{P}(S_{t+1} \mid S_t, A_t, S_{t-1}, A_{t-1}, \dots) = \mathbb{P}(S_{t+1} \mid S_t, A_t) $$

</div>

- Если датчики робота не дают полной картины (нет скорости, окклюзии лидара), среда становится **POMDP** (Partially Observable MDP).
- В POMDP агенту требуется память (буфер истории $H_t$ или рекуррентная сеть LSTM/GRU).

</div>

<div class="card card-accent mt-2">

### 💰 Дисконтированная отдача (Return)
$$ G_t = \sum_{k=0}^\infty \gamma^k R_{t+k+1} $$
Цель агента — найти стратегию $\pi(a \mid s)$, максимизирующую $J(\pi) = \mathbb{E}_{\tau \sim \pi}[G_0]$.

</div>
</div>
</div>

---

<!-- Slide 4 -->
## Функции ценности и уравнения Беллмана <span class="badge badge-time">15–20 мин</span>

<div class="grid-2">
<div class="col">
<div class="card">

### 📊 Функции ценности $V^\pi(s)$ и $Q^\pi(s, a)$
- **Ценность состояния (State-Value Function):**
  $$ V^\pi(s) = \mathbb{E}_\pi \left[ \sum_{k=0}^\infty \gamma^k R_{t+k+1} \;\middle|\; S_t = s \right] $$
- **Ценность действия (Action-Value / Q-Function):**
  $$ Q^\pi(s, a) = \mathbb{E}_\pi \left[ \sum_{k=0}^\infty \gamma^k R_{t+k+1} \;\middle|\; S_t = s, A_t = a \right] $$
- **Функция преимущества (Advantage Function):**
  $$ A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s) $$
  Показывает, насколько действие $a$ лучше среднего действия стратегии $\pi$.

</div>
</div>

<div class="col">
<div class="card card-accent">

### ⚡ Рекуррентные уравнения Беллмана
Ценность текущего шага разбивается на мгновенную награду и дисконтированную ценность следующего состояния:

<div class="math-block">

$$ V^\pi(s) = \sum_{a \in \mathcal{A}} \pi(a|s) \sum_{s', r} p(s', r | s, a) \left[ r + \gamma V^\pi(s') \right] $$

</div>

<div class="math-block">

$$ Q^\pi(s, a) = \sum_{s', r} p(s', r | s, a) \left[ r + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s', a') \right] $$

</div>

### 🏆 Уравнение оптимальности Беллмана для $Q^*$
$$ Q^*(s, a) = \mathcal{R}(s, a) + \gamma \sum_{s'} \mathcal{P}(s'|s, a) \max_{a'} Q^*(s', a') $$
Оптимальная стратегия извлекается жадно: $\pi^*(s) = \arg\max_a Q^*(s, a)$.

</div>
</div>
</div>

---

<!-- Slide 5 -->
## Динамическое программирование: Policy & Value Iteration <span class="badge badge-time">20–25 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🔄 Policy Iteration (Итерация по стратегиям)
Чередование оценивания и улучшения до сходимости:

1. **Policy Evaluation (Оценка ценности):**
   Решение системы линейных уравнений для текущей $\pi_k$:
   $$ V_{i+1}(s) = \sum_a \pi_k(a|s) \sum_{s', r} p(s', r|s, a)[r + \gamma V_i(s')] $$
2. **Policy Improvement (Жадное улучшение):**
   $$ \pi_{k+1}(s) = \arg\max_a \sum_{s', r} p(s', r|s, a)[r + \gamma V^{\pi_k}(s')] $$
- **Теорема об улучшении стратегии:** гарантирует $V^{\pi_{k+1}}(s) \ge V^{\pi_k}(s)$ для всех $s$.

</div>
</div>

<div class="col">
<div class="card card-success">

### 📈 Value Iteration (Итерация по ценностям)
Объединение шага оценки и жадного выбора в единый оператор Беллмана:

<div class="math-block">

$$ V_{k+1}(s) = \max_{a \in \mathcal{A}} \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma V_k(s') \right] $$

</div>

- **Теорема Банаха о неподвижной точке:**
  Оператор Беллмана $\mathcal{T}^*$ является сжимающим отображением с коэффициентом $\gamma < 1$:
  $$ \|\mathcal{T}^* V - \mathcal{T}^* U\|_\infty \le \gamma \|V - U\|_\infty $$
  Гарантирует экспоненциальную сходимость к $V^*$.

</div>

<div class="card card-alert mt-2">

### 🛑 Вычислительный барьер в робототехнике
Требует полного знания модели $\mathcal{P}(s'|s,a)$. Дискретизация 12-мерного шасси дает $100^{12}$ состояний (Curse of Dimensionality).

</div>
</div>
</div>

---

<!-- Slide 6 -->
## Внестратегическое обучение: Q-Learning <span class="badge badge-time">25–30 мин</span>

<div class="grid-2">
<div class="col">
<div class="card">

### 🎲 Model-Free: Обучение по опыту (Watkins, 1989)
Агент исследует среду, совершая шаги $(s_t, a_t, r_{t+1}, s_{t+1})$, без знания матрицы вероятностей переходов $\mathcal{P}$.

<div class="math-block">

$$ Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \delta_t $$

</div>

Где **ошибка временной разности (TD Error):**
$$ \delta_t = \underbrace{R_{t+1} + \gamma \max_{a} Q(S_{t+1}, a)}_{\text{TD Target (оценка Беллмана)}} - \underbrace{Q(S_t, A_t)}_{\text{Текущая оценка}} $$

- **Скорость обучения $\alpha \in (0, 1]$:** вес нового опыта.
- **Off-Policy свойство:** данные собираются по исследовательской $\epsilon$-жадной стратегии, а целевое значение использует $\max_a Q(s', a)$.

</div>
</div>

<div class="col">
<div class="card card-accent">

### ⚖️ Компромисс Exploration vs Exploitation
- **$\epsilon$-жадная стратегия:**
  $$ a_t = \begin{cases} \arg\max_a Q(s_t, a), & \text{с вер. } 1 - \epsilon \\ \text{случайное действие}, & \text{с вер. } \epsilon \end{cases} $$
- **Условия сходимости Роббинса-Монро:**
  $$ \sum_{t=1}^\infty \alpha_t = \infty, \quad \sum_{t=1}^\infty \alpha_t^2 < \infty $$
  Гарантируют сходимость $Q \to Q^*$ почти наверное при посещении всех пар $(s, a)$.

</div>

<div class="card card-alert mt-2">

### ⚠️ Проблема табличного подхода
В робототехнике состояния непрерывны (угол сустава $\theta \in [-\pi, \pi]$). Таблица $Q(s, a)$ требует непрерывной аппроксимации нейросетями!

</div>
</div>
</div>

---

<!-- Slide 7 -->
## Аппроксимация с помощью нейронных сетей (DQN) <span class="badge badge-time">30–35 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🧠 Deep Q-Network (Mnih et al., Nature 2015)
Замена таблицы нейросетью с весами $\theta$: $Q(s, a; \theta) \approx Q^*(s, a)$.

<div class="math-block">

$$ \mathcal{L}(\theta) = \mathbb{E}_{(s, a, r, s') \sim \mathcal{D}} \left[ \left( r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta) \right)^2 \right] $$

</div>

### 🛡️ Две ключевые стабилизирующие инновации
1. **Experience Replay Buffer $\mathcal{D}$:**
   - Хранит $10^5 - 10^6$ переходов $(s, a, r, s')$.
   - Сэмплирование случайных мини-батчей разрушает временную автокорреляцию данных.
2. **Target Network $\theta^-$:**
   - Замороженная копия весов для вычисления TD-цели; обновляется каждые $C$ шагов.
   - Устраняет проблему «гонки за движущейся мишенью».

</div>
</div>

<div class="col">
<div class="card" style="padding: 6px;">

![DQN Architecture](../../assets/images/lecture-06/dqn_architecture.svg)

</div>
</div>
</div>

---

<!-- Slide 8 -->
## Методы градиента стратегии (Policy Gradient) <span class="badge badge-time">35–40 мин</span>

<div class="grid-2">
<div class="col">
<div class="card">

### 🎯 Прямая параметризация стратегии $\pi_\theta(a|s)$
В робототехнике управления приводами непрерывны ($a \in \mathbb{R}^m$). Поиск $\max_a Q(s, a)$ вычислительно невозможен на каждом такте 500 Гц.
- Политика параметризуется нейросетью: например, гауссиана $\pi_\theta(a|s) = \mathcal{N}(\mu_\theta(s), \Sigma_\theta)$.
- **Целевой функционал:** $J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)]$.

</div>

<div class="card card-accent mt-2">

### 📜 Теорема о градиенте стратегии (Sutton et al.)
Градиент целевого функционала не требует знания производных физики среды $\nabla_\theta \mathcal{P}$:

<div class="math-block">

$$ \nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta} \left[ \sum_{t=0}^T \nabla_\theta \log \pi_\theta(A_t \mid S_t) G_t \right] $$

</div>

</div>
</div>

<div class="col">
<div class="card card-success">

### 💡 Алгоритм REINFORCE (Williams, 1992)
1. Собрать траекторию $\tau = (s_0, a_0, r_1, \dots, s_T)$ по политике $\pi_\theta$.
2. Вычислить отдачи для каждого шага: $G_t = \sum_{k=t}^T \gamma^{k-t} R_{k+1}$.
3. Обновить параметры:
   $$ \theta \leftarrow \theta + \alpha \sum_{t=0}^T \nabla_\theta \log \pi_\theta(a_t|s_t) \cdot (G_t - b(s_t)) $$

</div>

<div class="card card-alert mt-2">

### 📉 Базисная линия (Baseline) $b(s)$
- Вычитание $b(s) \approx V(s)$ не смещает математическое ожидание градиента ($\mathbb{E}[\nabla \log \pi \cdot b] = 0$), но колоссально **снижает дисперсию**.
- Недостаток REINFORCE: оценка $G_t$ методом Монте-Карло медленна и требует дожидаться конца эпизода.

</div>
</div>
</div>

---

<!-- Slide 9 -->
## Actor-Critic Архитектуры <span class="badge badge-time">40–45 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🎭 Синергия двух нейросетей
Actor-Critic объединяет преимущества Policy Gradient и функций ценности:

- **Актёр (Actor) $\pi_\theta(a|s)$:** Формирует управляющие воздействия на приводы робота.
- **Критик (Critic) $V_\phi(s)$:** Оценивает ценность состояний и учит Актёра.
- Вместо Монте-Карло $G_t$ используется TD-ошибка (сигнал преимущества):
  $$ \delta_t = R_{t+1} + \gamma V_\phi(S_{t+1}) - V_\phi(S_t) \approx A(S_t, A_t) $$

### ⚡ Правила обновления
- **Актёр:** $\theta \leftarrow \theta + \alpha_\theta \nabla_\theta \log \pi_\theta(a_t|s_t) \cdot \delta_t$
- **Критик:** $\phi \leftarrow \phi - \alpha_\phi \nabla_\phi \left( \frac{1}{2} \delta_t^2 \right)$

</div>
</div>

<div class="col">
<div class="card" style="padding: 6px;">

![Actor-Critic Architecture](../../assets/images/lecture-06/actor_critic_architecture.svg)

</div>
</div>
</div>

---

<!-- Slide 10 -->
## Proximal Policy Optimization (PPO) <span class="badge badge-time">45–50 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🛑 Проблема коллапса политики (Policy Collapse)
В стандартном Policy Gradient слишком большой шаг оптимизатора в пространстве параметров $\theta$ приводит к необратимому падению робота и разрушению стратегии.

### ✂️ Клиппированный функционал PPO (Schulman, 2017)
Отношение вероятностей действий: $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$.

<div class="math-block">

$$ L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t \right) \right] $$

</div>

- Если $A_t > 0$ (действие удачное), $r_t$ ограничивается сверху $1+\epsilon$ ($\epsilon \approx 0.2$).
- Если $A_t < 0$ (действие плохое), $r_t$ ограничивается снизу $1-\epsilon$.
- Предотвращает разрушительно большие обновления стратегии без дорогой матрицы Фишера (как в TRPO).

</div>
</div>

<div class="col">
<div class="card card-success">

### 📐 Generalized Advantage Estimation (GAE)
Оценка преимущества с балансировкой смещения и дисперсии:

<div class="math-block">

$$ \hat{A}_t^{\text{GAE}(\gamma, \lambda)} = \sum_{l=0}^\infty (\gamma \lambda)^l \delta_{t+l}^V $$

</div>

- $\lambda = 0 \implies \hat{A}_t = \delta_t$ (минимальная дисперсия, смещение от $V$).
- $\lambda = 1 \implies \hat{A}_t = G_t - V(s_t)$ (без смещения, максимальная дисперсия).
- Для робототехники стандарт: $\lambda \in [0.95, 0.98]$.

</div>

<div class="card card-alert mt-2">

### 🏆 Почему PPO — стандарт локомоции?
Идеально параллелится на GPU (Isaac Sim, 4096 сред), численно стабилен, не требует калибровки гиперпараметров под каждый мотор.

</div>
</div>
</div>

---

<!-- Slide 11 -->
## Алгоритмы для непрерывного управления (SAC) <span class="badge badge-time">50–55 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🔥 Принцип максимума энтропии (Haarnoja, 2018)
Soft Actor-Critic максимизирует не только суммарное вознаграждение, но и случайность поведения (разнообразие исследуемых действий):

<div class="math-block">

$$ J(\pi) = \sum_{t=0}^T \mathbb{E}_{(s_t, a_t) \sim \rho_\pi} \left[ r(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot \mid s_t)) \right] $$

</div>

Где энтропия распределения действий:
$$ \mathcal{H}(\pi(\cdot \mid s_t)) = \mathbb{E}_{a \sim \pi}[-\log \pi(a \mid s_t)] $$

- **Температура $\alpha > 0$:** баланс между жадной оптимизацией задачи и исследованием пространства действий. Настраивается автоматически через градиентный спуск.

</div>
</div>

<div class="col">
<div class="card card-success">

### 🛡️ Архитектурные преимущества SAC
1. **Off-Policy буфер опыта:** переиспользует прошлые данные, повышая эффективность по сэмплам в 10–20 раз по сравнению с On-Policy PPO.
2. **Двойной критик (Clipped Double Q-Learning):**
   $$ y = r + \gamma \left( \min_{i=1,2} Q_{\bar{\phi}_i}(s', a') - \alpha \log \pi_\theta(a'|s') \right) $$
   Исключает систематическую переоценку Q-функции.
3. **Робастность к внешним ударам:** максимальная энтропия учит робота нескольким равноценным способам парирования возмущений.

</div>

<div class="card mt-2">

### ⚙️ Практика применения
Стандарт де-факто для манипуляций манипуляторами и реальных стендов без симулятора (обучение прямо на железе).

</div>
</div>
</div>

---

<!-- Slide 12 -->
## Обучение с использованием модели (Model-Based RL) <span class="badge badge-time">55–60 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🔮 Парадигма изучения динамики среды
Вместо прямой аппроксимации стратегии агент обучает модель перехода:
$$ s_{t+1} = f_\phi(s_t, a_t) + \epsilon $$

### Две ветви использования модели:
1. **Планирование в реальном времени (Planning / MPC):**
   - На каждом шаге модель генерирует сотни прогнозов траекторий.
   - Метод кросс-энтропии (CEM) или MPPI выбирает оптимальную последовательность действий $a_{t:t+H}$.
   - Примеры: **PETS** (Chua et al.), **PlaNet**, **Dreamer** (Hafner et al.).
2. **Синтез опыта (Dyna / World Models):**
   - Модель используется как бесконечный симулятор для генерации синтетических rollouts для обучения Model-Free алгоритма (SAC/PPO).
   - Пример: **MBPO** (Janner et al.).

</div>
</div>

<div class="col">
<div class="card card-success">

### 📈 Ключевой плюс: Sample Efficiency
Требует на 1–2 порядка меньше реальных взаимодействий со средой (часы вместо месяцев работы шасси).

</div>

<div class="card card-alert mt-2">

### ⚠️ Фундаментальный вызов: Compounding Error
Накопление ошибки прогноза шагов:
$$ \|s_{t+H} - \hat{s}_{t+H}\| \sim \mathcal{O}(e^{L H}) $$

- Неточность в модели контакта приводит к нереалистичным симуляциям (робот «левитирует» над землей в воображаемой модели).
- Решение: ансамбли нейросетей для оценки эпистемической неопределенности и ограничение длины воображаемого горизонта ($H \le 5$).

</div>
</div>
</div>

---

<!-- Slide 13 -->
## Инженерия функции вознаграждения (Reward Shaping) <span class="badge badge-time">60–65 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🎯 Разреженная (Sparse) vs Плотная (Dense) награда
- **Sparse Reward:** $R = +1$ при достижении цели, $0$ иначе. Исключает нежелательное поведение, но требует миллиардов шагов случайного блуждания.
- **Dense Reward:** Скалярный градиент на каждом шаге. Направляет оптимизацию, но подвержен явлению **Reward Hacking**.

### 📜 Теорема Ng, Harada, Russell (1999)
Потенциальное преобразование награды сохраняет оптимальную стратегию $\pi^*$:
$$ F(s, a, s') = \gamma \Phi(s') - \Phi(s) $$
Любое другое произвольное добавление штрафов может привести к паразитным локальным минимумам!

</div>
</div>

<div class="col">
<div class="card card-success">

### 🦿 Типовой профиль награды для четвероногого робота
$$ R_t = R_{\text{task}} - R_{\text{penalty}} $$

- **Отслеживание скорости:** $w_v \exp(-\|v_{xy} - v^*\|^2 / \sigma_v^2)$
- **Стабилизация корпуса:** $- w_\omega (\omega_x^2 + \omega_y^2) - w_{\text{pitch}} \theta^2$
- **Энергоэффективность:** $- w_\tau \sum_{i=1}^{12} \tau_i^2 - w_{\text{power}} \sum |\tau_i \dot{q}_i|$
- **Плавность моментов:** $- w_{\Delta \tau} \|\tau_t - \tau_{t-1}\|^2$ (защита редукторов)
- **Контакт стоп:** $- w_{\text{slip}} \|v_{\text{foot}}\| \cdot \mathbb{I}_{\text{contact}}$ (запрет проскальзывания)

</div>

<div class="card card-alert mt-2">

### 🕵️ Inverse RL (Обучение по демонстрациям)
Если функцию награды невозможно сформулировать аналитически, её извлекают из демонстраций эксперта-оператора (IRL / GAIL).

</div>
</div>
</div>

---

<!-- Slide 14 -->
## Перенос из симуляции в реальность (Sim-to-Real) <span class="badge badge-time">65–70 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🌉 Разрыв реальности (Reality Gap)
Физические симуляторы неизбежно упрощают мир:
- Люфты в циклоидальных редукторах и упругость звеньев.
- Задержки в CAN/EtherCAT шинах (10–30 мс).
- Немоделируемое трение резины о влажный грунт и траву.

### 🎲 Domain Randomization (Рандомизация среды)
Варьирование параметров физики во время обучения в 4096 параллельных мирах GPU:
- Масса звеньев: $m \sim U(0.8m_0, 1.2m_0)$
- Трение стоп: $\mu \sim U(0.2, 1.25)$
- Запаздывание управляющего сигнала: $\Delta t \sim U(5, 35)$ мс
- Шум энкодеров и IMU: $\sigma_{\text{pos}}, \sigma_{\text{vel}}, \sigma_{\text{acc}}$

</div>
</div>

<div class="col">
<div class="card" style="padding: 6px;">

![Teacher Student](../../assets/images/lecture-06/teacher_student_sim2real.svg)

</div>
</div>
</div>

---

<!-- Slide 15 -->
## Интерактивный стенд: Управление обратным маятником (Cart-Pole: LQR vs RL) <span class="badge badge-time">70–85 мин</span>

<div class="interactive-container">
<div class="interactive-header">

<span><i class="interactive-dot"></i> Интерактивная демонстрация: Синтез политики локомоции и балансировки (LQR vs Shaped RL)</span>
<span>Исследование влияния штрафа за энергию $w_u$, парирование внешних толчков и пределы устойчивости</span>

</div>
<iframe src="http://localhost:5599/widgets/rl-policy-shaping/index.html" class="interactive-frame"></iframe>

</div>

<!-- 
Методические указания лектору (15 минут семинарской практики):
1. Задача 1: Продемонстрируйте студентам влияние веса wu. При малом wu (0.05) тележка агрессивно позиционируется, но токи и графики u(t) зашкаливают. При wu=2.0 движение плавное, но время установления возрастает.
2. Задача 2: Нажмите «⚡ Внешний толчок». В режиме Dense RL каскадный регулятор быстро парирует импульс. В режиме Sparse RL система раскачивается и теряет равновесие.
3. Задача 3: Переключите в Optimal LQR и задайте сильное отклонение (>40°). Линейный регулятор теряет устойчивость из-за неучтенной нелинейности гравитации sin(θ) != θ.
-->

---

<!-- Slide 16 -->
## Итоги и перспективы RL в робототехнике <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 📌 Ключевые выводы лекции
1. **Смена парадигмы:** Сложные контакты (шагающие роботы, манипуляция) эффективнее моделировать в высокопроизводительных GPU-симуляторах (Isaac Sim, MuJoCo MJX), чем аналитически в OCP.
2. **Actor-Critic (PPO / SAC):** Рабочие лошадки робототехники. Обеспечивают стабильное обучение в непрерывных пространствах действий с инференсом $< 1$ мс.
3. **Reward Shaping & Sim-to-Real:** Грамотный дизайн штрафов за энергию и рывки в связке с Teacher-Student дистилляцией позволяет переносить обученные политики на реальные шасси ANYmal, Spot, Unitree.

</div>
</div>

<div class="col">
<div class="card card-success">

### 🔮 Мост к Лекции 07: Foundation Models и VLA
- Обучение с подкреплением дает превосходную низкоуровневую моторику, но не понимает семантику окружающей среды.
- В следующей лекции: **Vision-Language-Action (VLA)**, диффузионные политики (**Diffusion Policy**) и мультимодальные модели действий для манипуляций мобильных платформ.

</div>

<div class="card mt-2">

### ❓ Вопросы для самопроверки
1. Почему в непрерывном управлении шагающим роботом Q-Learning уступает Policy Gradient?
2. За счет чего Teacher-Student архитектура способна ориентироваться на рельефе без прямого измерения карты высот?

</div>
</div>
</div>
