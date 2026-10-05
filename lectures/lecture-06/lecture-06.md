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

<span class="badge badge-accent">Бакалавриат, 3 курс</span> <span class="badge badge-info">Лекция 06</span>

</div>

---

<!-- Slide 2 -->
## Введение и мотивация <span class="badge badge-time">00–05 мин</span>

<div class="grid-2">
<div class="col">

**Ограничения классических подходов (MPC)**
- **Разрывные контакты:** Классическое оптимальное управление испытывает вычислительные трудности при оптимизации траекторий с жесткими ударными взаимодействиями стоп о грунт.
- **Неаналитические поверхности:** Сыпучие, скользкие и деформируемые поверхности (песок, грязь, лед) сложно поддаются точному аналитическому моделированию.

</div>
<div class="col">
<div class="card card-alert">

**Математическая проблема**
Разрывы производных в уравнениях динамики при контакте (смена размерности фазового пространства, недифференцируемость) нарушают допущения градиентных методов оптимизации, используемых в MPC.

</div>
</div>
</div>

---

<!-- Slide 3 -->
## План лекции на 90 минут <span class="badge badge-time">05–07 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

**Часть 1: Математический аппарат непрерывного RL** (45 мин)
1. Марковский процесс принятия решений (MDP)
2. Постановка задачи оптимизации политики
3. Теорема о градиенте политики (Policy Gradient)
4. Алгоритмы PPO и SAC
5. Конструирование функций награды (Reward Shaping)

</div>
</div>
<div class="col">
<div class="card card-success">

**Часть 2: Sim-to-Real, симуляторы на GPU и локомоция** (45 мин)
1. Разрыв моделирования (Sim-to-Real Gap)
2. Высокопроизводительные GPU-симуляторы физики
3. Рандомизация среды (Domain Randomization)
4. Архитектура привилегированного обучения (Teacher-Student)
5. Динамическая локомоция четвероногих и двуногих роботов
6. Сравнение и гибридизация MPC и RL

</div>
</div>
</div>

---

<!-- Slide 4 -->
## 1. Марковский процесс принятия решений (MDP) <span class="badge badge-time">07–15 мин</span>

<div class="grid-2">
<div class="col">

Формализация задачи обучения с подкреплением описывается кортежем MDP:
$$\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$$

- $\mathcal{S}$ — непрерывное пространство состояний.
- $\mathcal{A}$ — непрерывное пространство действий.
- $\mathcal{P}(s_{t+1}|s_t, a_t)$ — функция переходной динамики среды.
- $\mathcal{R}(s_t, a_t)$ — скалярная функция локальной награды.
- $\gamma$ — коэффициент дисконтирования.

</div>
<div class="col">
<div class="card card-accent">

**Политика и траектория**
- **Стохастическая политика** $\pi_\theta(a|s)$ — распределение вероятностей действий при заданном состоянии, параметризованное $\theta$.
- **Траектория** $\tau = (s_0, a_0, s_1, a_1, \dots)$.
- **Дисконтированная отдача** $R(\tau) = \sum_{t=0}^{\infty} \gamma^t \mathcal{R}(s_t, a_t)$.

</div>
</div>
</div>

---

<!-- Slide 5 -->
## 2. Постановка задачи оптимизации политики <span class="badge badge-time">15–20 мин</span>

<div class="grid-2">
<div class="col">

**Целевой функционал**
Оптимизация сводится к максимизации ожидаемой дисконтированной отдачи по траекториям, индуцированным политикой $\pi_\theta$:
$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)] \to \max_\theta$$

**Функции ценности**
- **Функция ценности состояния:** $V^\pi(s)$
- **Функция действия-ценности:** $Q^\pi(s, a)$

</div>
<div class="col">
<div class="card card-info">

**Уравнение Беллмана**
Рекурсивная взаимосвязь, позволяющая оценивать функции ценности:
$$Q^\pi(s_t, a_t) = \mathbb{E}_{s_{t+1}}\left[ \mathcal{R}(s_t,a_t) + \gamma V^\pi(s_{t+1}) \right]$$
$$V^\pi(s_{t+1}) = \mathbb{E}_{a_{t+1}\sim\pi}[Q^\pi(s_{t+1}, a_{t+1})]$$

</div>
</div>
</div>

---

<!-- Slide 6 -->
## 3. Теорема о градиенте политики (Policy Gradient Theorem) <span class="badge badge-time">20–28 мин</span>

<div class="grid-2">
<div class="col">

**Вывод градиента**
Для аналитического вычисления градиента функционала применяется Policy Gradient Theorem:
$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}\left[ \sum_{t=0}^T \nabla_\theta \ln \pi_\theta(a_t|s_t) Q^\pi(s_t, a_t) \right]$$

Логарифмическая производная масштабируется оценкой полезности действия.

</div>
<div class="col">
<div class="card card-accent">

**Преимущество (Advantage)**
Для снижения дисперсии градиента используется функция преимущества:
$$A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s)$$
$A^\pi > 0$ означает, что выбранное действие $a_t$ лучше усредненного действия.

</div>
</div>
</div>

---

<!-- Slide 7 -->
## 4. Алгоритм PPO (Proximal Policy Optimization) <span class="badge badge-time">28–35 мин</span>

<div class="grid-2">
<div class="col">

Стандартный градиент политики может приводить к катастрофически большим изменениям параметров. PPO ограничивает шаг обновления.

**Суррогатный функционал с клиппингом (Clipped Surrogate Objective)**
$$L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min(r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t) \right]$$
где $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$.

</div>
<div class="col">
<div class="card card-success">

**Свойства алгоритма**
- Защита от деструктивных шагов обновления в непрерывных пространствах действий.
- Стабильная монотонная сходимость.
- Широкое применение в робототехнике.

</div>
</div>
</div>

---

<!-- Slide 8 -->
## 5. Алгоритм SAC (Soft Actor-Critic) <span class="badge badge-time">35–40 мин</span>

<div class="grid-2">
<div class="col">

**Принцип максимальной энтропии (Maximum Entropy RL)**
SAC стимулирует максимизацию энтропии $\mathcal{H}$ стохастической политики:
$$J(\theta) = \sum_{t=0}^T \mathbb{E}\left[ \mathcal{R}(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot|s_t)) \right]$$

Стохастические непрерывные политики.

</div>
<div class="col">
<div class="card card-accent">

**Преимущества SAC**
- Робастность к мультимодальным возмущениям.
- Обученная политика распределяет вероятность по широкому набору допустимых действий, повышая устойчивость на физическом роботе.

</div>
</div>
</div>

---

<!-- Slide 9 -->
## 6. Конструирование функций награды (Reward Shaping) <span class="badge badge-time">40–45 мин</span>

<div class="grid-2">
<div class="col">

**Компромисс при формировании награды**
- Следование целевой скорости.
- Энергоэффективность моторов (штраф за $\sum \tau_i \dot{q}_i$).
- Гладкость ускорений.
- Штрафы за сильные удары о грунт.

</div>
<div class="col">
<div class="card card-alert">

**Проблема нежелательных локальных оптимумов**
- Неправильно подобранные веса слагаемых награды приводят к нежелательному эксплуатационному поведению.
- Тонкая настройка (Reward Shaping) требует значительных инженерных усилий.

</div>
</div>
</div>

---

<!-- Slide 10 -->
## 7. Разрыв моделирования (Sim-to-Real Gap) <span class="badge badge-time">45–50 мин</span>

<div class="grid-2">
<div class="col">

**Несоответствие динамики симулятора и физического робота**
- Немоделируемое трение (кулоновское и вязкое).
- Люфты редукторов.
- Податливость приводов и передач.

</div>
<div class="col">
<div class="card card-alert">

**Сенсорные и системные несоответствия**
- Запаздывание сенсоров.
- Асимметричные задержки в шине данных.
- Шумы проприоцептивных датчиков.

</div>
</div>
</div>

---

<!-- Slide 11 -->
## 8. Высокопроизводительные GPU-симуляторы физики <span class="badge badge-time">50–55 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

**Параллельная симуляция**
Для сбора репрезентативной выборки RL требует огромного объема опыта.
Параллельная симуляция 4096+ роботов выполняется в едином тензорном пространстве памяти GPU.

</div>
</div>
<div class="col">

**Передовые среды:**
- **NVIDIA Isaac Sim:** Использует движок PhysX 5 и библиотеку Warp.
- **MuJoCo MJX:** Портирование классического MuJoCo на архитектуру JAX.

</div>
</div>

---

<!-- Slide 12 -->
## 9. Рандомизация среды (Domain Randomization) <span class="badge badge-time">55–60 мин</span>

<div class="grid-2">
<div class="col">

**Случайное распределение параметров симуляции**
- Массы звеньев $m \sim \mathcal{U}(m_{\min}, m_{\max})$.
- Коэффициенты трения кулоновского и вязкого взаимодействия $\mu$.

</div>
<div class="col">
<div class="card card-accent">

**Дополнительные возмущения**
- Задержки в шине CAN ($\Delta t_{delay}$).
- Смещения центра масс (CoM).
- Повышает робастность при переносе на реального робота.

</div>
</div>
</div>

---

<!-- Slide 13 -->
## Диаграмма: Преодоление разрыва моделирования Sim-to-Real <span class="badge badge-time">60–62 мин</span>

<div style="text-align: center;">
<img src="../../assets/images/lecture-07/teacher_student_sim2real.svg" alt="Teacher-Student Sim2Real Architecture" style="max-height: 400px;">
</div>

<div class="card card-info" style="margin-top: 1rem; text-align: center;">

Архитектура преодоления разрыва моделирования (Sim-to-Real Gap).

</div>

---

<!-- Slide 14 -->
## 10. Архитектура привилегированного обучения (Teacher-Student) <span class="badge badge-time">62–70 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

**Фаза 1: Обучение политики «Учителя» (Teacher Policy)**
Учитель имеет доступ к неизмеряемым параметрам:
- Точная геометрия рельефа.
- Контактные силы и трение.

</div>
</div>
<div class="col">
<div class="card card-success">

**Фаза 2: Дистилляция в политику «Ученика» (Student Policy)**
Передача знаний через рекуррентные сети (LSTM/GRU/TCN) или трансформеры:
- Входы: история бортовой проприоцепции ($q, \dot{q}, \text{IMU}$).

</div>
</div>
</div>

---

<!-- Slide 15 -->
## 11. Наблюдаемость среды и оценка скрытых параметров <span class="badge badge-time">70–75 мин</span>

<div class="grid-2">
<div class="col">

**Неявная системная идентификация (Implicit System Identification)**
При дистилляции Ученик учится оценивать скрытые параметры среды, которые ему неизвестны напрямую.

</div>
<div class="col">
<div class="card card-info">

**Латентный вектор $z_t$**
Рекуррентная часть сети агрегирует историю сенсорных показаний в латентный вектор.
Вектор сжимает информацию о внешних возмущениях, рельефе и задержках.

</div>
</div>
</div>

---

<!-- Slide 16 -->
## 12. Динамическая локомоция четвероногих роботов <span class="badge badge-time">75–80 мин</span>

<div class="grid-2">
<div class="col">

**Кейсы применения:**
- **ANYmal (ETH Zürich)**
- **Unitree Go2**
- **Boston Dynamics Spot**

</div>
<div class="col">
<div class="card card-accent">

**Преодоление препятствий**
- Каменистые насыпи.
- Ступени и лестницы.
- Скользкие поверхности.
Высокая адаптивность и динамичность движений.

</div>
</div>
</div>

---

<!-- Slide 17 -->
## 13. Двуногая локомоция (Bipedal Locomotion) <span class="badge badge-time">80–84 мин</span>

<div class="grid-2">
<div class="col">

**Специфика двуногих систем**
- Системы с плавающей базой.
- Малая площадь опоры.
- Высокие требования к динамическому равновесию.

</div>
<div class="col">
<div class="card card-alert">

**Роботы Cassie и Digit**
- Удержание динамического равновесия при внешних импульсных ударах.
- Сложность управления по сравнению с четвероногими платформами.

</div>
</div>
</div>

---

<!-- Slide 18 -->
## 14. Сравнение классического MPC и нейросетевого RL в задачах локомоции <span class="badge badge-time">84–87 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-info">

**Классический MPC**
- **Преимущества:** Математические гарантии устойчивости, точный учет ограничений.
- **Недостатки:** Вычислительная сложность, консерватизм моделей ZMP.

</div>
</div>
<div class="col">
<div class="card card-accent">

**Нейросетевой RL**
- **Преимущества:** Время инференса $< 2$ мс (MLP-сеть), устойчивость к разрывным контактам.
- **Недостатки:** Отсутствие формальных доказательств сходимости, опасность деградации за пределами распределения обучения (OOD).

</div>
</div>
</div>

---

<!-- Slide 19 -->
## 15. Гибридные архитектуры (MPC + RL) <span class="badge badge-time">87–89 мин</span>

<div class="grid-2">
<div class="col">

**RL для оптимизации MPC**
- RL выступает как генератор опорных контактов.
- RL аппроксимирует терминальную стоимость (Cost-to-Go) для QP/MPC.

</div>
<div class="col">
<div class="card card-success">

**MPC как фильтр безопасности**
- MPC выступает как защитный барьер безопасности (Safety Filter / Control Barrier Functions, CBF) для RL-политики, гарантируя отсутствие нарушений физических ограничений.

</div>
</div>
</div>

---

<!-- Slide 20 -->
## Резюме лекции <span class="badge badge-time">89–90 мин</span>

<div class="grid-2">
<div class="col">

**Ключевые аспекты:**
- Переход от ручного аналитического моделирования к обучаемым политикам локомоции.
- Использование GPU-симуляторов для генерации данных.

</div>
<div class="col">
<div class="card card-accent">

- Преодоление Sim-to-Real Gap методами Domain Randomization и Teacher-Student.
- Высокая эффективность RL в задачах динамической локомоции на сложном рельефе.

</div>
</div>
</div>

---

<!-- Slide 21 -->
## Рекомендуемая академическая литература <span class="badge badge-time">90 мин</span>

<div class="grid-2">
<div class="col">

**Базовые учебники:**
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction*. MIT press.

**Ключевые статьи:**
- Статьи лаборатории ETH Robotic Systems Lab.

</div>
<div class="col">
<div class="card card-info">

**Современные исследования локомоции:**
- Miki, T., et al. (2022). *Learning robust perceptive locomotion for quadrupedal robots in the wild*. Science Robotics.
- Lee, J., et al. (2020). *Learning quadrupedal locomotion over challenging terrain*. Science Robotics.

</div>
</div>
</div>
