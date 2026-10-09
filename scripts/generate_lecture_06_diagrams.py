#!/usr/bin/env python3
"""
Generate high-density, professional SVG diagrams for Lecture 06 (Reinforcement Learning in Robotics).
Color palette: robotics-minimal
Primary: #1e293b, Accent Blue: #2563eb, Success: #059669, Warning: #d97706, Danger: #dc2626,
Background: #f8fafc, Border: #e2e8f0, Text Muted: #64748b, Font: Inter / JetBrains Mono.
"""

import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'lecture-06')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_rl_taxonomy():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 540" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <filter id="shadow" x="-3%" y="-4%" width="106%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" rx="12" fill="url(#bgGrad)" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title & Subtitle -->
  <g transform="translate(28, 30)">
    <text x="0" y="0" font-family="Inter, system-ui, sans-serif" font-size="17" font-weight="800" fill="#0f172a">Таксономия обучения с подкреплением (Murphy, 2023)</text>
    <text x="0" y="20" font-family="Inter, system-ui, sans-serif" font-size="12" fill="#64748b">Иерархическая классификация алгоритмов: Model-Free vs Model-Based и способы представления политики</text>
  </g>

  <!-- Level 0: Root Machine Learning -->
  <g transform="translate(380, 72)" filter="url(#shadow)">
    <rect width="220" height="38" rx="8" fill="#1e293b" stroke="#0f172a" stroke-width="1.2"/>
    <text x="110" y="23" text-anchor="middle" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="#ffffff">Machine Learning</text>
  </g>

  <!-- Connectors from Root to 3 ML Paradigms -->
  <path d="M 430,110 L 430,126 L 140,126 L 140,140" stroke="#94a3b8" stroke-width="1.5" fill="none"/>
  <path d="M 490,110 L 490,140" stroke="#94a3b8" stroke-width="1.5" fill="none"/>
  <path d="M 550,110 L 550,126 L 660,126 L 660,140" stroke="#2563eb" stroke-width="2" fill="none"/>

  <!-- Level 1: 3 Paradigms -->
  <!-- Supervised -->
  <g transform="translate(45, 140)">
    <rect width="190" height="42" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
    <text x="95" y="21" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#475569">Supervised Learning</text>
    <text x="95" y="34" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="#64748b">y ≈ f(x), разметка пар</text>
  </g>

  <!-- Unsupervised -->
  <g transform="translate(395, 140)">
    <rect width="190" height="42" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
    <text x="95" y="21" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#475569">Unsupervised Learning</text>
    <text x="95" y="34" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="#64748b">p(x), кластеризация</text>
  </g>

  <!-- Reinforcement Learning Highlighted -->
  <g transform="translate(560, 140)" filter="url(#shadow)">
    <rect width="200" height="42" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="1.8"/>
    <text x="100" y="21" text-anchor="middle" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#1e40af">Reinforcement Learning</text>
    <text x="100" y="34" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="#2563eb">max E[∑ γᵗ Rₜ], скалярная награда</text>
  </g>

  <!-- Connectors from RL to Model-Free and Model-Based -->
  <path d="M 660,182 L 660,202 L 315,202 L 315,218" stroke="#2563eb" stroke-width="1.8" fill="none"/>
  <path d="M 660,182 L 660,202 L 815,202 L 815,218" stroke="#d97706" stroke-width="1.8" fill="none"/>

  <!-- Level 2: Model-Free vs Model-Based -->
  <!-- Left Big Branch: Model-Free RL -->
  <g transform="translate(24, 218)">
    <rect width="580" height="260" rx="8" fill="#f8fafc" stroke="#bfdbfe" stroke-width="1.5"/>
    <rect width="580" height="28" rx="8" fill="#1d4ed8"/>
    <text x="16" y="19" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">Model-Free RL (Без модели динамики среды)</text>
    <text x="564" y="19" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#bfdbfe">Опыт: (s, a, r, s')</text>

    <!-- 3 Sub-families inside Model-Free -->
    <!-- 1. Value-Based -->
    <g transform="translate(12, 38)">
      <rect width="176" height="210" rx="6" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>
      <rect width="176" height="22" rx="6" fill="#f1f5f9"/>
      <text x="88" y="15" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#1e293b">Value-Based</text>
      
      <g transform="translate(8, 30)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        <text x="0" y="12" font-weight="700" fill="#0f172a">Идея:</text>
        <text x="0" y="26">Оценка Q*(s, a),</text>
        <text x="0" y="39">π(s) = argmax Q</text>
        
        <text x="0" y="60" font-weight="700" fill="#0f172a">Ключевые алгоритмы:</text>
        <text x="0" y="74" font-family="JetBrains Mono" font-size="9" fill="#2563eb">• Q-Learning (табл.)</text>
        <text x="0" y="88" font-family="JetBrains Mono" font-size="9" fill="#2563eb">• DQN (Mnih 2015)</text>
        <text x="0" y="102" font-family="JetBrains Mono" font-size="9" fill="#2563eb">• Double DQN</text>
        <text x="0" y="116" font-family="JetBrains Mono" font-size="9" fill="#2563eb">• Rainbow</text>

        <text x="0" y="138" font-weight="700" fill="#d97706">Пространство действий:</text>
        <text x="0" y="152" fill="#475569">Дискретное |A| &lt; ∞</text>
        <text x="0" y="168" font-size="8.5" fill="#64748b">argmax по непрерывному A вычислительно дорог</text>
      </g>
    </g>

    <!-- 2. Policy-Based -->
    <g transform="translate(200, 38)">
      <rect width="176" height="210" rx="6" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>
      <rect width="176" height="22" rx="6" fill="#f1f5f9"/>
      <text x="88" y="15" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#1e293b">Policy-Based</text>
      
      <g transform="translate(8, 30)" font-family="Inter, sans-serif" font-size="9.5" fill="#334155">
        <text x="0" y="12" font-weight="700" fill="#0f172a">Идея:</text>
        <text x="0" y="26">Прямая параметризация</text>
        <text x="0" y="39">политики π_θ(a|s)</text>
        
        <text x="0" y="60" font-weight="700" fill="#0f172a">Ключевые алгоритмы:</text>
        <text x="0" y="74" font-family="JetBrains Mono" font-size="9" fill="#059669">• REINFORCE (MC)</text>
        <text x="0" y="88" font-family="JetBrains Mono" font-size="9" fill="#059669">• Natural PG</text>
        <text x="0" y="102" font-family="JetBrains Mono" font-size="9" fill="#059669">• TRPO (Trust Region)</text>

        <text x="0" y="124" font-weight="700" fill="#dc2626">Ограничение:</text>
        <text x="0" y="138" fill="#475569">Высокая дисперсия</text>
        <text x="0" y="152" fill="#475569">оценки Монте-Карло,</text>
        <text x="0" y="166" fill="#475569">медленная сходимость</text>
      </g>
    </g>

    <!-- 3. Actor-Critic (SOTA Robotics) -->
    <g transform="translate(388, 38)">
      <rect width="180" height="210" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.3"/>
      <rect width="180" height="22" rx="6" fill="#2563eb"/>
      <text x="90" y="15" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#ffffff">Actor-Critic (Робототехника)</text>
      
      <g transform="translate(8, 30)" font-family="Inter, sans-serif" font-size="9.5" fill="#1e293b">
        <text x="0" y="12" font-weight="700" fill="#1e40af">Идея: Синергия</text>
        <text x="0" y="26">Actor π_θ(a|s) + Critic V_ϕ(s)</text>
        <text x="0" y="39" fill="#2563eb">Критик гасит дисперсию</text>
        
        <text x="0" y="60" font-weight="700" fill="#1e40af">Рабочие лошадки SOTA:</text>
        <text x="0" y="74" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#1d4ed8">• PPO (On-policy, клиппинг)</text>
        <text x="0" y="88" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#1d4ed8">• SAC (Off-policy, энтропия)</text>
        <text x="0" y="102" font-family="JetBrains Mono" font-size="9" fill="#334155">• TD3 / DDPG</text>

        <text x="0" y="124" font-weight="700" fill="#059669">Стандарт локомоции:</text>
        <text x="0" y="138" fill="#047857">Непрерывные приводы A ⊆ ℝᵈ</text>
        <text x="0" y="152" fill="#047857">Масштабируется на GPU</text>
        <text x="0" y="166" font-size="8.5" fill="#64748b">Isaac Sim, MuJoCo MJX</text>
      </g>
    </g>
  </g>

  <!-- Right Branch: Model-Based RL -->
  <g transform="translate(620, 218)">
    <rect width="336" height="260" rx="8" fill="#fffbeb" stroke="#fde68a" stroke-width="1.5"/>
    <rect width="336" height="28" rx="8" fill="#d97706"/>
    <text x="16" y="19" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">Model-Based RL (Модель s' = f(s, a))</text>
    <text x="320" y="19" text-anchor="end" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#fef3c7">Sample-Efficient</text>

    <!-- Sub-branches -->
    <g transform="translate(12, 38)">
      <!-- Known Model -->
      <rect width="312" height="96" rx="6" fill="#ffffff" stroke="#fde68a" stroke-width="1"/>
      <text x="10" y="18" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#92400e">Априорная модель (Given Physics Model)</text>
      <g transform="translate(10, 24)" font-family="Inter, sans-serif" font-size="9.5" fill="#451a03">
        <text x="0" y="14">• Динамическое программирование (Value Iteration)</text>
        <text x="0" y="28">• Оптимальное управление: LQR, iLQR, NMPC</text>
        <text x="0" y="42">• Поиск по дереву решений: MCTS (AlphaZero)</text>
        <text x="0" y="58" font-size="8.5" fill="#78350f">Требует точных аналитических уравнений контактов</text>
      </g>

      <!-- Learned Model -->
      <g transform="translate(0, 106)">
        <rect width="312" height="104" rx="6" fill="#ffffff" stroke="#fde68a" stroke-width="1"/>
        <text x="10" y="18" font-family="Inter, sans-serif" font-size="10" font-weight="700" fill="#92400e">Обучаемая модель (Learned World Model)</text>
        <g transform="translate(10, 24)" font-family="Inter, sans-serif" font-size="9.5" fill="#451a03">
          <text x="0" y="14">• Планирование на лету: PETS, PlaNet, Dreamer</text>
          <text x="0" y="28">• Синтез опыта (Dyna): Dyna-Q, MBPO, MuZero</text>
          <text x="0" y="44" font-weight="700" fill="#b45309">Плюс: Высокая эффективность данных</text>
          <text x="0" y="58" font-size="8.5" fill="#78350f">Минус: Накопление ошибки модели (Compounding error)</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Bottom Takeaway Badge -->
  <g transform="translate(28, 492)">
    <rect width="928" height="32" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
    <text x="14" y="20" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">
      <tspan font-weight="700" fill="#0f172a">Вывод для робототехники:</tspan> В непрерывной локомоции доминирует <tspan font-weight="700" fill="#2563eb">Model-Free Actor-Critic (PPO / SAC)</tspan> благодаря параллельной симуляции на GPU, снимающей дефицит сэмплов.
    </text>
  </g>
</svg>'''
    filepath = os.path.join(OUTPUT_DIR, 'rl_taxonomy_murphy.svg')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {filepath}")

def generate_dqn_architecture():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 480" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#dc2626"/>
    </marker>
    <marker id="arrow-slate" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#64748b"/>
    </marker>
    <filter id="shadow" x="-3%" y="-4%" width="106%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Header -->
  <g transform="translate(28, 28)">
    <text x="0" y="0" font-family="Inter, system-ui, sans-serif" font-size="16.5" font-weight="800" fill="#0f172a">Архитектура Deep Q-Network (DQN) и стабилизация обучения</text>
    <text x="0" y="20" font-family="Inter, system-ui, sans-serif" font-size="11.5" fill="#64748b">Решение проблемы нестабильности аппроксимации: буфер Experience Replay и замороженная целевая сеть Target Network</text>
  </g>

  <!-- Left: Environment & Agent Interaction -->
  <g transform="translate(28, 70)" filter="url(#shadow)">
    <!-- Environment Box -->
    <rect width="210" height="150" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="210" height="26" rx="8" fill="#334155"/>
    <text x="14" y="17" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">Среда (Environment)</text>
    
    <g transform="translate(14, 40)" font-family="Inter, sans-serif" font-size="10" fill="#1e293b">
      <text x="0" y="12" font-weight="700" fill="#0f172a">Робот / Игра / Симулятор</text>
      <text x="0" y="28" fill="#475569">Принимает действие: aₜ</text>
      <text x="0" y="44" fill="#475569">Возвращает состояние: sₜ₊₁</text>
      <text x="0" y="60" fill="#475569">Скалярную награду: rₜ₊₁</text>
      <rect x="0" y="74" width="180" height="22" rx="4" fill="#eff6ff" stroke="#bfdbfe"/>
      <text x="8" y="89" font-family="JetBrains Mono" font-size="9.5" fill="#1e40af">eₜ = (sₜ, aₜ, rₜ₊₁, sₜ₊₁)</text>
    </g>
  </g>

  <!-- Replay Buffer Box (Center-Left) -->
  <g transform="translate(28, 246)" filter="url(#shadow)">
    <rect width="210" height="180" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <rect width="210" height="26" rx="8" fill="#2563eb"/>
    <text x="14" y="17" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Experience Replay Buffer 𝒟</text>

    <!-- Buffer visualization slices -->
    <g transform="translate(14, 38)">
      <rect x="0" y="0" width="182" height="18" rx="3" fill="#ffffff" stroke="#93c5fd"/>
      <text x="6" y="13" font-family="JetBrains Mono" font-size="8.5" fill="#1e40af">(s₁, a₁, r₂, s₂)</text>
      <rect x="0" y="22" width="182" height="18" rx="3" fill="#ffffff" stroke="#93c5fd"/>
      <text x="6" y="35" font-family="JetBrains Mono" font-size="8.5" fill="#1e40af">(s₂, a₂, r₃, s₃)</text>
      <rect x="0" y="44" width="182" height="18" rx="3" fill="#dbeafe" stroke="#3b82f6"/>
      <text x="6" y="57" font-family="JetBrains Mono" font-size="8.5" font-weight="700" fill="#1d4ed8">Batch B ~ U(𝒟) [i.i.d.]</text>
      <rect x="0" y="66" width="182" height="18" rx="3" fill="#ffffff" stroke="#93c5fd"/>
      <text x="6" y="79" font-family="JetBrains Mono" font-size="8.5" fill="#1e40af">(sₜ, aₜ, rₜ₊₁, sₜ₊₁)</text>

      <text x="0" y="106" font-family="Inter" font-size="9.5" font-weight="700" fill="#1e40af">Цель буфера:</text>
      <text x="0" y="120" font-family="Inter" font-size="9" fill="#334155">1. Разрушение автокорреляции</text>
      <text x="0" y="132" font-family="Inter" font-size="9" fill="#334155">2. Многократное переиспользование</text>
    </g>
  </g>

  <!-- Arrow Env -> Buffer -->
  <path d="M 133,220 L 133,244" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)" fill="none"/>
  <text x="142" y="235" font-family="JetBrains Mono" font-size="8.5" fill="#2563eb">push(eₜ)</text>

  <!-- Online Q-Network (Center Top) -->
  <g transform="translate(290, 70)" filter="url(#shadow)">
    <rect width="280" height="165" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.8"/>
    <rect width="280" height="26" rx="8" fill="#1d4ed8"/>
    <text x="14" y="17" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">Основная Q-сеть: Q(s, a; θ)</text>
    <text x="266" y="17" text-anchor="end" font-family="JetBrains Mono" font-size="9.5" fill="#93c5fd">Online θ</text>

    <!-- Network layers -->
    <g transform="translate(16, 38)">
      <rect x="0" y="6" width="45" height="70" rx="4" fill="#f1f5f9" stroke="#cbd5e1"/>
      <text x="22" y="36" text-anchor="middle" font-family="Inter" font-size="9" fill="#475569">Вход s</text>
      <text x="22" y="48" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="#64748b">ℝⁿ</text>

      <path d="M 47,41 L 68,41" stroke="#94a3b8" stroke-width="1.5" fill="none"/>

      <!-- Hidden Layers -->
      <rect x="70" y="0" width="70" height="82" rx="4" fill="#eff6ff" stroke="#bfdbfe"/>
      <text x="105" y="32" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="#1e40af">MLP / CNN</text>
      <text x="105" y="48" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="#2563eb">Веса θ</text>
      <text x="105" y="62" text-anchor="middle" font-family="Inter" font-size="7.5" fill="#64748b">ReLU / Dense</text>

      <path d="M 142,41 L 163,41" stroke="#94a3b8" stroke-width="1.5" fill="none"/>

      <!-- Output Q values -->
      <rect x="165" y="6" width="80" height="70" rx="4" fill="#f0fdf4" stroke="#86efac"/>
      <text x="205" y="24" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="#166534">Q(s, a₁)</text>
      <text x="205" y="41" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="#166534">Q(s, a₂)</text>
      <text x="205" y="58" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="#166534">Q(s, aₘ)</text>
    </g>

    <text x="16" y="142" font-family="Inter" font-size="9.5" fill="#475569">
      Выбор действия: <tspan font-family="JetBrains Mono" font-weight="700" fill="#2563eb">aₜ = argmaxₐ Q(sₜ, a; θ)</tspan> (ε-greedy)
    </text>
  </g>

  <!-- Target Q-Network (Center Bottom) -->
  <g transform="translate(290, 275)" filter="url(#shadow)">
    <rect width="280" height="150" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="1.5"/>
    <rect width="280" height="26" rx="8" fill="#475569"/>
    <text x="14" y="17" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">Целевая Q-сеть: Q(s', a'; θ⁻)</text>
    <text x="266" y="17" text-anchor="end" font-family="JetBrains Mono" font-size="9.5" fill="#cbd5e1">Frozen θ⁻</text>

    <g transform="translate(16, 38)">
      <rect x="0" y="6" width="45" height="55" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="22" y="32" text-anchor="middle" font-family="Inter" font-size="9" fill="#475569">Вход s'</text>

      <path d="M 47,33 L 68,33" stroke="#94a3b8" stroke-width="1.5" fill="none"/>

      <rect x="70" y="0" width="70" height="66" rx="4" fill="#ffffff" stroke="#94a3b8"/>
      <text x="105" y="28" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="#334155">Заморозка</text>
      <text x="105" y="44" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="#475569">θ⁻ = θ_old</text>

      <path d="M 142,33 L 163,33" stroke="#94a3b8" stroke-width="1.5" fill="none"/>

      <rect x="165" y="6" width="80" height="55" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="205" y="36" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" font-weight="700" fill="#334155">maxₐ Q(s', a')</text>
    </g>

    <text x="16" y="128" font-family="Inter" font-size="9" fill="#64748b">
      Обновление каждые C шагов: <tspan font-family="JetBrains Mono" fill="#0f172a">θ⁻ ← θ</tspan> (или Polyak τ)
    </text>
  </g>

  <!-- Periodic sync arrow from Online to Target -->
  <path d="M 330,237 L 330,273" stroke="#64748b" stroke-width="1.8" stroke-dasharray="4,3" marker-end="url(#arrow-slate)" fill="none"/>
  <text x="338" y="258" font-family="Inter" font-size="8.5" fill="#64748b">Периодическая копия θ⁻ ← θ</text>

  <!-- Arrow Replay Buffer -> Networks -->
  <path d="M 240,310 L 265,310 L 265,150 L 288,150" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arrow)" fill="none"/>
  <text x="246" y="142" font-family="JetBrains Mono" font-size="8.5" fill="#2563eb">s</text>

  <path d="M 240,350 L 288,350" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow-slate)" fill="none"/>
  <text x="252" y="342" font-family="JetBrains Mono" font-size="8.5" fill="#64748b">s'</text>

  <!-- Action from Online Network to Env -->
  <path d="M 290,110 L 260,110 L 260,110 L 240,110" stroke="#059669" stroke-width="2" marker-end="url(#arrow-green)" fill="none"/>
  <text x="246" y="102" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#059669">aₜ</text>

  <!-- Right: Bellman Target & Loss Computation -->
  <g transform="translate(615, 140)" filter="url(#shadow)">
    <rect width="295" height="235" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
    <rect width="295" height="26" rx="8" fill="#0f172a"/>
    <text x="14" y="17" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Целевое значение Беллмана и Loss</text>

    <!-- Bellman Target y_i -->
    <g transform="translate(14, 38)">
      <rect width="267" height="48" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
      <text x="10" y="18" font-family="Inter" font-size="9.5" font-weight="700" fill="#1e40af">Цель Беллмана (Target):</text>
      <text x="10" y="36" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#1d4ed8">y = r + γ · maxₐ Q(s', a; θ⁻)</text>
    </g>

    <!-- Flow into Loss -->
    <path d="M 147,88 L 147,106" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arrow)" fill="none"/>

    <!-- Loss Equation -->
    <g transform="translate(14, 108)">
      <rect width="267" height="52" rx="6" fill="#fef2f2" stroke="#fecaca"/>
      <text x="10" y="18" font-family="Inter" font-size="9.5" font-weight="700" fill="#991b1b">Функция потерь (TD Loss):</text>
      <text x="10" y="38" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#dc2626">ℒ(θ) = 𝔼_B [ (y − Q(s, a; θ))² ]</text>
    </g>

    <!-- Flow back to update theta -->
    <path d="M 147,162 L 147,180" stroke="#dc2626" stroke-width="1.5" marker-end="url(#arrow-red)" fill="none"/>

    <g transform="translate(14, 182)">
      <rect width="267" height="38" rx="6" fill="#f0fdf4" stroke="#bbf7d0"/>
      <text x="10" y="16" font-family="Inter" font-size="9.5" font-weight="700" fill="#166534">Шаг оптимизации (Adam/SGD):</text>
      <text x="10" y="30" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#15803d">θ ← θ − α · ∇_θ ℒ(θ)</text>
    </g>
  </g>

  <!-- Connectors from Target Net and Online Net to Bellman Box -->
  <path d="M 572,130 L 613,155" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arrow)" fill="none"/>
  <path d="M 572,345 L 613,175" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow-slate)" fill="none"/>

  <!-- Backprop loop arrow to Online Network -->
  <path d="M 748,222 L 748,245 L 530,245 L 530,237" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrow-red)" fill="none"/>
  <text x="590" y="240" font-family="Inter" font-size="8.5" fill="#dc2626">Градиент ∇_θ ℒ обновляет только θ</text>
</svg>'''
    filepath = os.path.join(OUTPUT_DIR, 'dqn_architecture.svg')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {filepath}")

def generate_actor_critic_architecture():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 490" width="100%" height="100%">
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#d97706"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#7c3aed"/>
    </marker>
    <filter id="shadow" x="-3%" y="-4%" width="106%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title -->
  <g transform="translate(28, 28)">
    <text x="0" y="0" font-family="Inter, system-ui, sans-serif" font-size="16.5" font-weight="800" fill="#0f172a">Архитектура Actor-Critic: Замкнутый контур управления</text>
    <text x="0" y="20" font-family="Inter, system-ui, sans-serif" font-size="11.5" fill="#64748b">Разделение ролей: Актёр формирует управляющее воздействие, Критик оценивает ценность состояния и вычисляет TD-ошибку</text>
  </g>

  <!-- Environment (Bottom Center) -->
  <g transform="translate(260, 345)" filter="url(#shadow)">
    <rect width="420" height="105" rx="8" fill="#1e293b" stroke="#0f172a" stroke-width="1.5"/>
    <rect width="420" height="26" rx="8" fill="#0f172a"/>
    <text x="16" y="17" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">Среда (Environment: Физический робот / Isaac Sim)</text>

    <g transform="translate(16, 38)" font-family="Inter, sans-serif" font-size="10.5" fill="#e2e8f0">
      <text x="0" y="14">• Физический отклик: sₜ₊₁ = f(sₜ, aₜ) + возмущения dₜ</text>
      <text x="0" y="32">• Функция вознаграждения: rₜ₊₁ = R(sₜ, aₜ, sₜ₊₁) (Reward Shaping)</text>
      <text x="0" y="50" fill="#94a3b8">• Частота контура: 50–500 Гц на бортовом компьютере робота</text>
    </g>
  </g>

  <!-- Left: Actor Module -->
  <g transform="translate(48, 85)" filter="url(#shadow)">
    <rect width="360" height="215" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.8"/>
    <rect width="360" height="28" rx="8" fill="#2563eb"/>
    <text x="14" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">Актёр (Actor / Policy Network): π_θ(a | s)</text>

    <g transform="translate(14, 40)" font-family="Inter, sans-serif" font-size="10" fill="#1e293b">
      <text x="0" y="12" font-weight="700" fill="#1e40af">Назначение:</text>
      <text x="80" y="12" fill="#334155">Генерация команд приводам робота</text>

      <!-- Architecture spec -->
      <rect x="0" y="24" width="332" height="42" rx="4" fill="#ffffff" stroke="#bfdbfe"/>
      <text x="8" y="40" font-family="Inter" font-weight="700" fill="#1e40af">Вход:</text>
      <text x="44" y="40" font-family="JetBrains Mono" fill="#334155">sₜ (углы суставов q, скорости q̇, IMU ω, g)</text>
      <text x="8" y="56" font-family="Inter" font-weight="700" fill="#1e40af">Выход:</text>
      <text x="52" y="56" font-family="JetBrains Mono" fill="#2563eb">aₜ ~ 𝒩(μ_θ(sₜ), Σ_θ) (моменты / целевые углы)</text>

      <text x="0" y="84" font-weight="700" fill="#1e40af">Правило обновления параметров θ (Policy Gradient):</text>
      <rect x="0" y="92" width="332" height="44" rx="4" fill="#ffffff" stroke="#bfdbfe"/>
      <text x="8" y="110" font-family="JetBrains Mono" font-size="10.5" font-weight="700" fill="#1d4ed8">∇_θ J(θ) = 𝔼 [ ∇_θ log π_θ(aₜ|sₜ) · δₜ ]</text>
      <text x="8" y="126" font-family="Inter" font-size="9" fill="#64748b">где δₜ — сигнал преимущества (Advantage), полученный от Критика</text>

      <text x="0" y="152" font-size="9.5" fill="#475569">
        При <tspan font-weight="700" fill="#059669">δₜ &gt; 0</tspan>: действие успешнее среднего ⇒ вероятность ↑
      </text>
      <text x="0" y="166" font-size="9.5" fill="#475569">
        При <tspan font-weight="700" fill="#dc2626">δₜ &lt; 0</tspan>: действие привело к штрафу ⇒ вероятность ↓
      </text>
    </g>
  </g>

  <!-- Right: Critic Module -->
  <g transform="translate(532, 85)" filter="url(#shadow)">
    <rect width="360" height="215" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.8"/>
    <rect width="360" height="28" rx="8" fill="#059669"/>
    <text x="14" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">Критик (Critic / Value Network): V_ϕ(s)</text>

    <g transform="translate(14, 40)" font-family="Inter, sans-serif" font-size="10" fill="#1e293b">
      <text x="0" y="12" font-weight="700" fill="#166534">Назначение:</text>
      <text x="80" y="12" fill="#334155">Оценка ожидаемой суммарной отдачи</text>

      <!-- Architecture spec -->
      <rect x="0" y="24" width="332" height="42" rx="4" fill="#ffffff" stroke="#bbf7d0"/>
      <text x="8" y="40" font-family="Inter" font-weight="700" fill="#166534">Вход:</text>
      <text x="44" y="40" font-family="JetBrains Mono" fill="#334155">sₜ (состояние системы) или (sₜ, aₜ)</text>
      <text x="8" y="56" font-family="Inter" font-weight="700" fill="#166534">Выход:</text>
      <text x="52" y="56" font-family="JetBrains Mono" fill="#15803d">V_ϕ(sₜ) ∈ ℝ (скалярная ценность состояния)</text>

      <text x="0" y="84" font-weight="700" fill="#166534">Вычисление TD-ошибки (TD Error / Advantage):</text>
      <rect x="0" y="92" width="332" height="44" rx="4" fill="#ffffff" stroke="#bbf7d0"/>
      <text x="8" y="110" font-family="JetBrains Mono" font-size="10.5" font-weight="700" fill="#047857">δₜ = rₜ₊₁ + γ · V_ϕ(sₜ₊₁) − V_ϕ(sₜ)</text>
      <text x="8" y="126" font-family="Inter" font-size="9" fill="#64748b">Оценка: насколько шаг превзошел средние ожидания</text>

      <text x="0" y="152" font-size="9.5" fill="#475569">
        Обучение критика: минимизация MSE ошибки Беллмана
      </text>
      <text x="0" y="166" font-family="JetBrains Mono" font-size="9" fill="#166534">
        ℒ(ϕ) = 1/2 · δₜ² ⇒ ϕ ← ϕ − α_v · ∇_ϕ ℒ(ϕ)
      </text>
    </g>
  </g>

  <!-- Connectors and Information Flow -->
  <!-- 1. Critic passes TD Error delta_t to Actor -->
  <path d="M 532,192 L 410,192" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrow-purple)" fill="none"/>
  <rect x="424" y="174" width="94" height="20" rx="4" fill="#f5f3ff" stroke="#ddd6fe"/>
  <text x="471" y="188" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" font-weight="700" fill="#6d28d9">Сигнал δₜ</text>

  <!-- 2. Actor sends Action a_t to Environment -->
  <path d="M 190,300 L 190,397 L 258,397" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)" fill="none"/>
  <rect x="150" y="340" width="80" height="20" rx="4" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="190" y="354" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" font-weight="700" fill="#1d4ed8">Действие aₜ</text>

  <!-- 3. Environment sends State s_t to Actor and Critic -->
  <path d="M 470,345 L 470,318 L 300,318 L 300,302" stroke="#059669" stroke-width="2" marker-end="url(#arrow-green)" fill="none"/>
  <path d="M 470,318 L 650,318 L 650,302" stroke="#059669" stroke-width="2" marker-end="url(#arrow-green)" fill="none"/>
  <rect x="426" y="308" width="88" height="20" rx="4" fill="#ecfdf5" stroke="#a7f3d0"/>
  <text x="470" y="322" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" font-weight="700" fill="#047857">Состояние sₜ</text>

  <!-- 4. Environment sends Reward r_t to Critic -->
  <path d="M 680,380 L 780,380 L 780,302" stroke="#d97706" stroke-width="2" marker-end="url(#arrow-amber)" fill="none"/>
  <rect x="735" y="340" width="90" height="20" rx="4" fill="#fffbeb" stroke="#fde68a"/>
  <text x="780" y="354" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" font-weight="700" fill="#b45309">Награда rₜ₊₁</text>

  <!-- Footer summary -->
  <g transform="translate(28, 458)">
    <rect width="884" height="24" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
    <text x="12" y="16" font-family="Inter" font-size="9" fill="#475569">
      <tspan font-weight="700" fill="#0f172a">Ключевой эффект:</tspan> Использование функции ценности Критика V(s) снижает дисперсию градиента на порядки по сравнению с REINFORCE, обеспечивая устойчивое обучение шагающих роботов.
    </text>
  </g>
</svg>'''
    filepath = os.path.join(OUTPUT_DIR, 'actor_critic_architecture.svg')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {filepath}")

def generate_teacher_student_sim2real():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" width="100%" height="100%">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#7c3aed"/>
    </marker>
    <filter id="shadow" x="-3%" y="-4%" width="106%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title -->
  <g transform="translate(28, 28)">
    <text x="0" y="0" font-family="Inter, system-ui, sans-serif" font-size="16.5" font-weight="800" fill="#0f172a">Sim-to-Real: Двухэтапная дистилляция Teacher-Student</text>
    <text x="0" y="20" font-family="Inter, system-ui, sans-serif" font-size="11.5" fill="#64748b">Преодоление Reality Gap: обучение в симуляции с привилегированной информацией и клонирование поведения на проприоцепцию</text>
  </g>

  <!-- Stage 1 Box: Teacher in Simulation -->
  <g transform="translate(28, 70)" filter="url(#shadow)">
    <rect width="560" height="195" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <rect width="560" height="26" rx="8" fill="#2563eb"/>
    <text x="14" y="17" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">Этап 1: Обучение Учителя (Teacher Policy) в GPU-симуляции (Isaac Sim)</text>

    <!-- Inputs to Teacher -->
    <g transform="translate(14, 38)">
      <!-- Proprioception -->
      <rect x="0" y="0" width="160" height="52" rx="4" fill="#ffffff" stroke="#bfdbfe"/>
      <text x="8" y="16" font-family="Inter" font-size="9" font-weight="700" fill="#1e40af">Проприоцепция s_proprio:</text>
      <text x="8" y="30" font-family="JetBrains Mono" font-size="8.5" fill="#334155">q, q̇ (углы, скорости)</text>
      <text x="8" y="44" font-family="JetBrains Mono" font-size="8.5" fill="#334155">IMU (ω, угловая скор.)</text>

      <!-- Privileged info -->
      <rect x="0" y="60" width="160" height="85" rx="4" fill="#fef3c7" stroke="#fcd34d"/>
      <text x="8" y="16" font-family="Inter" font-size="9" font-weight="700" fill="#92400e">🔒 Привилегированные данные:</text>
      <text x="8" y="30" font-family="Inter" font-size="8.5" fill="#78350f">• Точная карта высот terrain</text>
      <text x="8" y="44" font-family="Inter" font-size="8.5" fill="#78350f">• Силы контактов стоп F_c</text>
      <text x="8" y="58" font-family="Inter" font-size="8.5" fill="#78350f">• Коэффициент трения μ</text>
      <text x="8" y="72" font-family="Inter" font-size="8.5" fill="#78350f">• Масса m и центр масс CoM</text>

      <!-- Connectors to Teacher Net -->
      <path d="M 162,26 L 198,60" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arrow)" fill="none"/>
      <path d="M 162,100 L 198,75" stroke="#d97706" stroke-width="1.5" marker-end="url(#arrow)" fill="none"/>

      <!-- Teacher Policy MLP -->
      <rect x="200" y="35" width="165" height="75" rx="6" fill="#ffffff" stroke="#2563eb" stroke-width="1.8"/>
      <text x="282" y="56" text-anchor="middle" font-family="Inter" font-size="10.5" font-weight="700" fill="#1d4ed8">Политика Учителя</text>
      <text x="282" y="72" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" fill="#2563eb">π_teacher(a | s_priv)</text>
      <text x="282" y="90" text-anchor="middle" font-family="Inter" font-size="8.5" fill="#64748b">Обучена PPO в симуляторе</text>

      <!-- Output action -->
      <path d="M 367,72 L 405,72" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)" fill="none"/>
      <rect x="408" y="52" width="130" height="40" rx="4" fill="#ffffff" stroke="#bfdbfe"/>
      <text x="473" y="68" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#1e40af">a_teacher</text>
      <text x="473" y="82" text-anchor="middle" font-family="Inter" font-size="8" fill="#64748b">Идеальные действия</text>

      <text x="8" y="152" font-family="Inter" font-size="9" fill="#1e40af">
        ✓ 4096 параллельных роботов в Isaac Sim; обучение занимает ~20 минут на GPU
      </text>
    </g>
  </g>

  <!-- Stage 2 Box: Student Policy Distillation -->
  <g transform="translate(28, 280)" filter="url(#shadow)">
    <rect width="560" height="220" rx="8" fill="#f0fdf4" stroke="#10b981" stroke-width="1.5"/>
    <rect width="560" height="26" rx="8" fill="#059669"/>
    <text x="14" y="17" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#ffffff">Этап 2: Дистилляция Ученика (Student Policy) через историю проприоцепции</text>

    <g transform="translate(14, 38)">
      <!-- Student Input: History Only -->
      <rect x="0" y="0" width="160" height="80" rx="4" fill="#ffffff" stroke="#86efac"/>
      <text x="8" y="16" font-family="Inter" font-size="9" font-weight="700" fill="#166534">История сенсоров H_t:</text>
      <text x="8" y="30" font-family="JetBrains Mono" font-size="8.5" fill="#334155">{s_t, s_t-1, ..., s_t-k}</text>
      <text x="8" y="44" font-family="JetBrains Mono" font-size="8.5" fill="#334155">{a_t-1, ..., a_t-k}</text>
      <text x="8" y="60" font-family="Inter" font-size="8" fill="#64748b">Только реальные энкодеры</text>
      <text x="8" y="72" font-family="Inter" font-size="8" fill="#dc2626">БЕЗ привилегий и карты!</text>

      <!-- Arrow to Student Network -->
      <path d="M 162,40 L 198,40" stroke="#059669" stroke-width="1.5" marker-end="url(#arrow-green)" fill="none"/>

      <!-- Student Architecture (TCN / GRU / MLP + Latent Estimator) -->
      <rect x="200" y="10" width="165" height="110" rx="6" fill="#ffffff" stroke="#059669" stroke-width="1.8"/>
      <text x="282" y="28" text-anchor="middle" font-family="Inter" font-size="10.5" font-weight="700" fill="#166534">Политика Ученика</text>
      
      <!-- Latent Estimator Sub-box -->
      <rect x="210" y="36" width="145" height="34" rx="3" fill="#f0fdf4" stroke="#a7f3d0"/>
      <text x="282" y="49" text-anchor="middle" font-family="Inter" font-size="8.5" font-weight="700" fill="#047857">Эстиматор среды (TCN/GRU)</text>
      <text x="282" y="62" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="#059669">z_t = g(H_t) (скрытый вектор)</text>

      <text x="282" y="86" text-anchor="middle" font-family="JetBrains Mono" font-size="9" fill="#15803d">π_student(a | H_t, z_t)</text>
      <text x="282" y="102" text-anchor="middle" font-family="Inter" font-size="8" fill="#64748b">Клонирование поведения (BC)</text>

      <!-- Arrow to Action -->
      <path d="M 367,65 L 405,65" stroke="#059669" stroke-width="2" marker-end="url(#arrow-green)" fill="none"/>
      <rect x="408" y="45" width="130" height="40" rx="4" fill="#ffffff" stroke="#86efac"/>
      <text x="473" y="61" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#166534">a_student</text>
      <text x="473" y="75" text-anchor="middle" font-family="Inter" font-size="8" fill="#64748b">Команда на моторы</text>

      <!-- Distillation Loss Equation -->
      <rect x="0" y="128" width="538" height="42" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="10" y="145" font-family="Inter" font-size="9" font-weight="700" fill="#0f172a">Функция потерь дистилляции (Supervised Behavioral Cloning):</text>
      <text x="10" y="160" font-family="JetBrains Mono" font-size="9.5" font-weight="700" fill="#7c3aed">ℒ_distill = 𝔼 [ || π_student(H_t) − a_teacher ||² ] + λ · || z_t − z_priv ||²</text>
    </g>
  </g>

  <!-- Distillation Supervision Arrow connecting Stage 1 to Stage 2 -->
  <path d="M 473,182 L 473,260 L 473,322" stroke="#7c3aed" stroke-width="2.2" stroke-dasharray="5,4" marker-end="url(#arrow-purple)" fill="none"/>
  <rect x="424" y="248" width="100" height="22" rx="4" fill="#f5f3ff" stroke="#ddd6fe"/>
  <text x="474" y="262" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="#6d28d9">Учитель обучает</text>

  <!-- Right: Real Robot Hardware (Deployment) -->
  <g transform="translate(610, 70)" filter="url(#shadow)">
    <rect width="322" height="430" rx="8" fill="#f8fafc" stroke="#334155" stroke-width="1.8"/>
    <rect width="322" height="28" rx="8" fill="#1e293b"/>
    <text x="16" y="19" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">Развертывание на реальном роботе</text>

    <g transform="translate(16, 42)" font-family="Inter, sans-serif" font-size="10" fill="#1e293b">
      <rect x="0" y="0" width="290" height="70" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="10" y="18" font-weight="700" fill="#0f172a">Бортовой компьютер (Onboard Edge):</text>
      <text x="10" y="34" fill="#334155">• NVIDIA Jetson Orin Nano / AGX</text>
      <text x="10" y="48" fill="#334155">• Инференс нейросети: &lt; 1 мс (TensorRT)</text>
      <text x="10" y="62" font-weight="700" fill="#059669">• Частота контура: 50–200 Гц</text>

      <g transform="translate(0, 82)">
        <rect x="0" y="0" width="290" height="110" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
        <text x="10" y="18" font-weight="700" fill="#1e40af">Сенсорный поток реального шасси:</text>
        <text x="10" y="34" font-family="JetBrains Mono" font-size="9" fill="#334155">• 12x угловых энкодеров суставов</text>
        <text x="10" y="48" font-family="JetBrains Mono" font-size="9" fill="#334155">• 12x скоростей моторов (q̇)</text>
        <text x="10" y="62" font-family="JetBrains Mono" font-size="9" fill="#334155">• 6-DOF IMU (акселерометр + гироскоп)</text>
        <text x="10" y="76" font-family="JetBrains Mono" font-size="9" fill="#334155">• Буфер 10–20 предыдущих шагов</text>
        <text x="10" y="94" font-size="9" font-weight="700" fill="#2563eb">→ Напрямую на вход Student Policy</text>
      </g>

      <g transform="translate(0, 204)">
        <rect x="0" y="0" width="290" height="96" rx="6" fill="#f0fdf4" stroke="#bbf7d0"/>
        <text x="10" y="18" font-weight="700" fill="#166534">Почему это работает на улице?</text>
        <text x="10" y="34" font-size="9.5" fill="#334155">• Неявная оценка рельефа по отдаче стоп</text>
        <text x="10" y="48" font-size="9.5" fill="#334155">• Domain Randomization в симуляторе</text>
        <text x="10" y="62" font-size="9.5" fill="#334155">• Устойчивость к скользким грунтам и грязи</text>
        <text x="10" y="78" font-size="9" font-weight="700" fill="#047857">Примеры: Слепой паркур ANYmal, Unitree Go2</text>
      </g>

      <g transform="translate(0, 312)">
        <rect x="0" y="0" width="290" height="58" rx="6" fill="#fef2f2" stroke="#fecaca"/>
        <text x="10" y="16" font-weight="700" fill="#991b1b">⚠️ Ограничение дистилляции:</text>
        <text x="10" y="32" font-size="9" fill="#7f1d1d">Ученик не может превзойти учителя;</text>
        <text x="10" y="46" font-size="9" fill="#7f1d1d">требуется достаточная емкость буфера истории H_t</text>
      </g>
    </g>
  </g>

  <!-- Deployment Arrow from Student Output to Real Robot -->
  <path d="M 548,345 L 606,345" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)" fill="none"/>
</svg>'''
    filepath = os.path.join(OUTPUT_DIR, 'teacher_student_sim2real.svg')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {filepath}")

def generate_agent_environment_loop():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 450" width="100%" height="100%">
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#d97706"/>
    </marker>
    <filter id="shadow" x="-3%" y="-4%" width="106%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title -->
  <g transform="translate(28, 28)">
    <text x="0" y="0" font-family="Inter, system-ui, sans-serif" font-size="16.5" font-weight="800" fill="#0f172a">Анатомия RL: Замкнутый цикл взаимодействия Агента и Среды</text>
    <text x="0" y="20" font-family="Inter, system-ui, sans-serif" font-size="11.5" fill="#64748b">Фундаментальный контур: принятие решений на основе обратной связи методом проб и ошибок (Trial and Error)</text>
  </g>

  <!-- Left Box: Agent -->
  <g transform="translate(36, 75)" filter="url(#shadow)">
    <rect width="360" height="260" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
    <rect width="360" height="32" rx="10" fill="#2563eb"/>
    <text x="16" y="21" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="#ffffff">Агент (Agent / Бортовой контроллер)</text>

    <g transform="translate(16, 44)" font-family="Inter, sans-serif" font-size="10.5" fill="#1e293b">
      <!-- Policy component -->
      <rect x="0" y="0" width="328" height="58" rx="6" fill="#ffffff" stroke="#bfdbfe"/>
      <text x="12" y="20" font-weight="700" fill="#1e40af">1. Стратегия / Политика: π_θ(a | s)</text>
      <text x="12" y="36" font-size="9.5" fill="#334155">• Отображает текущее состояние в управляющее действие</text>
      <text x="12" y="50" font-family="JetBrains Mono" font-size="9" fill="#2563eb">aₜ = π_θ(sₜ) (детерминированная) или aₜ ~ π_θ(·|sₜ)</text>

      <!-- Learning Algorithm -->
      <g transform="translate(0, 68)">
        <rect x="0" y="0" width="328" height="58" rx="6" fill="#ffffff" stroke="#bfdbfe"/>
        <text x="12" y="20" font-weight="700" fill="#1e40af">2. Алгоритм обучения (Policy Optimization)</text>
        <text x="12" y="36" font-size="9.5" fill="#334155">• Обновляет веса нейросети θ по градиенту отдачи</text>
        <text x="12" y="50" font-family="JetBrains Mono" font-size="9" fill="#1d4ed8">θ ← θ + α · ∇_θ J(θ) (максимизация суммарной награды)</text>
      </g>

      <!-- Internal Value / Memory -->
      <g transform="translate(0, 136)">
        <rect x="0" y="0" width="328" height="56" rx="6" fill="#ffffff" stroke="#bfdbfe"/>
        <text x="12" y="18" font-weight="700" fill="#1e40af">3. Память / Функция ценности (Value / Critic)</text>
        <text x="12" y="34" font-size="9.5" fill="#334155">• Оценка перспективности текущей ситуации V(s), Q(s,a)</text>
        <text x="12" y="48" font-size="9.5" fill="#64748b">• Буфер опыта 𝒟 = {(s, a, r, s')}</text>
      </g>
    </g>
  </g>

  <!-- Right Box: Environment -->
  <g transform="translate(564, 75)" filter="url(#shadow)">
    <rect width="360" height="260" rx="10" fill="#f8fafc" stroke="#64748b" stroke-width="2"/>
    <rect width="360" height="32" rx="10" fill="#334155"/>
    <text x="16" y="21" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="#ffffff">Среда (Environment: Робот + Физический мир)</text>

    <g transform="translate(16, 44)" font-family="Inter, sans-serif" font-size="10.5" fill="#1e293b">
      <!-- Mechanics & Physics -->
      <rect x="0" y="0" width="328" height="58" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
      <text x="12" y="20" font-weight="700" fill="#0f172a">1. Физическая динамика: P(s' | s, a)</text>
      <text x="12" y="36" font-size="9.5" fill="#334155">• Уравнения движения шасси, контакт стоп с грунтом</text>
      <text x="12" y="50" font-family="JetBrains Mono" font-size="9" fill="#059669">sₜ₊₁ = f(sₜ, aₜ) + шумы, трение, упругость</text>

      <!-- Sensors -->
      <g transform="translate(0, 68)">
        <rect x="0" y="0" width="328" height="58" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
        <text x="12" y="20" font-weight="700" fill="#0f172a">2. Сенсорная подсистема (Observation)</text>
        <text x="12" y="36" font-size="9.5" fill="#334155">• Энкодеры суставов (q, q̇), 6-DOF IMU (акселерометр)</text>
        <text x="12" y="50" font-size="9.5" fill="#475569">• Камеры глубины, тактильные датчики стоп</text>
      </g>

      <!-- Reward Function -->
      <g transform="translate(0, 136)">
        <rect x="0" y="0" width="328" height="56" rx="6" fill="#fffbeb" stroke="#fde68a"/>
        <text x="12" y="18" font-weight="700" fill="#92400e">3. Функция вознаграждения: R(s, a)</text>
        <text x="12" y="34" font-size="9.5" fill="#78350f">• Формирует критерий успеха задачи (Reward Shaping)</text>
        <text x="12" y="48" font-family="JetBrains Mono" font-size="9" fill="#b45309">rₜ₊₁ = + Скорость − w_u ||u||² − Штраф_падения</text>
      </g>
    </g>
  </g>

  <!-- Forward Flow: Action a_t (Top) -->
  <path d="M 396,135 L 560,135" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow-blue)" fill="none"/>
  <rect x="420" y="105" width="120" height="26" rx="5" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="480" y="122" text-anchor="middle" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#1d4ed8">Действие aₜ</text>

  <!-- Backward Flow 1: State / Observation s_{t+1} (Center) -->
  <path d="M 564,225 L 400,225" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" fill="none"/>
  <rect x="410" y="202" width="140" height="24" rx="5" fill="#ecfdf5" stroke="#a7f3d0"/>
  <text x="480" y="218" text-anchor="middle" font-family="JetBrains Mono" font-size="10.5" font-weight="700" fill="#047857">Состояние sₜ₊₁</text>

  <!-- Backward Flow 2: Reward r_{t+1} (Bottom) -->
  <path d="M 564,285 L 400,285" stroke="#d97706" stroke-width="3" marker-end="url(#arrow-amber)" fill="none"/>
  <rect x="420" y="262" width="120" height="24" rx="5" fill="#fffbeb" stroke="#fde68a"/>
  <text x="480" y="278" text-anchor="middle" font-family="JetBrains Mono" font-size="10.5" font-weight="700" fill="#b45309">Награда rₜ₊₁</text>

  <!-- Bottom Key Insight Callout -->
  <g transform="translate(36, 360)">
    <rect width="888" height="68" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="16" y="24" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0f172a">
      Ключевое отличие от Supervised Learning и классического управления:
    </text>
    <text x="16" y="42" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">
      1. <tspan font-weight="700" fill="#2563eb">Нет разметки идеальных действий:</tspan> Никто не сообщает роботу правильный крутящий момент; есть только скалярное подтверждение успеха rₜ₊₁.
    </text>
    <text x="16" y="58" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">
      2. <tspan font-weight="700" fill="#059669">Не требуется аналитическая модель динамики на борту:</tspan> Агент адаптируется к сложным нелинейным контактам через накопленный опыт.
    </text>
  </g>
</svg>'''
    filepath = os.path.join(OUTPUT_DIR, 'agent_environment_loop.svg')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {filepath}")

def generate_credit_assignment_problem():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" width="100%" height="100%">
  <defs>
    <linearGradient id="caBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <filter id="caShadow" x="-3%" y="-4%" width="106%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
    <marker id="caArrowRed" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0,1 L 7,4 L 0,7 Z" fill="#dc2626"/>
    </marker>
    <marker id="caArrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0,1 L 7,4 L 0,7 Z" fill="#059669"/>
    </marker>
    <marker id="caArrowBlue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0,1 L 7,4 L 0,7 Z" fill="#2563eb"/>
    </marker>
  </defs>

  <rect width="100%" height="100%" rx="12" fill="url(#caBg)" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title & Subtitle -->
  <g transform="translate(28, 28)">
    <text x="0" y="0" font-family="Inter, system-ui, sans-serif" font-size="16" font-weight="800" fill="#0f172a">Проблема приписывания заслуг (Credit Assignment Problem)</text>
    <text x="0" y="20" font-family="Inter, system-ui, sans-serif" font-size="11.5" fill="#64748b">Сравнение слепой оценки Монте-Карло в чистом Policy Gradient и локальной TD-ошибки в Actor-Critic</text>
  </g>

  <!-- Section 1: Pure Policy Gradient / REINFORCE (Top) -->
  <g transform="translate(28, 70)" filter="url(#caShadow)">
    <rect width="904" height="195" rx="8" fill="#fef2f2" stroke="#fecaca" stroke-width="1.2"/>
    <rect width="904" height="28" rx="8" fill="#fee2e2"/>
    <text x="14" y="19" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#991b1b">
      1. Чистый Policy Gradient (REINFORCE): Слепая глобальная отдача Монте-Карло G_t
    </text>

    <!-- Timeline Steps -->
    <g transform="translate(24, 48)">
      <!-- Step 1 -->
      <circle cx="40" cy="30" r="14" fill="#dcfce7" stroke="#16a34a" stroke-width="1.8"/>
      <text x="40" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#15803d">t=1</text>
      <text x="40" y="58" text-anchor="middle" font-family="Inter" font-size="9" fill="#166534">Баланс ✓</text>

      <!-- Step 2 -->
      <path d="M 58,30 L 102,30" stroke="#94a3b8" stroke-width="1.5" fill="none"/>
      <circle cx="120" cy="30" r="14" fill="#dcfce7" stroke="#16a34a" stroke-width="1.8"/>
      <text x="120" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#15803d">t=2</text>
      <text x="120" y="58" text-anchor="middle" font-family="Inter" font-size="9" fill="#166534">Шаг ✓</text>

      <!-- Dots -->
      <path d="M 138,30 L 182,30" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" fill="none"/>
      <text x="210" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="14" font-weight="700" fill="#64748b">...</text>
      <path d="M 238,30 L 282,30" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" fill="none"/>

      <!-- Step 99 -->
      <circle cx="300" cy="30" r="14" fill="#dcfce7" stroke="#16a34a" stroke-width="1.8"/>
      <text x="300" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#15803d">t=99</text>
      <text x="300" y="58" text-anchor="middle" font-family="Inter" font-size="9" fill="#166534">Бег 2 м/с ✓</text>

      <!-- Step 100 Fall -->
      <path d="M 318,30 L 372,30" stroke="#ef4444" stroke-width="2" marker-end="url(#caArrowRed)" fill="none"/>
      <circle cx="395" cy="30" r="16" fill="#fee2e2" stroke="#dc2626" stroke-width="2.2"/>
      <text x="395" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="800" fill="#b91c1c">t=100</text>
      <text x="395" y="60" text-anchor="middle" font-family="Inter" font-size="9.5" font-weight="700" fill="#dc2626">Падение ✗</text>

      <!-- Episode Return block -->
      <g transform="translate(450, 10)">
        <rect width="395" height="56" rx="6" fill="#ffffff" stroke="#fca5a5" stroke-width="1.2"/>
        <text x="12" y="20" font-family="Inter" font-size="10.5" font-weight="700" fill="#991b1b">Финал эпизода: штраф за падение r₁₀₀ = -100</text>
        <text x="12" y="36" font-family="JetBrains Mono" font-size="10" fill="#dc2626">G₀ = ∑ γᵗ rₜ = -86.4 (отрицательная отдача)</text>
        <text x="12" y="49" font-family="Inter" font-size="9" fill="#7f1d1d">Градиент: ∇_θ J = 𝔼 [ ∑ ∇ log π(aₜ|sₜ) · Gₜ ]</text>
      </g>

      <!-- Red Feedback Penalty Arrow sweeping backwards across ALL steps -->
      <g transform="translate(10, 78)">
        <path d="M 400,10 L 40,10" stroke="#dc2626" stroke-width="2.5" marker-end="url(#caArrowRed)" fill="none" stroke-dasharray="6,3"/>
        <rect x="75" y="0" width="290" height="20" rx="4" fill="#fee2e2" stroke="#f87171"/>
        <text x="220" y="14" text-anchor="middle" font-family="Inter" font-size="9.5" font-weight="700" fill="#b91c1c">
          Штраф G_t &lt; 0 подавляет ВСЕ 100 шагов подряд!
        </text>
        <text x="15" y="36" font-family="Inter" font-size="10" fill="#7f1d1d">
          <tspan font-weight="700">Катастрофа дисперсии:</tspan> Агент разучивается делать идеальные шаги 1–99 из-за единственной кочки на шаге 100.
        </text>
      </g>
    </g>
  </g>

  <!-- Section 2: Actor-Critic with Advantage / TD Error (Bottom) -->
  <g transform="translate(28, 285)" filter="url(#caShadow)">
    <rect width="904" height="205" rx="8" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.2"/>
    <rect width="904" height="28" rx="8" fill="#dcfce7"/>
    <text x="14" y="19" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#166534">
      2. Архитектура Actor-Critic: Локальное приписывание заслуг через TD-ошибку δ_t (Advantage)
    </text>

    <!-- Timeline Steps -->
    <g transform="translate(24, 48)">
      <!-- Step 1 Local TD -->
      <circle cx="40" cy="30" r="14" fill="#ffffff" stroke="#16a34a" stroke-width="1.8"/>
      <text x="40" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#15803d">t=1</text>
      <path d="M 40,48 L 40,64" stroke="#16a34a" stroke-width="2" marker-end="url(#caArrowGreen)" fill="none"/>
      <text x="40" y="78" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#15803d">δ₁ &gt; 0 (+)</text>

      <!-- Step 2 Local TD -->
      <path d="M 58,30 L 102,30" stroke="#94a3b8" stroke-width="1.5" fill="none"/>
      <circle cx="120" cy="30" r="14" fill="#ffffff" stroke="#16a34a" stroke-width="1.8"/>
      <text x="120" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#15803d">t=2</text>
      <path d="M 120,48 L 120,64" stroke="#16a34a" stroke-width="2" marker-end="url(#caArrowGreen)" fill="none"/>
      <text x="120" y="78" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#15803d">δ₂ &gt; 0 (+)</text>

      <!-- Dots -->
      <path d="M 138,30 L 182,30" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" fill="none"/>
      <text x="210" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="14" font-weight="700" fill="#64748b">...</text>
      <path d="M 238,30 L 282,30" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" fill="none"/>

      <!-- Step 99 Local TD -->
      <circle cx="300" cy="30" r="14" fill="#ffffff" stroke="#16a34a" stroke-width="1.8"/>
      <text x="300" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="700" fill="#15803d">t=99</text>
      <path d="M 300,48 L 300,64" stroke="#16a34a" stroke-width="2" marker-end="url(#caArrowGreen)" fill="none"/>
      <text x="300" y="78" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="#15803d">δ₉₉ &gt; 0 (+)</text>

      <!-- Step 100 Fall Local TD -->
      <path d="M 318,30 L 372,30" stroke="#ef4444" stroke-width="2" marker-end="url(#caArrowRed)" fill="none"/>
      <circle cx="395" cy="30" r="16" fill="#fee2e2" stroke="#dc2626" stroke-width="2.2"/>
      <text x="395" y="34" text-anchor="middle" font-family="JetBrains Mono" font-size="10" font-weight="800" fill="#b91c1c">t=100</text>
      <path d="M 395,50 L 395,66" stroke="#dc2626" stroke-width="2.5" marker-end="url(#caArrowRed)" fill="none"/>
      <text x="395" y="80" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" font-weight="800" fill="#b91c1c">δ₁₀₀ ≪ 0 (-)</text>

      <!-- Critic Explanation Box -->
      <g transform="translate(450, 10)">
        <rect width="395" height="66" rx="6" fill="#ffffff" stroke="#86efac" stroke-width="1.2"/>
        <text x="12" y="18" font-family="Inter" font-size="10.5" font-weight="700" fill="#166534">Критик оценивает каждый шаг локально (TD-ошибка):</text>
        <text x="12" y="35" font-family="JetBrains Mono" font-size="10" fill="#15803d">δₜ = rₜ₊₁ + γ V_ϕ(sₜ₊₁) - V_ϕ(sₜ)</text>
        <text x="12" y="50" font-family="Inter" font-size="9.5" fill="#334155">Шаги 1–99: результат не хуже ожиданий ⇒ <tspan font-weight="700" fill="#16a34a">δₜ ≥ 0 (поощрение)</tspan></text>
        <text x="12" y="62" font-family="Inter" font-size="9.5" fill="#334155">Шаг 100: внезапный срыв траектории ⇒ <tspan font-weight="700" fill="#dc2626">δ₁₀₀ &lt; 0 (точечный штраф)</tspan></text>
      </g>

      <!-- Bottom takeaway -->
      <g transform="translate(10, 96)">
        <rect width="840" height="26" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
        <text x="12" y="17" font-family="Inter" font-size="10" fill="#1e293b">
          💡 <tspan font-weight="700" fill="#047857">Точечное обучение:</tspan> Актор закрепляет успешные шаги бега (1–99) и пенализирует <tspan font-weight="700" fill="#b91c1c">исключительно ошибку на шаге 100</tspan>. Дисперсия снижена на порядки!
        </text>
      </g>
    </g>
  </g>
</svg>'''
    filepath = os.path.join(OUTPUT_DIR, 'credit_assignment_problem.svg')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {filepath}")

def generate_continuous_action_barrier():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" width="100%" height="100%">
  <defs>
    <linearGradient id="cabBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <filter id="cabShadow" x="-3%" y="-4%" width="106%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" rx="12" fill="url(#cabBg)" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Title & Subtitle -->
  <g transform="translate(28, 28)">
    <text x="0" y="0" font-family="Inter, system-ui, sans-serif" font-size="16" font-weight="800" fill="#0f172a">Барьер непрерывного действия в Value-Based методах</text>
    <text x="0" y="20" font-family="Inter, system-ui, sans-serif" font-size="11.5" fill="#64748b">Почему классический Q-Learning / DQN терпит неудачу в реальном управлении приводами роботов</text>
  </g>

  <!-- Left: Discrete Action Space (DQN Success) -->
  <g transform="translate(28, 70)" filter="url(#cabShadow)">
    <rect width="436" height="375" rx="8" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
    <rect width="436" height="30" rx="8" fill="#059669"/>
    <text x="14" y="20" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">
      Дискретные действия (Atari / GridWorld) — DQN работает
    </text>

    <g transform="translate(16, 46)">
      <text x="0" y="14" font-family="Inter" font-size="11" font-weight="700" fill="#166534">Пространство действий конечно: |A| = 4 кнопки</text>
      <text x="0" y="30" font-family="JetBrains Mono" font-size="10" fill="#334155">A = { Влево, Вправо, Прыжок, Огонь }</text>

      <!-- Architecture Box -->
      <rect x="0" y="44" width="404" height="110" rx="6" fill="#ffffff" stroke="#bbf7d0"/>
      <text x="12" y="64" font-family="Inter" font-size="10.5" font-weight="700" fill="#1e293b">Архитектура сети DQN:</text>
      <text x="12" y="82" font-family="JetBrains Mono" font-size="10" fill="#2563eb">Вход: Состояние s (кадр пикселей 84×84)</text>
      <text x="12" y="100" font-family="JetBrains Mono" font-size="10" fill="#059669">Выход: 4 числа [Q(s, a₁), Q(s, a₂), Q(s, a₃), Q(s, a₄)]</text>
      <text x="12" y="130" font-family="Inter" font-size="9.5" fill="#475569">Сеть за один прямой проход вычисляет ценность ВСЕХ действий.</text>

      <!-- Argmax Evaluation Box -->
      <g transform="translate(0, 168)">
        <rect width="404" height="66" rx="6" fill="#ecfdf5" stroke="#6ee7b7"/>
        <text x="12" y="20" font-family="Inter" font-size="10.5" font-weight="700" fill="#065f46">Операция выбора оптимального действия:</text>
        <text x="12" y="40" font-family="JetBrains Mono" font-size="12" font-weight="800" fill="#047857">a* = argmax_a Q(s, a)  ⇒  O(|A|) = 4 операции</text>
        <text x="12" y="56" font-family="Inter" font-size="9.5" fill="#065f46">Выполняется за 0.001 мс (банальный поиск max в массиве из 4 чисел).</text>
      </g>

      <!-- Verdict Box -->
      <g transform="translate(0, 248)">
        <rect width="404" height="64" rx="6" fill="#ffffff" stroke="#a7f3d0"/>
        <text x="12" y="20" font-family="Inter" font-size="10.5" font-weight="700" fill="#15803d">✅ Итог для дискретных задач:</text>
        <text x="12" y="38" font-family="Inter" font-size="9.5" fill="#334155">Критик одновременно служит регулятором. Выбор действия детерминирован и вычислительно бесплатен.</text>
      </g>
    </g>
  </g>

  <!-- Right: Continuous Action Space (Robotics Failure of pure argmax) -->
  <g transform="translate(496, 70)" filter="url(#cabShadow)">
    <rect width="436" height="375" rx="8" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.5"/>
    <rect width="436" height="30" rx="8" fill="#dc2626"/>
    <text x="14" y="20" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">
      Непрерывные действия (Робототехника) — Тупик DQN
    </text>

    <g transform="translate(16, 46)">
      <text x="0" y="14" font-family="Inter" font-size="11" font-weight="700" fill="#991b1b">Пространство действий непрерывно: a ∈ ℝ¹²</text>
      <text x="0" y="30" font-family="JetBrains Mono" font-size="10" fill="#334155">12 суставов: τ_i ∈ [-30, +30] Н·м (бесконечность)</text>

      <!-- Architecture Box -->
      <rect x="0" y="44" width="404" height="110" rx="6" fill="#ffffff" stroke="#fecaca"/>
      <text x="12" y="64" font-family="Inter" font-size="10.5" font-weight="700" fill="#1e293b">Что вычисляет Q-сеть в непрерывном случае?</text>
      <text x="12" y="82" font-family="JetBrains Mono" font-size="10" fill="#2563eb">Вход: Состояние s + вектор моментов a ∈ ℝ¹²</text>
      <text x="12" y="100" font-family="JetBrains Mono" font-size="10" fill="#dc2626">Выход: ОДНО скалярное число Q(s, a) ∈ ℝ</text>
      <text x="12" y="130" font-family="Inter" font-size="9.5" fill="#7f1d1d">Сеть НЕ МОЖЕТ выдать все Q сразу — их бесконечно много!</text>

      <!-- Argmax Evaluation Box -->
      <g transform="translate(0, 168)">
        <rect width="404" height="66" rx="6" fill="#fee2e2" stroke="#f87171"/>
        <text x="12" y="20" font-family="Inter" font-size="10.5" font-weight="700" fill="#991b1b">Проблема вычисления argmax на борту робота:</text>
        <text x="12" y="38" font-family="JetBrains Mono" font-size="11" font-weight="800" fill="#b91c1c">a* = argmax_{a ∈ ℝ¹²} Q(s, a)  ⇒  Нелинейная NLP!</text>
        <text x="12" y="56" font-family="Inter" font-size="9.5" fill="#7f1d1d">Численный градиентный поиск оптимума требует 50–200 мс (лимит 2 мс!).</text>
      </g>

      <!-- Discrete Grid Explosion Box -->
      <g transform="translate(0, 248)">
        <rect width="404" height="64" rx="6" fill="#ffffff" stroke="#fca5a5"/>
        <text x="12" y="18" font-family="Inter" font-size="10" font-weight="700" fill="#991b1b">Дискретизация моторов (всего по 5 точек на сустав):</text>
        <text x="12" y="34" font-family="JetBrains Mono" font-size="10.5" font-weight="700" fill="#b91c1c">5¹² = 244 140 625 комбинаций на каждом шаге!</text>
        <text x="12" y="52" font-family="Inter" font-size="9.5" font-weight="700" fill="#15803d">💡 Решение: Нужна сеть Актора π_θ(s) → a (инференс 0.2 мс)!</text>
      </g>
    </g>
  </g>
</svg>'''
    filepath = os.path.join(OUTPUT_DIR, 'continuous_action_barrier.svg')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {filepath}")

if __name__ == '__main__':
    print("=== Generating Lecture 06 SVGs ===")
    generate_agent_environment_loop()
    generate_rl_taxonomy()
    generate_dqn_architecture()
    generate_actor_critic_architecture()
    generate_teacher_student_sim2real()
    generate_credit_assignment_problem()
    generate_continuous_action_barrier()
    print("=== Lecture 06 SVGs Successfully Generated ===")
