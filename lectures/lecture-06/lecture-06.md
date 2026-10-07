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
<div class="lead">

# **Планирование движений мобильных роботов**
## Лекция 06: Обучение с подкреплением (Deep RL) в робототехнике: от марковских процессов к Sim-to-Real и управлению локомоцией

<span class="badge badge-accent">Бакалавриат, 3 курс</span> <span class="badge badge-info">⏱️ 90 минут</span> <span class="badge badge-success">Sim-to-Real • Isaac Sim • PPO • SAC</span>

</div>

---

<!-- Slide 2 -->
## Введение: Кризис классического управления в динамической локомоции <span class="badge badge-time">00–05 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-alert">

### 🛑 Ограничения классического MPC
- **Разрывные контакты:** Удар стопы о грунт приводит к мгновенной смене динамики. Градиентные оптимизаторы QP/NLP в MPC теряют сходимость.
- **Сложные грунты:** Сыпучие насыпи, снег, мокрый лед и деформируемые поверхности не имеют точных аналитических моделей трения.
- **Вычислительное запаздывание:** Решение нелинейного OCP на каждом такте требует 10–50 мс, что критично для балансировки при внезапных толчках.

</div>
</div>

<div class="col">
<div class="card card-success">

### 🚀 Парадигма обучения с подкреплением (RL)
- **Black-Box динамика:** Модель движения — это физический симулятор, а не система дифференциальных уравнений на борту.
- **Офлайн-синтез:** Миллионы часов падений и проб отрабатываются на GPU до включения реального робота.
- **Инференс за 1 миллисекунду:** На борту выполняется только прямой прогон легкой нейросети (MLP, 500+ Гц), мгновенно парирующей удары.

</div>
</div>
</div>

---

<!-- Slide 3 -->
## План лекции на 90 минут <span class="badge badge-time">05–07 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### Часть 1: Основы непрерывного RL и классификация (43 мин)
1. Марковский процесс принятия решений (MDP) и отдача
2. Функции ценности $V(s), Q(s, a)$ и интуиция Policy Gradient
3. **Классификация современных методов RL** (Model-Free / Model-Based)
4. Алгоритмы локомоции: **PPO** и **SAC**
5. Конструирование функций награды (Reward Shaping)
6. **Интерактивный симулятор: Синтез политики и Reward Shaping в браузере**

</div>
</div>

<div class="col">
<div class="card card-success">

### Часть 2: Sim-to-Real, достижения и сравнение с OC (40 мин)
7. Разрыв моделирования (Sim-to-Real Gap) и рандомизация (Domain Randomization)
8. GPU-симуляторы физики (Isaac Sim, MuJoCo MJX)
9. Архитектура привилегированного обучения (Teacher-Student)
10. **Современные достижения RL в робототехнике (SOTA)**
11. **Сравнительный анализ: Оптимальное управление (MPC) vs Deep RL**
12. Гибридные архитектуры (MPC + RL) и резюме

</div>
</div>
</div>

---

<!-- Slide 4 -->
## 1. Марковский процесс принятия решений (MDP) <span class="badge badge-time">07–14 мин</span>

<div class="grid-2">
<div class="col">

Формализация задачи взаимодействия робота со средой описывается кортежем MDP:
$$\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$$

- $\mathcal{S} \subset \mathbb{R}^n$ — непрерывное **пространство состояний** (углы суставов $q$, скорости $\dot{q}$, ориентация IMU, линейные ускорения).
- $\mathcal{A} \subset \mathbb{R}^m$ — непрерывное **пространство действий** (целевые углы для ПД-контроллеров или моменты $\tau$).
- $\mathcal{P}(s_{t+1}|s_t, a_t)$ — физика среды (гравитация, реакции опор, трение).
- $\mathcal{R}(s_t, a_t)$ — скалярная локальная награда.
- $\gamma \in [0.95, 0.99]$ — коэффициент дисконтирования горизонта.

</div>

<div class="col">
<div class="card card-accent">

### 🎯 Целевой функционал
Робот ищет параметры $\theta$ стохастической политики $\pi_\theta(a|s)$, максимизируя математическое ожидание дисконтированной отдачи:

$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^{\infty} \gamma^t \mathcal{R}(s_t, a_t) \right] \to \max_\theta$$

- **Политика** $\pi_\theta(a|s) = \mathcal{N}(\mu_\theta(s), \Sigma_\theta(s))$ выдает распределение вероятностей действий.
- Стохастичность необходима на этапе обучения для исследования пространства движений (Exploration).

</div>
</div>
</div>

---

<!-- Slide 5 -->
## 2. Функции ценности и интуиция Policy Gradient <span class="badge badge-time">14–22 мин</span>

<div class="grid-2">
<div class="col">

### Функции ценности: Оценка качества состояний
- **Функция ценности состояния:** Ожидаемая отдача из состояния $s$:
  $$V^\pi(s) = \mathbb{E}_\pi \left[ \sum_{t=0}^\infty \gamma^t \mathcal{R}_t \;\Big|\; s_0 = s \right]$$
- **Функция действия-ценности:** Ценность выбора конкретного действия $a$:
  $$Q^\pi(s, a) = \mathbb{E}_\pi \left[ \sum_{t=0}^\infty \gamma^t \mathcal{R}_t \;\Big|\; s_0 = s, a_0 = a \right]$$

</div>

<div class="col">
<div class="card card-success">

### 💡 Физический смысл теоремы Policy Gradient
Градиент функционала качества вычисляется без дифференцирования динамики среды $\mathcal{P}$:

$$\nabla_\theta J(\theta) = \mathbb{E} \left[ \sum_{t=0}^T \nabla_\theta \ln \pi_\theta(a_t|s_t) \cdot A^\pi(s_t, a_t) \right]$$

- **Преимущество (Advantage):**
  $$A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s)$$
- **Интуиция:** Если действие $a_t$ оказалось лучше среднего ($A > 0$), увеличиваем вероятность его выбора. Если действие привело к падению ($A < 0$) — снижаем его вероятность.

</div>
</div>
</div>

---

<!-- Slide 6 -->
## 3. Классификация современных подходов RL в робототехнике <span class="badge badge-time">22–29 мин</span>

<div class="grid-3" style="font-size: 0.9em;">
<div class="col">
<div class="card card-accent">

### 🟢 Model-Free On-Policy
**Алгоритм:** **PPO (Proximal Policy Optimization)**
- Обучается **только на свежих данных**, собранных текущей политикой.
- **Плюсы:** Предельная стабильность сходимости, простая параллелизация на GPU.
- **Минусы:** Низкая эффективность использования данных (Sample Inefficient).
- **Область:** Доминирует в локомоции роботов в симуляторах.

</div>
</div>

<div class="col">
<div class="card card-info">

### 🔵 Model-Free Off-Policy
**Алгоритмы:** **SAC (Soft Actor-Critic), TD3**
- Повторно использует старый опыт из буфера памяти (**Replay Buffer**).
- **Плюсы:** Требует в 10–20 раз меньше шагов среды для обучения.
- **Минусы:** Труднее масштабировать на 4096 параллельных сред GPU.
- **Область:** Обучение манипуляторов напрямую на физических роботах.

</div>
</div>

<div class="col">
<div class="card card-success">

### 🟣 Model-Based RL
**Алгоритмы:** **DreamerV3, MBPO**
- Обучает компактную модель мира $\hat{s}_{t+1} = f(s_t, a_t)$ в латентном пространстве.
- **Плюсы:** «Мечтает» о миллионах вариантов без обращения к симулятору.
- **Минусы:** Ошибки аппроксимации модели накапливаются на длинном горизонте.
- **Область:** Перспективные гибриды с VLA и навигация.

</div>
</div>
</div>

---

<!-- Slide 7 -->
## 4. Рабочие лошадки локомоции: PPO и SAC <span class="badge badge-time">29–36 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🛡️ PPO: Защита от разрушительных обновлений
Стандартный градиентный шаг может катастрофически сломать походку робота. PPO вводит клиппинг отношения вероятностей $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$:

$$L^{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t \left[ \min\Big(r_t(\theta) \hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\Big) \right]$$

- Клиппинг (обычно $\epsilon = 0.2$) запрещает политике меняться слишком резко за одну итерацию.
- **Золотой стандарт** для ANYmal, Unitree, Figure и Tesla Optimus.

</div>
</div>

<div class="col">
<div class="card card-success">

### 🎲 SAC: Принцип максимальной энтропии
SAC решает задачу не только максимизации награды, но и сохранения вариативности (стохастичности) действий:

$$J(\theta) = \mathbb{E} \left[ \sum_{t=0}^T \gamma^t \Big(\mathcal{R}(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot|s_t))\Big) \right]$$

- Энтропия $\mathcal{H}$ стимулирует исследовать альтернативные позы.
- Робот не «закрепощается» в одной позе, что делает походку устойчивой к случайным внешним толчкам.

</div>
</div>
</div>

---

<!-- Slide 8 -->
## 5. Конструирование функций награды (Reward Shaping) <span class="badge badge-time">36–42 мин</span>

<div class="grid-2">
<div class="col">

В отличие от игр, где награда бинарна (+1 за победу), локомоция требует многокритериального проектирования:

$$\mathcal{R}_t = w_v R_{\text{speed}} + w_\theta R_{\text{balance}} - w_\tau R_{\text{torque}} - w_{\Delta} R_{\text{smooth}} - w_c R_{\text{slip}}$$

1. **Целевые слагаемые (Task Rewards):**
   - Отслеживание линейной скорости: $\exp(-\|v_{xy} - v_{xy}^*\|^2 / \sigma_v)$
   - Отслеживание рыскания: $\exp(-(\omega_z - \omega_z^*)^2 / \sigma_\omega)$
2. **Физические штрафы (Regularization):**
   - Нагрев обмоток двигателей: $-\sum \tau_i^2$ (Омические потери $I^2 R$)
   - Механические рывки: $-\sum (\tau_{t} - \tau_{t-1})^2$ (Защита редукторов)
   - Проскальзывание опорных стоп: $-\|v_{\text{foot}}\| \cdot F_{\text{contact}}$

</div>

<div class="col">
<div class="card card-alert">

### ⚠️ Ловушки локальных оптимумов
- **Слишком высокий штраф за энергию:** Робот предпочитает лечь на живот и не двигаться, чтобы не тратить ток.
- **Слишком малый штраф за рывки:** Появляется высокочастотный дребезг (Chattering), разрушающий волновые редукторы на физическом шасси.
- **Reward Exploitation:** Агент находит нефизичные артефакты симулятора (например, отталкивание от невидимых граней коллизий).

</div>
</div>
</div>

---

<!-- Slide 9 -->
## Интерактивный симулятор: Синтез политики и Reward Shaping <span class="badge badge-time">42–48 мин</span>

<div class="interactive-container">
<div class="interactive-header">
<span><i class="interactive-dot"></i> Интерактивная среда RL: Балансировка и трекинг целевой позы</span>
<span>Исследование влияния весов w_p, w_θ, w_u и сравнение с классическим LQR</span>
</div>
<iframe src="http://localhost:5599/widgets/rl-policy-shaping/index.html" class="interactive-frame"></iframe>
</div>

---

<!-- Slide 10 -->
## 6. Разрыв моделирования (Sim-to-Real Gap) и Domain Randomization <span class="badge badge-time">48–54 мин</span>

<div class="grid-2">
<div class="col">

### В чем корень разрыва реальности?
Политика, обученная в идеальном симуляторе, падает на реальном роботе за 2 секунды из-за факторов:
1. **Люфты и упругость:** Волновые редукторы имеют нелинейный люфт и крутильную жесткость.
2. **Задержки в шине (CAN Bus):** Команда на мотор запаздывает на 5–15 мс; задержка асимметрична.
3. **Температурный дрейф:** При нагреве мотора сопротивление обмотки растет, снижая развиваемый момент.

</div>

<div class="col">
<div class="card card-accent">

### 🎲 Domain Randomization (DR)
При обучении каждый из 4096 параллельных роботов помещается в уникальный физический мир:
- Масса корпуса: $m \sim \mathcal{U}(0.85 m_0, 1.25 m_0)$
- Трение стопы о грунт: $\mu \sim \mathcal{U}(0.2, 1.2)$
- Смещение центра масс: $\Delta \text{CoM} \sim \mathcal{U}(-3\,\text{см}, +3\,\text{см})$
- Задержка контура: $\Delta t \sim \mathcal{U}(2\,\text{мс}, 20\,\text{мс})$
- Шум энкодеров суставов: $\sigma_q \sim \mathcal{N}(0, 0.02\,\text{рад})$

*Результат:* Политика учится быть инвариантной к неточностям динамики.

</div>
</div>
</div>

---

<!-- Slide 11 -->
## 7. Высокопроизводительные GPU-симуляторы физики <span class="badge badge-time">54–59 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### ⚡ Парадигма тензорной симуляции на GPU
Раньше (CPU, Gazebo/Bullet): 1 робот = 1 поток процессора. Обучение походки занимало недели.

**Современный стек (NVIDIA Isaac Sim / MuJoCo MJX):**
- Вся симуляция (4096+ сред) исполняется **полностью в тензорной памяти одного GPU** (NVIDIA RTX 4090 / A100).
- Данные наблюдений $s_t$ не копируются через шину PCIe в память CPU — нейросеть обучается прямо в тензорах Torch/JAX.
- **Скорость сбора опыта:** 100 000+ кадров физики в секунду. 10 лет реального опыта набирается за **20–30 минут**.

</div>
</div>

<div class="col">

### Ключевые программные среды (2024–2026)
1. **NVIDIA Isaac Sim / Isaac Lab (PhysX 5 & Warp):**
   - Индустриальный стандарт для четвероногих и гуманоидных роботов (Unitree, Figure, Boston Dynamics).
   - Точные модели контактов и поддержка параллельного рейкастинга лидаров.
2. **MuJoCo MJX (DeepMind / Google):**
   - Портирование физического движка MuJoCo на компилятор JAX.
   - Идеально для легковесных платформ и дифференцируемой физики.

</div>
</div>

---

<!-- Slide 12 -->
## 8. Архитектура Teacher-Student (Привилегированное обучение) <span class="badge badge-time">59–67 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### Фаза 1: Учитель (Teacher Policy)
Обучается в симуляторе с доступом к **привилегированной информации** $e_t$, которую невозможно измерить датчиками реального робота:
- Точная карта высот рельефа под стопами;
- Векторы контактных сил и коэффициент трения $\mu$;
- Точное положение центра масс CoM.
*Учитель оперирует полным марковским состоянием $s_t = (o_t, e_t)$.*

</div>
</div>

<div class="col">
<div class="card card-success">

### Фаза 2: Ученик (Student Policy)
Дистиллируется из Учителя через имитационное обучение (MSE потерь действий):
- На вход поступает **только бортовая история** сенсоров: $H_t = [o_t, o_{t-1}, \dots, o_{t-K}]$ (углы суставов, IMU).
- Рекуррентная сеть (TCN / GRU / MLP) сжимает историю в латентный вектор $z_t$.
- **Неявная идентификация системы:** Вектор $z_t$ автоматически восстанавливает свойства рельефа и трение по проскальзыванию ног!

</div>
</div>
</div>

---

<!-- Slide 13 -->
## Диаграмма: Преодоление разрыва моделирования Sim-to-Real <span class="badge badge-time">67–70 мин</span>

<div style="text-align: center;">
<img src="../../assets/images/lecture-07/teacher_student_sim2real.svg" alt="Teacher-Student Sim2Real Architecture" style="max-height: 420px;">
</div>

<div class="card card-info" style="margin-top: 0.5rem; text-align: center; font-size: 0.9em;">
Двухэтапная дистилляция: от идеального всеведения Учителя на GPU к компактной робастной бортовой политике Ученика.
</div>

---

<!-- Slide 14 -->
## 9. Современные достижения RL в робототехнике (SOTA) <span class="badge badge-time">70–77 мин</span>

<div class="grid-3" style="font-size: 0.9em;">
<div class="col">
<div class="card card-info">

### 🐕 Слепой паркур ANYmal
*(ETH Zürich, Science Robotics)*
- Робот преодолевает каменистые завалы и лестничные марши **вслепую** (без лидара и камер), опираясь только на латентную оценку $z_t$.
- Бег по снегу, мокрому льду и грязи со скоростью до 3.5 м/с.

</div>
</div>

<div class="col">
<div class="card card-success">

### 🏃 Динамический бег Cassie / H1
*(UC Berkeley & Unitree)*
- Двуногие платформы с плавающей базой удерживают равновесие при сильных ударах человека.
- Сальто назад, прыжки на тумбу и динамический бег на 100 метров, синтезированные сквозным RL в Isaac Sim.

</div>
</div>

<div class="col">
<div class="card card-accent">

### 🖐️ Ловкие манипуляции кистями
*(OpenAI, Сбер, ИТМО)*
- Сборка кубика Рубика и вращение двух шаров в ладони (In-Hand Manipulation).
- Синтез сотен координационных синергий пальцев при наличии трения качения и скольжения.

</div>
</div>
</div>

---

<!-- Slide 15 -->
## 10. Сравнение классического MPC и нейросетевого RL <span class="badge badge-time">77–84 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-info">

### 📐 Оптимальное управление (MPC)
- **Плюсы:**
  - Строгие математические доказательства устойчивости (функции Ляпунова).
  - Жесткое гарантированное соблюдение ограничений ($u \in \mathcal{U}, x \in \mathcal{X}$).
- **Минусы:**
  - Тяжелые численные расчеты онлайн (50 Гц макс).
  - Сбои при разрывах контактов (Infeasible QP).
  - Требует кропотливой ручной калибровки физических моделей.

</div>
</div>

<div class="col">
<div class="card card-accent">

### 🧠 Обучение с подкреплением (Deep RL)
- **Плюсы:**
  - Время инференса **$< 1$ мс** на борту (частота 500–1000 Гц).
  - Робастность к ударным разрывным контактам и скольжению.
  - Синтезирует сложные нелинейные биомеханические компенсации.
- **Минусы:**
  - «Черный ящик»: отсутствие формальных гарантий безопасности.
  - Риск аварии при попадании в состояния вне распределения обучения (OOD).

</div>
</div>
</div>

---

<!-- Slide 16 -->
## 11. Гибридные архитектуры: Синергия MPC и RL <span class="badge badge-time">84–88 мин</span>

<div class="grid-2">
<div class="col">

В передовых роботах MPC и RL не исключают, а дополняют друг друга:

1. **RL как генератор референсов для MPC:**
   Нейросеть генерирует оптимальные точки постановки ног (Footstep Planning) и профили реакций опор, а быстрый выпуклый QP-регулятор рассчитывает моменты.
2. **RL как терминальная стоимость (Cost-to-Go):**
   Функция ценности $V^\pi(x)$ обученного RL выступает терминальным слагаемым $\Phi(x_N)$ в MPC, сжимая необходимый предиктивный горизонт с 2 секунд до 0.2 секунд!

</div>

<div class="col">
<div class="card card-success">

### 🛡️ MPC как фильтр безопасности (Safety Filter)
- Нейросетевая политика формирует желаемое действие $u_{\text{RL}}$.
- На выходе стоит легковесный контроллер на базе функций барьера управления (**Control Barrier Functions, CBF**):
  $$\min_{u} \|u - u_{\text{RL}}\|^2 \quad \text{s.t.} \quad L_f B(x) + L_g B(x) u + \alpha(B(x)) \ge 0$$
- Если действие RL грозит опрокидыванием или превышением предела момента, CBF мгновенно корректирует команду до безопасной границы.

</div>
</div>
</div>

---

<!-- Slide 17 -->
## Резюме лекции <span class="badge badge-time">88–90 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### 🔑 Ключевые выводы
- Разрывные контакты ломают классический градиентный MPC — решение лежит в переходе к обучению на основе взаимодействия (RL).
- **PPO** является стандартом локомоции благодаря суррогатному клиппингу, а **SAC** дает максимальную робастность за счет энтропии.
- Параллельные симуляторы на GPU (Isaac Sim) позволяют генерировать десятилетия опыта за минуты.

</div>
</div>

<div class="col">
<div class="card card-success">

### 🚀 Инженерный мост к Лекции 07
- Преодоление Sim-to-Real gap строится на двух китах: **Domain Randomization** и **Teacher-Student**.
- RL решил задачу стабильного перемещения ног в пространстве.
- **Следующий вопрос курса (Лекция 07):** Как перейти от слепого бега ног к осмысленному манипулированию предметами и пониманию команд человека через мультимодальные модели (VLA)?

</div>
</div>
</div>

---

<!-- Slide 18 -->
## Рекомендуемая академическая литература <span class="badge badge-time">90 мин</span>

<div class="grid-2">
<div class="col">

**Фундаментальные учебники:**
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. MIT Press.
- Bertsekas, D. (2019). *Reinforcement Learning and Optimal Control*. Athena Scientific.

**Ключевые статьи по алгоритмам:**
- Schulman, J., et al. (2017). *Proximal Policy Optimization Algorithms* (PPO). arXiv.
- Haarnoja, T., et al. (2018). *Soft Actor-Critic: Off-Policy Maximum Entropy Deep RL* (SAC). ICML.

</div>
<div class="col">
<div class="card card-info">

**Прорывы Sim-to-Real и локомоции:**
- Miki, T., Lee, J., Hwangbo, J., & Hutter, M. (2022). *Learning robust perceptive locomotion for quadrupedal robots in the wild*. Science Robotics.
- Lee, J., et al. (2020). *Learning quadrupedal locomotion over challenging terrain*. Science Robotics.
- Rudin, N., et al. (2022). *Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning*. CoRL.

</div>
</div>
</div>
