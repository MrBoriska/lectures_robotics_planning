---
marp: true
theme: robotics-minimal
size: 16:9
paginate: true
header: "Планирование для мобильных роботов | Лекция 06"
footer: "Курс лекций • Лекция 06 • Слайд %PAGE% из %TOTAL%"
math: mathjax
---

<!-- _class: lead invert -->
<!-- _header: "" -->
<!-- _footer: "" -->

# **Планирование движений мобильных роботов**
## Лекция 06: [Название темы будет предоставлено]

<div class="mt-4">
  <span class="badge badge-blue">⏱️ Продолжительность: 90 минут</span>
  <span class="badge badge-green">Курс: Мобильная робототехника</span>
  <span class="badge badge-purple">Marp + Interactive Engine</span>
</div>

---

<!-- _header: "Лекция 06 | Структура занятия" -->

## Тайминг и структура лекции <span class="badge badge-time">⏱️ 90 минут</span>

<div class="grid-2 mt-4">

<div class="card card-accent">
  <h3>Часть 1: Теория и концепции (45 мин)</h3>
  <ul>
    <li><strong>00–15 мин:</strong> Мотивация, связь с предыдущей лекцией, постановка задачи.</li>
    <li><strong>15–35 мин:</strong> Математический аппарат и теоретический фундамент метода.</li>
    <li><strong>35–45 мин:</strong> Анализ допущений, свойств сходимости и вычислительной сложности.</li>
  </ul>
</div>

<div class="card card-accent">
  <h3>Часть 2: Алгоритмы и практика (45 мин)</h3>
  <ul>
    <li><strong>45–65 мин:</strong> Пошаговая реализация алгоритма, псевдокод и структуры данных.</li>
    <li><strong>65–75 мин:</strong> <span class="badge badge-green">Интерактивная демонстрация</span> и разбор поведения в симуляторе.</li>
    <li><strong>75–85 мин:</strong> Ограничения реальных роботов (динамика, шум сенсоров, латентность).</li>
    <li><strong>85–90 мин:</strong> Резюме, контрольные вопросы и дискуссия.</li>
  </ul>
</div>

</div>

---

## 1. Введение и постановка проблемы <span class="badge badge-time">00–15 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Контекст и предпосылки темы:</h3>
    <p>[Здесь будет размещено описание проблемы, мотивирующие примеры из реальной робототехники и связь с предыдущими занятиями курса.]</p>
    <ul>
      <li>Цель планирования в рамках данной парадигмы.</li>
      <li>Где и почему стандартные подходы терпят неудачу.</li>
      <li>Области применения: автономные автомобили, AGV, складские AMR, БПЛА.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-alert">
    <h3>Ключевые вызовы:</h3>
    <ul>
      <li>Вычислительная сложность в пространствах высокой размерности.</li>
      <li>Локальные экстремумы и неполнота информации.</li>
      <li>Динамические и неголономные ограничения шасси.</li>
    </ul>
  </div>
</div>

</div>

---

## 2. Теоретический базис и математическая модель <span class="badge badge-time">15–35 мин</span>

<div class="grid-2">

<div class="col">
  <p>Формальное описание целевой функции и пространства поиска:</p>

  <div class="formula-box">
    2690136J(\tau) = \int_{0}^{T} \mathcal{L}(x(t), u(t)) \, dt + \Phi(x(T))2690136
    2690136\text{s.t.} \quad \dot{x}(t) = f(x(t), u(t)), \quad x(t) \in \mathcal{X}_{free}2690136
  </div>

  <div class="card">
    <h3>Свойства пространства:</h3>
    <ul>
      <li>Топология пространства состояний.</li>
      <li>Метрика расстояния и функции допустимости.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card card-accent">
    <h3>Анализ сходимости и оптимальности:</h3>
    <ul>
      <li><strong>Вероятностная полнота (Probabilistic Completeness):</strong>
        2690136\lim_{N \to \infty} P(\text{нахождение пути} \mid \text{путь существует}) = 12690136
      </li>
      <li><strong>Асимптотическая оптимальность (Asymptotic Optimality):</strong>
        2690136\lim_{N \to \infty} \text{Cost}(Path_N) = c^*2690136
      </li>
    </ul>
  </div>
</div>

</div>

---

## 3. Алгоритмическое ядро и реализация <span class="badge badge-time">35–55 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card">
    <h3>Псевдокод алгоритма:</h3>
    <pre><code>def plan_trajectory(start, goal, obstacles):
    state_tree = initialize_tree(start)
    for iteration in range(MAX_ITER):
        target_sample = sample_space(goal_bias)
        nearest_node = find_nearest(state_tree, target_sample)
        new_state = propagate_model(nearest_node, target_sample)
        if collision_free(new_state, obstacles):
            state_tree.add(new_state)
            if reaches_goal(new_state, goal):
                return extract_optimal_path(new_state)
    return FAILURE</code></pre>
  </div>
</div>

<div class="col">
  <div class="card card-success">
    <h3>Ключевые оптимизации:</h3>
    <ul>
      <li><strong>Пространственные индексы:</strong> hBcd tree / R-tree для ускорения поиска ближайших соседей $\mathcal{O}(\log N)$.</li>
      <li><strong>Collision Checking:</strong> иерархии BVH (Bounding Volume Hierarchies).</li>
      <li><strong>Goal Biasing:</strong> адаптивное смещение выборки к целевой зоне.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _header: "Интерактивная практика | Лекция 06" -->

## Интерактивная демонстрация: Исследование алгоритма <span class="badge badge-green">⏱️ 55–70 мин</span>

<div class="interactive-container">
  <div class="interactive-header">
    <span><i class="interactive-dot"></i> Интерактивный алгоритмический симулятор</span>
    <span>Экспериментируйте с параметрами и картой препятствий в реальном времени</span>
  </div>
  <iframe src="../../widgets/astar-grid/index.html" class="interactive-frame"></iframe>
</div>

---

## 4. Специфика реального робота и интеграция в ROS <span class="badge badge-time">70–85 мин</span>

<div class="grid-2">

<div class="col">
  <div class="card card-accent">
    <h3>Учет физических ограничений:</h3>
    <ul>
      <li><strong>Пределы ускорений:</strong> $|a_v| \le a_{max}, \quad |\alpha_\omega| \le \alpha_{max}$.</li>
      <li><strong>Задержка контура управления (Latency):</strong> прогнозирование состояния вперед на время реакции системы ($\tau_{delay} \approx 50\text{--}100$ мс).</li>
      <li><strong>Отказоустойчивость:</strong> аварийное торможение при приближении динамического объекта.</li>
    </ul>
  </div>
</div>

<div class="col">
  <div class="card">
    <h3>Архитектурная интеграция (ROS 2 / Nav2):</h3>
    <ul>
      <li>Плагин для <code>nav2_core::GlobalPlanner</code> или <code>Controller</code>.</li>
      <li>Подписка на <code>/costmap/costmap_raw</code> и <code>/odom</code>.</li>
      <li>Публикация траектории в топик <code>/plan</code> и команд скорости в <code>/cmd_vel</code>.</li>
    </ul>
  </div>
</div>

</div>

---

<!-- _class: invert -->
<!-- _header: "Лекция 06 | Заключение" -->

## Резюме и вопросы для обсуждения <span class="badge badge-time">85–90 мин</span>

<div class="grid-2">

<div class="card">
  <h3>Главные выводы занятия:</h3>
  <ol>
    <li>Теоретические свойства и границы применимости изученного метода.</li>
    <li>Влияние настройки гиперпараметров на сходимость и вычислительную сложность.</li>
    <li>Практические особенности переноса с идеальной симуляции на физический робот.</li>
  </ol>
</div>

<div class="card card-accent">
  <h3>Контрольные вопросы:</h3>
  <ul>
    <li>При каких условиях алгоритм теряет свойство оптимальности?</li>
    <li>Как изменится поведение робота при зашумленной одометрии?</li>
    <li>Каков вычислительный предел метода при увеличении числа степеней свободы?</li>
  </ul>
</div>

</div>
