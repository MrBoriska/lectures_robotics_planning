# 📖 Стивен М. Лаваль: «Planning Algorithms» (Кембриджский университет)

В данной директории размещен полный текст фундаментального учебника:
* **Файл:** [`lavalle_planning_algorithms.pdf`](lavalle_planning_algorithms.pdf) (842 стр., Cambridge University Press)
* **Автор:** Prof. Steven M. LaValle (University of Illinois at Urbana-Champaign / University of Oulu)
* **Официальный ресурс:** [http://msl.cs.uiuc.edu/planning/](http://msl.cs.uiuc.edu/planning/)

---

## 🗺️ Тематическая структура книги и маппинг на курс

### Часть I: Дискретное планирование (Discrete Planning)
* **Глава 2: Discrete Planning**
  - Графы состояний, деревья поиска.
  - Поиск в ширину (BFS), поиск в глубину (DFS), алгоритм Дейкстры.
  - Алгоритм $A^*$ и свойства эвристических функций (Admissibility, Monotonicity / Consistency).
  - Динамическое программирование (принцип оптимальности Беллмана).
  - *Использование в курсе:* **Лекция 01** (Дискретный поиск и сеточные методы).

### Часть II: Планирование движений (Motion Planning)
* **Глава 3: Geometric Representations and Transformations**
  - Представление твердых тел в 2D и 3D ($SE(2), SE(3)$).
  - Матрицы однородных преобразований, кватернионы, углы Эйлера.
* **Глава 4: The Configuration Space ($\mathcal{C}$-space)**
  - Топология конфигурационного пространства, многообразия (Manifolds).
  - Препятствия в $\mathcal{C}$-space ($\mathcal{C}_{obs}$ и $\mathcal{C}_{free}$).
  - Сумма Минковского $\mathcal{O} \oplus (-\mathcal{A})$ и алгоритмы вычисления.
  - *Использование в курсе:* **Лекция 01** и **Лекция 02**.
* **Глава 5: Sampling-Based Motion Planning**
  - Вероятностные дорожные карты (PRM - Probabilistic Roadmaps).
  - Быстро исследующие случайные деревья (RRT - Rapidly-exploring Random Trees).
  - Метрики расхождения и дисперсии (Discrepancy & Dispersion), квазислучайные последовательности (Халтон, Соболь).
  - Проверка коллизий (Collision Detection).
  - *Использование в курсе:* **Лекция 02** и **Лекция 03**.
* **Глава 6: Combinatorial Motion Planning**
  - Графы видимости (Visibility Graphs).
  - Точная декомпозиция на ячейки (Exact Cellular Decomposition).
  - Диаграммы Вороного и обобщенные диаграммы (GVD).
* **Глава 7: Extensions of Basic Motion Planning**
  - Планирование в среде с подвижными препятствиями (Time-space planning).
  - Замкнутые кинематические цепи (Closed kinematic chains).
* **Глава 8: Feedback Motion Planning**
  - Поля потенциалов (Potential Fields, метод Хатиба).
  - Навигационные функции Римона-Кодичека (Navigation Functions) без локальных минимумов.
  - *Использование в курсе:* **Лекция 03** и **Лекция 04**.

### Часть IV: Планирование с дифференциальными связями (Differential Constraints)
* **Глава 13: Differential Models**
  - Фазовое пространство состояний $X$.
  - Неголономные связи (Nonholonomic constraints) колесных шасси:
    $$\dot{x} \sin\theta - \dot{y} \cos\theta = 0$$
  - Модель автомобиля Дубинса (Dubins car, только движение вперед).
  - Модель автомобиля Ридса-Шеппа (Reeds-Shepp car, движение вперед и назад).
  - Дифференциальный привод (Differential drive) и шасси с прицепом.
* **Глава 14: Sampling-Based Planning Under Differential Constraints**
  - Кинодинамическое планирование (Kinodynamic Planning).
  - Неголономный RRT (Nonholonomic RRT with forward integration of system dynamics).
  - Двунаправленные деревья под дифференциальными ограничениями.
* **Глава 15: System Theory and Analytical Techniques**
  - Управляемость по Ли (Lie brackets, алгебры Ли).
  - Скобки Ли для проверки неголономной интегрируемости связей.
  - *Использование в курсе:* **Лекции 05, 06, 07**.
