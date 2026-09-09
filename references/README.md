# 📚 База первоисточников и академических курсов (References & Foundations)

Для формирования глубокого, математически строгого и практически применимого содержания курса лекций по планированию для мобильных роботов в репозиторий загружены и структурированы материалы трех ведущих мировых школ:

```
references/
├── lavalle_planning_algorithms/   # Стивен Лаваль: фундаментальный учебник (842 стр.)
│   ├── lavalle_planning_algorithms.pdf
│   └── README.md
├── eth_zurich/                    # ETH Zürich: Autonomous Mobile Robots (Siegwart et al.)
│   ├── eth_amr_planning_summary.pdf
│   └── README.md
├── mit/                           # MIT: Principles of Autonomy, Karaman/Frazzoli RRT*
│   ├── mit_16_410_lec14_informed_search.pdf
│   ├── mit_16_410_lec15_sampling_based_planning.pdf
│   ├── mit_16_410_lec18_milp_motion_planning.pdf
│   ├── karaman_frazzoli_rrt_star_optimal_planning.pdf
│   └── README.md
└── README.md                      # Данный обзорный файл
```

---

## 🏛️ Сводная матрица источников

| Источник | Организация / Автор | Ключевой вклад в наш курс | Загруженные файлы |
| :--- | :--- | :--- | :--- |
| **Planning Algorithms** | **Steven M. LaValle** (UIUC / Oulu) | • Математика $\mathcal{C}$-space и суммы Минковского<br>• Неголономные связи и скобки Ли<br>• Модели Дубинса и Ридса-Шеппа<br>• Теория сэмплинга (дисперсия, квазислучайность) | [`lavalle_planning_algorithms.pdf`](lavalle_planning_algorithms/lavalle_planning_algorithms.pdf) |
| **Autonomous Mobile Robots** | **ETH Zürich** (Roland Siegwart, Marco Hutter) | • Практический навигационный стек мобильного робота<br>• Локальное планирование: DWA (Dynamic Window Approach)<br>• Предотвращение столкновений: VO / RVO<br>• Гармонические потенциальные поля (устранение ловушек)<br>• Инкрементальное перепланирование ($D^*$) | [`eth_amr_planning_summary.pdf`](eth_zurich/eth_amr_planning_summary.pdf) |
| **Principles of Autonomy & Optimal Planning** | **MIT** (Emilio Frazzoli, Sertac Karaman, Brian Williams) | • Информированный поиск ($A^*$, Branch & Bound)<br>• Асимптотическая оптимальность ($RRT^*$, $PRM^*$)<br>• Смешанно-целочисленное программирование (MILP)<br>• Оптимизация траекторий (Direct Collocation) | [`mit_16_410_lec14_informed_search.pdf`](mit/mit_16_410_lec14_informed_search.pdf)<br>[`mit_16_410_lec15_sampling_based_planning.pdf`](mit/mit_16_410_lec15_sampling_based_planning.pdf)<br>[`mit_16_410_lec18_milp_motion_planning.pdf`](mit/mit_16_410_lec18_milp_motion_planning.pdf)<br>[`karaman_frazzoli_rrt_star_optimal_planning.pdf`](mit/karaman_frazzoli_rrt_star_optimal_planning.pdf) |

---

## 🧭 Рекомендуемый синтез 8 лекций на основе первоисточников

Ниже предложена синергетическая декомпозиция курса (каждая лекция на 90 минут), объединяющая глубину Лаваля, прикладную мощь навигации ETH и оптимальные алгоритмы MIT:

1. **Лекция 01: Введение, конфигурационное пространство ($\mathcal{C}$-space) и дискретный поиск**
   - *Источники:* LaValle (гл. 3, 4, 2), MIT 16.410 (Lec 14), ETH (Planning II).
   - $\mathcal{C}$-space, сумма Минковского, Occupancy Grid, Dijkstra, $A^*$, допустимые и монотонные эвристики.
2. **Лекция 02: Геометрические дорожные карты и сэмплирующие алгоритмы (PRM, RRT)**
   - *Источники:* LaValle (гл. 5, 6), MIT 16.410 (Lec 15), ETH (Planning II).
   - Visibility Graph, диаграммы Вороного (GVD), Probabilistic Roadmap (PRM), классический RRT, вероятностная полнота.
3. **Лекция 03: Асимптотически оптимальное планирование ($RRT^*$, $PRM^*$) и эвристики**
   - *Источники:* MIT Karaman & Frazzoli (IJRR 2011), Informed $RRT^*$.
   - Доказательство неоптимальности базового RRT, переподключение ветвей (Rewiring), $RRT^*$, Informed $RRT^*$, $k$-d tree.
4. **Лекция 04: Потенциальные поля, навигационные функции и гармонические поля**
   - *Источники:* LaValle (гл. 8), ETH (Planning I - Harmonic fields).
   - Метод потенциалов Хатиба, проблема локальных минимумов (U-ловушки), Navigation Functions Римона-Кодичека, уравнение Лапласа $\Delta U = 0$ (Dirichlet/Neumann).
5. **Лекция 05: Неголономная кинематика и локальное планирование (DWA, TEB, VO)**
   - *Источники:* ETH (Planning I - DWA, VO), LaValle (гл. 13).
   - Дифференциальный привод, модель Аккермана, Dynamic Window Approach (DWA), Timed Elastic Band (TEB), Velocity Obstacles (VO/RVO).
6. **Лекция 06: Аналитические траектории для колесных роботов (Дубинс, Ридс-Шепп, сплайны)**
   - *Источники:* LaValle (гл. 13.2, 15), MIT 16.485.
   - Минимальный радиус поворота, кривые Дубинса (LSL, RSR, LSR...), кривые Ридса-Шеппа (с реверсом), $C^1/C^2$ сглаживание сплайнами, клотоиды.
7. **Лекция 07: Кинодинамическое планирование и оптимизация траекторий**
   - *Источники:* LaValle (гл. 14), MIT 16.410 (Lec 18 - MILP), MIT 6.832 (Direct Collocation).
   - Учет сил, масс и моментов инерции; Kinodynamic RRT; постановка траекторной оптимизации: Direct Shooting, Direct Collocation, безопасные коридоры (SFC).
8. **Лекция 08: Динамическое перепланирование, неопределенность и архитектура ROS 2 / Nav2**
   - *Источники:* ETH (Planning II - D* Lite), LaValle (гл. 11, 12), Nav2 Architecture.
   - Инкрементальные алгоритмы ($D^*$, $D^*$ Lite), планирование при зашумленных датчиках, реальный стек Nav2 (BT Navigator, Costmap Layers, Recovery Behaviors).
