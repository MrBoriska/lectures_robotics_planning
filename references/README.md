# Первоисточники

Каталог содержит литературу, на которую опирается курс. Файлы хранятся в Git LFS
(см. `.gitattributes`) и в сборке не участвуют.

```
references/
├── lavalle_planning_algorithms/   LaValle S. M. Planning Algorithms
├── eth_zurich/                    ETH Zürich, Autonomous Mobile Robots
└── mit/                           MIT 16.410/16.413 и статья Karaman & Frazzoli
```

## Состав

| Источник | Автор, организация | Год | Файл |
| :--- | :--- | :--- | :--- |
| Planning Algorithms | Steven M. LaValle, UIUC / Oulu; Cambridge University Press | 2006 | [`lavalle_planning_algorithms.pdf`](lavalle_planning_algorithms/lavalle_planning_algorithms.pdf) |
| Autonomous Mobile Robots, конспект раздела по планированию | R. Siegwart, M. Hutter, M. Chli, C. Cadena; ETH Zürich (ASL, RSL) | — | [`eth_amr_planning_summary.pdf`](eth_zurich/eth_amr_planning_summary.pdf) |
| Principles of Autonomy and Decision Making, лекция 14 | E. Frazzoli, MIT 16.410/16.413 | — | [`mit_16_410_lec14_informed_search.pdf`](mit/mit_16_410_lec14_informed_search.pdf) |
| То же, лекция 15 | E. Frazzoli, MIT 16.410/16.413 | — | [`mit_16_410_lec15_sampling_based_planning.pdf`](mit/mit_16_410_lec15_sampling_based_planning.pdf) |
| То же, лекция 18 | E. Frazzoli, MIT 16.410/16.413 | — | [`mit_16_410_lec18_milp_motion_planning.pdf`](mit/mit_16_410_lec18_milp_motion_planning.pdf) |
| Sampling-based Algorithms for Optimal Motion Planning, IJRR 30(7) | S. Karaman, E. Frazzoli; MIT LIDS | 2011 | [`karaman_frazzoli_rrt_star_optimal_planning.pdf`](mit/karaman_frazzoli_rrt_star_optimal_planning.pdf) |

## Тематический охват

| Тема | Где рассматривается |
| :--- | :--- |
| Конфигурационное пространство, сумма Минковского, топология $SE(2)$ | LaValle, гл. 3–4 |
| Дискретный поиск, $A^*$, свойства эвристик | LaValle гл. 2; MIT, лекция 14 |
| Граф видимости, диаграмма Вороного, точная декомпозиция на ячейки | LaValle, гл. 6; ETH |
| Методы, основанные на выборке: PRM, RRT, вероятностная полнота | LaValle гл. 5; MIT, лекция 15 |
| Асимптотическая оптимальность, $RRT^*$, $PRM^*$ | Karaman & Frazzoli, 2011 |
| Потенциальные поля, навигационные функции, гармонические поля | LaValle гл. 8; ETH |
| Локальное планирование: DWA, VO / RVO | ETH |
| Инкрементальное перепланирование: $D^*$, $D^*$ Lite | ETH |
| Дифференциальные связи, модели Дубинса и Ридса-Шеппа | LaValle, гл. 13 |
| Кинодинамическое планирование | LaValle, гл. 14 |
| Смешанно-целочисленное программирование в планировании | MIT, лекция 18 |

Постраничная разметка каждого источника приведена в README соответствующего
подкаталога.
