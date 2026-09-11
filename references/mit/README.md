# MIT. Материалы по планированию

## Лекции курса 16.410/16.413 «Principles of Autonomy and Decision Making»

Лектор — Emilio Frazzoli.

**[`mit_16_410_lec14_informed_search.pdf`](mit_16_410_lec14_informed_search.pdf)
— Информированный поиск.** Алгоритм $A^*$; построение допустимых и монотонных
эвристик; метод ветвей и границ; соотношение между качеством эвристики и числом
раскрытых вершин.

**[`mit_16_410_lec15_sampling_based_planning.pdf`](mit_16_410_lec15_sampling_based_planning.pdf)
— Планирование, основанное на выборке.** Вероятностные дорожные карты (PRM);
быстро исследующие случайные деревья (RRT); вероятностная полнота и её отличие
от полноты разрешения.

**[`mit_16_410_lec18_milp_motion_planning.pdf`](mit_16_410_lec18_milp_motion_planning.pdf)
— Математическое программирование в планировании.** Смешанно-целочисленное
линейное программирование (MILP); формулировка условий непересечения препятствий
методом «большого $M$»; оптимизация траектории при линейной динамике.

## Статья

**[`karaman_frazzoli_rrt_star_optimal_planning.pdf`](karaman_frazzoli_rrt_star_optimal_planning.pdf)**

S. Karaman, E. Frazzoli. Sampling-based Algorithms for Optimal Motion Planning.
*International Journal of Robotics Research*, 2011, vol. 30, no. 7, pp. 846–894.
MIT Laboratory for Information and Decision Systems.

Работа показывает, что PRM и RRT в исходной формулировке вероятностно полны, но
не асимптотически оптимальны: вероятность сходимости решения RRT к оптимальному
при $n \to \infty$ равна нулю. Авторы предлагают варианты $\text{PRM}^*$ и
$\text{RRT}^*$, в которых радиус окрестности убывает как
$r_n \propto (\log n / n)^{1/d}$, и доказывают их асимптотическую оптимальность.
В $\text{RRT}^*$ вводятся две дополнительные процедуры — выбор родителя с
наименьшей суммарной стоимостью и переподключение соседей (rewiring).
