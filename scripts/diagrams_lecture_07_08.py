#!/usr/bin/env python3
"""
diagrams_lecture_07_08.py

Generates mathematically and architecturally rigorous SVG diagrams for:
- Lecture 07: RL, Diffusion Policy, VLA, and World Action Models (WAM)
- Lecture 08: Humanoid Robotics SOTA (Helix, Full-Body WBC RL, China Supply Chain, Bottlenecks)
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'assets', 'images')

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def write_svg(filepath, content):
    ensure_dir(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Generated: {filepath}")

# =========================================================================
# LECTURE 07 DIAGRAMS
# =========================================================================

def generate_teacher_student_sim2real():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-07', 'teacher_student_sim2real.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 430" width="880" height="430">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="url(#bgGrad)" rx="12"/>
  <rect width="100%" height="100%" fill="none" stroke="#e2e8f0" stroke-width="1.5" rx="12"/>

  <!-- Title Badge -->
  <g transform="translate(24, 20)">
    <rect width="330" height="28" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#1e40af">
      ⚡ ПАРАДИГМА TEACHER-STUDENT В SIM-TO-REAL
    </text>
    <text x="350" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Дистилляция привилегированного опыта ➔ бортовая политика
    </text>
  </g>

  <!-- Column 1: Teacher in GPU Sim -->
  <g transform="translate(24, 65)" filter="url(#shadow)">
    <rect width="255" height="340" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
    <rect width="255" height="32" rx="8" fill="#2563eb"/>
    <text x="12" y="21" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">
      1. Учитель в GPU-симуляторе
    </text>

    <g transform="translate(14, 46)" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">
      <rect x="0" y="0" width="227" height="24" rx="4" fill="#eff6ff" stroke="#dbeafe"/>
      <text x="8" y="16" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#1d4ed8">
        Isaac Sim / PhysX 5 / Newton
      </text>

      <text x="0" y="44" font-weight="700" fill="#0f172a">Параллелизм на GPU:</text>
      <text x="6" y="60">• 10 000 – 50 000 сред сразу</text>
      <text x="6" y="76">• 10 лет опыта за 20 минут</text>

      <text x="0" y="104" font-weight="700" fill="#1e40af">Привилегированные данные s_t:</text>
      <text x="6" y="120">✔ Истинный профиль высот рельефа</text>
      <text x="6" y="136">✔ Точные силы реакций опор F_contact</text>
      <text x="6" y="152">✔ Трение поверхности μ и масса m</text>
      <text x="6" y="168">✔ Вектор внешних возмущений F_ext</text>

      <rect x="0" y="185" width="227" height="90" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="10" y="205" font-weight="700" fill="#2563eb">Политика Учителя π_teacher:</text>
      <text x="10" y="223" font-family="JetBrains Mono, monospace" font-size="9" fill="#0f172a">
        a_t ~ PPO(a_t | s_t^privileged)
      </text>
      <text x="10" y="243" font-size="9.5" fill="#64748b">Обучается идеальной походке,</text>
      <text x="10" y="259" font-size="9.5" fill="#64748b">зная ВСЁ о физике мира</text>
    </g>
  </g>

  <!-- Arrow 1 -> 2 -->
  <g transform="translate(285, 220)">
    <path d="M 0,0 L 26,0" stroke="#3b82f6" stroke-width="2.5" stroke-dasharray="4,3"/>
    <polygon points="26,0 18,-5 18,5" fill="#3b82f6"/>
    <text x="-6" y="-12" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#2563eb">Клон</text>
  </g>

  <!-- Column 2: Supervised Distillation & Domain Randomization -->
  <g transform="translate(315, 65)" filter="url(#shadow)">
    <rect width="265" height="340" rx="8" fill="#ffffff" stroke="#c084fc" stroke-width="1.5"/>
    <rect width="265" height="32" rx="8" fill="#9333ea"/>
    <text x="12" y="21" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">
      2. Дистилляция &amp; Randomization
    </text>

    <g transform="translate(14, 46)" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">
      <rect x="0" y="0" width="237" height="24" rx="4" fill="#faf5ff" stroke="#f3e8ff"/>
      <text x="8" y="16" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#7e22ce">
        Loss = ||π_student(o_t) - a_teacher||²
      </text>

      <text x="0" y="44" font-weight="700" fill="#0f172a">Сенсоры Ученика o_t (Бортовые):</text>
      <text x="6" y="60">✖ НЕТ карты высот и сил контакта!</text>
      <text x="6" y="76">✔ Энкодеры углов и скоростей q, q̇</text>
      <text x="6" y="92">✔ Линейное ускорение и гироскоп IMU</text>
      <text x="6" y="108">✔ История за 50 шагов (Transformer/TCN)</text>

      <rect x="0" y="125" width="237" height="150" rx="6" fill="#fdf4ff" stroke="#e9d5ff"/>
      <text x="8" y="145" font-weight="700" fill="#9333ea">🎲 Domain Randomization:</text>
      <text x="12" y="165" font-size="9.5">• Массы звеньев: ± 30%</text>
      <text x="12" y="181" font-size="9.5">• Коэффициент трения: μ ∈ [0.2, 1.3]</text>
      <text x="12" y="197" font-size="9.5">• Задержки шины моторов: 5–25 мс</text>
      <text x="12" y="213" font-size="9.5">• Случайные толчки: F_push до 150 Н</text>
      <text x="12" y="229" font-size="9.5">• Шумы сенсоров: гауссов шум датчиков</text>
      <text x="8" y="255" font-weight="700" fill="#7e22ce">➔ Реальность становится частным случаем!</text>
    </g>
  </g>

  <!-- Arrow 2 -> 3 -->
  <g transform="translate(586, 220)">
    <path d="M 0,0 L 26,0" stroke="#059669" stroke-width="2.5"/>
    <polygon points="26,0 18,-5 18,5" fill="#059669"/>
    <text x="-4" y="-12" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#059669">Deploy</text>
  </g>

  <!-- Column 3: Physical Robot Deployment -->
  <g transform="translate(618, 65)" filter="url(#shadow)">
    <rect width="238" height="340" rx="8" fill="#ffffff" stroke="#86efac" stroke-width="1.5"/>
    <rect width="238" height="32" rx="8" fill="#059669"/>
    <text x="12" y="21" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">
      3. Реальный робот (Zero-Shot)
    </text>

    <g transform="translate(14, 46)" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">
      <rect x="0" y="0" width="210" height="24" rx="4" fill="#ecfdf5" stroke="#d1fae5"/>
      <text x="8" y="16" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#047857">
        Zero-Shot Sim-to-Real
      </text>

      <text x="0" y="44" font-weight="700" fill="#065f46">Бортовое исполнение:</text>
      <text x="6" y="60">• Частота контура: 50–100 Гц</text>
      <text x="6" y="76">• Нейросеть (ONNX / TensorRT)</text>
      <text x="6" y="92">• Время инференса: &lt; 2 мс</text>

      <text x="0" y="120" font-weight="700" fill="#0f172a">Эмерджентные свойства:</text>
      <text x="6" y="138">✔ Слепая ходьба по лестницам</text>
      <text x="6" y="154">✔ Бег по льду, грязи и гравию</text>
      <text x="6" y="170">✔ Мгновенная реакция на пинки</text>
      <text x="6" y="186">✔ Вставание после падения</text>

      <rect x="0" y="205" width="210" height="70" rx="6" fill="#f0fdf4" stroke="#bbf7d0"/>
      <text x="8" y="225" font-weight="700" fill="#15803d">Итог:</text>
      <text x="8" y="243" font-size="9.5" fill="#166534">Без единой строчки уравнений</text>
      <text x="8" y="259" font-size="9.5" fill="#166534">динамики перевернутого маятника!</text>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


def generate_diffusion_policy_multimodal():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-07', 'diffusion_policy_multimodal.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 400" width="880" height="400">
  <defs>
    <filter id="shadowDP" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title Badge -->
  <g transform="translate(24, 18)">
    <rect width="360" height="28" rx="6" fill="#fdf2f8" stroke="#fbcfe8"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#be185d">
      🌊 DIFFUSION POLICY &amp; МУЛЬТИМОДАЛЬНОСТЬ
    </text>
    <text x="380" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Почему среднеквадратичная ошибка (MSE) убивает манипуляцию
    </text>
  </g>

  <!-- Left Card: Failure of MSE -->
  <g transform="translate(24, 58)" filter="url(#shadowDP)">
    <rect width="400" height="320" rx="8" fill="#ffffff" stroke="#fca5a5" stroke-width="1.5"/>
    <rect width="400" height="30" rx="8" fill="#ef4444"/>
    <text x="12" y="20" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">
      ❌ Проблема: Обычная регрессия (MSE / L2 Loss)
    </text>

    <!-- Visual Box -->
    <g transform="translate(20, 45)">
      <rect width="360" height="150" rx="6" fill="#fef2f2" stroke="#fee2e2"/>
      
      <!-- Start robot -->
      <circle cx="40" cy="75" r="10" fill="#64748b"/>
      <text x="25" y="105" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#334155">Старт (s_0)</text>

      <!-- Obstacle -->
      <rect x="170" y="50" width="35" height="50" rx="4" fill="#dc2626" opacity="0.85"/>
      <text x="165" y="115" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#991b1b">Препятствие</text>

      <!-- Trajectory Left (50%) -->
      <path d="M 40,75 Q 120,20 280,35" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-dasharray="4,3"/>
      <text x="290" y="38" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#2563eb">Путь 1 (50% данных)</text>

      <!-- Trajectory Right (50%) -->
      <path d="M 40,75 Q 120,130 280,115" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-dasharray="4,3"/>
      <text x="290" y="120" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#2563eb">Путь 2 (50% данных)</text>

      <!-- Averaged Crash Path -->
      <path d="M 40,75 L 170,75" fill="none" stroke="#b91c1c" stroke-width="3.5"/>
      <polygon points="170,75 160,70 160,80" fill="#b91c1c"/>
      <text x="70" y="70" font-family="Inter, sans-serif" font-size="9.5" font-weight="700" fill="#b91c1c">
        Среднее (a_L + a_R)/2 ➔ Удар!
      </text>
    </g>

    <g transform="translate(20, 210)" font-family="Inter, sans-serif" font-size="10" fill="#334155">
      <text x="0" y="14" font-weight="700" fill="#991b1b">Математический коллапс регрессии:</text>
      <text x="6" y="32">• При обучении минимизируется E[||â - a||²].</text>
      <text x="6" y="50">• Оптимум MSE для мультимодального распределения —</text>
      <text x="6" y="68">  это среднее значение E[a], которое физически невозможно!</text>
      <text x="6" y="86">• Робот парализуется или врезается ровно в центр препятствия.</text>
    </g>
  </g>

  <!-- Right Card: Diffusion Policy -->
  <g transform="translate(450, 58)" filter="url(#shadowDP)">
    <rect width="406" height="320" rx="8" fill="#ffffff" stroke="#86efac" stroke-width="1.5"/>
    <rect width="406" height="30" rx="8" fill="#059669"/>
    <text x="12" y="20" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">
      ✔ Решение: Diffusion Policy &amp; Action Chunking (ACT)
    </text>

    <!-- Visual Box -->
    <g transform="translate(20, 45)">
      <rect width="366" height="150" rx="6" fill="#f0fdf4" stroke="#dcfce7"/>
      
      <!-- Noise Step K -->
      <g transform="translate(15, 20)">
        <rect width="85" height="110" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
        <text x="8" y="18" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#64748b">Шаг K (Шум)</text>
        <path d="M 10,60 Q 25,30 40,80 T 70,50" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2,2"/>
        <path d="M 10,75 Q 35,95 55,45 T 75,70" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2,2"/>
        <text x="12" y="98" font-family="JetBrains Mono, monospace" font-size="8" fill="#64748b">a^K ~ N(0, I)</text>
      </g>

      <path d="M 106,75 L 126,75" stroke="#10b981" stroke-width="2"/>
      <polygon points="126,75 118,71 118,79" fill="#10b981"/>

      <!-- Denoising Steps -->
      <g transform="translate(132, 20)">
        <rect width="90" height="110" rx="4" fill="#ffffff" stroke="#86efac"/>
        <text x="8" y="18" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#059669">Denoising Net</text>
        <path d="M 10,50 Q 40,30 80,40" fill="none" stroke="#3b82f6" stroke-width="1.8"/>
        <path d="M 10,70 Q 40,90 80,80" fill="none" stroke="#3b82f6" stroke-width="1.8"/>
        <text x="8" y="98" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#047857">ε_θ(a^k, k, obs)</text>
      </g>

      <path d="M 228,75 L 248,75" stroke="#10b981" stroke-width="2"/>
      <polygon points="248,75 240,71 240,79" fill="#10b981"/>

      <!-- Final Trajectory -->
      <g transform="translate(254, 20)">
        <rect width="96" height="110" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.5"/>
        <text x="8" y="18" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#047857">Итог a^0 (Чанк)</text>
        <path d="M 10,40 Q 45,25 85,35" fill="none" stroke="#059669" stroke-width="2.5"/>
        <circle cx="85" cy="35" r="3" fill="#059669"/>
        <text x="8" y="70" font-family="Inter, sans-serif" font-size="8" fill="#334155">Четкий выбор</text>
        <text x="8" y="84" font-family="Inter, sans-serif" font-size="8" font-weight="700" fill="#059669">ОДНОЙ ветви!</text>
        <text x="8" y="100" font-family="JetBrains Mono, monospace" font-size="7.5" fill="#15803d">H = 16 шагов</text>
      </g>
    </g>

    <g transform="translate(20, 210)" font-family="Inter, sans-serif" font-size="10" fill="#334155">
      <text x="0" y="14" font-weight="700" fill="#047857">Преимущества диффузии и ACT:</text>
      <text x="6" y="32">• Моделирует произвольные многомодальные распределения.</text>
      <text x="6" y="50">• Action Chunking: выдает сразу 16–32 шага вперед ➔</text>
      <text x="6" y="68">  гарантирует идеальную плавность без рывков.</text>
      <text x="6" y="86">• SOTA 2024: основа манипуляторов Figure 02, Tesla, π0.</text>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


def generate_vla_architecture_pipeline():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-07', 'vla_architecture_pipeline.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 410" width="880" height="410">
  <defs>
    <filter id="shadowVLA" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title Badge -->
  <g transform="translate(24, 16)">
    <rect width="360" height="28" rx="6" fill="#f0f9ff" stroke="#bae6fd"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#0369a1">
      🧠 АРХИТЕКТУРА VLA (VISION-LANGUAGE-ACTION)
    </text>
    <text x="380" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Преобразование мультимодального понимания в моторику робота
    </text>
  </g>

  <!-- Block 1: Multimodal Inputs -->
  <g transform="translate(24, 56)" filter="url(#shadowVLA)">
    <rect width="180" height="330" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.2"/>
    <rect width="180" height="28" rx="8" fill="#0284c7"/>
    <text x="10" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">1. Входы Сенсоров</text>

    <g transform="translate(12, 42)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
      <rect x="0" y="0" width="156" height="75" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="8" y="18" font-weight="700" fill="#0284c7">📷 RGB-Камеры:</text>
      <text x="8" y="34">• Вид головы (Third-person)</text>
      <text x="8" y="48">• Камеры запястий (Wrist)</text>
      <text x="8" y="64" font-family="JetBrains Mono, monospace" font-size="8" fill="#64748b">224×224 @ 20 FPS</text>

      <rect x="0" y="85" width="156" height="70" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="8" y="103" font-weight="700" fill="#059669">💬 Текстовая цель:</text>
      <text x="8" y="121">«Возьми кружку и</text>
      <text x="8" y="135"> поставь в посудомойку»</text>
      <text x="8" y="149" font-size="8" fill="#64748b">(Естественный язык)</text>

      <rect x="0" y="165" width="156" height="85" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="8" y="183" font-weight="700" fill="#d97706">🦾 Проприоцепция:</text>
      <text x="8" y="201">• Углы суставов q_t</text>
      <text x="8" y="215">• Поза схвата (EE pose)</text>
      <text x="8" y="229">• Состояние пальцев</text>
      <text x="8" y="243" font-family="JetBrains Mono, monospace" font-size="8" fill="#64748b">x, y, z, roll, pitch, yaw</text>
    </g>
  </g>

  <!-- Arrow 1 -> 2 -->
  <path d="M 208,210 L 228,210" stroke="#94a3b8" stroke-width="2"/>
  <polygon points="228,210 220,206 220,214" fill="#94a3b8"/>

  <!-- Block 2: Tokenizers & Encoders -->
  <g transform="translate(232, 56)" filter="url(#shadowVLA)">
    <rect width="180" height="330" rx="8" fill="#ffffff" stroke="#c084fc" stroke-width="1.2"/>
    <rect width="180" height="28" rx="8" fill="#7c3aed"/>
    <text x="10" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">2. Энкодеры Токенов</text>

    <g transform="translate(12, 42)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
      <rect x="0" y="0" width="156" height="80" rx="5" fill="#faf5ff" stroke="#e9d5ff"/>
      <text x="8" y="18" font-weight="700" fill="#7c3aed">Vision Transformer:</text>
      <text x="8" y="34">• SigLIP / DINOv2</text>
      <text x="8" y="50">• Патчи 14×14 ➔</text>
      <text x="8" y="68" font-family="JetBrains Mono, monospace" font-size="8.5" fill="#6b21a8">256 визуальных токенов</text>

      <rect x="0" y="90" width="156" height="65" rx="5" fill="#faf5ff" stroke="#e9d5ff"/>
      <text x="8" y="108" font-weight="700" fill="#7c3aed">Text Tokenizer:</text>
      <text x="8" y="126">• BPE токенизация</text>
      <text x="8" y="144" font-family="JetBrains Mono, monospace" font-size="8.5" fill="#6b21a8">T_lang токенов</text>

      <rect x="0" y="165" width="156" height="85" rx="5" fill="#faf5ff" stroke="#e9d5ff"/>
      <text x="8" y="183" font-weight="700" fill="#7c3aed">Action Projector:</text>
      <text x="8" y="201">• MLP проекция позы</text>
      <text x="8" y="217">• Совмещение размерностей</text>
      <text x="8" y="235" font-family="JetBrains Mono, monospace" font-size="8.5" fill="#6b21a8">d_model = 4096</text>
    </g>
  </g>

  <!-- Arrow 2 -> 3 -->
  <path d="M 416,210 L 436,210" stroke="#94a3b8" stroke-width="2"/>
  <polygon points="436,210 428,206 428,214" fill="#94a3b8"/>

  <!-- Block 3: Foundation Backbone -->
  <g transform="translate(440, 56)" filter="url(#shadowVLA)">
    <rect width="190" height="330" rx="8" fill="#ffffff" stroke="#818cf8" stroke-width="1.2"/>
    <rect width="190" height="28" rx="8" fill="#4f46e5"/>
    <text x="10" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">3. VLM Backbone</text>

    <g transform="translate(12, 42)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
      <rect x="0" y="0" width="166" height="110" rx="5" fill="#eef2ff" stroke="#c7d2fe"/>
      <text x="8" y="18" font-weight="700" fill="#4338ca">Мультимодальный LLM:</text>
      <text x="8" y="36">• OpenVLA (Llama-2 7B)</text>
      <text x="8" y="52">• Octo / RT-2 / π0</text>
      <text x="8" y="68">• Self-Attention слои</text>
      <text x="8" y="86" font-size="8.5" fill="#4338ca">Семантическое связывание:</text>
      <text x="8" y="100" font-size="8" fill="#64748b">«где чашка» ➔ «как взять»</text>

      <rect x="0" y="120" width="166" height="130" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="8" y="138" font-weight="700" fill="#0f172a">Параметры обучения:</text>
      <text x="8" y="156">• Pre-training: интернет-текст</text>
      <text x="8" y="172">  и миллионы картинок</text>
      <text x="8" y="190">• Co-fine-tuning: Open X-</text>
      <text x="8" y="206">  Embodiment (1M+ робото-</text>
      <text x="8" y="222">  траекторий из 22 институтов)</text>
    </g>
  </g>

  <!-- Arrow 3 -> 4 -->
  <path d="M 634,210 L 654,210" stroke="#94a3b8" stroke-width="2"/>
  <polygon points="654,210 646,206 646,214" fill="#94a3b8"/>

  <!-- Block 4: Action Heads -->
  <g transform="translate(658, 56)" filter="url(#shadowVLA)">
    <rect width="198" height="330" rx="8" fill="#ffffff" stroke="#86efac" stroke-width="1.2"/>
    <rect width="198" height="28" rx="8" fill="#059669"/>
    <text x="10" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">4. Генерация Действий</text>

    <g transform="translate(12, 42)" font-family="Inter, sans-serif" font-size="9" fill="#334155">
      <rect x="0" y="0" width="174" height="115" rx="5" fill="#f0fdf4" stroke="#bbf7d0"/>
      <text x="8" y="16" font-weight="700" fill="#047857">Вариант А: Токенизация (RT-2)</text>
      <text x="8" y="32">• Дискретизация на 256 бинов</text>
      <text x="8" y="48">• Действие = обычные токены LLM</text>
      <text x="8" y="64" font-family="JetBrains Mono, monospace" font-size="8" fill="#15803d">&lt;128&gt;&lt;45&gt;&lt;210&gt;...</text>
      <text x="8" y="80" font-size="8" fill="#b91c1c">✖ Дрожание и медлительность</text>
      <text x="8" y="96" font-size="8" fill="#b91c1c">✖ Авторегрессия (по 1 числу)</text>

      <rect x="0" y="125" width="174" height="125" rx="5" fill="#ecfdf5" stroke="#6ee7b7"/>
      <text x="8" y="141" font-weight="700" fill="#065f46">Вариант Б: Flow Matching (π0)</text>
      <text x="8" y="157">• Непрерывная диффузия</text>
      <text x="8" y="173">• Action Chunking (H=16–50)</text>
      <text x="8" y="189" font-family="JetBrains Mono, monospace" font-size="8" fill="#047857">Δx, Δy, Δz, Δq, Gripper</text>
      <text x="8" y="207" font-weight="700" fill="#047857">✔ Плавность траектории</text>
      <text x="8" y="223" font-weight="700" fill="#047857">✔ Инференс на GPU за 30 мс</text>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


def generate_world_action_model_rollout():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-07', 'world_action_model_rollout.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 390" width="880" height="390">
  <defs>
    <filter id="shadowWAM" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title Badge -->
  <g transform="translate(24, 18)">
    <rect width="370" height="28" rx="6" fill="#fef3c7" stroke="#fde68a"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#b45309">
      🌐 WORLD ACTION MODELS (WAM) &amp; МЫСЛЕННЫЙ РОЛЛАУТ
    </text>
    <text x="395" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Генеративные модели физики для безопасного планирования
    </text>
  </g>

  <!-- Left: Current state & action candidates -->
  <g transform="translate(24, 60)" filter="url(#shadowWAM)">
    <rect width="230" height="305" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <rect width="230" height="28" rx="8" fill="#475569"/>
    <text x="12" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
      1. Текущий Кадр &amp; Кандидаты
    </text>

    <g transform="translate(14, 40)" font-family="Inter, sans-serif" font-size="10" fill="#334155">
      <rect x="0" y="0" width="202" height="70" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="8" y="18" font-weight="700" fill="#0f172a">Состояние s_t:</text>
      <text x="8" y="36">• Визуальный кадр камеры</text>
      <text x="8" y="52">• Положение руки и объектов</text>

      <text x="0" y="95" font-weight="700" fill="#2563eb">Сэмплер действий a_{t:t+H}:</text>
      
      <rect x="0" y="105" width="202" height="42" rx="4" fill="#eff6ff" stroke="#bfdbfe"/>
      <text x="8" y="122" font-weight="700" fill="#1d4ed8">Кандидат 1 (Действие A):</text>
      <text x="8" y="138" font-size="9" fill="#1e40af">Резкий захват чашки сбоку</text>

      <rect x="0" y="155" width="202" height="42" rx="4" fill="#f0fdf4" stroke="#bbf7d0"/>
      <text x="8" y="172" font-weight="700" fill="#15803d">Кандидат 2 (Действие B):</text>
      <text x="8" y="188" font-size="9" fill="#166534">Плавный подъем за ручку</text>

      <text x="0" y="222" font-size="9" fill="#64748b">
        Как выбрать лучшее без риска уронить и разбить кружку?
      </text>
    </g>
  </g>

  <!-- Arrow 1 -> 2 -->
  <path d="M 258,210 L 284,210" stroke="#94a3b8" stroke-width="2"/>
  <polygon points="284,210 276,206 276,214" fill="#94a3b8"/>

  <!-- Center: WAM Latent Predictor -->
  <g transform="translate(288, 60)" filter="url(#shadowWAM)">
    <rect width="280" height="305" rx="8" fill="#ffffff" stroke="#f59e0b" stroke-width="1.5"/>
    <rect width="280" height="28" rx="8" fill="#d97706"/>
    <text x="12" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
      2. WAM (Модель Мира с Действием)
    </text>

    <g transform="translate(14, 40)" font-family="Inter, sans-serif" font-size="10" fill="#334155">
      <rect x="0" y="0" width="252" height="45" rx="4" fill="#fffbeb" stroke="#fef3c7"/>
      <text x="8" y="18" font-weight="700" fill="#b45309">Формула прогноза:</text>
      <text x="8" y="34" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#92400e">
        ŝ_{t+1} ~ P(s_{t+1} | s_t, a_t)
      </text>

      <text x="0" y="65" font-weight="700" fill="#0f172a">Технологический базис WAM:</text>
      <text x="6" y="82">• Genie (Google) / UniSim / DayDreamer</text>
      <text x="6" y="98">• Пространственно-временные диффузионные</text>
      <text x="6" y="114">  видео-модели (Video Diffusion Transformer)</text>
      <text x="6" y="130">• Латентное предсказание динамики</text>

      <rect x="0" y="145" width="252" height="95" rx="5" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="8" y="165" font-weight="700" fill="#2563eb">Мысленная симуляция (Mental Rollout):</text>
      <text x="8" y="183" font-size="9.5">Модель «воображает» видео будущего</text>
      <text x="8" y="199" font-size="9.5">на 3–5 секунд вперед со всеми законами</text>
      <text x="8" y="215" font-size="9.5">гравитации, скольжения и трения.</text>
    </g>
  </g>

  <!-- Arrow 2 -> 3 -->
  <path d="M 572,210 L 598,210" stroke="#94a3b8" stroke-width="2"/>
  <polygon points="598,210 590,206 590,214" fill="#94a3b8"/>

  <!-- Right: Evaluation & Action Selection -->
  <g transform="translate(602, 60)" filter="url(#shadowWAM)">
    <rect width="254" height="305" rx="8" fill="#ffffff" stroke="#86efac" stroke-width="1.2"/>
    <rect width="254" height="28" rx="8" fill="#059669"/>
    <text x="12" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
      3. Оценка Риска и Выбор
    </text>

    <g transform="translate(14, 40)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
      <!-- Candidate 1 Eval -->
      <rect x="0" y="0" width="226" height="85" rx="5" fill="#fef2f2" stroke="#fecaca"/>
      <text x="8" y="18" font-weight="700" fill="#dc2626">Результат прогноза A:</text>
      <text x="8" y="34">• В воображении чашка задета</text>
      <text x="8" y="48">• Вода расплескалась, скол</text>
      <text x="8" y="66" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#b91c1c">
        Оценка: ОШИБКА (Cost = ∞)
      </text>

      <!-- Candidate 2 Eval -->
      <rect x="0" y="95" width="226" height="85" rx="5" fill="#f0fdf4" stroke="#bbf7d0"/>
      <text x="8" y="113" font-weight="700" fill="#15803d">Результат прогноза B:</text>
      <text x="8" y="129">• Уверенный захват ручки</text>
      <text x="8" y="143">• Равновесие сохранено</text>
      <text x="8" y="161" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#15803d">
        Оценка: УСПЕХ (Cost = MIN)
      </text>

      <rect x="0" y="190" width="226" height="48" rx="4" fill="#ecfdf5" stroke="#a7f3d0"/>
      <text x="8" y="210" font-weight="700" fill="#047857">Команда на моторы:</text>
      <text x="8" y="226" font-size="9" fill="#065f46">Исполняем ТОЛЬКО вариант B!</text>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


def generate_edge_compute_multirate():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-07', 'edge_compute_multirate.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 390" width="880" height="390">
  <defs>
    <filter id="shadowMC" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title Badge -->
  <g transform="translate(24, 18)">
    <rect width="360" height="28" rx="6" fill="#f5f3ff" stroke="#ddd6fe"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#6d28d9">
      ⏱️ МНОГОТАКТОВАЯ ИЕРАРХИЯ &amp; ВЫЧИСЛЕНИЯ
    </text>
    <text x="385" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Как тяжелая 7B модель уживается с микросекундным балансом
    </text>
  </g>

  <!-- 4 Level Stack Rows -->
  <g transform="translate(24, 58)" filter="url(#shadowMC)">
    <!-- Level 1: Cloud Reasoner -->
    <g transform="translate(0, 0)">
      <rect width="832" height="60" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
      <rect width="140" height="60" rx="6" fill="#475569"/>
      <text x="16" y="26" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Уровень 1: Cloud</text>
      <text x="16" y="44" font-family="JetBrains Mono, monospace" font-size="9" fill="#cbd5e1">0.1 – 0.5 Гц</text>

      <text x="160" y="24" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#0f172a">
        Глобальное планирование миссии (GPT-4o / Claude 3.5 / Gemini)
      </text>
      <text x="160" y="42" font-family="Inter, sans-serif" font-size="9.5" fill="#64748b">
        Декомпозиция задачи: «Прибери со стола» ➔ «1. Найти кружку; 2. Перенести в раковину; 3. Протереть стол»
      </text>

      <rect x="680" y="14" width="135" height="32" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
      <text x="692" y="34" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#475569">
        Latency: ~2000 мс
      </text>
    </g>

    <!-- Level 2: VLA / WAM Onboard -->
    <g transform="translate(0, 72)">
      <rect width="832" height="68" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.2"/>
      <rect width="140" height="68" rx="6" fill="#2563eb"/>
      <text x="16" y="30" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Уровень 2: VLA</text>
      <text x="16" y="48" font-family="JetBrains Mono, monospace" font-size="9" fill="#bfdbfe">2 – 10 Гц</text>

      <text x="160" y="26" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#1e40af">
        Бортовая мультимодальная политика (OpenVLA / π0 / Octo / Helix)
      </text>
      <text x="160" y="44" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        Обработка RGB-D камер, генерация траекторий рабочих органов (End-Effector waypoints) и чанков действий
      </text>
      <text x="160" y="58" font-family="Inter, sans-serif" font-size="8.5" fill="#2563eb">
        Железо: NVIDIA Jetson AGX Orin / Thor (FP8 / INT8 квантизация, 40–60 Вт)
      </text>

      <rect x="680" y="18" width="135" height="32" rx="4" fill="#dbeafe" stroke="#93c5fd"/>
      <text x="692" y="38" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#1d4ed8">
        Latency: 100–300 мс
      </text>
    </g>

    <!-- Level 3: Full-body WBC RL Policy -->
    <g transform="translate(0, 152)">
      <rect width="832" height="68" rx="6" fill="#fdf4ff" stroke="#e9d5ff" stroke-width="1.2"/>
      <rect width="140" height="68" rx="6" fill="#9333ea"/>
      <text x="16" y="30" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Уровень 3: WBC RL</text>
      <text x="16" y="48" font-family="JetBrains Mono, monospace" font-size="9" fill="#f3e8ff">50 – 200 Гц</text>

      <text x="160" y="26" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#7e22ce">
        Полнотельная политика баланса и координации (Isaac Sim: PhysX / Newton)
      </text>
      <text x="160" y="44" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        Координирует все 20–30+ степеней свободы: подстраивает наклон таза, стоп и торса под движение рук
      </text>
      <text x="160" y="58" font-family="Inter, sans-serif" font-size="8.5" fill="#9333ea">
        Компактная MLP / Transformer на TensorRT (чистый C++ инференс без оверхеда Python)
      </text>

      <rect x="680" y="18" width="135" height="32" rx="4" fill="#f3e8ff" stroke="#d8b4fe"/>
      <text x="692" y="38" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#7e22ce">
        Latency: 5 – 10 мс
      </text>
    </g>

    <!-- Level 4: Motor Joint Controllers -->
    <g transform="translate(0, 232)">
      <rect width="832" height="60" rx="6" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1.2"/>
      <rect width="140" height="60" rx="6" fill="#059669"/>
      <text x="16" y="26" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Уровень 4: Моторы</text>
      <text x="16" y="44" font-family="JetBrains Mono, monospace" font-size="9" fill="#a7f3d0">1000 Гц (1 кГц)</text>

      <text x="160" y="24" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#065f46">
        Низкоуровневый импеданс и FOC-драйверы (Field-Oriented Control)
      </text>
      <text x="160" y="42" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        Шина EtherCAT / CAN-FD: прямое управление токами фаз BLDC моторов, отслеживание крутящего момента
      </text>

      <rect x="680" y="14" width="135" height="32" rx="4" fill="#d1fae5" stroke="#6ee7b7"/>
      <text x="692" y="34" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#047857">
        Latency: &lt; 1 мс
      </text>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


# =========================================================================
# LECTURE 08 DIAGRAMS
# =========================================================================

def generate_helix_fullbody_architecture():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-08', 'helix_fullbody_architecture.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 430" width="880" height="430">
  <defs>
    <filter id="shadowHelix" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title Badge -->
  <g transform="translate(24, 18)">
    <rect width="410" height="28" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#1e40af">
      🤖 SOTA АРХИТЕКТУРА ГУМАНОИДА (HELIX / FIGURE)
    </text>
    <text x="435" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Двухуровневый симбиоз VLA-планировщика и Full-Body WBC RL
    </text>
  </g>

  <!-- High Level Tier Box -->
  <g transform="translate(24, 60)" filter="url(#shadowHelix)">
    <rect width="832" height="135" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
    <rect width="832" height="28" rx="8" fill="#2563eb"/>
    <text x="14" y="19" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">
      ВЕРХНИЙ УРОВЕНЬ: Медленная VLA-политика (2–10 Гц) — Helix / OpenAI / Vision-Language-Action
    </text>

    <g transform="translate(16, 40)" font-family="Inter, sans-serif" font-size="10" fill="#334155">
      <!-- Input sensory block -->
      <rect x="0" y="0" width="220" height="75" rx="5" fill="#f8fafc" stroke="#cbd5e1"/>
      <text x="10" y="18" font-weight="700" fill="#1e40af">Входы сенсорного восприятия:</text>
      <text x="10" y="34">• 6 RGB-D камер со всего корпуса</text>
      <text x="10" y="48">• Микрофон (речь человека)</text>
      <text x="10" y="62">• Семантическая карта окружения</text>

      <!-- Reasoning core -->
      <rect x="235" y="0" width="310" height="75" rx="5" fill="#eff6ff" stroke="#bfdbfe"/>
      <text x="10" y="18" font-weight="700" fill="#1d4ed8">Ядро рассуждений и семантики:</text>
      <text x="10" y="34">• VLM / Helix: распознавание деталей и инструментов</text>
      <text x="10" y="48">• Голосовой диалог и синтез намерений в реальном времени</text>
      <text x="10" y="62">• Субмиллиметровая визуальная коррекция позы кистей</text>

      <!-- Output target -->
      <rect x="560" y="0" width="240" height="75" rx="5" fill="#f0fdf4" stroke="#86efac"/>
      <text x="10" y="18" font-weight="700" fill="#047857">Выход для всего тела:</text>
      <text x="10" y="34">✔ Траектории кистей (x_ee, R_ee)</text>
      <text x="10" y="48">✔ Чанки действий пальцев рук</text>
      <text x="10" y="62">✔ Целевое направление шага v_cmd</text>
    </g>
  </g>

  <!-- Big Arrow Between Tiers -->
  <g transform="translate(425, 202)">
    <path d="M 0,0 L 0,22" stroke="#6366f1" stroke-width="3"/>
    <polygon points="0,22 -6,14 6,14" fill="#6366f1"/>
    <text x="14" y="14" font-family="Inter, sans-serif" font-size="9" font-weight="700" fill="#4f46e5">
      Цели рабочих органов (End-Effector goals) + Намерения
    </text>
  </g>

  <!-- Low Level Tier Box -->
  <g transform="translate(24, 230)" filter="url(#shadowHelix)">
    <rect width="832" height="175" rx="8" fill="#ffffff" stroke="#c084fc" stroke-width="1.5"/>
    <rect width="832" height="28" rx="8" fill="#9333ea"/>
    <text x="14" y="19" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">
      НИЖНИЙ УРОВЕНЬ: Быстрая Full-Body WBC RL-политика (50–200 Гц) — Isaac Sim (PhysX 5 / Newton)
    </text>

    <g transform="translate(16, 40)" font-family="Inter, sans-serif" font-size="10" fill="#334155">
      <!-- Architecture details -->
      <rect x="0" y="0" width="260" height="115" rx="5" fill="#faf5ff" stroke="#e9d5ff"/>
      <text x="10" y="18" font-weight="700" fill="#7e22ce">Обучение в Isaac Sim:</text>
      <text x="10" y="36">• Физика PhysX 5 и Newton / Warp</text>
      <text x="10" y="52">• 30 000 роботов параллельно на GPU</text>
      <text x="10" y="68">• Teacher-Student дистилляция</text>
      <text x="10" y="84">• Domain Randomization масс и трения</text>
      <text x="10" y="100" font-family="JetBrains Mono, monospace" font-size="8.5" fill="#6b21a8">Latency: 5 мс (TensorRT)</text>

      <!-- Why RL won over classical QP WBC -->
      <rect x="275" y="0" width="280" height="115" rx="5" fill="#fdf4ff" stroke="#d8b4fe"/>
      <text x="10" y="18" font-weight="700" fill="#9333ea">Почему Full-Body RL победил QP WBC?</text>
      <text x="10" y="34">✖ Классический QP WBC требует точной</text>
      <text x="10" y="48">  модели твердого тела и ломается при ударах</text>
      <text x="10" y="64">✔ RL учит целостной биомеханике:</text>
      <text x="16" y="80">тянешься рукой вперед ➔ корпус</text>
      <text x="16" y="94">автоматически подается назад для баланса!</text>

      <!-- Physical Actuators -->
      <rect x="570" y="0" width="230" height="115" rx="5" fill="#ecfdf5" stroke="#a7f3d0"/>
      <text x="10" y="18" font-weight="700" fill="#047857">Исполнение моторами (1 кГц):</text>
      <text x="10" y="36">• 28–44 шарнира тела</text>
      <text x="10" y="52">• Импеданс моторов: τ = K_p(q* - q) - K_d q̇</text>
      <text x="10" y="68">• Прямое управление крутящим моментом</text>
      <text x="10" y="84">• Волновые и планетарные редукторы</text>
      <text x="10" y="100" font-weight="700" fill="#047857">✔ Абсолютная устойчивость</text>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


def generate_humanoid_landscape_matrix():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-08', 'humanoid_landscape_matrix.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 430" width="880" height="430">
  <defs>
    <filter id="shadowMatrix" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title Badge -->
  <g transform="translate(24, 16)">
    <rect width="390" height="28" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#0f172a">
      🏆 МИРОВОЙ ЛАНДШАФТ ГУМАНОИДОВ (2024–2026)
    </text>
    <text x="415" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Сравнение ключевых технологических стеков и подходов
    </text>
  </g>

  <!-- 4 Columns / Cards -->
  <!-- 1. Tesla Optimus Gen 2 -->
  <g transform="translate(24, 56)" filter="url(#shadowMatrix)">
    <rect width="195" height="350" rx="8" fill="#ffffff" stroke="#f87171" stroke-width="1.5"/>
    <rect width="195" height="30" rx="8" fill="#dc2626"/>
    <text x="10" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Tesla Optimus Gen 2</text>

    <g transform="translate(10, 42)" font-family="Inter, sans-serif" font-size="9" fill="#334155">
      <text x="0" y="12" font-weight="700" fill="#b91c1c">Приводы &amp; Механика:</text>
      <text x="4" y="26">• Собственные приводы Tesla</text>
      <text x="4" y="38">• Линейные винтовые (ноги)</text>
      <text x="4" y="50">• Вращательные шарниры</text>
      <text x="4" y="62">• Кисти: 11 DoF ➔ 22 DoF</text>
      <text x="4" y="74">• Вес: 57 кг (-10 кг в Gen 2)</text>

      <text x="0" y="96" font-weight="700" fill="#b91c1c">Стек Управления:</text>
      <text x="4" y="110">• Сквозные нейросети (FSD стек)</text>
      <text x="4" y="122">• Обучение на человеческом видео</text>
      <text x="4" y="134">• Бортовой чип Tesla FSD HW4</text>
      <text x="4" y="146">• Тактильные сенсоры в пальцах</text>

      <rect x="0" y="165" width="175" height="70" rx="4" fill="#fef2f2" stroke="#fee2e2"/>
      <text x="6" y="180" font-weight="700" fill="#991b1b">Реальные задачи:</text>
      <text x="6" y="196">Сортировка ячеек 4680</text>
      <text x="6" y="210">на гигафабрике в Техасе</text>
      <text x="6" y="224" font-weight="700" fill="#b91c1c">Цель: тираж &gt; миллиона</text>
    </g>
  </g>

  <!-- 2. Figure 02 -->
  <g transform="translate(235, 56)" filter="url(#shadowMatrix)">
    <rect width="195" height="350" rx="8" fill="#ffffff" stroke="#60a5fa" stroke-width="1.5"/>
    <rect width="195" height="30" rx="8" fill="#2563eb"/>
    <text x="10" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Figure 02 (OpenAI)</text>

    <g transform="translate(10, 42)" font-family="Inter, sans-serif" font-size="9" fill="#334155">
      <text x="0" y="12" font-weight="700" fill="#1d4ed8">Приводы &amp; Механика:</text>
      <text x="4" y="26">• Полностью скрытая проводка</text>
      <text x="4" y="38">• Кастомные сочленения</text>
      <text x="4" y="50">• Кисти 16 DoF с тактильностью</text>
      <text x="4" y="62">• Батарея 2.25 кВт·ч (+50%)</text>
      <text x="4" y="74">• Вес: 70 кг, рост 170 см</text>

      <text x="0" y="96" font-weight="700" fill="#1d4ed8">Стек Управления:</text>
      <text x="4" y="110">• 3x GPU на борту робота</text>
      <text x="4" y="122">• Модель Helix (VLA + диалог)</text>
      <text x="4" y="134">• OpenAI речевой движок</text>
      <text x="4" y="146">• 6 встроенных RGB камер</text>

      <rect x="0" y="165" width="175" height="70" rx="4" fill="#eff6ff" stroke="#dbeafe"/>
      <text x="6" y="180" font-weight="700" fill="#1e40af">Реальные задачи:</text>
      <text x="6" y="196">Установка листового металла</text>
      <text x="6" y="210">на заводе BMW (Спартанберг)</text>
      <text x="6" y="224" font-weight="700" fill="#1d4ed8">Точность: субмиллиметровая</text>
    </g>
  </g>

  <!-- 3. Boston Dynamics Electric Atlas -->
  <g transform="translate(446, 56)" filter="url(#shadowMatrix)">
    <rect width="195" height="350" rx="8" fill="#ffffff" stroke="#fbbf24" stroke-width="1.5"/>
    <rect width="195" height="30" rx="8" fill="#d97706"/>
    <text x="10" y="20" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#ffffff">Electric Atlas (BD)</text>

    <g transform="translate(10, 42)" font-family="Inter, sans-serif" font-size="9" fill="#334155">
      <text x="0" y="12" font-weight="700" fill="#b45309">Приводы &amp; Механика:</text>
      <text x="4" y="26">• Полный отказ от гидравлики</text>
      <text x="4" y="38">• Сверхмощные электроприводы</text>
      <text x="4" y="50">• Вращение суставов на 360°!</text>
      <text x="4" y="62">• Нечеловеческая кинематика</text>
      <text x="4" y="74">• Компактный дизайн торса</text>

      <text x="0" y="96" font-weight="700" fill="#b45309">Стек Управления:</text>
      <text x="4" y="110">• Гибрид RL-политик и</text>
      <text x="4" y="122">  модельного планирования</text>
      <text x="4" y="134">• Круговое зрение 360°</text>
      <text x="4" y="146">• Экстремальная динамика</text>

      <rect x="0" y="165" width="175" height="70" rx="4" fill="#fffbeb" stroke="#fef3c7"/>
      <text x="6" y="180" font-weight="700" fill="#92400e">Реальные задачи:</text>
      <text x="6" y="196">Тяжелые манипуляции деталями</text>
      <text x="6" y="210">на заводах Hyundai Motor</text>
      <text x="6" y="224" font-weight="700" fill="#b45309">Фокус: индустриальная мощь</text>
    </g>
  </g>

  <!-- 4. Unitree G1 (Китайский прорыв) -->
  <g transform="translate(657, 56)" filter="url(#shadowMatrix)">
    <rect width="195" height="350" rx="8" fill="#ffffff" stroke="#4ade80" stroke-width="1.5"/>
    <rect width="195" height="30" rx="8" fill="#16a34a"/>
    <text x="10" y="20" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Unitree G1 ($16 000)</text>

    <g transform="translate(10, 42)" font-family="Inter, sans-serif" font-size="9" fill="#334155">
      <text x="0" y="12" font-weight="700" fill="#15803d">Приводы &amp; Механика:</text>
      <text x="4" y="26">• 23–43 степеней свободы</text>
      <text x="4" y="38">• Пиковый момент: 120 Н·м</text>
      <text x="4" y="50">• Складной корпус (рюкзак)</text>
      <text x="4" y="62">• Вес: всего 35 кг!</text>
      <text x="4" y="74">• Цена: от $16 000 (ШОК рынка)</text>

      <text x="0" y="96" font-weight="700" fill="#15803d">Стек Управления:</text>
      <text x="4" y="110">• RL локомоция (Isaac Sim)</text>
      <text x="4" y="122">• Динамический паркур, прыжки</text>
      <text x="4" y="134">• Лидар Livox MID-360 + RealSense</text>
      <text x="4" y="146">• 8-ядерный CPU + GPU</text>

      <rect x="0" y="165" width="175" height="70" rx="4" fill="#f0fdf4" stroke="#dcfce7"/>
      <text x="6" y="180" font-weight="700" fill="#166534">Реальные задачи:</text>
      <text x="6" y="196">Массовые R&amp;D лаборатории,</text>
      <text x="6" y="210">патрулирование, образование</text>
      <text x="6" y="224" font-weight="700" fill="#15803d">Старт массовых поставок</text>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


def generate_china_supply_chain_cluster():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-08', 'china_supply_chain_cluster.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 400" width="880" height="400">
  <defs>
    <filter id="shadowChina" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title Badge -->
  <g transform="translate(24, 18)">
    <rect width="400" height="28" rx="6" fill="#fef2f2" stroke="#fecaca"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#b91c1c">
      🇨🇳 ФЕНОМЕН КИТАЯ: ЦЕПОЧКИ ПОСТАВОК И СКОРОСТЬ
    </text>
    <text x="430" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Почему китайские гуманоиды стоят $16k и обновляются за недели
    </text>
  </g>

  <!-- Left: Geographic Clusters Map/Box -->
  <g transform="translate(24, 58)" filter="url(#shadowChina)">
    <rect width="410" height="320" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <rect width="410" height="28" rx="8" fill="#334155"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
      Кластер Дельты реки Янцзы &amp; Гуандун (Радиус 150 км)
    </text>

    <g transform="translate(14, 38)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
      <rect x="0" y="0" width="380" height="58" rx="5" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="10" y="18" font-weight="700" fill="#0284c7">📍 Сучжоу (Suzhou) — Сердце редукторов:</text>
      <text x="10" y="34">• Заводы Leader Harmonious Drive (Leaderdrive)</text>
      <text x="10" y="48">• Мировой лидер по объему волновых редукторов (Harmonic)</text>

      <rect x="0" y="66" width="380" height="58" rx="5" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="10" y="84" font-weight="700" fill="#059669">📍 Шэньчжэнь &amp; Дунгуань — Электроника и моторы:</text>
      <text x="10" y="100">• Бесколлекторные моторы (BLDC), энкодеры, инверторы</text>
      <text x="10" y="114">• Изготовление пресс-форм и ЧПУ за 48 часов</text>

      <rect x="0" y="132" width="380" height="58" rx="5" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="10" y="150" font-weight="700" fill="#7c3aed">📍 Ханчжоу (Hangzhou) — Экосистема робототехники:</text>
      <text x="10" y="166">• Штаб-квартира Unitree Robotics</text>
      <text x="10" y="180">• Прямой доступ к поставщикам без посредников</text>

      <rect x="0" y="198" width="380" height="65" rx="5" fill="#fff1f2" stroke="#fecdd3"/>
      <text x="10" y="216" font-weight="700" fill="#e11d48">⚡ Скорость итерации (Hardware Sprint):</text>
      <text x="10" y="232">В США изготовление новой детали занимает 6–10 недель.</text>
      <text x="10" y="248">В Шэньчжэне: чертеж утром ➔ готовая деталь вечером!</text>
    </g>
  </g>

  <!-- Right: Cost Disruption Comparison -->
  <g transform="translate(450, 58)" filter="url(#shadowChina)">
    <rect width="406" height="320" rx="8" fill="#ffffff" stroke="#86efac" stroke-width="1.2"/>
    <rect width="406" height="28" rx="8" fill="#15803d"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
      Ценовой Демпинг Компонентов (США vs Китай)
    </text>

    <g transform="translate(14, 38)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
      <!-- Item 1: Harmonic Drive -->
      <rect x="0" y="0" width="376" height="52" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="8" y="16" font-weight="700" fill="#0f172a">Волновой редуктор (Harmonic Drive):</text>
      <text x="8" y="32">Западный аналог (Harmonic Drive SE):</text>
      <text x="260" y="32" font-family="JetBrains Mono, monospace" font-size="9" fill="#dc2626">$1 500 – $2 500</text>
      <text x="8" y="46">Китайский аналог (Leaderdrive):</text>
      <text x="260" y="46" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#16a34a">$200 – $350 (в 7 раз!)</text>

      <!-- Item 2: Frameless Torque Motor -->
      <rect x="0" y="60" width="376" height="52" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="8" y="76" font-weight="700" fill="#0f172a">Бескорпусный моментный двигатель:</text>
      <text x="8" y="92">Западный (Kollmorgen / Maxon):</text>
      <text x="260" y="92" font-family="JetBrains Mono, monospace" font-size="9" fill="#dc2626">$800 – $1 200</text>
      <text x="8" y="106">Китайский аналог:</text>
      <text x="260" y="106" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#16a34a">$70 – $120 (в 10 раз!)</text>

      <!-- Item 3: 6-Axis F/T Sensor -->
      <rect x="0" y="120" width="376" height="52" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="8" y="136" font-weight="700" fill="#0f172a">6-осевой датчик силы/момента:</text>
      <text x="8" y="152">Западный (ATI Industrial):</text>
      <text x="260" y="152" font-family="JetBrains Mono, monospace" font-size="9" fill="#dc2626">$4 000 – $7 000</text>
      <text x="8" y="166">Китайский аналог (Kunwei):</text>
      <text x="260" y="166" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#16a34a">$400 – $700 (в 10 раз!)</text>

      <!-- Total Robot Cost -->
      <rect x="0" y="180" width="376" height="80" rx="5" fill="#f0fdf4" stroke="#bbf7d0"/>
      <text x="8" y="200" font-weight="700" fill="#166534">Итоговая стоимость готового робота:</text>
      <text x="8" y="220">• Американский стартап (Figure, Agility, 1X): $120 000 – $250 000</text>
      <text x="8" y="240" font-weight="700" fill="#15803d">• Китайский серийный Unitree G1: ВСЕГО $16 000</text>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


def generate_humanoid_bottlenecks_radar():
    filepath = os.path.join(OUTPUT_DIR, 'lecture-08', 'humanoid_bottlenecks_radar.svg')
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 410" width="880" height="410">
  <defs>
    <filter id="shadowBN" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title Badge -->
  <g transform="translate(24, 18)">
    <rect width="410" height="28" rx="6" fill="#fff1f2" stroke="#fecdd3"/>
    <text x="12" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#be123c">
      🚧 4 ГЛАВНЫХ БАРЬЕРА АНТРОПОМОРФНОЙ РОБОТОТЕХНИКИ
    </text>
    <text x="440" y="19" font-family="Inter, sans-serif" font-size="11.5" fill="#64748b">
      Что реально отделяет лаборатории от массового внедрения
    </text>
  </g>

  <!-- 4 Bottlenecks Cards 2x2 -->
  <g transform="translate(24, 58)" filter="url(#shadowBN)">
    <!-- 1. The Data Wall -->
    <g transform="translate(0, 0)">
      <rect width="405" height="155" rx="8" fill="#ffffff" stroke="#fca5a5" stroke-width="1.2"/>
      <rect width="405" height="28" rx="8" fill="#ef4444"/>
      <text x="12" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
        1. Проблема «Стены Данных» (Data Wall)
      </text>

      <g transform="translate(12, 38)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        <text x="0" y="14" font-weight="700" fill="#991b1b">У роботов нет своего интернета:</text>
        <text x="6" y="30">• LLM обучаются на триллионах общедоступных токенов текста.</text>
        <text x="6" y="46">• В робототехнике нет открытых терабайт физических действий.</text>
        <text x="6" y="62">• Телеоперация (человек в Apple Vision Pro + экзоскелет) стоит</text>
        <text x="6" y="78">  сотни долларов за час данных и не масштабируется.</text>
        <text x="0" y="98" font-weight="700" fill="#dc2626">Итог: острая нехватка разнообразных датасетов манипуляций.</text>
      </g>
    </g>

    <!-- 2. Thermal & Energy -->
    <g transform="translate(425, 0)">
      <rect width="405" height="155" rx="8" fill="#ffffff" stroke="#fdba74" stroke-width="1.2"/>
      <rect width="405" height="28" rx="8" fill="#f97316"/>
      <text x="12" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
        2. Энергетика &amp; Тепловыделение (Thermal Limits)
      </text>

      <g transform="translate(12, 38)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        <text x="0" y="14" font-weight="700" fill="#c2410c">Физика моторов и батарей:</text>
        <text x="6" y="30">• Время активной ходьбы на батарее 1–2 кВт·ч: ВСЕГО 1.5–2 часа.</text>
        <text x="6" y="46">• Статическое удержание позы: человек тратит минимум калорий,</text>
        <text x="6" y="62">  а электромотор греется током I²R даже без совершения работы!</text>
        <text x="6" y="78">• Перегрев приводов при подъеме тяжестей и падение момента.</text>
        <text x="0" y="98" font-weight="700" fill="#ea580c">Итог: требуется частая смена АКБ или принудительное охлаждение.</text>
      </g>
    </g>

    <!-- 3. Dexterous Hands -->
    <g transform="translate(0, 168)">
      <rect width="405" height="155" rx="8" fill="#ffffff" stroke="#c084fc" stroke-width="1.2"/>
      <rect width="405" height="28" rx="8" fill="#9333ea"/>
      <text x="12" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
        3. Ловкость Кистей против Прочности
      </text>

      <g transform="translate(12, 38)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        <text x="0" y="14" font-weight="700" fill="#7e22ce">Трилемма руки робота:</text>
        <text x="6" y="30">• В кисти человека 27 костей и тысячи механорецепторов.</text>
        <text x="6" y="46">• Робо-кисти либо высокоподвижные (16–22 DoF), но хрупкие и ломаются</text>
        <text x="6" y="62">  от первого удара о стол, либо прочные клешни без мелкой моторики.</text>
        <text x="6" y="78">• Тактильная чувствительность (GelSight, кожа) недолговечна к истиранию.</text>
        <text x="0" y="98" font-weight="700" fill="#9333ea">Итог: кисть стоит как треть робота и требует частого ремонта.</text>
      </g>
    </g>

    <!-- 4. Safety & Contacts -->
    <g transform="translate(425, 168)">
      <rect width="405" height="155" rx="8" fill="#ffffff" stroke="#86efac" stroke-width="1.2"/>
      <rect width="405" height="28" rx="8" fill="#16a34a"/>
      <text x="12" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">
        4. Нестационарный Контакт &amp; Безопасность
      </text>

      <g transform="translate(12, 38)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        <text x="0" y="14" font-weight="700" fill="#15803d">Работа бок о бок с человеком:</text>
        <text x="6" y="30">• Робот весом 60–80 кг с металлическими звеньями опасен.</text>
        <text x="6" y="46">• Нейросети склонны к «галлюцинациям действий» при редких помехах.</text>
        <text x="6" y="62">• Отсутствие международных стандартов сертификации (ISO) для</text>
        <text x="6" y="78">  автономных двуногих роботов на производствах рядом с людьми.</text>
        <text x="0" y="98" font-weight="700" fill="#16a34a">Итог: строгие защитные зоны или снижение скорости движений.</text>
      </g>
    </g>
  </g>
</svg>'''
    write_svg(filepath, svg)


def generate_lecture_07_08_diagrams():
    print("=== Generating Rigorous Diagrams for Lectures 07 and 08 ===")
    generate_teacher_student_sim2real()
    generate_diffusion_policy_multimodal()
    generate_vla_architecture_pipeline()
    generate_world_action_model_rollout()
    generate_edge_compute_multirate()
    generate_helix_fullbody_architecture()
    generate_humanoid_landscape_matrix()
    generate_china_supply_chain_cluster()
    generate_humanoid_bottlenecks_radar()
    print("=== Lectures 07 and 08 Diagrams Successfully Generated! ===")

if __name__ == '__main__':
    generate_lecture_07_08_diagrams()
