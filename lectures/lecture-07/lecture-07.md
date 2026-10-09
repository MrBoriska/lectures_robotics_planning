---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
math: katex
header: "Планирование для мобильных роботов | Лекция 07"
footer: "Курс лекций • Лекция 07"
---

<!-- Slide 1 -->
<div class="lead">

# **Планирование движений мобильных роботов**
## Лекция 07: Мультимодальные модели и генеративные политики управления: VLA, Diffusion Policy, ACT и модели мира (WAM)

<span class="badge badge-accent">Бакалавриат, 3 курс</span> <span class="badge badge-info">⏱️ 90 минут</span> <span class="badge badge-success">VLA • Diffusion Policy • ACT • Flow Matching</span>

</div>

---

<!-- Slide 2 -->
## Введение: Переход к открытому миру <span class="badge badge-time">00–05 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### Замкнутые задачи локомоции (Лекция 06)
- Строго формализованные целевые функции (скорость, равновесие).
- Компактный вектор наблюдений (углы суставов, IMU).
- Фокус на динамической устойчивости и преодолении грунтов.
- **Ограничение:** Робот не понимает, *зачем* и *куда* он идет с точки зрения семантики человека.

</div>
</div>

<div class="col">
<div class="card card-success">

### Семантические манипуляции в открытом мире (Лекция 07)
- Отсутствие явных аналитических моделей взаимодействия с неструктурированными объектами.
- Высокоразмерные мультимодальные входы (RGB-D камеры, инструкции на естественном языке).
- **Главный вызов:** Обобщение на новые предметы (Zero-shot generalization) — как взять чашку, которую робот никогда не видел при обучении?

</div>
</div>
</div>

---

<!-- Slide 3 -->
## План лекции на 90 минут <span class="badge badge-time">05–07 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### Часть 1: Имитационное обучение и диффузия (43 мин)
1. Ограничения классического клонирования поведения (BC)
2. **Проблема мультимодальности:** Почему MSE Loss терпит крах?
3. Архитектура Action Chunking with Transformers (**ACT**)
4. Генеративные диффузионные политики (**Diffusion Policy**)
5. Согласование непрерывных потоков (**Flow Matching**)
6. **Интерактивный симулятор: Diffusion Policy vs MSE в браузере**

</div>
</div>

<div class="col">
<div class="card card-success">

### Часть 2: Архитектуры VLA и бортовой инференс (40 мин)
7. **Анатомия VLA: Связь с классическим Deep Learning** (ViT + LLM + Action Head)
8. **Где VLA побеждает, а где проигрывает классике (MPC/RL)**
9. **Современные достижения VLA (RT-2, OpenVLA, $\pi_0$, Helix)**
10. Модели мира действий (World Action Models, WAM)
11. Разрыв вычислительных частот (Latency Gap) и Edge-железо
12. Резюме лекции и литература

</div>
</div>
</div>

---

<!-- Slide 4 -->
## 1. Ограничения классического клонирования поведения (BC) <span class="badge badge-time">07–14 мин</span>

<div class="grid-2">
<div class="col">

Клонирование поведения (Behavioral Cloning, BC) сводит управление роботом к классическому обучению с учителем (Supervised Learning) на демонстрациях человека:

$$\min_\theta \mathbb{E}_{(s, a) \sim \mathcal{D}} \left[ \mathcal{L}(a, \pi_\theta(s)) \right]$$

где $\mathcal{D} = \{\tau_1, \tau_2, \dots\}$ — датасет траекторий телеоперации эксперта.

Обычно в качестве лосса $\mathcal{L}$ использовалась среднеквадратичная ошибка (MSE):
$$\mathcal{L}_{\text{MSE}} = \|a - \pi_\theta(s)\|^2$$

</div>

<div class="col">
<div class="card card-alert">

### Фундаментальные дефекты простого BC
1. **Сдвиг ковариат (Covariate Shift):**
   На каждом шаге инференса нейросеть делает крошечную ошибку $\varepsilon$. Ошибки интегрируются во времени.
2. **Квадратичный каскадный уход $\mathcal{O}(T^2)$:**
   Робот быстро отклоняется от траектории эксперта и попадает в состояния, которых **никогда не было в датасете** $\mathcal{D}$. Не зная, как восстановиться, политика совершает неадекватные движения и зависает.

</div>
</div>
</div>

---

<!-- Slide 5 -->
## 2. Проблема мультимодальности: Почему MSE неприменим <span class="badge badge-time">14–22 мин</span>

<div class="grid-2">
<div class="col">

В реальной робототехнике почти любая задача **мультимодальна**:
- Человек может обойти препятствие **слева** ($a_1$) или **справа** ($a_2$).
- Робот может взять чашку за ручку ($a_{\text{handle}}$) или за ободок ($a_{\text{rim}}$).

Минимизация MSE-лосса аналитически сводится к поиску математического ожидания распределения:
$$\pi^*(s) = \arg\min_a \mathbb{E}[\|a - a^*\|^2] = \mathbb{E}[a^* | s] \approx \frac{a_1 + a_2}{2}$$

</div>

<div class="col">
<div class="card card-danger">

### Катастрофическое усреднение
Если для объезда колонны допустимы действия:
$$a_1 = -1.0 \;\text{(влево)}, \quad a_2 = +1.0 \;\text{(вправо)}$$

Среднее действие по MSE:
$$a_{\text{mean}} = \frac{-1.0 + 1.0}{2} = 0.0 \;\text{(лобовой удар!)}$$

- MSE оптимизирует распределение под гауссиану, усредняя пики.
- Требуется аппарат **генеративных моделей**, способных сэмплировать один из валидных пиков, а не их середину.

</div>
</div>
</div>

---

<!-- Slide 6 -->
## Мультимодальность: Регрессия против Диффузии <span class="badge badge-time">22–25 мин</span>

<div class="diagram-box">
  <img src="../../assets/images/lecture-07/diffusion_policy_multimodal.svg" alt="Сравнение MSE-регрессии и диффузионных политик при мультимодальном целевом распределении" />
</div>

---

<!-- Slide 7 -->
## 3. Архитектура Action Chunking with Transformers (ACT) <span class="badge badge-time">25–32 мин</span>

<div class="grid-2">
<div class="col">

### Предсказание действий пакетами (Action Chunks)
Вместо генерации единичного действия $a_t$ (порождающего высокочастотный марковский дребезг), ACT предсказывает цельный сплайн на $K$ шагов вперед:

$$A_t = [a_t, a_{t+1}, a_{t+2}, \dots, a_{t+K-1}] \in \mathbb{R}^{K \times m}$$

- Архитектура базируется на **CVAE** (условный вариационный автоэнкодер) с трансформерным энкодером и декодером.
- Проприоцепция и визуальные токены выступают контекстом в механизме внимания (Cross-Attention).

</div>

<div class="col">
<div class="card card-success">

### Временное ансамблирование (Temporal Ensembling)
- На каждом такте $t$ генерируется новый чанк $A_t$.
- На скользящем окне прогнозы перекрываются во времени.
- Итоговое действие вычисляется экспоненциальным взвешиванием:
  $$a_t = \sum_{i=0}^{K-1} w_i A_{t-i}[i], \quad w_i \propto \exp(-m \cdot i)$$
- **Результат:** Исключительная плавность движений манипулятора без рывков сервоприводов.

</div>
</div>
</div>

---

<!-- Slide 8 -->
## 4. Генеративные диффузионные политики (Diffusion Policy) <span class="badge badge-time">32–40 мин</span>

<div class="grid-2">
<div class="col">

### Диффузия как процесс скульптора
Вместо прямой регрессии траектория $A_0$ генерируется итеративным удалением шума из чистого гауссовского шума $A_K \sim \mathcal{N}(0, \mathbf{I})$ за $K$ дискретных шагов:

1. **Прямой процесс (разрушение):** Добавление шума по расписанию $\beta_k$:
   $$q(a_k | a_{k-1}) = \mathcal{N}(a_k; \sqrt{1-\beta_k} a_{k-1}, \beta_k \mathbf{I})$$
2. **Обратный процесс (генерация):** Нейросеть $\epsilon_\theta(a_k, k, o)$ оценивает добавленный шум, обусловленный картинкой $o$:
   $$a_{k-1} = \frac{1}{\sqrt{\alpha_k}} \left( a_k - \frac{\beta_k}{\sqrt{1 - \bar{\alpha}_k}} \epsilon_\theta(a_k, k, o) \right) + \sigma_k z$$

</div>

<div class="col">
<div class="card card-accent">

### Почему это идеально для роботов?
- **Выразительность:** Диффузия естественным образом моделирует произвольные многовершинные распределения с острыми границами.
- **Стабильность обучения:** Обучение сети шума $\epsilon_\theta$ сводится к простому квадратичному лоссу $\mathbb{E}[\|\epsilon - \epsilon_\theta\|^2]$, без нестабильности GAN.
- **Сглаженность:** Выходное действие — это согласованная гладкая траектория в $SE(3)$.

</div>
</div>
</div>

---

<!-- Slide 9 -->
## 5. Согласование непрерывных потоков (Flow Matching) <span class="badge badge-time">40–45 мин</span>

<div class="grid-2">
<div class="col">

### Проблема классической диффузии (DDPM)
- Генерация траектории требует 16–32 шагов инференса сети $\epsilon_\theta$.
- При частоте нейросети 50 Гц задержка составляет $16 \times 20\,\text{мс} = 320\,\text{мс}$ (слишком медленно для реакции на препятствия).
- Траектории в латентном пространстве броуновские (извилистые).

</div>

<div class="col">
<div class="card card-success">

### Flow Matching (Continuous Probability Flow)
Определяет непрерывное векторное поле вероятностного потока через ОДУ:
$$\frac{dx}{dt} = v_\theta(x, t), \quad t \in [0, 1]$$

- Использование принципа **Оптимального Транспорта (Optimal Transport Flow)** спрямляет траектории переноса от шума к действию.
- Достаточно **всего 2–4 шагов** интегрирования ОДУ (метод Эйлера / Хойна)!
- **Индустриальный прорыв:** Используется в модели **$\pi_0$ (Physical Intelligence)** для высокоскоростного складывания одежды.

</div>
</div>
</div>

---

<!-- Slide 10 -->
## Интерактивный симулятор: Diffusion Policy vs MSE <span class="badge badge-time">45–52 мин</span>

<div class="interactive-container">
<div class="interactive-header">
<span><i class="interactive-dot"></i> Интерактивная генерация действий: Преодоление мультимодальности</span>
<span>Сравнение катастрофы усреднения MSE, 16 шагов Diffusion DDPM и 4 шагов Flow Matching</span>
</div>
<iframe src="http://localhost:5599/widgets/diffusion-policy-interactive/index.html" class="interactive-frame"></iframe>
</div>

---

<!-- Slide 11 -->
## 6. Анатомия VLA: Связь с классическим Deep Learning <span class="badge badge-time">52–60 мин</span>

<div class="card card-accent" style="margin-bottom: 8px;">
Модели <strong>Vision-Language-Action (VLA)</strong> — это не магия, а модульный конструктор из классических архитектур Deep Learning:
</div>

<div class="grid-3" style="font-size: 0.9em;">
<div class="col">
<div class="card card-info">

### 1. Энкодеры восприятия
**Классика:** ResNet-50 (CNN), ViT (Vision Transformer, CLIP, SigLIP).
- **Вход:** Мультиракурсные RGB-камеры (на запястье и голове).
- **Роль:** Преобразует пиксели в сетку компактных визуальных эмбеддингов $Z_v \in \mathbb{R}^{P \times D}$. Робот «видит» пространственную геометрию.

</div>
</div>

<div class="col">
<div class="card card-success">

### 2. Когнитивное ядро
**Классика:** LLM / VLM (LLaVA, Gemma, Llama, PaLM).
- **Вход:** Визуальные токены + текст инструкции («Положи вилку справа от тарелки»).
- **Роль:** *Семантический ризонинг*. Механизм Self-Attention переносит знания об объектах и физике мира из интернета на робота.

</div>
</div>

<div class="col">
<div class="card card-alert">

### 3. Голова действий
**Классика:** MLP, Diffusion UNet, DiT (Diffusion Transformer).
- **Вход:** Скрытый вектор состояния из когнитивного ядра.
- **Роль:** Декодирует семантическое намерение в физические приращения позы схвата $\Delta x, \Delta y, \Delta z, \Delta \text{rot}, \text{gripper}$ на горизонт 1–2 с.

</div>
</div>
</div>

---

<!-- Slide 12 -->
## Архитектурный конвейер модели VLA <span class="badge badge-time">60–63 мин</span>

<div class="diagram-box">
  <img src="../../assets/images/lecture-07/vla_architecture_pipeline.svg" alt="Конвейер обработки визуальных, текстовых признаков и генерации действий в архитектуре VLA" />
</div>

---

<!-- Slide 13 -->
## 7. Границы применимости: Где VLA лучше, а где хуже классики <span class="badge badge-time">63–70 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-success">

### Где VLA — абсолютный лидер
1. **Открытый мир (Open-World):** Работа с новыми бытовыми предметами и упаковками без предварительной калибровки CAD-моделей.
2. **Семантическое целеполагание:** Команды вида: «Собери только опасный мусор», «Разложи фрукты по спелости». Классический MPC принципиально не понимает смысл слова «опасный».
3. **Мультизадачность (Multi-Task):** Одна весовая модель заменяет тысячи специализированных алгоритмов сортировки.

</div>
</div>

<div class="col">
<div class="card card-danger">

### Где VLA проигрывает классике (MPC/RL)
1. **Высокочастотная динамика:** VLA работает на **3–10 Гц**. Балансировка на двух ногах при ударе требует **$\ge 500$ Гц** (здесь доминируют MPC и RL).
2. **Гарантии безопасности:** Нейросеть может галлюцинировать. MPC гарантированно соблюдает барьеры (SFC) и конусы трения.
3. **Субмиллиметровая точность:** Задачи прецизионной сборки (вставка штифта с зазором 50 мкм) упираются в потерю разрешения на этапе визуального токенизатора.

</div>
</div>
</div>

---

<!-- Slide 14 -->
## 8. Современные достижения VLA (SOTA 2024–2026) <span class="badge badge-time">70–76 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### RT-1 & RT-2 (Google DeepMind)
- **RT-1:** Сверточный токенизатор TokenLearner + трансформер действий.
- **RT-2:** Прямой перенос весов интернет-VLM (PaLM-E). Действия кодируются как **текстовые токены** словаря: `action_x_128 action_y_245`.
- Продемонстрировал способность к рассуждению: робот выбрал «импровизированный молоток» (камень), когда обычного молотка не было на столе.

</div>
</div>

<div class="col">
<div class="card card-success">

### $\pi_0$ и OpenVLA
- **OpenVLA (Stanford / Berkeley, 2024):** 7B открытая модель на базе Llama 2, обученная на Open X-Embodiment (970 000+ траекторий). Доступна для fine-tuning по LoRA.
- **$\pi_0$ (Physical Intelligence, 2024):** Отказ от дискретных текстовых токенов в пользу Continuous Flow Matching.
  - Двуручное складывание белья, извлечение посуды из раковины.
  - Робот мгновенно адаптируется к сминанию ткани и изменению формы.

</div>
</div>
</div>

---

<!-- Slide 15 -->
## 9. Модели мира действий (World Action Models, WAM) <span class="badge badge-time">76–82 мин</span>

<div class="grid-2">
<div class="col">

### Генерация будущей реальности
World Action Models (WAM) формируют генеративный симулятор физики в воображении агента:
$$\hat{s}_{t+1} \sim P_\theta(s_{t+1} | s_t, a_t)$$

- Примеры: **DayDreamer, UniSim, Genie 2 (Google DeepMind)**.
- Обучаются самоконтролируемо (Self-Supervised) на миллионах часов видео.
- Робот может «представить», что произойдет с чашкой, если толкнуть ее вперед: разобьется ли она, или останется на столе?

</div>

<div class="col">
<div class="card card-accent">

### Планирование в латентном пространстве (Latent Imagination)
- Вместо выполнения опасных проб на реальном роботе генерируются сотни параллельных роллаутов в латентном пространстве модели мира.
- Алгоритм безградиентного предиктивного поиска (**MPPI**) оценивает исходы и выбирает безопасный план.
- **Нулевой износ:** Исследование границ устойчивости без риска поломки оборудования.

</div>
</div>
</div>

---

<!-- Slide 16 -->
## Предиктивное планирование WAM <span class="badge badge-time">82–84 мин</span>

<div class="diagram-box">
  <img src="../../assets/images/lecture-07/world_action_model_rollout.svg" alt="Схема латентного роллаута и предиктивного планирования с использованием модели мира" />
</div>

---

<!-- Slide 17 -->
## 10. Разрыв вычислительных частот (Latency Gap) <span class="badge badge-time">84–87 мин</span>

<div class="grid-2">
<div class="col">

### В чем проблема частот?
- **Модель VLA (7B трансформер):** Частота обновления **2–5 Гц** (время вычисления 200–500 мс).
- **Диффузионная политика действий:** Частота генерации сплайнов **20–50 Гц** (время 20–50 мс).
- **Сервоконтур моторов:** Частота ПИД/FOC-управления **1000 Гц** (время $< 1$ мс).

*Если подавать команду с LLM напрямую в мотор, робот потеряет устойчивость и упадет через 80 миллисекунд.*

</div>

<div class="col">
<div class="card card-accent">

### Многочастотная иерархия стека
1. **Облако / VLA (0.5–3 Гц):** Семантический план («Иди к столу, возьми яблоко»).
2. **Бортовая Diffusion/ACT (20–50 Гц):** Пакетная генерация сплайна движения руки в $SE(3)$.
3. **Низкоуровневая RL-политика (100–200 Гц):** Координация динамики всего тела (Whole-Body Balance).
4. **FOC-контроллер в приводе (1 кГц):** Силомоментное отслеживание токов: $\tau = K_p \Delta q - K_d \dot{q}$.

</div>
</div>
</div>

---

<!-- Slide 18 -->
## 11. Аппаратные платформы бортового инференса <span class="badge badge-time">87–88 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### Бортовые вычислители (Edge AI)
- **NVIDIA Jetson AGX Orin:** 275 TOPS, энергопотребление 60 Вт. Стандарт индустрии на 2024–2025 гг.
- **NVIDIA Jetson Thor (Архитектура Blackwell):** Свыше 1000 TOPS, аппаратные блоки Transformer Engine для бортового запуска VLA.
- На роботах Figure 02 устанавливается связка из трех GPU-модулей в едином теплоотводящем контуре торса.

</div>
</div>

<div class="col">
<div class="card card-success">

### Оптимизация и квантование моделей
- **Квантование FP8 / INT4:** Сжатие весов VLA с 14 ГБ до 3.5 ГБ без потери качества понимания сцены (AWQ, GPTQ).
- **TensorRT-LLM / vLLM:** Спекулятивное декодирование и оптимизация графов вычислений CUDA.
- **FlashAttention:** Снижение квадратичной сложности внимания на длинных контекстах камер.

</div>
</div>
</div>

---

<!-- Slide 19 -->
## Резюме лекции <span class="badge badge-time">88–90 мин</span>

<div class="grid-2">
<div class="col">
<div class="card card-accent">

### Ключевые выводы
- Простое клонирование поведения (MSE) проваливается из-за смещения распределений $\mathcal{O}(T^2)$ и катастрофического усреднения мод.
- **Diffusion Policy** и **Flow Matching** решили проблему мультимодальности, генерируя реалистичные траектории из шума.
- **VLA** соединяет мощь предобученных LLM/ViT с управлением манипуляторами для работы в открытом мире.

</div>
</div>

<div class="col">
<div class="card card-success">

### Финал курса (Лекция 08)
- Мы изучили: геометрию $\to$ кинематику $\to$ оптимальное управление $\to$ обучение с подкреплением $\to$ генеративный ИИ.
- **Впереди (Лекция 08):** Как эти технологии объединяются в современных **антропоморфных роботах-гуманоидах** (Tesla Optimus, Figure 02, Unitree), почему случился производственный бум в Китае и какие барьеры отделяют нас от их массового внедрения?

</div>
</div>
</div>

---

<!-- Slide 20 -->
## Рекомендуемая академическая литература <span class="badge badge-time">90 мин</span>

<div class="grid-2">
<div class="col">

**Диффузия и имитационное обучение:**
- Chi, C., et al. (2023). *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*. RSS.
- Zhao, T. Z., et al. (2023). *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware* (ACT). RSS.
- Lipman, Y., et al. (2023). *Flow Matching for Generative Modeling*. ICLR.

</div>
<div class="col">
<div class="card card-info">

**Модели VLA и Embodied AI:**
- Brohan, A., et al. (2023). *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control*. CoRL.
- Kim, M. J., et al. (2024). *OpenVLA: An Open-Source Vision-Language-Action Model*. arXiv.
- Black, K., et al. (Physical Intelligence, 2024). *$\pi_0$: A Vision-Language-Action Flow Model for General Robot Control*.
- Wu, P., Hafner, D., et al. (2022). *DayDreamer: World Models for Physical Robot Learning*. CoRL.

</div>
</div>
</div>
