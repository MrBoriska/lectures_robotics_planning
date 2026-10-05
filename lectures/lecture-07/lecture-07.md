---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
math: katex
header: "Планирование для мобильных роботов | Лекция 07"
footer: "Курс лекций • Лекция 07"
---

<!-- _class: lead -->
# **Планирование движений мобильных роботов**
## Лекция 07: Мультимодальные модели и генеративные политики управления: VLA, Diffusion Policy, ACT и модели мира (WAM)

<div class="badges">
  <span class="badge badge-primary">Сложность: Высокая</span>
  <span class="badge badge-secondary">Модуль 3</span>
</div>

---

## Введение: Переход к открытому миру <span class="badge badge-time">00–05 мин</span>

<div class="grid-2">
  <div class="col">
    <div class="card card-accent">
      <h3>Замкнутые задачи локомоции</h3>
      <ul>
        <li>Строго формализованные функции вознаграждения (Обучение с подкреплением).</li>
        <li>Ограниченное пространство состояний.</li>
        <li>Фокус на стабилизации динамики и устойчивости возмущений.</li>
      </ul>
    </div>
  </div>
  <div class="col">
    <div class="card card-success">
      <h3>Семантические манипуляции</h3>
      <ul>
        <li>Отсутствие явной аналитической модели взаимодействия (неструктурированная среда).</li>
        <li>Высокая размерность входных данных (визуальные и текстовые модальности).</li>
        <li>Требование к обобщению (Zero-shot generalization).</li>
      </ul>
    </div>
  </div>
</div>

---

## План лекции на 90 минут <span class="badge badge-time">05–07 мин</span>

<div class="grid-2">
  <div class="col">
    <div class="card card-accent">
      <h3>Часть 1 (45 мин)</h3>
      <p><strong>Имитационное обучение и генеративные политики</strong></p>
      <ul>
        <li>Проблемы клонирования поведения (BC).</li>
        <li>Мультимодальность распределений действий.</li>
        <li>Action Chunking with Transformers (ACT).</li>
        <li>Диффузионные политики (Diffusion Policy) и Flow Matching.</li>
      </ul>
    </div>
  </div>
  <div class="col">
    <div class="card card-accent">
      <h3>Часть 2 (45 мин)</h3>
      <p><strong>VLA-модели и бортовой инференс</strong></p>
      <ul>
        <li>Архитектуры Vision-Language-Action (VLA).</li>
        <li>Сравнительный анализ современных моделей (RT-2, OpenVLA, π₀).</li>
        <li>Модели мира действий (World Action Models).</li>
        <li>Вычислительный бюджет и задержки (Latency).</li>
      </ul>
    </div>
  </div>
</div>

---

## 1. Ограничения классического клонирования поведения <span class="badge badge-time">07–15 мин</span>

<div class="grid-2">
  <div class="col">
    <p>Клонирование поведения (Behavioral Cloning, BC) сводит задачу управления к обучению с учителем, максимизируя правдоподобие действий эксперта:</p>
    <p>$$ \min_\theta \mathbb{E}_{(s, a) \sim \mathcal{D}} \left[ \mathcal{L}(a, \pi_\theta(s)) \right] $$</p>
    <p>где $\mathcal{D}$ — набор демонстрационных траекторий.</p>
  </div>
  <div class="col">
    <div class="card card-alert">
      <h3>Фундаментальные проблемы</h3>
      <ul>
        <li><strong>Covariate Shift</strong>: Накопление ошибок аппроксимации приводит к выходу траектории за пределы обучающего распределения состояний.</li>
        <li><strong>Квадратичный рост ошибки</strong>: Расхождение между ожидаемой и экспертной траекториями растет как $\mathcal{O}(T^2)$, где $T$ — горизонт планирования.</li>
      </ul>
    </div>
  </div>
</div>

---

## 2. Проблема мультимодальности целевого распределения <span class="badge badge-time">15–22 мин</span>

<div class="grid-2">
  <div class="col">
    <p>Классическое BC часто использует среднеквадратичную ошибку (MSE Loss), что эквивалентно предположению об унимодальном гауссовском распределении целевой переменной.</p>
    <p>Если для состояния $s$ возможны два эквивалентных, но топологически различных действия $a_1$ и $a_2$ (например, обход препятствия слева или справа), минимизация MSE сходится к математическому ожиданию:</p>
    <p>$$ a_{mean} = \mathbb{E}[a|s] \approx \frac{a_1 + a_2}{2} $$</p>
  </div>
  <div class="col">
    <div class="card card-alert">
      <h3>Катастрофическое усреднение</h3>
      <p>Действие $a_{mean}$ может быть физически недопустимым (столкновение с препятствием), что делает среднеквадратичную регрессию неадекватной для задач со сложной топологией пространства решений.</p>
    </div>
  </div>
</div>

---

## 3. Архитектура Action Chunking with Transformers (ACT) <span class="badge badge-time">22–29 мин</span>

<div class="grid-2">
  <div class="col">
    <p>Метод ACT решает проблему накопления ошибок путем предсказания последовательности (чанка) будущих действий вместо единичного шага:</p>
    <p>$$ A_t = [a_t, a_{t+1}, \dots, a_{t+K-1}] $$</p>
    <p>Модель использует архитектуру CVAE (Conditional Variational Autoencoder), обусловленную текущими наблюдениями (изображение и проприоцепция).</p>
  </div>
  <div class="col">
    <div class="card card-success">
      <h3>Временное сглаживание</h3>
      <p>На каждом шаге $t$ алгоритм прогнозирует новый чанк и агрегирует пересекающиеся прогнозы (Temporal Ensembling) с экспоненциальным затуханием весов. Это радикально повышает гладкость траекторий и устойчивость к локальным ошибкам перцепции.</p>
    </div>
  </div>
</div>

---

## 4. Генеративные диффузионные политики <span class="badge badge-time">29–38 мин</span>

<div class="grid-2">
  <div class="col">
    <p>Диффузионные политики (Diffusion Policy) моделируют распределение действий $p(a|o)$ через обратный стохастический процесс. Формулировка опирается на стохастические дифференциальные уравнения (DDPM или Score-based generative models):</p>
    <p>$$ d \mathbf{x} = f(\mathbf{x}, t)dt + g(t)d\mathbf{w} $$</p>
    <p>Модель нейронной сети $\epsilon_\theta(\mathbf{x}_k, k, \mathbf{o})$ предсказывает инжектированный гауссовский шум.</p>
  </div>
  <div class="col">
    <div class="card card-accent">
      <h3>Процесс сэмплирования</h3>
      <p>Генерация траектории представляет собой процесс итеративного шумоподавления Ланжевена, где начальное случайное действие $\mathbf{x}_K \sim \mathcal{N}(0, I)$ постепенно преобразуется в допустимую управляющую траекторию, с учетом обусловливающего признака $\mathbf{o}$ (наблюдения).</p>
    </div>
  </div>
</div>

---

## Мультимодальность: Регрессия против Диффузии <span class="badge badge-time">38–41 мин</span>

<div class="diagram-box">
  <img src="../../assets/images/lecture-07/diffusion_policy_multimodal.svg" alt="Сравнение MSE-регрессии и диффузионных политик при мультимодальном целевом распределении" />
</div>

---

## 5. Согласование непрерывных потоков (Flow Matching) <span class="badge badge-time">41–45 мин</span>

<div class="grid-2">
  <div class="col">
    <p>Flow Matching представляет собой обобщение диффузионных моделей, определяющее переход от базового распределения к целевому не через дискретные марковские шаги, а через непрерывные векторные поля (Vector Fields) вероятностного потока (Probability Flow ODE):</p>
    <p>$$ \frac{dx}{dt} = v_\theta(x, t) $$</p>
  </div>
  <div class="col">
    <div class="card card-success">
      <h3>Вычислительные преимущества</h3>
      <ul>
        <li>Более прямые траектории в латентном пространстве.</li>
        <li>Возможность использования решателей ОДУ (Euler, Heun) с большим шагом.</li>
        <li>Сокращение числа итераций инференса (NFE) в 3-5 раз по сравнению со стандартным DDPM без потери выразительной способности.</li>
      </ul>
    </div>
  </div>
</div>

---

## 6. Входные модальности и кодирование наблюдений <span class="badge badge-time">45–52 мин</span>

<div class="grid-2">
  <div class="col">
    <div class="card card-accent">
      <h3>Перцептивные модальности</h3>
      <ul>
        <li><strong>Мультиракурсные камеры</strong>: Стерео- и RGB-D сенсоры для пространственной оценки.</li>
        <li><strong>Проприоцепция</strong>: Состояния суставов (углы, скорости, моменты).</li>
        <li><strong>Естественный язык</strong>: Текстовые инструкции для семантического обусловливания.</li>
      </ul>
    </div>
  </div>
  <div class="col">
    <p>Агрегация разнородных данных требует специализированных архитектур кодировщиков:</p>
    <ul>
      <li>Предварительно обученные <strong>Vision Transformers (ViT)</strong> (например, CLIP) или сверточные сети (ResNet-50) для экстракции визуальных признаков.</li>
      <li>Проекционные слои (MLP) для объединения проприоцептивного состояния и текстовых эмбеддингов.</li>
    </ul>
  </div>
</div>

---

## 7. Архитектуры Vision-Language-Action (VLA) <span class="badge badge-time">52–60 мин</span>

<div class="grid-2">
  <div class="col">
    <p>Модели VLA расширяют парадигму больших языковых моделей (LLM), вводя действия физического агента как дополнительную выходную модальность.</p>
    <p>Сквозное (end-to-end) отображение:</p>
    <p style="text-align: center;"><strong>Изображение + Текст $\to$ Траектория приводов</strong></p>
  </div>
  <div class="col">
    <div class="card card-success">
      <h3>Когнитивный базис</h3>
      <p>Использование весов предобученных мультимодальных LLM (VLM) обеспечивает робототехническую систему пониманием семантики сцены, объектов и физических законов (Common Sense Reasoning), недоступным при обучении исключительно на траекториях с нуля.</p>
    </div>
  </div>
</div>

---

## 8. Сравнительный анализ моделей VLA <span class="badge badge-time">60–67 мин</span>

<div class="grid-2">
  <div class="col">
    <div class="card card-accent">
      <h3>Эволюция подходов</h3>
      <ul>
        <li><strong>RT-1 / RT-2 (Google DeepMind)</strong>: Трансформерные архитектуры, рассматривающие действия как языковые токены.</li>
        <li><strong>OpenVLA</strong>: Открытая архитектура на базе Llama 2, оптимизированная под эффективность тонкой настройки (LoRA).</li>
      </ul>
    </div>
  </div>
  <div class="col">
    <div class="card card-accent">
      <h3>Новые парадигмы</h3>
      <ul>
        <li><strong>$\pi_0$ (Physical Intelligence)</strong>: Интеграция VLM с Continuous Flow Matching. Отказ от дискретной токенизации действий в пользу генерации непрерывных векторных полей, что критически важно для динамических манипуляций.</li>
      </ul>
    </div>
  </div>
</div>

---

## Архитектурный конвейер модели VLA <span class="badge badge-time">67–70 мин</span>

<div class="diagram-box">
  <img src="../../assets/images/lecture-07/vla_architecture_pipeline.svg" alt="Конвейер обработки визуальных, текстовых признаков и генерации действий в архитектуре VLA" />
</div>

---

## 9. Представление действий: Дискретные токены vs Диффузия <span class="badge badge-time">70–75 мин</span>

<div class="grid-2">
  <div class="col">
    <div class="card card-alert">
      <h3>Дискретная токенизация (Action Tokens)</h3>
      <p>Пространство непрерывных действий квантуется на $N$ корзин (bins). Действия генерируются авторегрессионно как элементы словаря.</p>
      <ul>
        <li>Потеря точности из-за дискретизации.</li>
        <li>Разрывность непрерывной динамики манипулятора.</li>
      </ul>
    </div>
  </div>
  <div class="col">
    <div class="card card-success">
      <h3>Непрерывный вывод (Diffusion / Flow Head)</h3>
      <p>LLM генерирует плотный латентный контекст, который подается в обусловленную диффузионную сеть (UNet или DiT).</p>
      <ul>
        <li>Высокоточный непрерывный контроль.</li>
        <li>Естественное моделирование мультимодальности.</li>
      </ul>
    </div>
  </div>
</div>

---

## 10. Модели мира действий (World Action Models) <span class="badge badge-time">75–80 мин</span>

<div class="grid-2">
  <div class="col">
    <p>World Action Models (WAM) формируют внутреннее понимание динамики среды агентом. Задачей модели мира является аппроксимация стохастической функции переходов системы:</p>
    <p>$$ P(s_{t+1}, r_{t} | s_{\le t}, a_{\le t}) $$</p>
    <p>Обучение производится самоконтролируемо (Self-Supervised) на массивах неразмеченных видеоданных взаимодействий с миром.</p>
  </div>
  <div class="col">
    <div class="card card-accent">
      <h3>Генерация будущих состояний</h3>
      <p>Модель способна генерировать реалистичные прогнозы развития сенсорного потока (изображений) при условии применения заданной последовательности действий, функционируя как ментальный симулятор.</p>
    </div>
  </div>
</div>

---

## Предиктивное планирование WAM <span class="badge badge-time">80–82 мин</span>

<div class="diagram-box">
  <img src="../../assets/images/lecture-07/world_action_model_rollout.svg" alt="Схема латентного роллаута и предиктивного планирования с использованием модели мира" />
</div>

---

## 11. Планирование в латентном пространстве <span class="badge badge-time">82–85 мин</span>

<div class="grid-2">
  <div class="col">
    <div class="card card-accent">
      <h3>Latent Imagination</h3>
      <p>Вместо выполнения действий в физической среде, агент совершает «воображаемые» (latent rollouts) траектории внутри скрытого пространства WAM.</p>
      <p>Алгоритмы производных безградиентных методов (например, Model Predictive Path Integral, MPPI) могут оценивать тысячи гипотетических планов.</p>
    </div>
  </div>
  <div class="col">
    <p><strong>Фундаментальные преимущества:</strong></p>
    <ul>
      <li>Высокая вычислительная эффективность (отсутствие рендеринга пикселей).</li>
      <li>Нулевой риск повреждения оборудования при исследовании граничных режимов.</li>
      <li>Возможность онлайн-коррекции политик без дополнительного сбора реальных данных.</li>
    </ul>
  </div>
</div>

---

## 12. Бюджет вычислений и Latency Gap <span class="badge badge-time">85–87 мин</span>

<div class="grid-2">
  <div class="col">
    <p>Интеграция тяжелых генеративных моделей в контур управления мобильного робота порождает критическую проблему асинхронности (Latency Gap) между вычислительными уровнями.</p>
    <ul>
      <li><strong>Уровень сервоприводов</strong> (ПИД-регуляторы): $\sim 1000$ Гц.</li>
      <li><strong>Проприоцептивные контроллеры</strong>: $100$ – $500$ Гц.</li>
    </ul>
  </div>
  <div class="col">
    <div class="card card-alert">
      <h3>Низкочастотные ИИ-модели</h3>
      <ul>
        <li><strong>Диффузионные политики (ACT/DDPM)</strong>: генерация чанков с частотой $20$ – $50$ Гц.</li>
        <li><strong>VLA-модели (LLM backbone)</strong>: инференс тяжелых сетей ($>7$B параметров) ограничивается частотой $3$ – $5$ Гц.</li>
      </ul>
      <p>Необходима строгая иерархия буферизации интерполяций!</p>
    </div>
  </div>
</div>

---

## Иерархия вычислительных контуров <span class="badge badge-time">87–88 мин</span>

<div class="diagram-box">
  <img src="../../assets/images/lecture-07/edge_compute_multirate.svg" alt="Асинхронная иерархия частотных контуров инференса VLA и низкоуровневого управления" />
</div>

---

## 13. Аппаратные платформы бортового инференса <span class="badge badge-time">88–89 мин</span>

<div class="grid-2">
  <div class="col">
    <div class="card card-accent">
      <h3>Edge AI Hardware</h3>
      <p>Развертывание VLA требует высокой энергоэффективности на ватт (TOPS/W). Текущий индустриальный стандарт представлен SoC-архитектурами:</p>
      <ul>
        <li>NVIDIA Jetson AGX Orin (до 275 TOPS).</li>
        <li>Анонсированная платформа NVIDIA Jetson Thor на базе архитектуры Blackwell для робототехники.</li>
      </ul>
    </div>
  </div>
  <div class="col">
    <div class="card card-success">
      <h3>Программная оптимизация</h3>
      <p>Для достижения целевых частот инференса применяются методы сжатия графов вычислений:</p>
      <ul>
        <li>Квантование весов: FP8, INT4 (AWQ, GPTQ).</li>
        <li>Фреймворки компиляции: TensorRT-LLM, vLLM.</li>
        <li>Ускорение внимания: FlashAttention.</li>
      </ul>
    </div>
  </div>
</div>

---

## Резюме лекции <span class="badge badge-time">89–90 мин</span>

<div class="card card-accent">
  <h3>Эволюция систем управления</h3>
  <ul>
    <li>Произошел фундаментальный сдвиг от аналитической обратной кинематики и классического RL к применению мультимодальных генеративных моделей для сквозного (end-to-end) управления в открытых средах.</li>
    <li>Клонирование поведения масштабировалось через прогнозирование чанков (ACT) и диффузионные процессы, решая проблему мультимодальности сред.</li>
    <li>Интеграция больших языковых моделей с непрерывным планированием (VLA) и симуляция реальности в скрытом пространстве (WAM) определяют современный горизонт исследований в области Embodied AI.</li>
  </ul>
</div>

---

## Рекомендуемая академическая литература

<div class="grid-2">
  <div class="col">
    <ul>
      <li><strong>Chi et al.</strong> (2023). <em>Diffusion Policy: Visuomotor Policy Learning via Action Diffusion</em>.</li>
      <li><strong>Zhao et al.</strong> (2023). <em>Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ACT)</em>.</li>
      <li><strong>Brohan et al.</strong> (2023). <em>RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control</em>.</li>
    </ul>
  </div>
  <div class="col">
    <ul>
      <li><strong>Kim et al.</strong> (2024). <em>OpenVLA: An Open-Source Vision-Language-Action Model</em>.</li>
      <li><strong>Black et al.</strong> (2024). <em>$\pi_0$: A Vision-Language-Action Flow Model for General Robot Control</em>. (Physical Intelligence).</li>
    </ul>
  </div>
</div>
