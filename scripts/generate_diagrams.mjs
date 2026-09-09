import fs from 'fs';
import path from 'path';

const svgFiles = {
  // --- LECTURE 01 ---
  'assets/images/lecture-01/minkowski_cspace.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g transform="translate(40, 30)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">1. Рабочее пространство W</text>
    <polygon points="60,60 160,50 200,130 110,160 40,110" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="95" y="110" font-family="Inter" font-size="12" font-weight="600" fill="#b91c1c">Препятствие O</text>
    <rect x="180" y="170" width="46" height="30" rx="3" fill="#dbeafe" stroke="#2563eb" stroke-width="2" transform="rotate(25, 203, 185)"/>
    <circle cx="203" cy="185" r="3" fill="#2563eb"/>
    <line x1="203" y1="185" x2="228" y2="196" stroke="#2563eb" stroke-width="2"/>
    <text x="160" y="235" font-family="Inter" font-size="12" font-weight="600" fill="#1d4ed8">Робот A(q) (размер &gt; 0)</text>
  </g>
  <g transform="translate(320, 140)">
    <path d="M0,15 L45,15 M35,7 L47,15 L35,23" stroke="#0284c7" stroke-width="3" fill="none" stroke-linecap="round"/>
    <text x="-15" y="-5" font-family="JetBrains Mono" font-size="13" fill="#0284c7">C_obs = O ⊕ (-A(0))</text>
    <text x="-5" y="40" font-family="Inter" font-size="12" fill="#475569">Сумма Минковского</text>
  </g>
  <g transform="translate(420, 30)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">2. Пространство C-space (срез θ)</text>
    <polygon points="40,40 180,30 230,140 130,190 20,120" fill="#fecaca" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 2"/>
    <polygon points="60,60 160,50 200,130 110,160 40,110" fill="#fee2e2" stroke="#f87171" stroke-width="1.5"/>
    <text x="80" y="110" font-family="Inter" font-size="12" font-weight="600" fill="#991b1b">C_obs (Раздутие)</text>
    <circle cx="195" cy="205" r="5" fill="#059669"/>
    <text x="165" y="230" font-family="Inter" font-size="12" font-weight="600" fill="#047857">Точка q ∈ C_free</text>
    <path d="M15,220 Q120,225 195,205 T240,100" stroke="#059669" stroke-width="2.5" fill="none" stroke-dasharray="3 3"/>
    <text x="15" y="245" font-family="Inter" font-size="12" fill="#475569">Безопасный путь точки</text>
  </g>
</svg>`,

  'assets/images/lecture-01/traversability_layers.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="32" font-family="Inter" font-size="15" font-weight="700" fill="#0f172a">Три фундаментальных уровня анализа проходимости (Traversability)</text>
  <g transform="translate(30, 60)">
    <rect width="200" height="225" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <rect width="200" height="32" rx="8" fill="#3b82f6"/>
    <text x="12" y="21" font-family="Inter" font-size="13" font-weight="700" fill="#ffffff">1. Геометрическая</text>
    <g transform="translate(14, 52)">
      <text x="0" y="0" font-family="Inter" font-size="11.5" fill="#334155">• Дорожный просвет (клиренс)</text>
      <text x="0" y="24" font-family="Inter" font-size="11.5" fill="#334155">• Угол въезда/съезда (Approach)</text>
      <text x="0" y="48" font-family="Inter" font-size="11.5" fill="#334155">• Предельный уклон: slope &lt; θ_max</text>
      <text x="0" y="72" font-family="Inter" font-size="11.5" fill="#334155">• Предельный шаг: h &#8804; h_step</text>
      <text x="0" y="96" font-family="Inter" font-size="11.5" fill="#334155">• Сенсоры: 3D LiDAR, ESDF, 2.5D</text>
      <rect x="0" y="115" width="172" height="42" rx="4" fill="#dbeafe"/>
      <text x="8" y="132" font-family="JetBrains Mono" font-size="11" fill="#1e40af">Критерий: геометрия</text>
      <text x="8" y="147" font-family="JetBrains Mono" font-size="11" fill="#1e40af">шасси не касается скал</text>
    </g>
  </g>
  <g transform="translate(250, 60)">
    <rect width="200" height="225" rx="8" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
    <rect width="200" height="32" rx="8" fill="#eab308"/>
    <text x="12" y="21" font-family="Inter" font-size="13" font-weight="700" fill="#ffffff">2. Опорная (Террамеханика)</text>
    <g transform="translate(14, 52)">
      <text x="0" y="0" font-family="Inter" font-size="11.5" fill="#334155">• Коэффициент трения μ (лед, песок)</text>
      <text x="0" y="24" font-family="Inter" font-size="11.5" fill="#334155">• Несущая способность грунта</text>
      <text x="0" y="48" font-family="Inter" font-size="11.5" fill="#334155">• Провал колес в грунт (sinkage)</text>
      <text x="0" y="72" font-family="Inter" font-size="11.5" fill="#334155">• Проскальзывание (wheel slip)</text>
      <text x="0" y="96" font-family="Inter" font-size="11.5" fill="#334155">• Модель Беккера-Вонга</text>
      <rect x="0" y="115" width="172" height="42" rx="4" fill="#fef08a"/>
      <text x="8" y="132" font-family="JetBrains Mono" font-size="11" fill="#854d0e">Критерий: передача</text>
      <text x="8" y="147" font-family="JetBrains Mono" font-size="11" fill="#854d0e">тяги без пробуксовки</text>
    </g>
  </g>
  <g transform="translate(470, 60)">
    <rect width="200" height="225" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
    <rect width="200" height="32" rx="8" fill="#22c55e"/>
    <text x="12" y="21" font-family="Inter" font-size="13" font-weight="700" fill="#ffffff">3. Семантическая</text>
    <g transform="translate(14, 52)">
      <text x="0" y="0" font-family="Inter" font-size="11.5" fill="#334155">• Классификация поверхностей:</text>
      <text x="0" y="24" font-family="Inter" font-size="11.5" fill="#334155">  - Асфальт: Cost = 1.0 (норма)</text>
      <text x="0" y="48" font-family="Inter" font-size="11.5" fill="#334155">  - Трава: Cost = 1.3 (безопасно)</text>
      <text x="0" y="72" font-family="Inter" font-size="11.5" fill="#334155">  - Лужи/грязь: Cost = 8.0 (риск)</text>
      <text x="0" y="96" font-family="Inter" font-size="11.5" fill="#334155">• Правила ПДД / зоны пешеходов</text>
      <rect x="0" y="115" width="172" height="42" rx="4" fill="#bbf7d0"/>
      <text x="8" y="132" font-family="JetBrains Mono" font-size="11" fill="#166534">Критерий: назначение</text>
      <text x="8" y="147" font-family="JetBrains Mono" font-size="11" fill="#166534">штрафов от нейросети</text>
    </g>
  </g>
</svg>`,

  'assets/images/lecture-01/sdf_gradient.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g transform="translate(40, 30)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Евклидово поле расстояний (ESDF) и изолинии</text>
    <ellipse cx="140" cy="140" rx="120" ry="90" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5" stroke-dasharray="4 2"/>
    <ellipse cx="140" cy="140" rx="95" ry="70" fill="#e0f2fe" stroke="#7dd3fc" stroke-width="1.5" stroke-dasharray="4 2"/>
    <ellipse cx="140" cy="140" rx="70" ry="50" fill="#bae6fd" stroke="#38bdf8" stroke-width="2"/>
    <ellipse cx="140" cy="140" rx="45" ry="30" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
    <text x="110" y="145" font-family="Inter" font-size="12" font-weight="700" fill="#ffffff">Преграда</text>
    <text x="140" y="98" font-family="JetBrains Mono" font-size="12" fill="#0284c7">SDF = +1.0</text>
    <text x="140" y="78" font-family="JetBrains Mono" font-size="12" fill="#0284c7">SDF = +2.0</text>
    <text x="140" y="58" font-family="JetBrains Mono" font-size="12" fill="#0284c7">SDF = +3.0</text>
  </g>
  <g transform="translate(370, 30)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Градиент ∇ESDF: непрерывные силы отталкивания</text>
    <ellipse cx="150" cy="140" rx="45" ry="30" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="120" y="145" font-family="Inter" font-size="12" font-weight="700" fill="#991b1b">Преграда</text>
    <path d="M150,110 L150,60 M145,70 L150,55 L155,70" stroke="#0284c7" stroke-width="2.5" fill="#0284c7"/>
    <path d="M195,140 L255,140 M245,135 L260,140 L245,145" stroke="#0284c7" stroke-width="2.5" fill="#0284c7"/>
    <path d="M150,170 L150,220 M145,210 L150,225 L155,210" stroke="#0284c7" stroke-width="2.5" fill="#0284c7"/>
    <path d="M105,140 L45,140 M55,135 L40,140 L55,145" stroke="#0284c7" stroke-width="2.5" fill="#0284c7"/>
    <text x="50" y="255" font-family="JetBrains Mono" font-size="12" fill="#0284c7">F_rep(x) = -∇ESDF(x) / ||∇ESDF||</text>
    <text x="50" y="275" font-family="Inter" font-size="12" fill="#475569">Используется в nvblox, CHOMP и NMPC</text>
  </g>
</svg>`,

  // --- LECTURE 02 ---
  'assets/images/lecture-02/visibility_vs_voronoi.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g transform="translate(30, 25)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Граф видимости (Visibility Graph)</text>
    <polygon points="50,60 110,40 90,110 40,100" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
    <polygon points="180,90 250,70 240,140 170,130" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
    <line x1="20" y1="140" x2="40" y2="100" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2"/>
    <line x1="20" y1="140" x2="90" y2="110" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2"/>
    <line x1="110" y1="40" x2="180" y2="90" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2"/>
    <line x1="90" y1="110" x2="170" y2="130" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2"/>
    <path d="M20,140 L40,100 L110,40 L250,70 L280,130" stroke="#2563eb" stroke-width="3" fill="none"/>
    <circle cx="20" cy="140" r="4" fill="#16a34a"/>
    <circle cx="280" cy="130" r="4" fill="#dc2626"/>
    <text x="0" y="210" font-family="Inter" font-size="12" font-weight="600" fill="#1e40af">✓ Минимальная длина пути</text>
    <text x="0" y="230" font-family="Inter" font-size="11" fill="#dc2626">✗ Прижимается вплотную к углам (риск коллизии!)</text>
  </g>
  <line x1="350" y1="20" x2="350" y2="300" stroke="#e2e8f0" stroke-width="2"/>
  <g transform="translate(380, 25)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Диаграмма Вороного (Voronoi / GVD)</text>
    <polygon points="50,60 110,40 90,110 40,100" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
    <polygon points="180,90 250,70 240,140 170,130" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>
    <path d="M20,70 Q140,95 140,20 M140,95 Q140,150 140,200 M140,95 Q210,110 280,40 M140,150 Q210,160 280,200" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3" fill="none"/>
    <path d="M20,140 Q80,145 140,150 Q175,155 240,180 L280,130" stroke="#059669" stroke-width="3" fill="none"/>
    <circle cx="20" cy="140" r="4" fill="#16a34a"/>
    <circle cx="280" cy="130" r="4" fill="#dc2626"/>
    <text x="0" y="210" font-family="Inter" font-size="12" font-weight="600" fill="#047857">✓ Максимальный запас безопасности (клиренс)</text>
    <text x="0" y="230" font-family="Inter" font-size="11" fill="#64748b">✗ Неоптимален по длине (удлинение на 15–30%)</text>
  </g>
</svg>`,

  'assets/images/lecture-02/theta_star_los.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g transform="translate(40, 25)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Классический A* (привязка к сетке)</text>
    <path d="M20,30 H260 M20,60 H260 M20,90 H260 M20,120 H260 M20,150 H260 M20,180 H260" stroke="#e2e8f0" stroke-width="1"/>
    <path d="M20,30 V180 M60,30 V180 M100,30 V180 M140,30 V180 M180,30 V180 M220,30 V180 M260,30 V180" stroke="#e2e8f0" stroke-width="1"/>
    <rect x="100" y="60" width="40" height="60" fill="#ef4444" opacity="0.8"/>
    <rect x="140" y="90" width="40" height="60" fill="#ef4444" opacity="0.8"/>
    <path d="M60,150 L100,150 L140,150 L180,150 L220,120 L220,60" stroke="#dc2626" stroke-width="3" fill="none"/>
    <circle cx="60" cy="150" r="4" fill="#16a34a"/>
    <circle cx="220" cy="60" r="4" fill="#2563eb"/>
    <text x="0" y="210" font-family="Inter" font-size="12" font-weight="600" fill="#dc2626">Ступенчатые зигзаги (45° и 90°)</text>
    <text x="0" y="230" font-family="Inter" font-size="12" fill="#475569">Длина: L = 3·1.0 + √2 + 2·1.0 = 6.41</text>
  </g>
  <g transform="translate(380, 25)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Сглаженный Theta* (Any-Angle)</text>
    <path d="M20,30 H260 M20,60 H260 M20,90 H260 M20,120 H260 M20,150 H260 M20,180 H260" stroke="#e2e8f0" stroke-width="1"/>
    <path d="M20,30 V180 M60,30 V180 M100,30 V180 M140,30 V180 M180,30 V180 M220,30 V180 M260,30 V180" stroke="#e2e8f0" stroke-width="1"/>
    <rect x="100" y="60" width="40" height="60" fill="#ef4444" opacity="0.8"/>
    <rect x="140" y="90" width="40" height="60" fill="#ef4444" opacity="0.8"/>
    <line x1="60" y1="150" x2="220" y2="60" stroke="#059669" stroke-width="1.5" stroke-dasharray="3 3"/>
    <path d="M60,150 L100,150 L220,60" stroke="#059669" stroke-width="3.5" fill="none"/>
    <circle cx="60" cy="150" r="4" fill="#16a34a"/>
    <circle cx="220" cy="60" r="4" fill="#2563eb"/>
    <text x="0" y="210" font-family="Inter" font-size="12" font-weight="600" fill="#059669">Прямая срезка через LineOfSight()</text>
    <text x="0" y="230" font-family="Inter" font-size="12" fill="#475569">Длина: L = 1.0 + √(3² + 3²) = 5.24 (-18% пути!)</text>
  </g>
</svg>`,

  // --- LECTURE 03 ---
  'assets/images/lecture-03/rrt_star_rewire.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g transform="translate(40, 25)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">1. Выбор лучшего родителя (ChooseParent)</text>
    <circle cx="140" cy="120" r="75" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="4 2"/>
    <text x="145" y="55" font-family="JetBrains Mono" font-size="12" fill="#0284c7">Радиус r_N</text>
    <circle cx="80" cy="140" r="5" fill="#334155"/><text x="60" y="160" font-family="Inter" font-size="11" fill="#475569">u_1 (c=12)</text>
    <circle cx="120" cy="80" r="5" fill="#334155"/><text x="100" y="70" font-family="Inter" font-size="11" fill="#475569">u_2 (c=8)</text>
    <circle cx="180" cy="150" r="5" fill="#334155"/><text x="185" y="165" font-family="Inter" font-size="11" fill="#475569">u_3 (c=15)</text>
    <circle cx="140" cy="120" r="6" fill="#16a34a"/>
    <text x="150" y="125" font-family="Inter" font-size="12" font-weight="700" fill="#16a34a">q_new</text>
    <line x1="120" y1="80" x2="140" y2="120" stroke="#16a34a" stroke-width="3"/>
    <text x="0" y="225" font-family="Inter" font-size="12" font-weight="600" fill="#0f172a">cost(u_2) + dist(u_2, q_new) = минимум</text>
    <text x="0" y="245" font-family="Inter" font-size="12" fill="#475569">Родителем назначается узел u_2</text>
  </g>
  <g transform="translate(380, 25)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">2. Переподключение соседей (Rewiring)</text>
    <circle cx="140" cy="120" r="75" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4 2"/>
    <circle cx="80" cy="140" r="5" fill="#334155"/>
    <circle cx="140" cy="120" r="6" fill="#16a34a"/>
    <circle cx="180" cy="150" r="5" fill="#334155"/><text x="185" y="170" font-family="Inter" font-size="11" fill="#475569">v (было c=15)</text>
    <line x1="195" y1="210" x2="180" y2="150" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3 3"/>
    <text x="195" y="215" font-family="Inter" font-size="10" fill="#ef4444">✕ старое ребро</text>
    <line x1="140" y1="120" x2="180" y2="150" stroke="#059669" stroke-width="3"/>
    <text x="0" y="225" font-family="Inter" font-size="12" font-weight="600" fill="#047857">cost(q_new) + dist(q_new, v) &lt; cost(v)</text>
    <text x="0" y="245" font-family="Inter" font-size="12" fill="#475569">Родитель v меняется на q_new: стоимость c=11</text>
  </g>
</svg>`,

  // --- LECTURE 04 ---
  'assets/images/lecture-04/apf_u_trap.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <g transform="translate(40, 25)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">1. Патология Хатиба: U-образная ловушка</text>
    <circle cx="150" cy="40" r="10" fill="#22c55e"/>
    <text x="135" y="20" font-family="Inter" font-size="12" font-weight="700" fill="#15803d">Цель (Goal)</text>
    <path d="M70,70 V150 H230 V70 H200 V125 H100 V70 Z" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <circle cx="150" cy="115" r="7" fill="#0284c7"/>
    <text x="120" y="105" font-family="Inter" font-size="11" font-weight="600" fill="#0369a1">Робот q</text>
    <line x1="150" y1="115" x2="150" y2="75" stroke="#2563eb" stroke-width="3"/>
    <polygon points="146,80 150,70 154,80" fill="#2563eb"/>
    <text x="156" y="85" font-family="Inter" font-size="11" font-weight="600" fill="#2563eb">F_att (к цели)</text>
    <line x1="150" y1="115" x2="150" y2="150" stroke="#dc2626" stroke-width="3"/>
    <polygon points="146,145 150,155 154,145" fill="#dc2626"/>
    <text x="156" y="145" font-family="Inter" font-size="11" font-weight="600" fill="#dc2626">F_rep (от дна)</text>
    <rect x="20" y="215" width="260" height="40" rx="4" fill="#fef2f2" stroke="#fecaca"/>
    <text x="30" y="235" font-family="JetBrains Mono" font-size="12" fill="#dc2626" font-weight="700">F_net = F_att + F_rep = 0</text>
    <text x="30" y="248" font-family="Inter" font-size="11" fill="#475569">Робот застревает в локальном минимуме!</text>
  </g>
  <g transform="translate(370, 25)">
    <text x="0" y="0" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">2. Решение: Гармоническое поле (ETH Zürich)</text>
    <circle cx="160" cy="40" r="10" fill="#22c55e"/>
    <text x="135" y="20" font-family="Inter" font-size="12" font-weight="700" fill="#15803d">U(goal) = 0</text>
    <path d="M80,70 V150 H240 V70 H210 V125 H110 V70 Z" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="135" y="145" font-family="Inter" font-size="11" fill="#b91c1c">U(obs) = 1</text>
    <path d="M160,115 Q130,115 100,165 Q80,200 60,120 Q50,40 150,40" stroke="#059669" stroke-width="2.5" fill="none"/>
    <path d="M160,115 Q190,115 220,165 Q240,200 260,120 Q270,40 170,40" stroke="#059669" stroke-width="2.5" fill="none"/>
    <rect x="20" y="215" width="280" height="50" rx="4" fill="#f0fdf4" stroke="#bbf7d0"/>
    <text x="30" y="233" font-family="JetBrains Mono" font-size="12" font-weight="700" fill="#166534">ΔU = ∇²U = 0 (Уравнение Лапласа)</text>
    <text x="30" y="250" font-family="Inter" font-size="11" fill="#475569">Принцип максимума: нет минимумов внутри!</text>
  </g>
</svg>`,

  'assets/images/lecture-04/dwa_space.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="26" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Dynamic Window Approach (DWA): Поиск в пространстве (v, ω)</text>
  <g transform="translate(40, 50)">
    <!-- Axes v and omega -->
    <line x1="20" y1="120" x2="280" y2="120" stroke="#94a3b8" stroke-width="1.5"/>
    <line x1="40" y1="20" x2="40" y2="220" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="270" y="140" font-family="JetBrains Mono" font-size="12" fill="#475569">v (м/с)</text>
    <text x="15" y="25" font-family="JetBrains Mono" font-size="12" fill="#475569">ω (рад/с)</text>

    <!-- Vs: Hardware Limits -->
    <rect x="40" y="40" width="220" height="160" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="200" y="55" font-family="Inter" font-size="11" fill="#64748b">Vs (пределы шасси)</text>

    <!-- Vd: Dynamic Window -->
    <rect x="100" y="80" width="100" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="105" y="98" font-family="Inter" font-size="11" font-weight="600" fill="#0369a1">Vd (окно ускорений τ)</text>

    <!-- Va: Admissible velocities (obstacle parabolic bound) -->
    <path d="M40,20 Q160,50 180,120 Q160,190 40,220 Z" fill="#fee2e2" opacity="0.4"/>
    <path d="M40,20 Q160,50 180,120 Q160,190 40,220" stroke="#ef4444" stroke-width="2" fill="none"/>
    <text x="70" y="195" font-family="Inter" font-size="11" fill="#dc2626">Зона столкновения</text>

    <!-- Optimal velocity sample -->
    <circle cx="165" cy="105" r="6" fill="#16a34a"/>
    <text x="175" y="110" font-family="Inter" font-size="12" font-weight="700" fill="#16a34a">(v*, ω*)</text>
  </g>
  <g transform="translate(360, 60)">
    <rect width="300" height="190" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="26" font-family="Inter" font-size="13" font-weight="700" fill="#0f172a">Пересечение 3-х пространств:</text>
    <text x="15" y="52" font-family="JetBrains Mono" font-size="12" fill="#0284c7">Vr = Vs ∩ Vd ∩ Va</text>
    <g transform="translate(15, 75)">
      <text x="0" y="0" font-family="Inter" font-size="11.5" fill="#334155">• Vs: конструктивные скорости шасси</text>
      <text x="0" y="22" font-family="Inter" font-size="11.5" fill="#334155">• Vd: скорости за квант времени τ</text>
      <text x="0" y="44" font-family="Inter" font-size="11.5" fill="#334155">• Va: скорости безопасного торможения</text>
      <text x="0" y="66" font-family="Inter" font-size="11.5" font-weight="600" fill="#16a34a">• Выбор максимума функции G(v, ω)</text>
      <text x="0" y="86" font-family="Inter" font-size="11" fill="#64748b">  G = α·heading + β·dist + γ·vel</text>
    </g>
  </g>
</svg>`,

  // --- LECTURE 05 ---
  'assets/images/lecture-05/dubins_words.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="28" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">6 канонических слов автомобиля Дубинса (LaValle гл. 15): LSL, RSR, LSR, RSL, LRL, RLR</text>
  <g transform="translate(40, 50)">
    <rect width="190" height="110" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="20" font-family="Inter" font-size="13" font-weight="700" fill="#0284c7">1. Слово LSL</text>
    <circle cx="50" cy="70" r="25" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2" fill="none"/>
    <circle cx="140" cy="70" r="25" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2" fill="none"/>
    <path d="M40,90 A25,25 0 0,1 50,45 L140,45 A25,25 0 0,1 160,85" stroke="#2563eb" stroke-width="2.5" fill="none"/>
    <circle cx="40" cy="90" r="3" fill="#16a34a"/>
    <circle cx="160" cy="85" r="3" fill="#dc2626"/>
    <text x="15" y="100" font-family="Inter" font-size="11" fill="#475569">Поворот L → Прямо S → L</text>
  </g>
  <g transform="translate(255, 50)">
    <rect width="190" height="110" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="20" font-family="Inter" font-size="13" font-weight="700" fill="#0284c7">2. Слово LSR</text>
    <circle cx="50" cy="75" r="22" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2" fill="none"/>
    <circle cx="140" cy="65" r="22" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2" fill="none"/>
    <path d="M40,93 A22,22 0 0,1 63,55 L125,83 A22,22 0 0,0 155,50" stroke="#059669" stroke-width="2.5" fill="none"/>
    <circle cx="40" cy="93" r="3" fill="#16a34a"/>
    <circle cx="155" cy="50" r="3" fill="#dc2626"/>
    <text x="15" y="100" font-family="Inter" font-size="11" fill="#475569">Внутренняя касательная</text>
  </g>
  <g transform="translate(470, 50)">
    <rect width="190" height="110" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="20" font-family="Inter" font-size="13" font-weight="700" fill="#0284c7">3. Слово LRL (без S)</text>
    <path d="M35,80 A20,20 0 0,1 65,55 A20,20 0 0,0 115,55 A20,20 0 0,1 145,80" stroke="#7c3aed" stroke-width="2.5" fill="none"/>
    <circle cx="35" cy="80" r="3" fill="#16a34a"/>
    <circle cx="145" cy="80" r="3" fill="#dc2626"/>
    <text x="15" y="100" font-family="Inter" font-size="11" fill="#475569">При близких целях (S = ∅)</text>
  </g>
  <g transform="translate(40, 180)">
    <rect width="620" height="110" rx="6" fill="#f0f9ff" stroke="#bae6fd"/>
    <text x="20" y="28" font-family="Inter" font-size="13" font-weight="700" fill="#0369a1">Аналитическая теорема Суссмана и Танга (Sussmann &amp; Tang, 1991):</text>
    <text x="20" y="52" font-family="Inter" font-size="12" fill="#475569">• Из принципа максимума Понтрягина следует: оптимальное управление u(t) ∈ {-1, 0, +1} (Bang-Bang).</text>
    <text x="20" y="72" font-family="Inter" font-size="12" fill="#475569">• Кратчайший путь между любыми позами в SE(2) состоит максимум из 3 участков окружностей и прямой.</text>
    <text x="20" y="92" font-family="JetBrains Mono" font-size="12" fill="#0284c7">Время аналитического расчета: t &lt; 0.5 микросекунды (идеально для Hybrid A* и RRT*)</text>
  </g>
</svg>`,

  // --- LECTURE 06 ---
  'assets/images/lecture-06/receding_horizon.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="28" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Принцип скользящего горизонта MPC (Receding Horizon Principle)</text>
  <g transform="translate(40, 50)">
    <text x="0" y="15" font-family="Inter" font-size="12" font-weight="700" fill="#0f172a">Такт k: Оптимизация на окне N шагов</text>
    <line x1="0" y1="50" x2="600" y2="50" stroke="#cbd5e1" stroke-width="2"/>
    <path d="M0,50 L120,50" stroke="#94a3b8" stroke-width="3"/>
    <circle cx="120" cy="50" r="6" fill="#0284c7"/>
    <text x="105" y="75" font-family="JetBrains Mono" font-size="12" fill="#0284c7">t_k (x_k)</text>
    <rect x="120" y="30" width="360" height="40" rx="4" fill="#e0f2fe" stroke="#38bdf8" stroke-dasharray="4 2"/>
    <path d="M120,50 Q240,10 480,50" stroke="#0284c7" stroke-width="2.5" fill="none"/>
    <circle cx="480" cy="50" r="5" fill="#0284c7" fill-opacity="0.5"/>
    <text x="440" y="85" font-family="JetBrains Mono" font-size="12" fill="#0284c7">t_{k+N}</text>
    <text x="220" y="25" font-family="Inter" font-size="12" font-weight="700" fill="#0369a1">Горизонт прогноза N шагов</text>
    <path d="M120,50 L160,42" stroke="#16a34a" stroke-width="4"/>
    <circle cx="160" cy="42" r="5" fill="#16a34a"/>
    <text x="125" y="95" font-family="Inter" font-size="12" font-weight="700" fill="#16a34a">Исполняется ТОЛЬКО u_0*</text>
  </g>
  <g transform="translate(40, 175)">
    <text x="0" y="15" font-family="Inter" font-size="12" font-weight="700" fill="#0f172a">Такт k+1: Сдвиг окна на Δt вперед и новый замер от SLAM</text>
    <line x1="0" y1="50" x2="600" y2="50" stroke="#cbd5e1" stroke-width="2"/>
    <path d="M0,50 L160,50" stroke="#94a3b8" stroke-width="3"/>
    <circle cx="160" cy="50" r="6" fill="#16a34a"/>
    <text x="135" y="75" font-family="JetBrains Mono" font-size="12" fill="#16a34a">t_{k+1}</text>
    <rect x="160" y="30" width="360" height="40" rx="4" fill="#dcfce7" stroke="#4ade80" stroke-dasharray="4 2"/>
    <path d="M160,50 Q280,15 520,50" stroke="#16a34a" stroke-width="2.5" fill="none"/>
    <circle cx="520" cy="50" r="5" fill="#16a34a" fill-opacity="0.5"/>
    <text x="480" y="85" font-family="JetBrains Mono" font-size="12" fill="#16a34a">t_{k+1+N}</text>
    <text x="250" y="25" font-family="Inter" font-size="12" font-weight="700" fill="#15803d">Сдвинутый горизонт N</text>
    <rect x="0" y="95" width="600" height="30" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
    <text x="15" y="115" font-family="Inter" font-size="12" fill="#475569">✓ Естественная обратная связь: компенсирует проскальзывание колес и задержки датчиков</text>
  </g>
</svg>`,

  // --- LECTURE 07 ---
  'assets/images/lecture-07/lie_bracket_commutator.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="28" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Скобка Ли [f1, f2]: Геометрия параллельной парковки</text>
  <g transform="translate(60, 60)">
    <path d="M60,180 L180,180" stroke="#0284c7" stroke-width="3"/>
    <polygon points="170,175 180,180 170,185" fill="#0284c7"/>
    <text x="95" y="200" font-family="Inter" font-size="12" font-weight="600" fill="#0284c7">1. Вперед (+ε·f1)</text>
    <path d="M180,180 L220,100" stroke="#eab308" stroke-width="3"/>
    <polygon points="212,103 220,100 220,110" fill="#eab308"/>
    <text x="215" y="145" font-family="Inter" font-size="12" font-weight="600" fill="#a16207">2. Руль влево (+ε·f2)</text>
    <path d="M220,100 L100,100" stroke="#0284c7" stroke-width="3"/>
    <polygon points="110,95 100,100 110,105" fill="#0284c7"/>
    <text x="130" y="90" font-family="Inter" font-size="12" font-weight="600" fill="#0284c7">3. Назад (-ε·f1)</text>
    <path d="M100,100 L60,140" stroke="#eab308" stroke-width="3"/>
    <polygon points="62,130 60,140 70,138" fill="#eab308"/>
    <text x="10" y="125" font-family="Inter" font-size="12" font-weight="600" fill="#a16207">4. Руль вправо (-ε·f2)</text>
    <circle cx="60" cy="180" r="5" fill="#16a34a"/><text x="40" y="195" font-size="11" fill="#16a34a">q(0)</text>
    <circle cx="60" cy="140" r="5" fill="#7c3aed"/><text x="40" y="145" font-size="11" fill="#7c3aed">q(4ε)</text>
    <line x1="60" y1="180" x2="60" y2="140" stroke="#7c3aed" stroke-width="4" stroke-linecap="round"/>
    <polygon points="56,150 60,140 64,150" fill="#7c3aed"/>
  </g>
  <g transform="translate(370, 60)">
    <rect width="280" height="200" rx="8" fill="#f5f3ff" stroke="#ddd6fe"/>
    <text x="18" y="30" font-family="Inter" font-size="14" font-weight="700" fill="#6d28d9">Результирующий боковой сдвиг:</text>
    <text x="18" y="60" font-family="JetBrains Mono" font-size="12" fill="#7c3aed" font-weight="700">Δq = ε² [f1, f2](q) + O(ε³)</text>
    <g transform="translate(18, 85)">
      <text x="0" y="0" font-family="Inter" font-size="12" fill="#475569">• Неголономный колесный робот</text>
      <text x="0" y="20" font-family="Inter" font-size="12" fill="#475569">  НЕ может двигаться боком мгновенно.</text>
      <text x="0" y="45" font-family="Inter" font-size="12" fill="#475569">• Но циклический маневр коммутатора</text>
      <text x="0" y="65" font-family="Inter" font-size="12" fill="#475569">  генерирует чистое боковое движение!</text>
      <text x="0" y="95" font-family="Inter" font-size="12" font-weight="700" fill="#15803d">Теорема Чоу-Рашевского (LARC):</text>
      <text x="0" y="113" font-family="Inter" font-size="12" fill="#475569">Робот с 2 моторами полностью управляем в SE(2)!</text>
    </g>
  </g>
</svg>`,

  // --- LECTURE 08 ---
  'assets/images/lecture-08/nav2_bt_tree.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="26" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Архитектура ROS 2 Nav2: Дерево поведения (Behavior Tree)</text>
  <g transform="translate(350, 45)">
    <rect x="-80" y="0" width="160" height="30" rx="5" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
    <text x="0" y="19" font-family="Inter" font-size="11" font-weight="600" text-anchor="middle" fill="#92400e">RecoveryNode (3x)</text>
  </g>
  <path d="M350,75 L200,105 M350,75 L500,105" stroke="#94a3b8" stroke-width="2"/>
  <g transform="translate(200, 105)">
    <rect x="-75" y="0" width="150" height="30" rx="5" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
    <text x="0" y="19" font-family="Inter" font-size="11" font-weight="600" text-anchor="middle" fill="#0369a1">PipelineSequence (→)</text>
  </g>
  <g transform="translate(500, 105)">
    <rect x="-75" y="0" width="150" height="30" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <text x="0" y="19" font-family="Inter" font-size="11" font-weight="600" text-anchor="middle" fill="#991b1b">ReactiveFallback (?)</text>
  </g>
  <path d="M200,135 L120,165 M200,135 L280,165" stroke="#94a3b8" stroke-width="2"/>
  <g transform="translate(120, 165)">
    <rect x="-65" y="0" width="130" height="34" rx="5" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
    <text x="0" y="16" font-family="Inter" font-size="11" font-weight="600" text-anchor="middle" fill="#15803d">ComputePath</text>
    <text x="0" y="28" font-family="JetBrains Mono" font-size="9" fill="#166534" text-anchor="middle">(Global 1 Hz)</text>
  </g>
  <g transform="translate(280, 165)">
    <rect x="-65" y="0" width="130" height="34" rx="5" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
    <text x="0" y="16" font-family="Inter" font-size="11" font-weight="600" text-anchor="middle" fill="#15803d">FollowPath</text>
    <text x="0" y="28" font-family="JetBrains Mono" font-size="9" fill="#166534" text-anchor="middle">(Local MPC 30 Hz)</text>
  </g>
  <path d="M500,135 L400,165 M500,135 L500,165 M500,135 L600,165" stroke="#94a3b8" stroke-width="2"/>
  <g transform="translate(400, 165)">
    <rect x="-45" y="0" width="90" height="34" rx="5" fill="#fdf4ff" stroke="#a855f7" stroke-width="1.5"/>
    <text x="0" y="16" font-family="Inter" font-size="11" font-weight="600" text-anchor="middle" fill="#7e22ce">ClearCostmap</text>
    <text x="0" y="28" font-family="Inter" font-size="9" fill="#6b21a8" text-anchor="middle">Шаг 1</text>
  </g>
  <g transform="translate(500, 165)">
    <rect x="-45" y="0" width="90" height="34" rx="5" fill="#fdf4ff" stroke="#a855f7" stroke-width="1.5"/>
    <text x="0" y="16" font-family="Inter" font-size="11" font-weight="600" text-anchor="middle" fill="#7e22ce">Spin (360°)</text>
    <text x="0" y="28" font-family="Inter" font-size="9" fill="#6b21a8" text-anchor="middle">Шаг 2</text>
  </g>
  <g transform="translate(600, 165)">
    <rect x="-45" y="0" width="90" height="34" rx="5" fill="#fdf4ff" stroke="#a855f7" stroke-width="1.5"/>
    <text x="0" y="16" font-family="Inter" font-size="11" font-weight="600" text-anchor="middle" fill="#7e22ce">BackUp (0.3m)</text>
    <text x="0" y="28" font-family="Inter" font-size="9" fill="#6b21a8" text-anchor="middle">Шаг 3</text>
  </g>
  <g transform="translate(30, 235)">
    <rect width="640" height="60" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="22" font-family="Inter" font-size="12" font-weight="700" fill="#0f172a">Преимущество Деревьев Поведения (BT) в робототехнике:</text>
    <text x="15" y="42" font-family="Inter" font-size="11" fill="#475569">• Нет комбинаторного взрыва состояний, как в FSM. • Модульность, асинхронные Action-клиенты и гибкая эскалация ошибок.</text>
  </g>
</svg>`,

  // --- NEW DIAGRAMS ---
  // LECTURE 03: Informed RRT* Ellipsoid
  'assets/images/lecture-03/informed_rrt_ellipse.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="26" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Informed RRT*: Сжатие пространства выборки в гиперэллипсоид</text>
  <g transform="translate(30, 45)">
    <!-- Ellipse and foci -->
    <ellipse cx="190" cy="120" rx="160" ry="85" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" stroke-dasharray="6 3"/>
    <!-- Start and Goal -->
    <circle cx="90" cy="120" r="7" fill="#16a34a"/>
    <text x="65" y="145" font-family="Inter" font-size="11" font-weight="700" fill="#15803d">x_start</text>
    <circle cx="290" cy="120" r="7" fill="#dc2626"/>
    <text x="275" y="145" font-family="Inter" font-size="11" font-weight="700" fill="#b91c1c">x_goal</text>
    <line x1="90" y1="120" x2="290" y2="120" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3"/>
    <text x="165" y="112" font-family="JetBrains Mono" font-size="10" fill="#64748b">c_min = ||x_start - x_goal||</text>
    <!-- Current Best Path -->
    <path d="M90,120 Q140,80 190,105 T290,120" stroke="#2563eb" stroke-width="2.5" fill="none"/>
    <text x="150" y="80" font-family="JetBrains Mono" font-size="10" font-weight="600" fill="#1d4ed8">c_best (текущий путь)</text>
    <!-- Accepted samples inside -->
    <circle cx="160" cy="70" r="3.5" fill="#16a34a"/><circle cx="220" cy="140" r="3.5" fill="#16a34a"/>
    <circle cx="120" cy="100" r="3.5" fill="#16a34a"/><circle cx="250" cy="90" r="3.5" fill="#16a34a"/>
    <text x="140" y="170" font-family="Inter" font-size="10" font-weight="600" fill="#16a34a">✓ Сэмплы внутри эллипсоида</text>
    <!-- Rejected samples outside -->
    <text x="20" y="35" font-family="Inter" font-size="12" fill="#ef4444" font-weight="700">✕</text>
    <text x="320" y="30" font-family="Inter" font-size="12" fill="#ef4444" font-weight="700">✕</text>
    <text x="340" y="180" font-family="Inter" font-size="12" fill="#ef4444" font-weight="700">✕</text>
    <text x="30" y="190" font-family="Inter" font-size="10" fill="#dc2626">✕ Отсекаются (длина &gt; c_best)</text>
    <!-- Dimensions -->
    <line x1="30" y1="210" x2="350" y2="210" stroke="#0284c7" stroke-width="1.5"/>
    <text x="140" y="225" font-family="JetBrains Mono" font-size="10" fill="#0284c7">Главная ось = c_best</text>
  </g>
  <g transform="translate(410, 45)">
    <rect width="260" height="230" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="24" font-family="Inter" font-size="13" font-weight="700" fill="#0f172a">Математика сжатия:</text>
    <g transform="translate(15, 45)">
      <text x="0" y="0" font-family="JetBrains Mono" font-size="10.5" fill="#0284c7">C_inf = {x | ||x-x_s|| + ||x-x_g|| &#8804; c_best}</text>
      <text x="0" y="24" font-family="Inter" font-size="11" fill="#334155">• Фокусы: x_start и x_goal</text>
      <text x="0" y="44" font-family="Inter" font-size="11" fill="#334155">• Полуоси: a = c_best / 2</text>
      <text x="0" y="64" font-family="Inter" font-size="11" fill="#334155">  b = &#8730;(c_best² - c_min²) / 2</text>
      <text x="0" y="88" font-family="Inter" font-size="11" fill="#334155">• При каждом улучшении пути:</text>
      <text x="0" y="106" font-family="Inter" font-size="11" font-weight="600" fill="#16a34a">  c_best &#8595; &#8658; эллипсоид сжимается!</text>
      <rect x="0" y="122" width="230" height="48" rx="4" fill="#f0fdf4" stroke="#bbf7d0"/>
      <text x="8" y="140" font-family="Inter" font-size="10.5" font-weight="700" fill="#166534">Вычислительный эффект:</text>
      <text x="8" y="158" font-family="Inter" font-size="10" fill="#166534">Сходимость к оптимуму в 10–50 раз быстрее</text>
    </g>
  </g>
</svg>`,

  // LECTURE 04: Timed Elastic Band (TEB)
  'assets/images/lecture-04/teb_elastic_band.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="26" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Timed Elastic Band (TEB): Траектория как деформируемая упругая лента</text>
  <g transform="translate(40, 50)">
    <!-- Band Path -->
    <path d="M30,170 Q100,165 150,110 T260,60" stroke="#0284c7" stroke-width="3" fill="none"/>
    <!-- Obstacle -->
    <circle cx="110" cy="80" r="30" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="92" y="84" font-family="Inter" font-size="11" font-weight="700" fill="#dc2626">Преграда</text>
    <!-- Repulsive force arrows from obstacle to band -->
    <line x1="125" y1="102" x2="145" y2="122" stroke="#dc2626" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="140" y="140" font-family="JetBrains Mono" font-size="9" fill="#dc2626">F_rep</text>
    <!-- Nodes (Poses) -->
    <g transform="translate(30, 170)">
      <circle cx="0" cy="0" r="6" fill="#16a34a"/>
      <text x="-15" y="18" font-family="Inter" font-size="10" font-weight="700" fill="#15803d">s_0</text>
    </g>
    <g transform="translate(90, 155)">
      <circle cx="0" cy="0" r="6" fill="#0284c7"/>
      <line x1="0" y1="0" x2="12" y2="-7" stroke="#ffffff" stroke-width="2"/>
      <text x="-5" y="20" font-family="Inter" font-size="10" font-weight="600" fill="#0369a1">s_1</text>
      <text x="25" y="-5" font-family="JetBrains Mono" font-size="9" fill="#7c3aed">&#916;T_1</text>
    </g>
    <g transform="translate(160, 105)">
      <circle cx="0" cy="0" r="6" fill="#0284c7"/>
      <line x1="0" y1="0" x2="14" y2="-6" stroke="#ffffff" stroke-width="2"/>
      <text x="10" y="18" font-family="Inter" font-size="10" font-weight="600" fill="#0369a1">s_2</text>
      <text x="25" y="-5" font-family="JetBrains Mono" font-size="9" fill="#7c3aed">&#916;T_2</text>
    </g>
    <g transform="translate(260, 60)">
      <circle cx="0" cy="0" r="6" fill="#dc2626"/>
      <text x="10" y="5" font-family="Inter" font-size="10" font-weight="700" fill="#b91c1c">s_goal</text>
    </g>
    <!-- Tension forces -->
    <path d="M40,165 L80,157" stroke="#10b981" stroke-width="1.5" stroke-dasharray="2 2"/>
    <text x="10" y="220" font-family="Inter" font-size="11" fill="#475569">Упругое сжатие времени (&#916;T &#8595;) vs отталкивание от стен</text>
  </g>
  <g transform="translate(360, 50)">
    <rect width="300" height="230" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="24" font-family="Inter" font-size="13" font-weight="700" fill="#0f172a">Оптимизация на фактор-графе (g2o):</text>
    <g transform="translate(15, 45)">
      <text x="0" y="0" font-family="JetBrains Mono" font-size="10.5" fill="#0284c7">B = {s_0, &#916;T_0, s_1, &#916;T_1, ..., s_n}</text>
      <text x="0" y="24" font-family="Inter" font-size="11" fill="#334155">• Позы s_i = (x_i, y_i, &#952;_i) в SE(2)</text>
      <text x="0" y="44" font-family="Inter" font-size="11" fill="#334155">• Временные интервалы &#916;T_i &gt; 0</text>
      <text x="0" y="68" font-family="Inter" font-size="11" font-weight="600" fill="#0f172a">Штрафные функции в графе:</text>
      <text x="0" y="88" font-family="Inter" font-size="10.5" fill="#334155">  1. Быстродействие: &#931; (&#916;T_i)²</text>
      <text x="0" y="106" font-family="Inter" font-size="10.5" fill="#334155">  2. Безопасность: f_obs(s_i) &#8594; 0</text>
      <text x="0" y="124" font-family="Inter" font-size="10.5" fill="#334155">  3. Кинематика: v &#8804; v_max, a &#8804; a_max, &#969; &#8804; &#969;_max</text>
      <rect x="0" y="136" width="270" height="36" rx="4" fill="#f0f9ff" stroke="#bae6fd"/>
      <text x="8" y="152" font-family="Inter" font-size="10" font-weight="600" fill="#0369a1">Решается за 5–15 мс методом Левенберга-Марквардта</text>
    </g>
  </g>
</svg>`,

  // LECTURE 05: Reeds-Shepp Curves
  'assets/images/lecture-05/reeds_shepp_curves.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="26" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Кривые Ридса-Шеппа: Маневры с реверсом (Cusp) и сравнение с Дубинсом</text>
  <g transform="translate(40, 50)">
    <rect width="280" height="150" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="22" font-family="Inter" font-size="12" font-weight="700" fill="#dc2626">1. Автомобиль Дубинса (Только вперед v = +1)</text>
    <path d="M40,120 C40,40 180,40 240,110" stroke="#dc2626" stroke-width="2.5" fill="none"/>
    <circle cx="40" cy="120" r="5" fill="#16a34a"/><circle cx="240" cy="110" r="5" fill="#2563eb"/>
    <text x="15" y="140" font-family="Inter" font-size="10.5" fill="#64748b">Вынужден делать огромную петлю RSR: L = 14.8 м</text>
  </g>
  <g transform="translate(360, 50)">
    <rect width="290" height="150" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="22" font-family="Inter" font-size="12" font-weight="700" fill="#16a34a">2. Ридс-Шепп (Вперед и назад v &#8712; {-1, +1})</text>
    <path d="M40,120 A30,30 0 0,0 85,90" stroke="#16a34a" stroke-width="3" fill="none"/>
    <path d="M85,90 A30,30 0 0,1 160,110" stroke="#2563eb" stroke-width="3" stroke-dasharray="4 2" fill="none"/>
    <circle cx="85" cy="90" r="4" fill="#d97706"/>
    <text x="88" y="80" font-family="Inter" font-size="10" font-weight="700" fill="#d97706">Точка смены хода (Cusp |)</text>
    <circle cx="40" cy="120" r="5" fill="#16a34a"/><circle cx="160" cy="110" r="5" fill="#2563eb"/>
    <text x="15" y="140" font-family="Inter" font-size="10.5" fill="#15803d">Маневр C|C (вперед + назад): L = 4.2 м (-70% пути!)</text>
  </g>
  <g transform="translate(40, 215)">
    <rect width="610" height="85" rx="6" fill="#f0f9ff" stroke="#bae6fd"/>
    <text x="15" y="20" font-family="Inter" font-size="12" font-weight="700" fill="#0369a1">9 канонических семейств Ридса-Шеппа (46 оптимальных слов):</text>
    <text x="15" y="40" font-family="JetBrains Mono" font-size="11" fill="#0284c7">C|C|C,  C|CC,  CC|C,  CC|CC,  C|C_&#960;/2 C,  CSC,  C|CSC,  CSC|C,  C|CS|C</text>
    <text x="15" y="65" font-family="Inter" font-size="11" fill="#475569">• Смена хода | соответствует остановке и переключению передачи на реверс.</text>
  </g>
</svg>`,

  // LECTURE 06: MPC Optimization Pipeline
  'assets/images/lecture-06/mpc_qp_pipeline.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="26" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Контур предиктивного управления (Closed-Loop Receding Horizon Pipeline)</text>
  <!-- Pipeline Blocks -->
  <g transform="translate(40, 50)">
    <rect x="0" y="0" width="130" height="60" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>
    <text x="65" y="26" font-family="Inter" font-size="11" font-weight="700" fill="#0369a1" text-anchor="middle">SLAM / EKF</text>
    <text x="65" y="44" font-family="JetBrains Mono" font-size="9.5" fill="#0284c7" text-anchor="middle">Состояние x_k</text>
  </g>
  <path d="M170,80 L215,80" stroke="#0284c7" stroke-width="2.5"/>
  <polygon points="212,76 220,80 212,84" fill="#0284c7"/>
  <g transform="translate(220, 40)">
    <rect x="0" y="0" width="220" height="80" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
    <text x="110" y="22" font-family="Inter" font-size="12" font-weight="700" fill="#15803d" text-anchor="middle">QP / SQP Солвер (acados)</text>
    <text x="110" y="42" font-family="JetBrains Mono" font-size="9" fill="#166534" text-anchor="middle">min &#931; (x-x_ref)ᵀQ(x-x_ref) + uᵀRu</text>
    <text x="110" y="60" font-family="JetBrains Mono" font-size="9" fill="#166534" text-anchor="middle">ограничения: u &#8712; U, x &#8712; X_free</text>
  </g>
  <path d="M440,80 L485,80" stroke="#16a34a" stroke-width="2.5"/>
  <polygon points="482,76 490,80 482,84" fill="#16a34a"/>
  <g transform="translate(490, 50)">
    <rect x="0" y="0" width="160" height="60" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
    <text x="80" y="26" font-family="Inter" font-size="11" font-weight="700" fill="#92400e" text-anchor="middle">Исполнение u_0*</text>
    <text x="80" y="44" font-family="JetBrains Mono" font-size="9.5" fill="#b45309" text-anchor="middle">(только 1-й шаг)</text>
  </g>
  <!-- Robot & Environment feedback -->
  <path d="M570,110 L570,175 L105,175 L105,110" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 2" fill="none"/>
  <polygon points="101,118 105,110 109,118" fill="#94a3b8"/>
  <text x="300" y="165" font-family="Inter" font-size="11" fill="#64748b" text-anchor="middle">Физический отклик шасси: x(t + &#916;t) с учетом трения и возмущений</text>
  <!-- Timing card below -->
  <g transform="translate(40, 205)">
    <rect width="610" height="90" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="22" font-family="Inter" font-size="12" font-weight="700" fill="#0f172a">Хронометраж такта RTI (Real-Time Iteration) на 50 Гц (бюджет 20 мс):</text>
    <g transform="translate(15, 40)">
      <rect x="0" y="0" width="420" height="18" rx="3" fill="#e0f2fe"/>
      <text x="10" y="13" font-family="Inter" font-size="10" fill="#0369a1">Preparation Phase (фоновая линеаризация): 12–15 мс</text>
      <rect x="425" y="0" width="130" height="18" rx="3" fill="#dcfce7"/>
      <text x="435" y="13" font-family="Inter" font-size="10" font-weight="700" fill="#15803d">Feedback QP: &lt; 1 мс</text>
      <text x="0" y="38" font-family="Inter" font-size="11" fill="#475569">Гарантирует отсутствие задержек в управлении рулевой рейкой и тягой.</text>
    </g>
  </g>
</svg>`,

  // LECTURE 07: Bicycle Model & Ackermann Kinematics
  'assets/images/lecture-07/car_kinematics_ackermann.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="26" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Кинематика автомобиля: Модель велосипеда и геометрия Аккермана</text>
  <g transform="translate(60, 50)">
    <!-- Base frame line -->
    <line x1="50" y1="160" x2="210" y2="160" stroke="#0f172a" stroke-width="4"/>
    <text x="115" y="180" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#0f172a">База L</text>
    <!-- Rear Wheel -->
    <rect x="35" y="140" width="30" height="40" rx="3" fill="#334155"/>
    <circle cx="50" cy="160" r="4" fill="#38bdf8"/>
    <text x="15" y="210" font-family="Inter" font-size="10.5" font-weight="700" fill="#0369a1">(x, y, &#952;)</text>
    <line x1="50" y1="160" x2="10" y2="160" stroke="#0284c7" stroke-width="2.5"/>
    <polygon points="15,156 5,160 15,164" fill="#0284c7"/>
    <text x="15" y="135" font-family="JetBrains Mono" font-size="10" fill="#0284c7">v_rear</text>
    <!-- Front Wheel with steering angle delta -->
    <g transform="translate(210, 160) rotate(-28)">
      <rect x="-15" y="-20" width="30" height="40" rx="3" fill="#334155"/>
      <circle cx="0" cy="0" r="4" fill="#f59e0b"/>
      <line x1="0" y1="0" x2="40" y2="0" stroke="#d97706" stroke-width="2.5"/>
      <polygon points="35,-4 45,0 35,4" fill="#d97706"/>
      <text x="10" y="-10" font-family="JetBrains Mono" font-size="10" fill="#d97706">v_front</text>
    </g>
    <!-- Steering angle arc -->
    <path d="M240,160 A30,30 0 0,0 236,146" stroke="#d97706" stroke-width="1.5" fill="none"/>
    <text x="245" y="152" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#d97706">&#948;</text>
    <!-- ICR and radius lines -->
    <line x1="50" y1="160" x2="50" y2="25" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3"/>
    <line x1="210" y1="160" x2="50" y2="25" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 3"/>
    <circle cx="50" cy="25" r="5" fill="#dc2626"/>
    <text x="60" y="30" font-family="Inter" font-size="11" font-weight="700" fill="#dc2626">МЦВ (ICR)</text>
    <text x="10" y="90" font-family="JetBrains Mono" font-size="10" fill="#475569">R = L / tan(&#948;)</text>
  </g>
  <g transform="translate(380, 50)">
    <rect width="280" height="235" rx="6" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="15" y="24" font-family="Inter" font-size="13" font-weight="700" fill="#0f172a">Уравнения движения:</text>
    <g transform="translate(15, 45)">
      <text x="0" y="0" font-family="JetBrains Mono" font-size="11" fill="#0284c7">x&#775; = v &#183; cos(&#952;)</text>
      <text x="0" y="22" font-family="JetBrains Mono" font-size="11" fill="#0284c7">y&#775; = v &#183; sin(&#952;)</text>
      <text x="0" y="44" font-family="JetBrains Mono" font-size="11" fill="#0284c7">&#952;&#775; = (v / L) &#183; tan(&#948;)</text>
      <text x="0" y="72" font-family="Inter" font-size="11" font-weight="700" fill="#dc2626">Связь Пфаффа (без проскальзывания):</text>
      <text x="0" y="92" font-family="JetBrains Mono" font-size="11" fill="#dc2626">x&#775; sin(&#952;) - y&#775; cos(&#952;) = 0</text>
      <text x="0" y="118" font-family="Inter" font-size="11" fill="#334155">• Неголономное ограничение:</text>
      <text x="0" y="136" font-family="Inter" font-size="10.5" fill="#475569">  боковая скорость мгновенно = 0</text>
      <text x="0" y="156" font-family="Inter" font-size="11" font-weight="600" fill="#16a34a">&#8658; Кривизна траектории: &#954; = tan(&#948;) / L</text>
      <text x="0" y="174" font-family="Inter" font-size="10.5" fill="#15803d">Ограничена: |&#954;| &#8804; tan(&#948;_max) / L</text>
    </g>
  </g>
</svg>`,

  // LECTURE 08: Multi-Rate Real-Time Stack
  'assets/images/lecture-08/realtime_stack_hierarchy.svg': `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 320" width="100%" height="100%">
  <rect width="100%" height="100%" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="30" y="26" font-family="Inter" font-size="14" font-weight="700" fill="#0f172a">Многотактовая архитектура реального времени автономного робота</text>
  <g transform="translate(40, 45)">
    <!-- Layer 1: Mission / BT -->
    <rect x="0" y="0" width="620" height="48" rx="6" fill="#fdf4ff" stroke="#c084fc" stroke-width="1.5"/>
    <text x="20" y="24" font-family="Inter" font-size="12" font-weight="700" fill="#7e22ce">1. Уровень миссии и поведение (Behavior Tree)</text>
    <rect x="510" y="10" width="90" height="26" rx="4" fill="#a855f7"/>
    <text x="555" y="27" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">0.5–2 Гц</text>
    <text x="20" y="40" font-family="Inter" font-size="10.5" fill="#6b21a8">Выбор целей, аварийные действия (Recovery), диспетчеризация задач</text>
    <!-- Layer 2: Global Planning -->
    <rect x="0" y="58" width="620" height="48" rx="6" fill="#eff6ff" stroke="#60a5fa" stroke-width="1.5"/>
    <text x="20" y="82" font-family="Inter" font-size="12" font-weight="700" fill="#1d4ed8">2. Глобальный планировщик пути (Global Planner)</text>
    <rect x="510" y="68" width="90" height="26" rx="4" fill="#3b82f6"/>
    <text x="555" y="85" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">1–5 Гц</text>
    <text x="20" y="98" font-family="Inter" font-size="10.5" fill="#1e40af">Smac Planner (Hybrid A*), D* Lite, Voronoi на глобальной Costmap</text>
    <!-- Layer 3: Local Planner / MPC -->
    <rect x="0" y="116" width="620" height="48" rx="6" fill="#f0fdf4" stroke="#4ade80" stroke-width="1.5"/>
    <text x="20" y="140" font-family="Inter" font-size="12" font-weight="700" fill="#15803d">3. Локальный планировщик траектории (Controller)</text>
    <rect x="510" y="126" width="90" height="26" rx="4" fill="#22c55e"/>
    <text x="555" y="143" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">20–50 Гц</text>
    <text x="20" y="156" font-family="Inter" font-size="10.5" fill="#166534">NMPC (acados), TEB, DWA — учет динамических людей и препятствий</text>
    <!-- Layer 4: Motor & Safety E-stop -->
    <rect x="0" y="174" width="620" height="48" rx="6" fill="#fef2f2" stroke="#f87171" stroke-width="1.5"/>
    <text x="20" y="198" font-family="Inter" font-size="12" font-weight="700" fill="#b91c1c">4. Приводы, энкодеры и аппаратная безопасность</text>
    <rect x="510" y="184" width="90" height="26" rx="4" fill="#ef4444"/>
    <text x="555" y="201" font-family="JetBrains Mono" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">500–1000 Гц</text>
    <text x="20" y="214" font-family="Inter" font-size="10.5" fill="#991b1b">CAN bus / micro-ROS, ПИД токов моторов, лазерный бампер (Safety E-stop)</text>
  </g>
  <g transform="translate(40, 275)">
    <text x="0" y="15" font-family="Inter" font-size="11.5" font-weight="600" fill="#0f172a">Принцип разделения контуров:</text>
    <text x="180" y="15" font-family="Inter" font-size="11" fill="#475569">Асинхронные очереди и буферы исключают блокировку нижних быстрых контуров верхними.</text>
  </g>
</svg>`
};

for (const [filePath, content] of Object.entries(svgFiles)) {
  const fullPath = path.resolve(filePath);
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, content.trim());
  console.log(`✓ Создана диаграмма: ${filePath}`);
}
console.log('Все SVG диаграммы успешно созданы!');
