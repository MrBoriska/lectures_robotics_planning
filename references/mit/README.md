# 🇺🇸 MIT: Материалы курсов по планированию автономных систем

В данной директории размещены лекции и научные публикации Массачусетского технологического института (MIT):

### Файлы в директории:
1. [`mit_16_410_lec14_informed_search.pdf`](mit_16_410_lec14_informed_search.pdf)
   * **Курс:** MIT 16.410/16.413 «Principles of Autonomy and Decision Making»
   * **Лектор:** Prof. Emilio Frazzoli
   * **Тема:** Информированный поиск, $A^*$, алгоритм ветвей и границ (Branch & Bound), построение монотонных эвристик.
2. [`mit_16_410_lec15_sampling_based_planning.pdf`](mit_16_410_lec15_sampling_based_planning.pdf)
   * **Курс:** MIT 16.410/16.413
   * **Лектор:** Prof. Emilio Frazzoli
   * **Тема:** Сэмплирующие алгоритмы планирования в $\mathcal{C}$-space, Probabilistic Roadmaps (PRM), Rapidly-exploring Random Trees (RRT), вероятностная полнота (Probabilistic Completeness).
3. [`mit_16_410_lec18_milp_motion_planning.pdf`](mit_16_410_lec18_milp_motion_planning.pdf)
   * **Курс:** MIT 16.410/16.413
   * **Лектор:** Prof. Emilio Frazzoli
   * **Тема:** Математическое программирование в планировании: смешанно-целочисленное линейное программирование (MILP / Big-M method) для гарантированного избежания столкновений и оптимизации траекторий.
4. [`karaman_frazzoli_rrt_star_optimal_planning.pdf`](karaman_frazzoli_rrt_star_optimal_planning.pdf)
   * **Авторы:** Sertac Karaman & Emilio Frazzoli (MIT Laboratory for Information and Decision Systems - LIDS)
   * **Название:** *«Sampling-based Algorithms for Optimal Motion Planning»* (International Journal of Robotics Research - IJRR, 2011)
   * **Значение:** Фундаментальная статья, доказавшая, что классические алгоритмы PRM и RRT **не сходятся к оптимальному пути** с вероятностью 1 (вероятность нахождения оптимума равна нулю!), и предложившая революционные алгоритмы **$RRT^*$** и **$PRM^*$** с доказательством асимптотической оптимальности через переподключение соседей (rewiring).

---

## 🔬 Дополнительные ключевые курсы MIT для курса

* **MIT 6.832: Underactuated Robotics (Prof. Russ Tedrake):**
  - Оптимизация траекторий (Trajectory Optimization).
  - Методы прямой коллокации (Direct Collocation) и прямого выстреливания (Direct Shooting).
  - Неголономное планирование и дифференциальная плоскостность (Differential Flatness).
  - Инвариантные трубки управляемости (Funnel Library / Hamilton-Jacobi Reachability).
* **MIT 16.485: Visual Navigation for Autonomous Vehicles - VNAV (Prof. Luca Carlone):**
  - Интеграция SLAM и Trajectory Planning в динамических средах.
  - Построение локальных безопасных коридоров (Safe Flight Corridors) с помощью выпуклой оптимизации.
