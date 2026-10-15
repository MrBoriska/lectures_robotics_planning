#!/usr/bin/env python3
"""
generate_lectures_07_08_diagrams.py

Схемы к лекциям 07 (продвинутые методы: координаты Френе, имитационное
обучение, диффузионные политики, навигационные модели), 08 (антропоморфные
роботы: история, ZMP, LIPM, точка захвата, современные архитектуры) и к блоку
«от пути к движению» лекции 02 (сглаживание, профиль скорости).

Графики строятся расчётом, без внешних зависимостей:
- профиль скорости вдоль B-сплайна двумя проходами (как в виджете velocity-profile);
- трапецеидальный и S-образный профили скорости;
- геометрия координат Френе, семейство полиномов 5-й степени и веер кандидатов
  с проверкой столкновений (как в виджете frenet-planner);
- смесь гауссиан демонстраций, прямой процесс зашумления и обратный процесс DDPM
  с точной функцией оценки (как в виджете diffusion-policy-interactive);
- траектории согласования потоков и диффузии в одномерном примере;
- LIPM: расходимость, полоса захвата, походка как последовательность маятников;
- D* Lite на сетке (сравнение с A* с нуля) и пример g/rhs;
- условные силуэты роботов в одном масштабе (рост и масса по данным производителей).

Примитивы SVG и палитра берутся из generate_lectures_05_06_diagrams.py.

Запуск: python3 scripts/generate_lectures_07_08_diagrams.py
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_lectures_05_06_diagrams import (  # noqa: E402
    svg_open, text, line, polyline, polygon, circle, rect, Axes, legend, write,
    linspace, box, INK, MUTED, LIGHT, GRID, BLUE, SKY, GREEN, AMBER, RED, PURPLE,
    PANEL, ROOT,
)

OUT02 = os.path.join(ROOT, 'assets', 'images', 'lecture-02')
OUT07 = os.path.join(ROOT, 'assets', 'images', 'lecture-07')
OUT08 = os.path.join(ROOT, 'assets', 'images', 'lecture-08')


def arrow(x1, y1, x2, y2, color=MUTED, width=2.0, dash=None):
    mk = {MUTED: 'arr', BLUE: 'arrB', RED: 'arrR', GREEN: 'arrG', PURPLE: 'arrP', AMBER: 'arrA'}.get(color, 'arr')
    return line(x1, y1, x2, y2, color, width, dash, mk)


def wrap_lines(x, y, lines_, size=14, color=INK, anchor='start', dy=20, weight=400):
    return [text(x, y + i * dy, s, size, color, anchor, weight) for i, s in enumerate(lines_)]


# ===========================================================================
# Общие вычисления лекции 07
# ===========================================================================

def bspline(ctrl, per=200):
    """Равномерный кубический B-сплайн с повторёнными концами; точки и кривизна."""
    c = [ctrl[0], ctrl[0]] + list(ctrl) + [ctrl[-1], ctrl[-1]]
    pts, kap = [], []
    for i in range(len(c) - 3):
        for k in range(per):
            t = k / per
            t2, t3 = t * t, t * t * t
            B = [(1 - t) ** 3 / 6, (3 * t3 - 6 * t2 + 4) / 6, (-3 * t3 + 3 * t2 + 3 * t + 1) / 6, t3 / 6]
            D = [-((1 - t) ** 2) / 2, (3 * t2 - 4 * t) / 2, (-3 * t2 + 2 * t + 1) / 2, t2 / 2]
            DD = [1 - t, 3 * t - 2, -3 * t + 1, t]
            comb = lambda w, d: sum(w[m] * c[i + m][d] for m in range(4))
            x1, y1, x2, y2 = comb(D, 0), comb(D, 1), comb(DD, 0), comb(DD, 1)
            sp = math.hypot(x1, y1)
            pts.append((comb(B, 0), comb(B, 1)))
            kap.append(abs(x1 * y2 - y1 * x2) / sp ** 3 if sp > 1e-9 else 0.0)
    pts.append(tuple(ctrl[-1]))
    kap.append(0.0)
    return pts, kap


def arclen(pts):
    s = [0.0]
    for i in range(1, len(pts)):
        s.append(s[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    return s


def resample(pts, kap, ds=0.02):
    cum = arclen(pts)
    L = cum[-1]
    n = max(2, round(L / ds))
    xy, kk, j = [], [], 0
    for k in range(n + 1):
        s = L * k / n
        while j < len(cum) - 2 and cum[j + 1] < s:
            j += 1
        seg = (cum[j + 1] - cum[j]) or 1
        a = min(1, max(0, (s - cum[j]) / seg))
        xy.append((pts[j][0] + a * (pts[j + 1][0] - pts[j][0]), pts[j][1] + a * (pts[j + 1][1] - pts[j][1])))
        kk.append(kap[j] + a * (kap[j + 1] - kap[j]))
    return xy, kk, L / n, L


def two_pass(vlim, ds, at):
    n = len(vlim)
    vf, vb = [0.0] * n, [0.0] * n
    for i in range(n - 1):
        vf[i + 1] = min(vlim[i + 1], math.sqrt(vf[i] ** 2 + 2 * at * ds))
    for i in range(n - 1, 0, -1):
        vb[i - 1] = min(vlim[i - 1], math.sqrt(vb[i] ** 2 + 2 * at * ds))
    v = [min(a, b) for a, b in zip(vf, vb)]
    T = sum(2 * ds / (v[i] + v[i + 1]) for i in range(n - 1) if v[i] + v[i + 1] > 1e-9)
    return vf, vb, v, T


TURN = [(0, 0), (7, 0), (7, 5)]
VMAX, AT, AN = 2.0, 0.8, 0.6


def turn_profile():
    pts, kap = bspline(TURN)
    xy, kk, ds, L = resample(pts, kap)
    vlim = [min(VMAX, math.sqrt(AN / k) if k > 1e-6 else 1e9) for k in kk]
    vf, vb, v, T = two_pass(vlim, ds, AT)
    return xy, kk, ds, L, vlim, vf, vb, v, T


# ===========================================================================
# Лекция 02 (дополнение) и место лекции 07: траектория по пути
# ===========================================================================

def l07_course_place():
    W, H = 1100, 300
    out = svg_open(W, H)
    out.append(text(550, 30, 'Где применяются методы лекции 07 в системе управления мобильным роботом', 18, INK, 'middle', 700))
    blocks = [
        ('Глобальный путь', ['A*, RRT*, лекции 02–04;', 'D* Lite при новой карте'], BLUE, '#eff6ff'),
        ('Траектория по пути', ['сглаживание и профиль', 'скорости, лекция 02'], INK, PANEL),
        ('Локальный план', ['DWA, MPPI, MPC,', 'решётка Френе'], BLUE, '#eff6ff'),
        ('Регуляторы приводов', ['скорости и моменты', '≈ 1 кГц'], INK, PANEL),
    ]
    x = 30
    for i, (t, s, c, f) in enumerate(blocks):
        out += box(x, 60, 230, 100, t, s, c, f, 16, 14)
        if i < 3:
            out.append(arrow(x + 230, 110, x + 262, 110, MUTED, 2.2))
        x += 265
    out.append(rect(30, 190, 1040, 90, '#faf5ff', PURPLE, 10, 1.6, '6 4'))
    out.append(text(48, 216, 'Обучаемые политики (части 3–4 лекции)', 16, PURPLE, 'start', 700))
    out += wrap_lines(48, 242, ['Диффузионная политика или NoMaD заменяет блоки «траектория» и «локальный план»: по изображениям сразу выдаёт',
                                'последовательность действий на ближайшие секунды. Классические блоки остаются как проверка безопасности.'], 14, INK)
    out.append(text(145, 52, 'часть 1', 13, BLUE, 'middle', 700))
    out.append(text(675, 52, 'часть 2', 13, BLUE, 'middle', 700))
    write(os.path.join(OUT07, 'course_place.svg'), out)


def l07_path_vs_trajectory():
    xy, kk, ds, L, vlim, vf, vb, v, T = turn_profile()
    W, H = 1100, 380
    out = svg_open(W, H)
    out.append(text(275, 30, 'Путь: где проехать', 17, INK, 'middle', 700))
    out.append(text(800, 30, 'Профиль скорости: как быстро', 17, INK, 'middle', 700))
    # план
    a = Axes(60, 50, 420, 290, (-1, 8.5), (-1, 5.6))
    sc_x = lambda x: a.px(x)
    out.append(polyline([a.p(*p) for p in TURN], LIGHT, 1.6, '6 5'))
    out.append(polyline([a.p(*p) for p in xy], BLUE, 4))
    for s_mark in range(2, int(L) + 1, 2):
        i = min(len(xy) - 1, round(s_mark / ds))
        out.append(circle(*a.p(*xy[i]), 5, '#fff', BLUE, 2))
        out.append(text(a.px(xy[i][0]) + (12 if s_mark < 8 else -12), a.py(xy[i][1]) + (20 if s_mark < 8 else 4), f's = {s_mark}', 13, BLUE, 'start' if s_mark < 8 else 'end'))
    out.append(circle(*a.p(0, 0), 7, INK))
    out.append(circle(*a.p(7, 5), 7, GREEN))
    out.append(text(a.px(0), a.py(0) + 28, 'старт', 13, INK, 'middle'))
    out.append(text(a.px(7) + 12, a.py(5) + 5, 'цель', 13, GREEN, 'start'))
    out.append(text(a.px(4.5), a.py(3.6), 'x(s), y(s) — точка пути', 14, INK, 'middle'))
    out.append(text(a.px(4.5), a.py(3.6) + 20, 's — пройденная длина, м', 14, MUTED, 'middle'))
    # профиль
    b = Axes(620, 60, 440, 250, (0, L), (0, 2.3))
    out += b.frame(xticks=range(0, int(L) + 1, 2), yticks=(0, 1, 2), xlabel='s, м', ylabel='v(s), м/с')
    out.append(polyline([b.p(i * ds, min(2.3, vl)) for i, vl in enumerate(vlim)], AMBER, 2.2))
    out.append(polyline([b.p(i * ds, vv) for i, vv in enumerate(v)], GREEN, 3.4))
    out.append(text(b.px(6.3), b.py(0.95), 'поворот: v ≤ √(a_{n,max}/κ)', 13, AMBER, 'middle', 700))
    out.append(text(b.px(1.0), b.py(2.12), 'v_{max}', 13, AMBER, 'start', 700))
    out.append(text(b.px(2.6), b.py(0.55), 'разгон', 13, GREEN, 'middle', 700))
    out.append(text(b.px(9.4), b.py(0.75), 'торможение', 13, GREEN, 'middle', 700))
    out.append(text(840, 362, f'Время по профилю: T = {T:.2f} с (v_{{max}} = 2 м/с, a_{{t,max}} = 0.8 м/с², a_{{n,max}} = 0.6 м/с²)', 13, MUTED, 'middle'))
    write(os.path.join(OUT02, 'path_vs_trajectory.svg'), out)
    return T


def l07_smoothing_curvature():
    ctrl = [(0, 0), (3, 0), (3, 3), (6, 3)]
    pts, kap = bspline(ctrl)
    xy, kk, ds, L = resample(pts, kap)
    W, H = 1100, 360
    out = svg_open(W, H)
    a = Axes(50, 60, 360, 250, (-0.6, 6.6), (-0.8, 3.8))
    out.append(text(230, 34, 'Ломаная A* и сглаженный путь', 16, INK, 'middle', 700))
    out.append(polyline([a.p(*p) for p in ctrl], RED, 2.6))
    out.append(polyline([a.p(*p) for p in xy], BLUE, 3))
    for p in ctrl:
        out.append(circle(*a.p(*p), 6, '#fff', RED, 2))
    out.append(text(a.px(3) + 10, a.py(0) + 4, 'P₁', 14, RED))
    out.append(text(a.px(3) - 10, a.py(3) - 10, 'P₂', 14, RED, 'end'))
    out += legend(70, 330, [('ломаная (контрольные точки)', RED, None)], 13)
    out += legend(320, 330, [('B-сплайн', BLUE, None)], 13)
    # кривизна (по доле пройденного пути, чтобы сравнить пути разной длины)
    b = Axes(520, 60, 540, 230, (0, 1), (0, 2.0))
    out.append(text(790, 34, 'Кривизна вдоль пути κ = dθ/ds', 16, INK, 'middle', 700))
    out += b.frame(xticks=(0, 0.25, 0.5, 0.75, 1), yticks=(0, 0.5, 1, 1.5, 2), xlabel='доля пройденного пути s/L', ylabel='κ, 1/м')
    out.append(polyline([b.p(i * ds / L, min(2, k)) for i, k in enumerate(kk)], BLUE, 2.6))
    for sv in (1 / 3, 2 / 3):
        X = b.px(sv)
        out.append(line(X, b.py(0), X, b.py(1.95), RED, 2.6, None, 'arrR'))
    out.append(text(b.px(0.5), b.py(1.6), 'ломаная: κ = ∞ в вершинах', 13, RED, 'middle', 700))
    out.append(line(b.px(0), b.py(0) - 1, b.px(1), b.py(0) - 1, RED, 2.6))
    kmax = max(kk)
    out.append(text(b.px(0.69), b.py(min(2, kmax)) - 30, f'сплайн: max κ = {kmax:.2f} 1/м,', 13, BLUE, 'start', 700))
    out.append(text(b.px(0.7), b.py(min(2, kmax)) - 12, f'R_{{min}} = {1 / kmax:.2f} м', 13, BLUE, 'start', 700))
    write(os.path.join(OUT02, 'smoothing_curvature.svg'), out)
    return kmax


def l07_two_pass():
    xy, kk, ds, L, vlim, vf, vb, v, T = turn_profile()
    W, H = 1100, 400
    out = svg_open(W, H)
    a = Axes(70, 50, 700, 290, (0, L), (0, 2.4))
    out += a.frame(xticks=range(0, int(L) + 1), yticks=(0, 0.5, 1, 1.5, 2), xlabel='s, м', ylabel='v, м/с')
    top = [a.p(0, 2.4)] + [a.p(i * ds, min(2.4, vl)) for i, vl in enumerate(vlim)] + [a.p(L, 2.4)]
    out.append(polygon(top, '#fef3c7', 0.7))
    out.append(polyline([a.p(i * ds, min(2.4, x)) for i, x in enumerate(vf)], BLUE, 2.2, '7 5'))
    out.append(polyline([a.p(i * ds, min(2.4, x)) for i, x in enumerate(vb)], RED, 2.2, '7 5'))
    out.append(polyline([a.p(i * ds, min(2.4, x)) for i, x in enumerate(vlim)], AMBER, 2.4))
    out.append(polyline([a.p(i * ds, x) for i, x in enumerate(v)], GREEN, 3.6))
    out.append(text(a.px(5.6), a.py(2.25), 'запрещено: v > v_{lim}(s)', 13, AMBER, 'middle', 700))
    out += legend(800, 80, [('v_{lim}(s) — предел скорости', AMBER, None), ('прямой проход: разгон', BLUE, '7 5'),
                            ('обратный проход: торможение', RED, '7 5'), ('итог: наименьшая из кривых', GREEN, None)], 14, 26)
    out += wrap_lines(800, 210, ['1. v_{lim}(s) = min(v_{max}, √(a_{n,max}/κ(s)))', '2. вперёд: v_f ← min(v_{lim}, √(v_f² + 2aΔs))',
                                 '3. назад:  v_b ← min(v_{lim}, √(v_b² + 2aΔs))', '4. v(s) = min(v_f, v_b)'], 14, INK, dy=24)
    out.append(text(800, 320, f'Время проезда T = {T:.2f} с', 14, GREEN, 'start', 700))
    write(os.path.join(OUT02, 'two_pass_profile.svg'), out)


def l07_trapezoid_scurve():
    """Перемещение на 4 м. Трапеция: |a| ≤ 1 м/с², v ≤ 1.5 м/с.
    S-образный профиль получен сглаживанием скорости трапеции скользящим средним
    шириной t_j = a_max / j_max = 0.5 с: путь сохраняется, ускорение становится
    трапецией, рывок ограничен j_max = 2 м/с³, время растёт ровно на t_j."""
    D, V, A, J = 4.0, 1.5, 1.0, 2.0
    tj = A / J
    ta = V / A
    Ttr = D / V + ta
    dt = 0.001

    def v_tr(t):
        if t <= 0 or t >= Ttr:
            return 0.0
        return min(A * t, V, A * (Ttr - t))

    n = int((Ttr + tj) / dt) + 1
    ts = [k * dt for k in range(n + 1)]
    vt = [v_tr(t) for t in ts]
    m = int(tj / dt)
    vs, acc = [], 0.0
    for k in range(len(ts)):
        acc += vt[k]
        if k >= m:
            acc -= vt[k - m]
        vs.append(acc / m)

    def deriv(arr):
        return [(arr[min(len(arr) - 1, k + 1)] - arr[max(0, k - 1)]) / (dt * (min(len(arr) - 1, k + 1) - max(0, k - 1))) for k in range(len(arr))]
    a_tr, a_s = deriv(vt), deriv(vs)
    j_s = deriv(a_s)
    W, H = 1100, 380
    out = svg_open(W, H)
    tmax = Ttr + tj + 0.2
    panels = [('v(t), м/с', vt, vs, (-0.1, 1.8), (0, 0.5, 1, 1.5)), ('a(t), м/с²', a_tr, a_s, (-1.3, 1.3), (-1, 0, 1)),
              ('рывок j(t), м/с³', None, j_s, (-2.6, 2.6), (-2, 0, 2))]
    for k, (lab, ytr, ys, yl, yt) in enumerate(panels):
        a = Axes(60 + k * 350, 60, 300, 230, (0, tmax), yl)
        out += a.frame(xticks=range(0, int(tmax) + 1), yticks=yt, xlabel='t, с', ylabel=lab)
        st = 10
        if ytr is not None:
            out.append(polyline([a.p(ts[i], ytr[i]) for i in range(0, len(ts), st)], RED, 2.4))
        else:
            out.append(text(a.px(tmax / 2), a.py(2.25), 'у трапеции рывок бесконечен', 13, RED, 'middle', 700))
            out.append(text(a.px(tmax / 2), a.py(2.25) + 16, 'в моменты скачков a(t)', 13, RED, 'middle'))
        out.append(polyline([a.p(ts[i], max(yl[0], min(yl[1], ys[i]))) for i in range(0, len(ts), st)], BLUE, 2.4))
    out += legend(60, 345, [('трапецеидальный: |a| ≤ 1 м/с²', RED, None)], 14)
    out += legend(420, 345, [('S-образный: |a| ≤ 1 м/с², |j| ≤ 2 м/с³', BLUE, None)], 14)
    out.append(text(60, 32, f'Перемещение на {D:g} м: трапеция за {Ttr:.2f} с, S-образный профиль за {Ttr + tj:.2f} с', 16, INK, 'start', 700))
    write(os.path.join(OUT02, 'trapezoid_scurve.svg'), out)
    return Ttr, Ttr + tj



# ===========================================================================
# Лекция 07. Часть 1: координаты Френе
# ===========================================================================

def catmull(points, per=60):
    out = []
    P = points
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(len(P) - 1, i + 2)]
        for k in range(per):
            t = k / per
            t2, t3 = t * t, t * t * t
            f = lambda a, b, c, d: 0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3)
            out.append((f(p0[0], p1[0], p2[0], p3[0]), f(p0[1], p1[1], p2[1], p3[1])))
    out.append(tuple(P[-1]))
    return out


class RefLine:
    def __init__(self, pts):
        dense = catmull(pts)
        self.cum = arclen(dense)
        self.pts = dense

    def at(self, s):
        cum, P = self.cum, self.pts
        s = max(0, min(cum[-1] - 1e-6, s))
        lo, hi = 0, len(cum) - 1
        while hi - lo > 1:
            m = (lo + hi) // 2
            if cum[m] <= s:
                lo = m
            else:
                hi = m
        a = (s - cum[lo]) / ((cum[hi] - cum[lo]) or 1)
        x = P[lo][0] + a * (P[hi][0] - P[lo][0])
        y = P[lo][1] + a * (P[hi][1] - P[lo][1])
        th = math.atan2(P[hi][1] - P[lo][1], P[hi][0] - P[lo][0])
        return x, y, th

    def xy(self, s, d):
        x, y, th = self.at(s)
        return x - d * math.sin(th), y + d * math.cos(th)


def quintic(x0, v0, a0, x1, v1, a1, T):
    c0, c1, c2 = x0, v0, a0 / 2
    b0 = x1 - (c0 + c1 * T + c2 * T * T)
    b1 = v1 - (c1 + 2 * c2 * T)
    b2 = a1 - 2 * c2
    c3 = (10 * b0 - 4 * b1 * T + 0.5 * b2 * T * T) / T ** 3
    c4 = (-15 * b0 + 7 * b1 * T - b2 * T * T) / T ** 4
    c5 = (6 * b0 - 3 * b1 * T + 0.5 * b2 * T * T) / T ** 5
    return [c0, c1, c2, c3, c4, c5]


def pev(c, t):
    p = sum(c[k] * t ** k for k in range(6))
    v = sum(k * c[k] * t ** (k - 1) for k in range(1, 6))
    a = sum(k * (k - 1) * c[k] * t ** (k - 2) for k in range(2, 6))
    j = sum(k * (k - 1) * (k - 2) * c[k] * t ** (k - 3) for k in range(3, 6))
    return p, v, a, j


def l07_frenet_frame():
    ref = RefLine([(0, 0), (4, 0.3), (8, 2.2), (12, 3.0), (16, 2.4)])
    W, H = 1100, 380
    out = svg_open(W, H)
    a = Axes(30, 30, 660, 330, (-1.5, 18.5), (-3.0, 7.0))
    out.append(f'<clipPath id="ffc"><rect x="{a.x0}" y="{a.y0}" width="{a.w}" height="{a.h}"/></clipPath>')
    out.append('<g clip-path="url(#ffc)">')
    S = ref.cum[-1]
    for d, col, wdt, dash in ((-1.75, MUTED, 2, None), (5.25, MUTED, 2, None), (1.75, LIGHT, 1.6, '10 8')):
        out.append(polyline([a.p(*ref.xy(s, d)) for s in linspace(0, S, 200)], col, wdt, dash))
    out.append(polyline([a.p(*ref.xy(s, 0)) for s in linspace(0, S, 200)], PURPLE, 3))
    s0, d0 = 9.0, 3.2
    rx, ry, th = ref.at(s0)
    px_, py_ = ref.xy(s0, d0)
    out.append(polyline([a.p(*ref.xy(s, -1.0)) for s in linspace(0, s0, 60)], PURPLE, 2, '4 4', marker='arrP'))
    out.append('</g>')
    ex, ey = ref.xy(S - 0.5, 0)
    out.append(text(a.px(ex), a.py(ey) + 26, 'опорная линия r(s)', 14, PURPLE, 'end', 700))
    mx, my = ref.xy(s0 / 2 - 1, -1.0)
    out.append(text(a.px(mx), a.py(my) + 20, 's — длина вдоль линии', 14, PURPLE, 'middle', 700))
    tx, ty = math.cos(th), math.sin(th)
    out.append(arrow(a.px(rx), a.py(ry), a.px(rx + 2.4 * tx), a.py(ry + 2.4 * ty), BLUE, 2.4))
    out.append(text(a.px(rx + 2.6 * tx), a.py(ry + 2.6 * ty) + 18, 't(s)', 15, BLUE, 'start', 700))
    out.append(arrow(a.px(rx), a.py(ry), a.px(px_), a.py(py_), GREEN, 2.6))
    out.append(text(a.px((rx + px_) / 2) - 10, a.py((ry + py_) / 2), 'd', 18, GREEN, 'end', 700))
    out.append(circle(a.px(rx), a.py(ry), 6, PURPLE))
    out.append(circle(a.px(px_), a.py(py_), 8, RED, '#fff', 2))
    out.append(text(a.px(px_) + 12, a.py(py_) - 8, 'робот P', 15, RED, 'start', 700))
    out += wrap_lines(730, 60, ['Координаты Френе: (s, d)'], 17, INK, weight=700)
    out += wrap_lines(730, 100, ['s — сколько проехано вдоль дороги;', 'd — насколько робот левее (d > 0)', 'или правее (d < 0) опорной линии.',
                                 '', 'Переход обратно в (x, y):', '  P = r(s) + d · n(s),', '  n(s) — единичная нормаль к линии.',
                                 '', 'Прямая и извилистая дорога', 'в координатах (s, d) выглядят', 'одинаково: полоса — это d ≈ const.'], 15, INK, dy=23)
    write(os.path.join(OUT07, 'frenet_frame.svg'), out)

def l07_quintic_family():
    W, H = 1100, 390
    out = svg_open(W, H)
    out.append(text(550, 28, 'Перестроение на соседнюю полосу (d: 0 → 3.5 м) полиномом 5-й степени за разное время T', 16, INK, 'middle', 700))
    a = Axes(70, 70, 460, 240, (0, 5.2), (-0.3, 4.0))
    out += a.frame(xticks=range(0, 6), yticks=(0, 1.75, 3.5), xlabel='t, с', ylabel='смещение d(t), м')
    b = Axes(620, 70, 440, 240, (0, 5.2), (-12, 12))
    out += b.frame(xticks=range(0, 6), yticks=(-10, -5, 0, 5, 10), xlabel='t, с', ylabel='рывок j(t) = d‴(t), м/с³')
    out.append(b.clip_id('qfc'))
    cols = [RED, AMBER, GREEN, BLUE]
    res = []
    for T, c in zip((2, 3, 4, 5), cols):
        co = quintic(0, 0, 0, 3.5, 0, 0, T)
        ts = linspace(0, T, 80)
        out.append(polyline([a.p(t, pev(co, t)[0]) for t in ts] + [a.p(5.2, 3.5)], c, 2.6))
        out.append(f'<g clip-path="url(#qfc)">' + polyline([b.p(t, pev(co, t)[3]) for t in ts], c, 2.2) + '</g>')
        Jj = sum(pev(co, t)[3] ** 2 for t in linspace(0, T, 400)) * T / 399
        res.append((T, Jj))
    out += legend(80, 352, [(f'T = {T} с: ∫j² dt = {J:.1f}', c, None) for (T, J), c in zip(res[:2], cols[:2])], 13)
    out += legend(330, 352, [(f'T = {T} с: ∫j² dt = {J:.1f}', c, None) for (T, J), c in zip(res[2:], cols[2:])], 13)
    out.append(text(840, 356, 'Вдвое короче манёвр — рывок в 8 раз больше (∝ 1/T³)', 13, MUTED, 'middle'))
    write(os.path.join(OUT07, 'quintic_family.svg'), out)
    return res

def l07_frenet_fan():
    ref = RefLine([(-5, 0), (0, 0), (20, 0), (40, 5), (60, 6), (80, 3)])
    obs_s, obs_d = 30.0, 0.0
    W, H = 1100, 350
    out = svg_open(W, H)
    a = Axes(30, 40, 1040, 275, (-2, 66), (-6, 12))
    out.append(a.clip_id('fanc'))
    out.append('<g clip-path="url(#fanc)">')
    sc = a.w / 68
    for d, col, wdt, dash in ((-1.75, MUTED, 2.2, None), (5.25, MUTED, 2.2, None), (1.75, LIGHT, 1.6, '12 10')):
        out.append(polyline([a.p(*ref.xy(s, d)) for s in linspace(0, 70, 140)], col, wdt, dash))
    ego_s, v = 8.0, 10.0
    best, cnt = None, {'ok': 0, 'col': 0}
    cands = []
    for dT in (-0.6, 0, 0.6, 1.75, 2.9, 3.5, 4.1):
        for T in (2, 3, 4, 5):
            co = quintic(0, 0, 0, dT, 0, 0, T)
            pts, col = [], False
            for t in linspace(0, 4.5, 46):
                d = pev(co, min(t, T))[0]
                s = ego_s + v * t
                pts.append(ref.xy(s, d))
                if abs(s - obs_s) < 5 and abs(d - obs_d) < 2.2:
                    col = True
            Jj = sum(pev(co, t)[3] ** 2 for t in linspace(0, T, 200)) * T / 199
            off = min(abs(dT), abs(dT - 3.5))
            cost = 0.1 * Jj + 5 * T + off * off + (3 if dT > 1.75 else 0)
            cands.append((pts, col, cost))
            if not col and (best is None or cost < best[2]):
                best = (pts, col, cost)
    for pts, col, cost in cands:
        cnt['col' if col else 'ok'] += 1
        out.append(polyline([a.p(*p) for p in pts], '#fca5a5' if col else '#93c5fd', 1.4))
    out.append(polyline([a.p(*p) for p in best[0]], GREEN, 3.6))

    def car(s, d, fill):
        x, y, th = ref.at(s)
        cx, cy = ref.xy(s, d)
        X, Y = a.p(cx, cy)
        ang = -math.degrees(th)
        return (f'<g transform="translate({X:.1f},{Y:.1f}) rotate({ang:.1f})">'
                f'<rect x="{-2.25 * sc:.1f}" y="{-0.9 * sc:.1f}" width="{4.5 * sc:.1f}" height="{1.8 * sc:.1f}" rx="3" fill="{fill}"/></g>')
    out.append(car(obs_s, obs_d, RED))
    out.append(car(ego_s, 0, BLUE))
    out.append('</g>')
    out.append(text(a.px(ref.xy(ego_s, 0)[0]), a.py(ref.xy(ego_s, 0)[1]) + 26, 'робот', 13, BLUE, 'middle', 700))
    ox, oy = ref.xy(obs_s, obs_d)
    out.append(text(a.px(ox), a.py(oy) + 28, 'стоящая машина', 13, RED, 'middle', 700))
    out.append(text(40, 24, f'Веер из {len(cands)} кандидатов (7 конечных смещений × 4 длительности): {cnt["col"]} пересекают препятствие, {cnt["ok"]} допустимы', 16, INK, 'start', 700))
    out += legend(40, 338, [('выбранный: наименьшая стоимость J среди допустимых', GREEN, None)], 13)
    out += legend(470, 338, [('допустимые', '#93c5fd', None)], 13)
    out += legend(640, 338, [('столкновение', '#fca5a5', None)], 13)
    write(os.path.join(OUT07, 'frenet_fan.svg'), out)
    return cnt


# ===========================================================================
# Лекция 07. Части 2–3: имитация, диффузия, NoMaD
# ===========================================================================

def l07_covariate_shift():
    W, H = 1100, 380
    out = svg_open(W, H)
    out.append(text(330, 30, 'Почему простое копирование действий эксперта уводит робота', 16, INK, 'middle', 700))
    a = Axes(50, 50, 560, 260, (0, 10), (-2.4, 2.4))
    out.append(rect(a.x0, a.py(1.2), a.w, a.py(-1.2) - a.py(1.2), '#f1f5f9', GRID, 0, 1))
    out.append(text(a.px(0.2), a.py(1.2) - 8, 'коридор: здесь были демонстрации', 13, MUTED))
    out.append(line(a.px(0), a.py(0), a.px(10), a.py(0), GREEN, 3))
    # клонирование: малая ошибка → незнакомое состояние → ошибка растёт; дальше от данных — хуже
    bc = [a.p(t, min(2.3, 0.022 * t * t + 0.0025 * t ** 3)) for t in linspace(0, 10, 80)]
    out.append(polyline(bc, RED, 2.8))
    dg = [a.p(t, 0.12 * math.sin(1.3 * t) * math.exp(-0.05 * t) + 0.05) for t in linspace(0, 10, 80)]
    out.append(polyline(dg, BLUE, 2.6, '7 4'))
    out.append(text(a.px(9.6), a.py(2.05), 'клонирование:', 13, RED, 'end', 700))
    out.append(text(a.px(9.6), a.py(2.05) + 16, 'ушёл из коридора', 13, RED, 'end'))
    out.append(text(a.px(7.0), a.py(-0.55), 'DAgger: остаётся рядом', 13, BLUE, 'middle', 700))
    out.append(text(a.px(3.0), a.py(0) + 18, 'эксперт', 13, GREEN, 'middle', 700))
    b = Axes(720, 60, 340, 230, (0, 50), (0, 50))
    out += b.frame(xticks=(0, 25, 50), yticks=(0, 25, 50), xlabel='длина эпизода T, шагов', ylabel='ожидаемое число ошибок')
    eps = 0.02
    out.append(polyline([b.p(T, min(50, eps * T * T)) for T in linspace(0, 50, 60)], RED, 2.6))
    out.append(polyline([b.p(T, eps * T * 10) for T in linspace(0, 50, 60)], BLUE, 2.6, '7 4'))
    out.append(text(b.px(36), b.py(44), 'клонирование ~ εT²', 13, RED, 'end', 700))
    out.append(text(b.px(48), b.py(13), 'DAgger ~ εT', 13, BLUE, 'end', 700))
    out.append(text(890, 362, 'ε — доля ошибок на состояниях из демонстраций (Ross et al., 2011)', 13, MUTED, 'middle'))
    write(os.path.join(OUT07, 'covariate_shift.svg'), out)



# --- смесь гауссиан траекторий (как в виджете) ---
M_PTS, AMP, SIG, ELL = 14, 1.55, 0.22, 2.5
XS = [-4.5 + (j + 1) / (M_PTS + 1) * 9 for j in range(M_PTS)]
MU_L = [AMP * math.sin(math.pi * (j + 1) / (M_PTS + 1)) for j in range(M_PTS)]
MU_R = [-v for v in MU_L]
SIGMA = [[SIG * SIG * math.exp(-((i - j) ** 2) / (2 * ELL * ELL)) + (1e-4 if i == j else 0) for j in range(M_PTS)] for i in range(M_PTS)]


def jacobi(S):
    n = len(S)
    a = [r[:] for r in S]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(60):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off < 1e-18:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-15:
                    continue
                th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(n)], V


LAM, U = jacobi(SIGMA)


def toE(y):
    return [sum(U[i][k] * y[i] for i in range(M_PTS)) for k in range(M_PTS)]


def fromE(z):
    return [sum(U[i][k] * z[k] for k in range(M_PTS)) for i in range(M_PTS)]


def sample_data(rng, left):
    z = [math.sqrt(max(0, l)) * rng.gauss(0, 1) for l in LAM]
    e = fromE(z)
    mu = MU_L if left else MU_R
    return [e[i] + mu[i] for i in range(M_PTS)]


def score(y, ab, wL=0.5):
    s = math.sqrt(ab)
    terms = []
    for mu, w in ((MU_L, wL), (MU_R, 1 - wL)):
        e = toE([y[i] - s * mu[i] for i in range(M_PTS)])
        q, wv = 0.0, []
        for k in range(M_PTS):
            d = ab * LAM[k] + 1 - ab
            q += e[k] * e[k] / d
            wv.append(e[k] / d)
        terms.append((math.log(w) - 0.5 * q, fromE(wv)))
    mx = max(t[0] for t in terms)
    r = [math.exp(t[0] - mx) for t in terms]
    tot = sum(r)
    r = [x / tot for x in r]
    return [-(r[0] * terms[0][1][i] + r[1] * terms[1][1][i]) for i in range(M_PTS)]


def abar(k, K):
    f = lambda x: math.cos((x + 0.008) / 1.008 * math.pi / 2) ** 2
    return min(0.9999, max(1e-4, f(k / K) / f(0)))


def ddpm_run(K, n, seed):
    rng = random.Random(seed)
    ys = [[rng.gauss(0, 1) for _ in range(M_PTS)] for _ in range(n)]
    snaps = {K: [y[:] for y in ys]}
    for step in range(K):
        k = K - step
        ab = abar(k, K)
        abp = abar(k - 1, K) if k - 1 > 0 else 1.0
        alpha = ab / abp
        beta = 1 - alpha
        new = []
        for y in ys:
            sc = score(y, ab)
            eps = [-math.sqrt(1 - ab) * v for v in sc]
            mean = [(y[i] - beta / math.sqrt(1 - ab) * eps[i]) / math.sqrt(alpha) for i in range(M_PTS)]
            if k - 1 > 0:
                sig = math.sqrt((1 - abp) / (1 - ab) * beta)
                mean = [m + sig * rng.gauss(0, 1) for m in mean]
            new.append(mean)
        ys = new
        snaps[k - 1] = [y[:] for y in ys]
    return snaps


def scene_axes(x0, y0, w, h):
    return Axes(x0, y0, w, h, (-5, 5), (-3.0, 3.0))


def draw_scene(a, trajs, color, width=1.6, opacity=1.0, obstacle=True, endpoints=True):
    out = []
    if obstacle:
        r = 0.9 * a.w / 10
        out.append(f'<circle cx="{a.px(0):.1f}" cy="{a.py(0):.1f}" r="{r:.1f}" fill="#fee2e2" stroke="{RED}" stroke-width="2"/>')
    for y in trajs:
        pts = [a.p(-4.5, 0)] + [a.p(XS[i], max(-3, min(3, y[i]))) for i in range(M_PTS)] + [a.p(4.5, 0)]
        out.append(polyline(pts, color, width, opacity=opacity))
    if endpoints:
        out.append(circle(*a.p(-4.5, 0), 6, INK))
        out.append(circle(*a.p(4.5, 0), 6, GREEN))
    return out


def l07_mse_vs_modes():
    rng = random.Random(7)
    demos = [sample_data(rng, rng.random() < 0.5) for _ in range(30)]
    mean = [0.5 * (l + r) for l, r in zip(MU_L, MU_R)]
    W, H = 1100, 330
    out = svg_open(W, H)
    a = scene_axes(40, 60, 480, 230)
    out.append(rect(a.x0, a.y0, a.w, a.h, '#ffffff', GRID, 6, 1))
    out += draw_scene(a, demos, MUTED, 1.3, 0.5)
    out.append(text(a.x0 + a.w / 2, 40, 'Демонстрации: объезд слева или справа (поровну)', 15, INK, 'middle', 700))
    b = scene_axes(580, 60, 480, 230)
    out.append(rect(b.x0, b.y0, b.w, b.h, '#ffffff', GRID, 6, 1))
    out += draw_scene(b, demos, LIGHT, 1.0, 0.35)
    out += draw_scene(b, [mean], RED, 3.4, obstacle=False)
    out.append(text(b.x0 + b.w / 2, 40, 'Ответ регрессии по MSE — среднее демонстраций', 15, INK, 'middle', 700))
    out.append(text(b.px(0), b.py(-1.6), 'среднее проходит через препятствие', 14, RED, 'middle', 700))
    out.append(text(550, 318, 'Минимум E[(a − f(o))²] по f достигается при f(o) = E[a | o] — среднем всех допустимых действий', 14, MUTED, 'middle'))
    write(os.path.join(OUT07, 'mse_vs_modes.svg'), out)


def l07_forward_noising():
    rng = random.Random(11)
    clean = sample_data(rng, True)
    noise = [rng.gauss(0, 1) for _ in range(M_PTS)]
    W, H = 1100, 290
    out = svg_open(W, H)
    levels = [1.0, 0.75, 0.4, 0.1, 0.0]
    for k, ab in enumerate(levels):
        a = scene_axes(20 + k * 216, 70, 200, 150)
        out.append(rect(a.x0, a.y0, a.w, a.h, '#ffffff', GRID, 6, 1))
        y = [math.sqrt(ab) * c + math.sqrt(1 - ab) * n for c, n in zip(clean, noise)]
        out += draw_scene(a, [y], BLUE if ab < 1 else GREEN, 2.2)
        out.append(text(a.x0 + a.w / 2, 56, f'ᾱ = {ab:g}', 15, INK, 'middle', 700))
        out.append(text(a.x0 + a.w / 2, 242, 'данные' if ab == 1 else ('чистый шум' if ab == 0 else f'шум {math.sqrt(1 - ab):.2f}'), 13, MUTED, 'middle'))
        if k < 4:
            out.append(arrow(a.x0 + a.w + 2, 145, a.x0 + a.w + 14, 145, MUTED, 1.6))
    out.append(text(550, 28, 'Прямой процесс: y_k = √ᾱ_k · y_0 + √(1 − ᾱ_k) · ε,  ε ~ N(0, I) — шум добавляется по расписанию', 16, INK, 'middle', 700))
    out.append(text(550, 272, 'Обучение: сеть ε_θ(y_k, k, o) учится угадывать добавленный шум ε. Это обычная регрессия, но по шуму, а не по действию.', 14, MUTED, 'middle'))
    write(os.path.join(OUT07, 'forward_noising.svg'), out)


def l07_reverse_process():
    K = 20
    snaps = ddpm_run(K, 10, 5)
    W, H = 1100, 300
    out = svg_open(W, H)
    shows = [20, 14, 8, 3, 0]
    for k, kk in enumerate(shows):
        a = scene_axes(20 + k * 216, 70, 200, 150)
        out.append(rect(a.x0, a.y0, a.w, a.h, '#ffffff', GRID, 6, 1))
        out += draw_scene(a, snaps[kk], GREEN if kk == 0 else BLUE, 1.5, 0.85)
        out.append(text(a.x0 + a.w / 2, 56, f'шаг k = {kk}', 15, INK, 'middle', 700))
        if k < 4:
            out.append(arrow(a.x0 + a.w + 2, 145, a.x0 + a.w + 14, 145, MUTED, 1.6))
    left = sum(1 for y in snaps[0] if y[6] > 0)
    hits = 0
    for y in snaps[0]:
        if any(math.hypot(XS[i], y[i]) < 0.9 for i in range(M_PTS)):
            hits += 1
    out.append(text(550, 28, f'Обратный процесс (DDPM, K = {K}): 10 выборок из шума превращаются в объезды', 16, INK, 'middle', 700))
    out.append(text(550, 248, f'Итог: {left} объездов слева, {10 - left} справа, через препятствие — {hits}. Каждая выборка выбирает один вариант, среднего нет.', 14, INK, 'middle'))
    out.append(text(550, 274, 'Шаг: y_{k−1} = (y_k − β_k/√(1 − ᾱ_k) · ε_θ(y_k, k, o)) / √α_k + σ_k z', 14, MUTED, 'middle'))
    write(os.path.join(OUT07, 'reverse_process.svg'), out)
    return left, hits


def l07_flow_vs_diffusion():
    """Одномерный пример: данные — смесь N(±1.5, 0.2²); пути выборок во времени."""
    mus, s2 = (1.5, -1.5), 0.04

    def post(x, mean_scale, var):
        ws = [math.exp(-(x - mean_scale * m) ** 2 / (2 * var)) for m in mus]
        t = sum(ws) or 1
        return [w / t for w in ws]

    def vel(x, tau):
        var = tau * tau * s2 + (1 - tau) ** 2
        r = post(x, tau, var)
        ex1 = sum(ri * (m + tau * s2 / var * (x - tau * m)) for ri, m in zip(r, mus))
        return (ex1 - x) / (1 - tau)

    def sc(x, ab):
        var = ab * s2 + 1 - ab
        r = post(x, math.sqrt(ab), var)
        return sum(ri * -(x - math.sqrt(ab) * m) / var for ri, m in zip(r, mus))

    rng = random.Random(21)
    x0s = [rng.gauss(0, 1) for _ in range(14)]
    W, H = 1100, 370
    out = svg_open(W, H)
    out.append(text(280, 30, 'Согласование потоков: ОДУ, гладкие пути', 15, INK, 'middle', 700))
    out.append(text(840, 30, 'Диффузия (DDPM): случайные блуждания', 15, INK, 'middle', 700))
    a = Axes(60, 70, 440, 220, (0, 1), (-2.6, 2.6))
    out += a.frame(xticks=(0, 0.5, 1), yticks=(-2, -1, 0, 1, 2), xlabel='время τ', ylabel='значение x')
    for x0 in x0s:
        x, pts, N = x0, [], 40
        for k in range(N + 1):
            tau = k / N
            pts.append(a.p(tau, x))
            if k < N:
                x += vel(x, tau) / N
        out.append(polyline(pts, GREEN, 1.8))
    b = Axes(620, 70, 440, 220, (0, 1), (-2.6, 2.6))
    out += b.frame(xticks=(0, 0.5, 1), yticks=(-2, -1, 0, 1, 2), xlabel='доля пройденных шагов', ylabel='значение x')
    K = 40
    for x0 in x0s:
        x, pts = x0, []
        for step in range(K + 1):
            pts.append(b.p(step / K, x))
            if step == K:
                break
            k = K - step
            ab = abar(k, K)
            abp = abar(k - 1, K) if k - 1 > 0 else 1.0
            alpha = ab / abp
            beta = 1 - alpha
            eps = -math.sqrt(1 - ab) * sc(x, ab)
            x = (x - beta / math.sqrt(1 - ab) * eps) / math.sqrt(alpha)
            if k - 1 > 0:
                x += math.sqrt((1 - abp) / (1 - ab) * beta) * rng.gauss(0, 1)
        out.append(polyline(pts, BLUE, 1.6))
    out.append(text(550, 352, 'Слева — шум N(0, 1), справа — данные: два варианта ±1.5. По почти прямым путям можно пройти за меньшее число шагов.', 14, MUTED, 'middle'))
    write(os.path.join(OUT07, 'flow_vs_diffusion.svg'), out)

def l07_diffusion_policy_arch():
    W, H = 1100, 380
    out = svg_open(W, H)
    out.append(text(550, 30, 'Диффузионная политика: на каждом такте — генерация пакета действий по наблюдениям', 17, INK, 'middle', 700))
    out += box(30, 60, 220, 110, 'Наблюдения o_t', ['изображения камер,', 'положения суставов', '(последние 2 кадра)'], INK, PANEL, 15, 13)
    out += box(30, 210, 220, 110, 'Кодировщик', ['ResNet / ViT:', 'изображение →', 'вектор признаков'], PURPLE, '#faf5ff', 15, 13)
    out.append(arrow(140, 170, 140, 206, MUTED))
    out += box(330, 60, 220, 110, 'Шум a^K', ['случайный пакет', 'из H действий', '~ N(0, I)'], AMBER, '#fffbeb', 15, 13)
    out += box(330, 210, 260, 110, 'Сеть ε_θ(a^k, k, o_t)', ['U-Net или трансформер:', 'предсказывает шум', 'в пакете действий'], BLUE, '#eff6ff', 15, 13)
    out.append(arrow(250, 265, 326, 265, PURPLE))
    out.append(text(288, 255, 'условие', 12, PURPLE, 'middle'))
    out.append(arrow(440, 170, 440, 206, AMBER))
    out.append(polyline([(590, 250), (640, 250), (640, 190), (560, 190), (560, 206)], BLUE, 2, '5 4', marker='arrB'))
    out.append(text(650, 222, 'повторить K раз', 13, BLUE, 'start', 700))
    out.append(text(650, 240, '(k = K, …, 1)', 13, BLUE, 'start'))
    out += box(770, 210, 300, 110, 'Пакет действий a_{t:t+H}', ['H = 16 шагов (≈ 1.6 с при 10 Гц);', 'исполняются первые n_a = 8,', 'затем новый пакет'], GREEN, '#ecfdf5', 15, 13)
    out.append(arrow(590, 290, 766, 290, GREEN))
    out.append(text(680, 280, 'a^0', 13, GREEN, 'middle', 700))
    out += wrap_lines(30, 352, ['Обучение: берём действие из демонстрации, добавляем шум уровня k, учим сеть угадывать этот шум (MSE по шуму).',
                                'Вывод: K шагов очистки (DDPM ~100, DDIM ~10). Числа H и n_a — из статьи Chi et al., 2023.'], 13, MUTED, dy=18)
    write(os.path.join(OUT07, 'diffusion_policy_arch.svg'), out)


def l07_action_chunks():
    W, H = 1100, 260
    out = svg_open(W, H)
    out.append(text(550, 28, 'Пакеты действий и скользящий горизонт: та же идея, что у MPC (лекция 05)', 16, INK, 'middle', 700))
    X = lambda t: 110 + t * 38
    out.append(arrow(X(0), 210, X(24.6), 210, MUTED, 1.6))
    for t in range(0, 25, 4):
        out.append(line(X(t), 206, X(t), 214, MUTED, 1.4))
        out.append(text(X(t), 230, str(t), 12, MUTED, 'middle'))
    out.append(text(X(24.6), 252, 'такт', 12, MUTED, 'end'))
    for r, (t0, c) in enumerate(((0, BLUE), (8, GREEN))):
        y = 56 + r * 70
        out.append(rect(X(t0), y, X(t0 + 16) - X(t0), 34, '#ffffff', c, 4, 1.6, '5 4'))
        out.append(rect(X(t0), y, X(t0 + 8) - X(t0), 34, c, c, 4, 1))
        out.append(text(X(t0) + 8, y + 22, f'исполняется a_{{{t0}}}…a_{{{t0 + 7}}}', 13, '#ffffff', 'start', 700))
        out.append(text(X(t0 + 8) + 8, y + 22, 'предсказано и отброшено', 13, c, 'start'))
        out.append(text(X(t0) - 8, y + 22, f'пакет {r + 1}', 13, c, 'end', 700))
    out.append(text(X(16) + 12, 184, 'предсказано H = 16, исполнено n_a = 8, затем новый пакет', 13, INK, 'start'))
    write(os.path.join(OUT07, 'action_chunks.svg'), out)

def l07_nomad_arch():
    W, H = 1100, 400
    out = svg_open(W, H)
    out.append(text(550, 30, 'NoMaD: одна сеть для движения к цели и для исследования (19 млн параметров)', 17, INK, 'middle', 700))
    for i in range(4):
        out.append(rect(30 + i * 22, 60 + i * 10, 120, 80, '#e0f2fe', SKY, 4, 1.4))
    out.append(text(110, 178, 'текущий и прошлые', 13, INK, 'middle'))
    out.append(text(110, 196, 'кадры камеры', 13, INK, 'middle'))
    out.append(rect(40, 240, 140, 90, '#fef3c7', AMBER, 4, 1.6))
    out.append(text(110, 280, 'изображение', 13, INK, 'middle'))
    out.append(text(110, 298, 'цели', 13, INK, 'middle'))
    out += box(230, 70, 190, 90, 'EfficientNet-B0', ['кадр → токен', '(256 чисел)'], PURPLE, '#faf5ff', 14, 13)
    out += box(230, 240, 190, 90, 'Кодировщик цели', ['(кадр, цель) → токен'], PURPLE, '#faf5ff', 14, 13)
    out.append(arrow(180, 115, 226, 115))
    out.append(arrow(180, 285, 226, 285))
    out += box(480, 140, 200, 120, 'Трансформер', ['4 слоя, 4 головы;', 'контекст c_t'], BLUE, '#eff6ff', 15, 13)
    out.append(arrow(420, 115, 476, 170))
    out.append(arrow(420, 285, 476, 230))
    out.append(rect(440, 290, 150, 50, '#fee2e2', RED, 6, 1.6))
    out.append(text(515, 312, 'маска цели m', 13, RED, 'middle', 700))
    out.append(text(515, 330, 'm = 1: цель скрыта', 12, RED, 'middle'))
    out += box(740, 60, 330, 110, 'Диффузионная голова', ['1D U-Net, K = 10 шагов очистки:', 'последовательность будущих', 'путевых точек робота'], GREEN, '#ecfdf5', 15, 13)
    out += box(740, 220, 330, 90, 'Голова расстояния', ['сколько шагов до цели', '(для топологического графа)'], AMBER, '#fffbeb', 15, 13)
    out.append(arrow(680, 180, 736, 120, GREEN))
    out.append(arrow(680, 220, 736, 262, AMBER))
    out += wrap_lines(30, 362, ['Обучение: более 100 часов езды разных роботов (наборы GNM, SACSoN); маска цели включается с вероятностью 0.5.',
                                'Результат (Sridhar et al., 2024): исследование без цели — 98 % успеха против 77 % у модели с генерацией подцелей в 335 млн параметров.'], 13, MUTED, dy=18)
    write(os.path.join(OUT07, 'nomad_arch.svg'), out)


def l07_topological_graph():
    W, H = 1100, 340
    out = svg_open(W, H)
    out.append(text(550, 28, 'Топологическая навигация: граф из запомненных кадров + обученная локальная политика', 16, INK, 'middle', 700))
    out.append(rect(30, 50, 620, 270, '#f8fafc', GRID, 8, 1.2))
    walls = [(30, 150, 280, 150), (380, 150, 650, 150), (330, 50, 330, 110), (330, 190, 330, 320), (500, 230, 650, 230)]
    for x1, y1, x2, y2 in walls:
        out.append(line(x1, y1, x2, y2, INK, 5))
    nodes = [(80, 100), (180, 90), (280, 110), (330, 150), (400, 110), (500, 90), (590, 110), (360, 210), (420, 280), (560, 280), (240, 230), (120, 260)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7), (7, 8), (8, 9), (7, 10), (10, 11)]
    path = [11, 10, 7, 3, 4, 5, 6]
    for i, j in edges:
        on = i in path and j in path and abs(path.index(i) - path.index(j)) == 1
        out.append(line(*nodes[i], *nodes[j], GREEN if on else LIGHT, 3.2 if on else 1.8))
    for k, (x, y) in enumerate(nodes):
        out.append(rect(x - 14, y - 10, 28, 20, '#e0f2fe', SKY, 3, 1.4))
    out.append(circle(nodes[11][0], nodes[11][1] + 22, 7, INK))
    out.append(text(nodes[11][0], nodes[11][1] + 46, 'робот', 13, INK, 'middle', 700))
    out.append(circle(nodes[6][0], nodes[6][1] - 22, 7, GREEN))
    out.append(text(nodes[6][0], nodes[6][1] - 36, 'цель (фото)', 13, GREEN, 'middle', 700))
    out.append(text(620, 210, 'граница', 12, AMBER, 'end'))
    out.append(text(620, 224, 'исследования', 12, AMBER, 'end'))
    out += wrap_lines(680, 70, ['Узел — кадр камеры, запомненный при проезде.', 'Ребро — голова расстояния считает,',
                                'что между кадрами несколько шагов.', '', 'Глобально: поиск пути по графу',
                                '(Дейкстра, A* — лекция 02).', '', 'Локально: диффузионная голова ведёт',
                                'робота к следующему кадру-подцели.', '', 'Нет цели в графе: маска m = 1,',
                                'робот исследует и пополняет граф.'], 14, INK, dy=21)
    write(os.path.join(OUT07, 'topological_graph.svg'), out)


# ===========================================================================
# Лекция 08
# ===========================================================================

# ===========================================================================
# Лекция 07. Часть 1: перепланирование при изменении карты (D* Lite)
# ===========================================================================

DW, DH = 26, 16
D_START, D_GOAL = (2, 8), (23, 8)
D_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def d_inside(x, y):
    return 0 <= x < DW and 0 <= y < DH


def d_cost(m, a, b):
    if (a in m) or (b in m):
        return math.inf
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx and dy and (((a[0] + dx, a[1]) in m) or ((a[0], a[1] + dy) in m)):
        return math.inf
    return math.sqrt(2) if dx and dy else 1.0


def d_nbrs(c):
    return [(c[0] + dx, c[1] + dy) for dx, dy in D_DIRS if d_inside(c[0] + dx, c[1] + dy)]


def d_h(a, b):
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)


class DStarLite:
    """D* Lite (Koenig, Likhachev, 2002) на 8-связной сетке, как в виджете dstar-lite."""

    def __init__(self, known, start):
        import heapq
        self.hq = heapq
        self.m = set(known)
        self.start, self.last, self.km = start, start, 0.0
        self.g, self.rhs, self.heap, self.inq = {}, {D_GOAL: 0.0}, [], {}
        self.push(D_GOAL)

    def G(self, c):
        return self.g.get(c, math.inf)

    def R(self, c):
        return self.rhs.get(c, math.inf)

    def key(self, c):
        k = min(self.G(c), self.R(c))
        return (k + d_h(self.start, c) + self.km, k)

    def push(self, c):
        k = self.key(c)
        self.inq[c] = k
        self.hq.heappush(self.heap, (k, c))

    def top(self):
        while self.heap and self.inq.get(self.heap[0][1]) != self.heap[0][0]:
            self.hq.heappop(self.heap)
        return self.heap[0][0] if self.heap else (math.inf, math.inf)

    def update(self, u):
        if u != D_GOAL:
            self.rhs[u] = min((d_cost(self.m, u, n) + self.G(n) for n in d_nbrs(u)), default=math.inf)
        self.inq.pop(u, None)
        if self.G(u) != self.R(u):
            self.push(u)

    def compute(self):
        expanded = []
        while self.top() < self.key(self.start) or self.R(self.start) != self.G(self.start):
            if not self.heap:
                break
            kold, u = self.hq.heappop(self.heap)
            self.inq.pop(u, None)
            if kold < self.key(u):
                self.push(u)
                continue
            expanded.append(u)
            if self.G(u) > self.R(u):
                self.g[u] = self.R(u)
                for n in d_nbrs(u):
                    self.update(n)
            else:
                self.g[u] = math.inf
                self.update(u)
                for n in d_nbrs(u):
                    self.update(n)
        return expanded

    def changed(self, cells, robot):
        self.km += d_h(self.last, robot)
        self.last = self.start = robot
        touch = set()
        for c in cells:
            self.m.add(c)
            touch.add(c)
            touch.update(d_nbrs(c))
        for c in touch:
            self.update(c)

    def plan(self):
        p, c = [self.start], self.start
        for _ in range(DW * DH):
            if c == D_GOAL:
                break
            n = min(d_nbrs(c), key=lambda n: d_cost(self.m, c, n) + self.G(n))
            if d_cost(self.m, c, n) + self.G(n) == math.inf:
                break
            c = n
            p.append(c)
        return p


def d_astar(m, s):
    import heapq
    g, closed, op, exp = {s: 0.0}, set(), [(d_h(s, D_GOAL), s)], []
    while op:
        _, u = heapq.heappop(op)
        if u in closed:
            continue
        closed.add(u)
        exp.append(u)
        if u == D_GOAL:
            break
        for n in d_nbrs(u):
            c = d_cost(m, u, n)
            if c == math.inf or n in closed:
                continue
            if g[u] + c < g.get(n, math.inf):
                g[n] = g[u] + c
                heapq.heappush(op, (g[n] + d_h(n, D_GOAL), n))
    return exp


def d_grid(ox, oy, cs, known, hidden, fill=None, path=None, trail=None, robot=None, sensor=None):
    out = []
    for y in range(DH):
        for x in range(DW):
            f = '#ffffff'
            if fill and (x, y) in fill:
                f = fill[(x, y)]
            if (x, y) in known:
                f = '#334155'
            out.append(rect(ox + x * cs, oy + y * cs, cs, cs, f, '#e2e8f0', 0, 0.6))
            if (x, y) in hidden and (x, y) not in known:
                out.append(rect(ox + x * cs + 2, oy + y * cs + 2, cs - 4, cs - 4, '#e2e8f0', '#94a3b8', 0, 0.8, '3 2'))
    P = lambda c: (ox + (c[0] + 0.5) * cs, oy + (c[1] + 0.5) * cs)
    if sensor and robot:
        X, Y = P(robot)
        out.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{(sensor + 0.5) * cs:.1f}" fill="none" stroke="{SKY}" stroke-width="1.3" stroke-dasharray="5 4"/>')
    if path:
        out.append(polyline([P(c) for c in path], GREEN, 2.6))
    if trail:
        out.append(polyline([P(c) for c in trail], BLUE, 2.4))
    gx, gy = P(D_GOAL)
    out.append(circle(gx, gy, cs * 0.42, GREEN))
    if robot:
        rx, ry = P(robot)
        out.append(circle(rx, ry, cs * 0.45, BLUE))
    return out


def l07_dstar_replanning():
    hidden = set((13, y) for y in range(0, 13))
    known = set()
    ds = DStarLite(known, D_START)
    first = ds.compute()
    robot, trail, sensor = D_START, [D_START], 2
    seen, events = set(), []
    while robot != D_GOAL and len(trail) < 200:
        robot = ds.plan()[1]
        ds.start = robot
        trail.append(robot)
        new = {c for c in hidden if c not in seen and (c[0] - robot[0]) ** 2 + (c[1] - robot[1]) ** 2 <= sensor * sensor + 0.5}
        if new:
            snap = dict(seen=set(seen), plan=ds.plan(), g=dict(ds.g), trail=list(trail), robot=robot, new=new)
            seen |= new
            ds.changed(new, robot)
            snap['rep'] = ds.compute()
            snap['exp_a'] = d_astar(seen, robot)
            snap['after'] = ds.plan()
            snap['seen_after'] = set(seen)
            events.append(snap)
    ev = max(events, key=lambda e: len(e['exp_a']) - len(e['rep']))
    robot, trail, new = ev['robot'], ev['trail'], ev['new']
    before_plan, g_before, rep, exp_a, seen = ev['plan'], ev['g'], ev['rep'], ev['exp_a'], ev['seen_after']
    known_before = ev['seen']
    tot_a, tot_d = sum(len(e['exp_a']) for e in events), sum(len(e['rep']) for e in events)
    W, H = 1100, 352
    out = svg_open(W, H)
    cs = 13
    panels = [
        ('До: план по тому, что известно', 'датчик ещё не видит новые клетки стены'),
        (f'A* с нуля: раскрыто {len(exp_a)} клеток', 'вся задача решается заново'),
        (f'D* Lite: раскрыто {len(rep)} клеток', 'исправлены только изменившиеся g'),
    ]
    gmax = max(v for v in g_before.values() if v < math.inf)
    for i, (t1, t2) in enumerate(panels):
        ox, oy = 18 + i * 362, 62
        out.append(text(ox + DW * cs / 2, 28, t1, 15, [INK, MUTED, AMBER][i], 'middle', 700))
        out.append(text(ox + DW * cs / 2, 47, t2, 13, MUTED, 'middle'))
        if i == 0:
            fill = {c: f'rgb({int(239 - 80 * v / gmax)},{int(246 - 60 * v / gmax)},255)' for c, v in g_before.items() if v < math.inf}
            out += d_grid(ox, oy, cs, known_before, hidden, fill, before_plan, trail, robot, sensor)
        elif i == 1:
            out += d_grid(ox, oy, cs, seen, hidden, {c: '#cbd5e1' for c in exp_a}, None, trail, robot, sensor)
        else:
            out += d_grid(ox, oy, cs, seen, hidden, {c: '#fdba74' for c in rep}, ev['after'], trail, robot, sensor)
    out += legend(18, 292, [('пройдено', BLUE, None)], 13)
    out += legend(140, 292, [('план', GREEN, None)], 13)
    out.append(rect(240, 284, 12, 12, '#334155', '#334155', 0, 1))
    out.append(text(258, 294, 'замеченная стена', 13, INK))
    out.append(rect(390, 284, 12, 12, '#e2e8f0', '#94a3b8', 0, 1, '3 2'))
    out.append(text(408, 294, 'ещё не замечена', 13, INK))
    out.append(text(18, 320, f'Сценарий «неизвестная стена», шаг {len(trail) - 1}: датчик (радиус 2 клетки) заметил новые клетки стены: {len(new)}.', 13, MUTED))
    out.append(text(18, 340, f'За весь проезд {len(events)} пересчётов: A* с нуля — {tot_a} раскрытий, D* Lite — {tot_d}.', 13, MUTED))
    write(os.path.join(OUT07, 'dstar_replanning.svg'), out)
    return len(first), len(exp_a), len(rep), tot_a, tot_d


def l07_g_rhs():
    """Маленький граф: значения g и rhs до изменения, сразу после и после пересчёта."""
    pos = {'S': (0, 1), 'B': (1, 0), 'A': (2, 0), 'G': (3, 1), 'C': (1.5, 2)}
    edges = {('S', 'B'): 1, ('B', 'A'): 1, ('A', 'G'): 1, ('S', 'C'): 2, ('C', 'G'): 3}

    def dist(ed):
        d = {n: math.inf for n in pos}
        d['G'] = 0
        for _ in range(10):
            for (u, v), w in ed.items():
                d[u] = min(d[u], d[v] + w)
                d[v] = min(d[v], d[u] + w)
        return d

    g0 = dist(edges)
    ed1 = dict(edges)
    ed1[('A', 'G')] = math.inf
    g1 = dist(ed1)

    def rhs(gv, ed):
        r = {}
        for n in pos:
            if n == 'G':
                r[n] = 0
                continue
            best = math.inf
            for (u, v), w in ed.items():
                if u == n:
                    best = min(best, w + gv[v])
                if v == n:
                    best = min(best, w + gv[u])
            r[n] = best
        return r
    snaps = [('1. До изменения', g0, rhs(g0, edges), edges, 'все вершины согласованы: g = rhs'),
             ('2. Ребро A–G перекрыто', g0, rhs(g0, ed1), ed1, 'у A теперь rhs ≠ g: вершина в очереди'),
             ('3. После пересчёта', g1, rhs(g1, ed1), ed1, 'изменились только S, B, A; C и G не тронуты')]
    W, H = 1100, 352
    out = svg_open(W, H)
    f = lambda v: '∞' if v == math.inf else f'{v:g}'
    for i, (title, gv, rv, ed, cap) in enumerate(snaps):
        ox = 20 + i * 362
        out.append(text(ox + 165, 30, title, 15, INK, 'middle', 700))
        P = lambda n: (ox + 40 + pos[n][0] * 90, 95 + pos[n][1] * 75)
        for (u, v), w in ed.items():
            (x1, y1), (x2, y2) = P(u), P(v)
            blocked = w == math.inf
            out.append(line(x1, y1, x2, y2, RED if blocked else LIGHT, 2.4, '6 4' if blocked else None))
            out.append(text((x1 + x2) / 2, (y1 + y2) / 2 - 6, '∞' if blocked else f'{w:g}', 13, RED if blocked else MUTED, 'middle', 700))
        for n in pos:
            x, y = P(n)
            bad = gv[n] != rv[n]
            changed = i == 2 and g0[n] != g1[n]
            col = AMBER if bad else (BLUE if changed else (GREEN if n == 'G' else INK))
            out.append(circle(x, y, 17, '#fff7ed' if bad else ('#eff6ff' if changed else '#ffffff'), col, 2.2))
            out.append(text(x, y + 5, n, 15, col, 'middle', 700))
            ly = y - 26 if n in ('A', 'B') else y + 34
            out.append(text(x, ly, f'g={f(gv[n])}, rhs={f(rv[n])}', 12, col, 'middle'))
        out.append(text(ox + 165, 308, cap, 13, MUTED, 'middle'))
    out.append(text(550, 338, 'g — сохранённая оценка расстояния до цели G; rhs(s) = min по соседям (c(s, s′) + g(s′)) — «что говорят соседи».', 13, INK, 'middle'))
    write(os.path.join(OUT07, 'g_rhs_example.svg'), out)
    return g1


def l07_act_arch():
    W, H = 1100, 372
    out = svg_open(W, H)
    out.append(text(550, 28, 'ACT: трансформер предсказывает пакет действий за один проход (Zhao и др., 2023)', 17, INK, 'middle', 700))
    out += box(30, 60, 200, 110, 'Наблюдения', ['4 камеры (кисти, сверху,', 'спереди) + углы', 'суставов двух рук'], INK, PANEL, 15, 13)
    out.append(arrow(230, 115, 280, 115))
    out += box(284, 60, 210, 110, 'Кодировщик', ['ResNet-18 для кадров,', 'трансформер-', 'кодировщик'], BLUE, '#eff6ff', 15, 13)
    out.append(arrow(494, 115, 544, 115))
    out += box(548, 60, 230, 110, 'Декодер', ['трансформер: сразу', 'k = 100 будущих', 'действий (≈ 2 с при 50 Гц)'], GREEN, '#ecfdf5', 15, 13)
    out.append(arrow(778, 115, 828, 115))
    out += box(832, 60, 238, 110, 'Пакет действий', ['углы 14 суставов', 'на 100 тактов вперёд'], GREEN, '#ecfdf5', 15, 13)
    out += box(284, 196, 210, 110, 'Стиль z (CVAE)', ['при обучении: сжатие', 'демонстрации; при работе', 'z = 0 (среднее)'], PURPLE, '#faf5ff', 15, 13)
    out.append(arrow(389, 196, 600, 172, PURPLE, 2, '6 4'))
    out.append(rect(548, 196, 522, 110, '#fffbeb', AMBER, 8, 1.4, '6 4'))
    out += wrap_lines(564, 230, ['Сглаживание по времени (temporal ensembling): пакеты', 'пересчитываются каждый такт, и действие на текущий такт —', 'взвешенное среднее предсказаний из разных пакетов.'], 13, INK, dy=20)
    out += wrap_lines(30, 332, ['Данные: около 50 демонстраций на задачу, собранных телеуправлением на дешёвом стенде ALOHA (две пары рук: ведущая и ведомая).',
                                'Отличие от диффузии: один проход сети вместо K шагов очистки; многомодальность — через стиль z, а не через случайный шум.'], 13, MUTED, dy=20)
    write(os.path.join(OUT07, 'act_arch.svg'), out)


def l08_timeline():
    W, H = 1100, 470
    out = svg_open(W, H)
    out.append(text(550, 28, 'Пять десятилетий антропоморфных роботов', 18, INK, 'middle', 700))
    X = lambda y: 50 + (y - 1965) / (2027 - 1965) * 1000
    eras = [(1965, 1995, 'статическая ходьба и ZMP', '#eff6ff', BLUE), (1995, 2016, 'динамика и оптимизация', '#fffbeb', AMBER),
            (2016, 2027, 'обучение', '#ecfdf5', GREEN)]
    for a, b, lab, fill, col in eras:
        out.append(rect(X(a), 190, X(b) - X(a), 30, fill, col, 0, 1.2))
        out.append(text((X(a) + X(b)) / 2, 210, lab, 13, col, 'middle', 700))
    for yr in range(1970, 2030, 10):
        out.append(line(X(yr), 220, X(yr), 228, MUTED, 1.4))
        out.append(text(X(yr), 243, str(yr), 12, MUTED, 'middle'))
    up = [(1968, 'ZMP (Вукобратович)'), (1973, 'WABOT-1 (Васэда)'), (1983, 'прыгающие роботы Raibert'),
          (1986, 'Honda E0'), (1996, 'Honda P2'), (2000, 'ASIMO'), (2005, 'BigDog'), (2013, 'Atlas (гидравлика)'),
          (2015, 'DARPA Robotics Challenge')]
    for k, (yr, lab) in enumerate(up):
        y = 176 - (k % 4) * 34
        out.append(line(X(yr), y + 4, X(yr), 190, LIGHT, 1.2))
        out.append(circle(X(yr), 190, 4, BLUE))
        out.append(text(X(yr), y, lab, 12.5, INK, 'middle'))
    # увеличенный участок 2016–2026
    Z = lambda y: 60 + (y - 2016) / (2026.6 - 2016) * 980
    out.append(polyline([(X(2016), 220), (Z(2016), 300)], LIGHT, 1.2, '4 4'))
    out.append(polyline([(X(2027), 220), (Z(2026.6), 300)], LIGHT, 1.2, '4 4'))
    out.append(rect(Z(2016), 300, Z(2026.6) - Z(2016), 26, '#ecfdf5', GREEN, 0, 1.2))
    out.append(text(Z(2016) + 8, 318, '2016–2026 подробнее', 12.5, GREEN, 'start', 700))
    for yr in range(2016, 2027):
        out.append(line(Z(yr), 326, Z(yr), 332, MUTED, 1.2))
        out.append(text(Z(yr), 346, str(yr), 12, MUTED, 'middle'))
    dn = [(2017.9, 0, 'Atlas: сальто назад'), (2019.6, 0, 'ФЁДОР на МКС'), (2021.6, 0, 'паркур Atlas'),
          (2023.6, 0, 'Unitree H1'), (2024.4, 1, 'электрический Atlas, Figure 02, Unitree G1'),
          (2025.15, 2, 'Helix (Figure), GR00T N1 (NVIDIA)'), (2025.85, 3, 'Грин (Сбер), AIDOL'), (2026.1, 4, 'Helix 02, ZEST, DreamZero')]
    for yr, row, lab in dn:
        y = 372 + row * 22
        out.append(line(Z(yr), 326, Z(yr), y - 12, LIGHT, 1.2))
        out.append(circle(Z(yr), 326, 4, GREEN))
        anchor = 'end' if yr > 2024 else 'middle'
        out.append(text(Z(yr) + (6 if anchor == 'end' else 0), y, lab, 12.5, INK, anchor))
    write(os.path.join(OUT08, 'humanoid_timeline.svg'), out)

def l08_static_vs_dynamic():
    W, H = 1100, 335
    out = svg_open(W, H)

    def figure(cx, lean, com_dx, title, sub, ok):
        o = []
        gy = 260
        o.append(line(cx - 160, gy, cx + 160, gy, INK, 2))
        o.append(rect(cx - 60, gy - 8, 120, 8, BLUE, BLUE, 2, 1))
        o.append(rect(cx - 60, gy - 2, 120, 24, '#ecfdf5', 'none', 0, 0))
        o.append(text(cx, gy + 16, 'опора', 12, GREEN, 'middle', 700))
        comx, comy = cx + com_dx, 110
        o.append(line(cx, gy - 8, comx, comy + 20, INK, 5))
        o.append(circle(comx, comy, 16, INK))
        o.append(text(comx, comy + 5, 'ЦМ', 11, '#ffffff', 'middle', 700))
        o.append(line(comx, comy + 16, comx, gy, PURPLE, 1.6, '5 4'))
        o.append(circle(comx, gy, 5, PURPLE))
        o.append(text(comx + 8, gy - 14, 'проекция ЦМ', 12, PURPLE, 'start'))
        o.append(text(cx, 40, title, 16, INK, 'middle', 700))
        o += wrap_lines(cx, 64, sub, 13, MUTED, 'middle', 18)
        o.append(text(cx, 318, ok, 13, GREEN if 'устойчив' in ok else RED, 'middle', 700))
        return o
    out += figure(200, 0, 25, 'Статическая устойчивость', ['проекция ЦМ внутри опоры', 'в любой момент'], 'устойчив даже при остановке')
    out += figure(550, 0, 110, 'Динамическая ходьба', ['проекция ЦМ вне опоры,', 'робот «падает» вперёд'], 'держится за счёт ускорений')
    o = []
    gy = 260
    cx = 900
    o.append(line(cx - 160, gy, cx + 160, gy, INK, 2))
    o.append(rect(cx - 60, gy - 8, 120, 8, BLUE, BLUE, 2, 1))
    for k in range(9):
        x = cx - 55 + k * 13.5
        h = 6 + 26 * math.exp(-((x - (cx + 25)) ** 2) / 1200)
        o.append(arrow(x, gy + 6 + h, x, gy + 6, AMBER, 1.6))
    o.append(circle(cx + 25, gy - 4, 6, RED))
    o.append(text(cx + 25, gy - 18, 'ZMP', 13, RED, 'middle', 700))
    o.append(text(cx, 40, 'Точка нулевого момента', 16, INK, 'middle', 700))
    o += wrap_lines(cx, 64, ['точка, где равнодействующая', 'реакции опоры не создаёт', 'опрокидывающего момента'], 13, MUTED, 'middle', 18)
    o.append(text(cx, 318, 'условие: ZMP строго внутри стопы', 13, INK, 'middle', 700))
    out += o
    write(os.path.join(OUT08, 'static_dynamic_zmp.svg'), out)


def l08_lipm():
    W, H = 1100, 360
    out = svg_open(W, H)
    # схема маятника
    gy, cx = 300, 170
    out.append(line(40, gy, 330, gy, INK, 2))
    out.append(rect(cx - 40, gy - 8, 80, 8, BLUE, BLUE, 2, 1))
    comx, comy = cx + 70, 110
    out.append(line(40, comy, 330, comy, LIGHT, 1.4, '5 5'))
    out.append(text(44, comy - 8, 'высота z = z₀ = const', 13, MUTED, 'start'))
    out.append(line(cx, gy - 4, comx, comy, INK, 4))
    out.append(circle(comx, comy, 16, INK))
    out.append(text(comx, comy + 5, 'm', 13, '#ffffff', 'middle', 700))
    out.append(circle(cx, gy - 4, 5, RED))
    out.append(text(cx - 8, gy + 22, 'p (ZMP)', 13, RED, 'middle', 700))
    out.append(line(cx, gy + 30, comx, gy + 30, PURPLE, 1.6, marker='arrP'))
    out.append(text((cx + comx) / 2, gy + 48, 'x − p', 13, PURPLE, 'middle', 700))
    out.append(arrow(comx + 22, comy, comx + 80, comy, GREEN, 2.4))
    out.append(text(comx + 52, comy - 12, 'ẍ', 15, GREEN, 'middle', 700))
    out.append(text(185, 40, 'Модель LIPM', 17, INK, 'middle', 700))
    out.append(text(185, 64, 'ẍ = ω² (x − p),  ω = √(g / z₀)', 15, INK, 'middle', 700))
    # решения
    a = Axes(440, 50, 600, 250, (0, 1.2), (-0.3, 0.6))
    out += a.frame(xticks=(0, 0.4, 0.8, 1.2), yticks=(-0.2, 0, 0.2, 0.4), xlabel='t, с', ylabel='x(t) − p, м')
    w = math.sqrt(9.81 / 0.9)
    cases = [(0.05, 0.0, RED, 'x₀ = 5 см, ẋ₀ = 0: падает вперёд'), (0.05, -0.05 * w, GREEN, 'ẋ₀ = −ωx₀: ξ = p, приходит в p'),
             (0.05, -0.30, BLUE, 'ẋ₀ = −0.3: падает назад')]
    for x0, v0, col, lab in cases:
        pts = []
        for t in linspace(0, 1.2, 120):
            x = x0 * math.cosh(w * t) + v0 / w * math.sinh(w * t)
            if -0.3 <= x <= 0.6:
                pts.append(a.p(t, x))
        out.append(polyline(pts, col, 2.6))
    out += legend(460, 330, [(cases[0][3], RED, None)], 13)
    out += legend(760, 330, [(cases[1][3], GREEN, None)], 13)
    out += legend(460, 352, [(cases[2][3], BLUE, None)], 13)
    out.append(text(760, 352, f'z₀ = 0.9 м, ω = {w:.2f} 1/с', 13, MUTED))
    write(os.path.join(OUT08, 'lipm_model.svg'), out)
    return w


def l08_capture_band():
    W, H = 1100, 360
    out = svg_open(W, H)
    w = math.sqrt(9.81 / 0.9)
    heel, toe = 0.06, 0.16
    a = Axes(70, 50, 560, 260, (-0.4, 0.6), (-1.0, 1.6))
    out += a.frame(xticks=(-0.4, -0.2, 0, 0.2, 0.4, 0.6), yticks=(-1, -0.5, 0, 0.5, 1, 1.5), xlabel='x − f, м', ylabel='ẋ, м/с', fmt='{:g}')
    band = [a.p(-0.4, w * (toe + 0.4)), a.p(0.6, w * (toe - 0.6)), a.p(0.6, w * (-heel - 0.6)), a.p(-0.4, w * (-heel + 0.4))]
    out.append(f'<clipPath id="cb"><rect x="{a.x0}" y="{a.y0}" width="{a.w}" height="{a.h}"/></clipPath>')
    out.append('<g clip-path="url(#cb)">')
    out.append(polygon(band, '#a7f3d0', 0.55, GREEN))
    # траектории после толчка под регулятором голеностопа
    for dv, col in ((0.3, GREEN), (0.6, RED)):
        x, v, pts = 0.0, dv, []
        for k in range(1200):
            xi = x + v / w
            p = max(-heel, min(toe, xi + 3 / w * xi))
            c, s = math.cosh(w * 0.001), math.sinh(w * 0.001)
            e = x - p
            x, v = p + e * c + v / w * s, e * w * s + v * c
            if k % 5 == 0:
                pts.append(a.p(x, v))
            if abs(x) > 0.6:
                break
        out.append(polyline([a.p(0, 0)] + pts, col, 2.6))
    out.append('</g>')
    out.append(text(a.px(-0.3), a.py(1.35), 'устоит без шага:', 13, GREEN, 'start', 700))
    out.append(text(a.px(-0.3), a.py(1.35) + 16, 'точка захвата ξ внутри стопы', 13, GREEN, 'start'))
    out.append(text(a.px(0.05), a.py(0.25), 'Δv = 0.3', 13, GREEN, 'start', 700))
    out.append(text(a.px(0.33), a.py(1.05), 'Δv = 0.6: падение', 13, RED, 'start', 700))
    out += wrap_lines(670, 70, ['Точка захвата (capture point):', '  ξ = x + ẋ / ω', '', 'Её движение:  ξ̇ = ω (ξ − p).',
                                '', 'p — внутри стопы, поэтому:', '• ξ в стопе → ZMP «догоняет» ξ,', '  робот останавливается;',
                                '• ξ за носком → ξ убегает', '  экспоненциально: нужен шаг', '  в точку ξ (или дальше).'], 15, INK, dy=22)
    write(os.path.join(OUT08, 'capture_band.svg'), out)


def l08_lipm_walking():
    """Периодическая походка LIPM: ZMP в центре каждой стопы, ЦМ — склейка решений."""
    W, H = 1100, 330
    out = svg_open(W, H)
    w = math.sqrt(9.81 / 0.9)
    L, Ts = 0.3, 0.5
    # периодичность: x(0) = −L/2, x(Ts) = L/2 относительно стопы, ẋ(0) = ẋ(Ts)
    v0 = w * (L / 2) * (1 + math.cosh(w * Ts)) / math.sinh(w * Ts)
    a = Axes(70, 50, 960, 220, (0, 6 * Ts), (-0.2, 1.9))
    out += a.frame(xticks=[k * Ts for k in range(7)], yticks=(0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8), xlabel='t, с', ylabel='положение, м', fmt='{:g}')
    zmp, com = [], []
    for k in range(6):
        f = k * L
        zmp += [a.p(k * Ts, f), a.p((k + 1) * Ts, f)]
        for t in linspace(0, Ts, 40):
            x = f + (-L / 2) * math.cosh(w * t) + v0 / w * math.sinh(w * t)
            com.append(a.p(k * Ts + t, x))
        out.append(rect(a.px(k * Ts) + 2, a.py(f) - 4, a.px((k + 1) * Ts) - a.px(k * Ts) - 4, 8, '#dbeafe', BLUE, 2, 1))
    out.append(polyline(zmp, RED, 2.4))
    out.append(polyline(com, INK, 2.8))
    out += legend(80, 300, [('ZMP p(t): ступеньками, в центре опорной стопы', RED, None)], 13)
    out += legend(520, 300, [('центр масс x(t): склейка решений LIPM', INK, None)], 13)
    out.append(text(550, 28, f'Ходьба как цепочка маятников: шаг {L} м за {Ts} с, скорость ЦМ при смене опоры {v0:.2f} м/с', 15, INK, 'middle', 700))
    write(os.path.join(OUT08, 'lipm_walking.svg'), out)
    return v0


def l08_raibert():
    W, H = 1100, 330
    out = svg_open(W, H)
    out.append(text(550, 28, 'Регулятор Raibert (1983–1986): три независимых простых закона вместо полной модели', 16, INK, 'middle', 700))
    items = [
        ('1. Высота прыжка', ['толчок ногой в фазе опоры', 'добавляет энергию;', 'регулирует высоту'], BLUE, '#eff6ff'),
        ('2. Скорость: куда ставить ногу', ['x_f = ẋ·T_s/2 + k(ẋ − ẋ_{зад})', 'нейтральная точка + поправка', 'на ошибку скорости'], GREEN, '#ecfdf5'),
        ('3. Наклон корпуса', ['момент в бедре во время', 'опоры выравнивает', 'корпус'], AMBER, '#fffbeb'),
    ]
    for k, (t, s, c, f) in enumerate(items):
        out += box(30 + k * 350, 60, 330, 130, t, s, c, f, 16, 14)
    out += wrap_lines(30, 230, ['Главная идея: устойчивость не обязана быть статической. Робот всё время «падает», но каждый шаг',
                                'ставит ногу так, чтобы падение компенсировалось. Это предшественник точки захвата (2006)',
                                'и путь Boston Dynamics: Raibert основал компанию в 1992 году.'], 15, INK, dy=24)
    write(os.path.join(OUT08, 'raibert_controller.svg'), out)


def l08_classical_stack():
    W, H = 1100, 330
    out = svg_open(W, H)
    out.append(text(550, 28, 'Классическая модельная схема управления гуманоидом (≈ 2010–2022)', 17, INK, 'middle', 700))
    blocks = [
        ('План шагов', ['A* по допустимым', 'местам постановки', '~1 Гц'], INK, PANEL),
        ('Траектория ЦМ', ['ZMP preview /', 'MPC центроидной', 'динамики, 10–100 Гц'], BLUE, '#eff6ff'),
        ('Полнотельное упр. (WBC)', ['QP с иерархией задач:', 'моменты всех суставов', '500–1000 Гц'], GREEN, '#ecfdf5'),
        ('Приводы', ['регуляторы тока', 'и момента', '≈ 10 кГц'], INK, PANEL),
    ]
    for k, (t, s, c, f) in enumerate(blocks):
        out += box(20 + k * 270, 60, 250, 120, t, s, c, f, 15, 13)
        if k < 3:
            out.append(arrow(20 + k * 270 + 250, 120, 20 + (k + 1) * 270 - 4, 120))
    out.append(text(150, 200, 'лекция 02', 13, MUTED, 'middle'))
    out.append(text(415, 200, 'лекция 05', 13, MUTED, 'middle'))
    out.append(rect(20, 220, 1060, 90, '#fff7ed', AMBER, 8, 1.4, '6 4'))
    out += wrap_lines(40, 248, ['Сильные стороны: предсказуемость, явные ограничения (трение, пределы моментов), объяснимость.',
                                'Слабые: нужна точная модель и ручная настройка десятков весов; трудно с неожиданными контактами,',
                                'скользкой опорой, падениями. Именно на этих местах обучаемые политики дали главный выигрыш.'], 14, INK, dy=22)
    write(os.path.join(OUT08, 'classical_stack.svg'), out)


def l08_wbc_qp():
    W, H = 1100, 330
    out = svg_open(W, H)
    out.append(text(550, 28, 'Полнотельное управление как задача квадратичного программирования', 17, INK, 'middle', 700))
    pr = [('Приоритет 1 (жёстко)', 'динамика; опора не скользит (конус трения); пределы моментов', RED, '#fee2e2'),
          ('Приоритет 2', 'равновесие: ускорение ЦМ и момент импульса по плану', AMBER, '#fffbeb'),
          ('Приоритет 3', 'движение стопы в переносе, руки к объекту', BLUE, '#eff6ff'),
          ('Приоритет 4', 'поза по умолчанию, плавность', MUTED, PANEL)]
    for k, (t, s, c, f) in enumerate(pr):
        out.append(rect(30, 52 + k * 52, 640, 44, f, c, 6, 1.4))
        out.append(text(46, 79 + k * 52, t, 14, c, 'start', 700))
        out.append(text(230, 79 + k * 52, s, 13, INK))
    out += wrap_lines(700, 70, ['Переменные: ускорения q̈,', 'силы контакта F, моменты τ.', '', 'min Σ wᵢ ‖Jᵢ q̈ + J̇ᵢ q̇ − ẍᵢ*‖²',
                                'при M q̈ + h = Sᵀτ + J_cᵀF,', '      F в конусе трения,', '      |τ| ≤ τ_{max}.', '',
                                'Решается заново ~1000 раз в секунду.'], 15, INK, dy=24)
    write(os.path.join(OUT08, 'wbc_qp.svg'), out)


def l08_motion_tracking():
    W, H = 1100, 360
    out = svg_open(W, H)
    out.append(text(550, 28, 'Обучение навыков по движениям человека: схема ZEST (2026; Atlas, Unitree G1, Spot)', 17, INK, 'middle', 700))
    srcs = [('Захват движения', 'мокап-костюм'), ('Видео', 'одна камера'), ('Анимация', 'без учёта физики')]
    for k, (t, s) in enumerate(srcs):
        out.append(rect(30, 56 + k * 66, 190, 54, '#e0f2fe', SKY, 6, 1.4))
        out.append(text(125, 78 + k * 66, t, 14, INK, 'middle', 700))
        out.append(text(125, 98 + k * 66, s, 13, MUTED, 'middle'))
        out.append(arrow(220, 83 + k * 66, 262, 150))
    out += box(266, 100, 200, 100, 'Перенос на робота', ['движение человека →', 'опорное движение', 'для суставов робота'], PURPLE, '#faf5ff', 14, 13)
    out.append(arrow(466, 150, 506, 150))
    out += box(510, 70, 300, 160, 'RL в симуляторе', ['награда: повторять опорное', 'движение; чаще трудные', 'фрагменты; вспомогательная', 'сила в начале обучения', '+ рандомизация параметров'], GREEN, '#ecfdf5', 15, 13)
    out.append(arrow(810, 150, 850, 150))
    out += box(854, 80, 220, 140, 'Робот', ['перенос без дообучения:', 'Atlas, Unitree G1,', 'четвероногий Spot'], INK, PANEL, 15, 13)
    out.append(rect(30, 268, 1044, 74, '#fffbeb', AMBER, 8, 1.4, '6 4'))
    out += wrap_lines(46, 294, ['Та же идея в Figure Helix 02 (2026): уровень S0 обучен по 1000+ часам движений людей, 200 000 сред',
                                'в симуляции, работает на 1 кГц и, по заявлению компании, заменил 109 504 строки ручного кода на C++.'], 14, INK, dy=22)
    write(os.path.join(OUT08, 'motion_tracking.svg'), out)


def l08_helix():
    W, H = 1100, 380
    out = svg_open(W, H)
    out.append(text(550, 28, 'Figure Helix: «медленная» и «быстрая» системы (2025) и полнотельный уровень S0 (Helix 02, 2026)', 16, INK, 'middle', 700))
    out += box(30, 60, 300, 120, 'S2: модель «зрение + язык»', ['7 млрд параметров, 7–9 Гц;', 'понимает сцену и команду;', 'выдаёт вектор-«намерение»'], PURPLE, '#faf5ff', 15, 13)
    out += box(400, 60, 300, 120, 'S1: визуомоторная политика', ['80 млн параметров, 200 Гц;', 'камеры + суставы + намерение', '→ цели для суставов'], BLUE, '#eff6ff', 15, 13)
    out += box(770, 60, 300, 120, 'S0: полнотельный регулятор', ['≈ 10 млн параметров, 1 кГц;', 'равновесие и контакты;', 'обучен RL (Helix 02)'], GREEN, '#ecfdf5', 15, 13)
    out.append(arrow(330, 120, 396, 120, PURPLE))
    out.append(text(363, 110, 'латентный', 12, PURPLE, 'middle'))
    out.append(text(363, 140, 'вектор', 12, PURPLE, 'middle'))
    out.append(arrow(700, 120, 766, 120, BLUE))
    out.append(arrow(920, 180, 920, 226, GREEN))
    out += box(770, 230, 300, 70, 'Приводы всего тела', ['ноги, корпус, руки, пальцы'], INK, PANEL, 15, 13)
    out += wrap_lines(30, 230, ['Helix (февраль 2025): 35 степеней свободы верхней части тела; ≈ 500 часов',
                                'телеуправляемых демонстраций; S2 и S1 работают на двух бортовых GPU.',
                                'Helix 02 (январь 2026): S1 управляет всем телом, ниже добавлен S0.',
                                'Пример из отчёта: 4 минуты загрузки посудомойки без вмешательства.',
                                'Это данные компании, независимой проверки нет.'], 14, INK, dy=22)
    out.append(text(30, 356, 'Аналог идеи «две системы»: Kahneman, «Думай медленно… решай быстро». Та же схема у NVIDIA GR00T N1 (2025).', 13, MUTED))
    write(os.path.join(OUT08, 'helix_architecture.svg'), out)


def l08_vla_vs_wam():
    W, H = 1100, 340
    out = svg_open(W, H)
    out.append(text(550, 28, 'VLA и модель мира с действиями (WAM): что предсказывает сеть', 17, INK, 'middle', 700))
    out.append(rect(20, 50, 520, 270, '#eff6ff', BLUE, 10, 1.4))
    out.append(text(280, 78, 'VLA: «зрение + язык → действие»', 16, BLUE, 'middle', 700))
    out += box(40, 100, 170, 80, 'Вход', ['кадр + команда'], INK, '#ffffff', 14, 13)
    out += box(250, 100, 270, 80, 'Предобученная VLM', ['+ голова действий'], BLUE, '#ffffff', 14, 13)
    out.append(arrow(210, 140, 246, 140, BLUE))
    out += box(250, 210, 270, 70, 'Выход', ['действия a_{t:t+H}'], GREEN, '#ffffff', 14, 13)
    out.append(arrow(385, 180, 385, 206, BLUE))
    out.append(text(40, 300, 'RT-2, OpenVLA, π₀, GR00T N1, Helix', 13, MUTED))
    out.append(rect(560, 50, 520, 270, '#ecfdf5', GREEN, 10, 1.4))
    out.append(text(820, 78, 'WAM: «видео + действие» совместно', 16, GREEN, 'middle', 700))
    out += box(580, 100, 170, 80, 'Вход', ['кадры + команда'], INK, '#ffffff', 14, 13)
    out += box(790, 100, 270, 80, 'Предобученная', ['видеодиффузионная модель'], GREEN, '#ffffff', 14, 13)
    out.append(arrow(750, 140, 786, 140, GREEN))
    out += box(790, 210, 130, 70, 'Будущие', ['кадры'], PURPLE, '#ffffff', 14, 13)
    out += box(930, 210, 130, 70, 'Действия', ['a_{t:t+H}'], GREEN, '#ffffff', 14, 13)
    out.append(arrow(925, 180, 855, 206, GREEN))
    out.append(arrow(925, 180, 995, 206, GREEN))
    out.append(text(580, 300, 'DreamZero (NVIDIA, 2026): 14 млрд параметров, 7 Гц', 13, MUTED))
    write(os.path.join(OUT08, 'vla_vs_wam.svg'), out)


def l08_frequency_hierarchy():
    W, H = 1100, 330
    out = svg_open(W, H)
    out.append(text(550, 28, 'Частоты уровней управления современного гуманоида (логарифмическая шкала)', 17, INK, 'middle', 700))
    a = Axes(290, 50, 760, 230, (-1, 4.3), (0, 7))
    for e in range(-1, 5):
        X = a.px(e)
        out.append(line(X, a.y0, X, a.y0 + a.h, GRID, 1))
        lab = {-1: '0.1 Гц', 0: '1 Гц', 1: '10 Гц', 2: '100 Гц', 3: '1 кГц', 4: '10 кГц'}[e]
        out.append(text(X, a.y0 + a.h + 18, lab, 13, MUTED, 'middle'))
    rows = [('языковой планировщик задачи', -1, 0, PURPLE), ('S2 Helix (VLM, 7 млрд)', math.log10(7), math.log10(9), PURPLE),
            ('WAM DreamZero (14 млрд)', math.log10(7), math.log10(7), GREEN), ('диффузионная политика', 1, math.log10(30), BLUE),
            ('S1 Helix (80 млн)', math.log10(200), math.log10(200), BLUE), ('S0 / RL-регулятор тела', 2.7, 3, GREEN),
            ('регулятор тока привода', 4, 4.3, INK)]
    for k, (lab, lo, hi, col) in enumerate(rows):
        y = a.py(6.5 - k)
        out.append(text(280, y + 5, lab, 14, INK, 'end'))
        x1, x2 = a.px(lo), max(a.px(hi), a.px(lo) + 10)
        out.append(rect(x1, y - 10, x2 - x1, 20, col, col, 4, 1))
    out.append(text(550, 318, 'Чем выше уровень, тем больше модель и реже решение; быстрые уровни небольшие и работают на борту.', 14, MUTED, 'middle'))
    write(os.path.join(OUT08, 'frequency_hierarchy.svg'), out)


def l08_course_map():
    W, H = 1100, 380
    out = svg_open(W, H)
    out.append(text(550, 28, 'Гуманоид как сумма курса: какой уровень опирается на какую лекцию', 17, INK, 'middle', 700))
    rows = [('Понять задачу и сцену', 'VLM / VLA, язык (S2)', 'лекция 08', PURPLE),
            ('Где можно стоять и идти', 'карты, проходимость, C-пространство', 'лекция 01', INK),
            ('Маршрут и места шагов', 'поиск на графе, выборка', 'лекции 02–03', INK),
            ('Как двигаться к цели', 'профиль скорости, модели движения, MPPI', 'лекции 02, 04', BLUE),
            ('Равновесие и траектория ЦМ', 'LIPM, точка захвата, MPC', 'лекции 05, 08', BLUE),
            ('Поведение по данным', 'RL, имитация, диффузия', 'лекции 06–07', GREEN),
            ('Безопасность', 'ограничения в MPC, фильтр CBF', 'лекции 05–06', RED)]
    for k, (a1, b1, c1, col) in enumerate(rows):
        y = 52 + k * 44
        out.append(rect(30, y, 1040, 38, PANEL if k % 2 else '#ffffff', GRID, 4, 1))
        out.append(text(46, y + 25, a1, 15, col, 'start', 700))
        out.append(text(420, y + 25, b1, 14, INK))
        out.append(text(1054, y + 25, c1, 14, MUTED, 'end', 700))
    write(os.path.join(OUT08, 'course_map.svg'), out)


# ===========================================================================
# Лекция 08: условные силуэты роботов (рисунки, не фотографии)
# ===========================================================================

BODY, EDGE = '#e2e8f0', '#334155'


def limb(pts, w, fill=BODY, edge=EDGE):
    """Конечность: толстая ломаная с обводкой."""
    return [polyline(pts, edge, w + 3), polyline(pts, fill, w)]


def shape(d, fill=BODY, edge=EDGE, width=1.6):
    return f'<path d="{d}" fill="{fill}" stroke="{edge}" stroke-width="{width}" stroke-linejoin="round"/>'


def humanoid(cx, gy, H, head='round', bulk=1.0, fill=BODY, accent=None, legs='straight', pose='stand', edge=EDGE):
    """Человекоподобный силуэт высотой H пикселей, стопы на линии gy.

    head: round | visor | box | lamp | none; legs: straight | bird (колени назад, вид сбоку) | wheels;
    pose: stand | tuck (прыжок с поджатыми ногами) | arms_up.
    """
    out = []
    acc = accent or fill
    y = lambda f: gy - f * H
    sw, hw = 0.135 * H * bulk, 0.075 * H * bulk           # полуширина плеч и таза
    sh, hip = y(0.80), y(0.50)
    lw, aw = max(4, 0.07 * H * bulk), max(3, 0.05 * H * bulk)
    # ноги
    if pose == 'tuck':
        for s in (-1, 1):
            out += limb([(cx + s * hw * 0.8, hip), (cx + s * hw * 1.4, y(0.40)), (cx + s * hw * 0.9, y(0.28))], lw, fill, edge)
    elif legs == 'bird':
        for s, dx in ((-1, -0.02), (1, 0.02)):
            out += limb([(cx + dx * H, hip), (cx + dx * H + 0.07 * H, y(0.30)), (cx + dx * H - 0.03 * H, y(0.14)),
                         (cx + dx * H + 0.01 * H, y(0.02))], lw * 0.8, fill, edge)
            out.append(shape(f'M{cx + dx * H - 0.04 * H:.1f},{gy:.1f} h{0.10 * H:.1f} l-0.0,-{0.025 * H:.1f} h-{0.10 * H:.1f} z', fill, edge))
    elif legs == 'wheels':
        for s in (-1, 1):
            out += limb([(cx + s * hw * 0.7, hip), (cx + s * hw * 0.9, y(0.12))], lw, fill, edge)
            out.append(circle(cx + s * hw * 0.9, gy - 0.07 * H, 0.07 * H, '#475569', edge))
    else:
        for s in (-1, 1):
            out += limb([(cx + s * hw * 0.75, hip), (cx + s * hw * 0.85, y(0.27)), (cx + s * hw * 0.85, y(0.035))], lw, fill, edge)
            out.append(shape(f'M{cx + s * hw * 0.85 - 0.045 * H:.1f},{gy:.1f} h{0.09 * H:.1f} v-{0.03 * H:.1f} '
                             f'q-{0.02 * H:.1f},-{0.012 * H:.1f} -{0.07 * H:.1f},0 z', fill, edge))
    # руки
    for s in (-1, 1):
        if pose in ('tuck', 'arms_up'):
            pts = [(cx + s * sw * 0.9, sh + 0.02 * H), (cx + s * sw * 1.5, y(0.90)), (cx + s * sw * 1.7, y(1.02))]
        else:
            pts = [(cx + s * sw * 0.95, sh + 0.02 * H), (cx + s * sw * 1.1, y(0.63)), (cx + s * sw * 1.05, y(0.47))]
        out += limb(pts, aw, fill, edge)
    # таз и туловище
    out.append(shape(f'M{cx - hw:.1f},{hip + 0.03 * H:.1f} L{cx + hw:.1f},{hip + 0.03 * H:.1f} L{cx + hw * 1.05:.1f},{y(0.58):.1f} '
                     f'L{cx - hw * 1.05:.1f},{y(0.58):.1f} z', fill, edge))
    out.append(shape(f'M{cx - sw:.1f},{sh:.1f} Q{cx:.1f},{sh - 0.03 * H:.1f} {cx + sw:.1f},{sh:.1f} L{cx + sw * 0.8:.1f},{y(0.57):.1f} '
                     f'L{cx - sw * 0.8:.1f},{y(0.57):.1f} z', fill, edge))
    if accent:
        out.append(shape(f'M{cx - sw * 0.55:.1f},{y(0.76):.1f} h{sw * 1.1:.1f} v{0.08 * H:.1f} h-{sw * 1.1:.1f} z', acc, 'none', 0))
    # голова
    hr = 0.065 * H
    hy = y(0.80) - 0.025 * H - hr
    if head != 'none':
        out.append(line(cx, sh, cx, hy + hr, edge, max(3, 0.03 * H)))
    if head == 'round':
        out.append(circle(cx, hy, hr, fill, edge, 1.6))
    elif head == 'visor':
        out.append(circle(cx, hy, hr, fill, edge, 1.6))
        out.append(shape(f'M{cx - hr * 0.8:.1f},{hy - hr * 0.25:.1f} h{hr * 1.6:.1f} v{hr * 0.6:.1f} h-{hr * 1.6:.1f} z', '#1e293b', 'none', 0))
    elif head == 'box':
        out.append(shape(f'M{cx - hr * 1.1:.1f},{hy - hr * 0.8:.1f} h{hr * 2.2:.1f} v{hr * 1.6:.1f} h-{hr * 2.2:.1f} z', fill, edge))
        out.append(circle(cx - hr * 0.45, hy, hr * 0.22, '#1e293b'))
        out.append(circle(cx + hr * 0.45, hy, hr * 0.22, '#1e293b'))
    elif head == 'lamp':
        out.append(circle(cx, hy, hr, fill, edge, 1.6))
        out.append(circle(cx, hy, hr * 0.55, accent or '#fde68a', '#1e293b', 1.2))
    return out


def quadruped(cx, gy, L, fill=BODY, edge=EDGE):
    """Четвероногий робот вид сбоку (BigDog), длина корпуса L пикселей."""
    out = []
    by = gy - 0.62 * L
    for x0, s in ((cx - 0.38 * L, 1), (cx - 0.25 * L, 1), (cx + 0.25 * L, -1), (cx + 0.38 * L, -1)):
        out += limb([(x0, by + 0.12 * L), (x0 + s * 0.12 * L, by + 0.35 * L), (x0, gy - 0.02 * L)], 0.05 * L, fill, edge)
    out.append(shape(f'M{cx - 0.5 * L:.1f},{by:.1f} h{L:.1f} v{0.18 * L:.1f} h-{L:.1f} z', fill, edge))
    out.append(shape(f'M{cx - 0.3 * L:.1f},{by - 0.06 * L:.1f} h{0.45 * L:.1f} v{0.06 * L:.1f} h-{0.45 * L:.1f} z', '#94a3b8', edge))
    return out


def ground(x1, x2, gy):
    return [line(x1, gy, x2, gy, '#94a3b8', 2), *[line(x, gy, x - 8, gy + 8, '#cbd5e1', 1) for x in range(int(x1) + 10, int(x2), 18)]]


def l08_bd_path():
    W, H = 1100, 410
    out = svg_open(W, H)
    out.append(text(550, 28, 'Путь Boston Dynamics: от четвероногого робота до электрического Atlas', 18, INK, 'middle', 700))
    gy, px_m = 290, 100                      # пикселей на метр
    out += ground(30, 1070, gy)
    out.append(line(60, gy - 1.5 * px_m, 60, gy, MUTED, 1))
    for m in (0.5, 1.0, 1.5):
        out.append(line(55, gy - m * px_m, 1070, gy - m * px_m, GRID, 1, '3 4'))
        out.append(text(50, gy - m * px_m + 4, f'{m:g} м', 11, MUTED, 'end'))
    items = [
        (150, '2005', 'BigDog', ['четыре ноги, гидравлика,', 'двигатель внутр. сгорания'], 'quad'),
        (355, '2013', 'Atlas (DARPA)', ['гидравлика, кабель питания', '≈ 1.88 м, ≈ 150 кг'], 'atlas13'),
        (560, '2016', 'новый Atlas', ['свой аккумулятор,', 'ходьба по снегу'], 'atlas16'),
        (765, '2017–2021', 'Atlas: сальто, паркур', ['движения оптимизированы', 'заранее, MPC на борту'], 'tuck'),
        (970, '2024', 'электрический Atlas', ['электроприводы,', 'обучение по движениям людей'], 'eatlas'),
    ]
    for cx, yr, name, cap, kind in items:
        if kind == 'quad':
            out += quadruped(cx, gy, 1.1 * px_m)
        elif kind == 'atlas13':
            out.append(polyline([(cx, gy - 1.95 * px_m), (cx + 30, gy - 2.25 * px_m), (cx + 70, gy - 2.25 * px_m)], '#475569', 2, '5 3'))
            out.append(text(cx + 76, gy - 2.21 * px_m, 'страховочный трос', 11, MUTED))
            out += humanoid(cx, gy, 1.88 * px_m, 'box', 1.35, '#cbd5e1', '#64748b')
        elif kind == 'atlas16':
            out += humanoid(cx, gy, 1.5 * px_m, 'box', 1.05, BODY, '#64748b')
        elif kind == 'tuck':
            sub = humanoid(cx, gy - 0.45 * px_m, 1.5 * px_m, 'box', 1.05, BODY, '#64748b', pose='tuck')
            out += sub
            out.append(f'<path d="M{cx - 70},{gy - 40} A 80 80 0 0 1 {cx + 70},{gy - 40}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#arrB)"/>')
        else:
            out += humanoid(cx, gy, 1.5 * px_m, 'lamp', 0.95, '#f1f5f9', '#bfdbfe')
        out.append(text(cx, gy + 30, yr, 15, BLUE, 'middle', 700))
        out.append(text(cx, gy + 50, name, 14, INK, 'middle', 700))
        out += wrap_lines(cx, gy + 70, cap, 12.5, MUTED, 'middle', 17)
    for a, b in ((150, 355), (355, 560), (560, 765), (765, 970)):
        out.append(arrow(a + 58, gy + 25, b - 58, gy + 25, LIGHT, 1.6))
    out.append(text(1070, 400, 'Условные силуэты в одном масштабе; рост и масса — по данным компании и DARPA.', 12, MUTED, 'end'))
    write(os.path.join(OUT08, 'bd_path.svg'), out)


def l08_lineup():
    W, H = 1100, 420
    out = svg_open(W, H)
    out.append(text(550, 28, 'Современные гуманоиды в одном масштабе (рост и масса — по данным производителей)', 17, INK, 'middle', 700))
    gy, px_m = 300, 130
    out += ground(40, 1080, gy)
    for m in (0.5, 1.0, 1.5, 2.0):
        out.append(line(70, gy - m * px_m, 1080, gy - m * px_m, GRID, 1, '3 4'))
        out.append(text(62, gy - m * px_m + 4, f'{m:g} м', 11, MUTED, 'end'))
    US, CN, JP, EU = BLUE, RED, MUTED, PURPLE
    bots = [
        ('человек', '', 1.75, None, 'ref', JP),
        ('ASIMO', 'Honda, 2011', 1.30, 48, dict(head='visor', bulk=1.15, fill='#f8fafc'), JP),
        ('Atlas', 'BD, 2013', 1.88, 150, dict(head='box', bulk=1.35, fill='#cbd5e1', accent='#64748b'), US),
        ('Digit', 'Agility', 1.75, 65, dict(head='box', bulk=0.9, legs='bird', fill='#e2e8f0', accent='#a5b4fc'), US),
        ('Figure 02', 'Figure AI, 2024', 1.68, 70, dict(head='visor', bulk=0.95, fill='#e5e7eb', accent='#334155'), US),
        ('Optimus', 'Tesla, 2022', 1.73, 73, dict(head='visor', bulk=1.0, fill='#f8fafc', accent='#0f172a'), US),
        ('Apollo', 'Apptronik', 1.73, 73, dict(head='visor', bulk=1.05, fill='#f1f5f9', accent='#38bdf8'), US),
        ('NEO', '1X', 1.65, 30, dict(head='round', bulk=0.9, fill='#ede9e3', accent='#d6cfc4'), EU),
        ('H1', 'Unitree, 2023', 1.80, 47, dict(head='box', bulk=0.95, fill='#e2e8f0', accent='#1e293b'), CN),
        ('G1', 'Unitree, 2024', 1.32, 35, dict(head='visor', bulk=1.0, fill='#e2e8f0', accent='#1e293b'), CN),
        ('R1', 'Unitree, 2025', 1.21, 25, dict(head='visor', bulk=1.0, fill='#e2e8f0', accent='#1e293b'), CN),
    ]
    step = 960 / len(bots)
    for i, (name, who, h, m, kw, col) in enumerate(bots):
        cx = 115 + i * step
        if kw == 'ref':
            for e in humanoid(cx, gy, h * px_m, 'round', 0.85, '#ffffff', None, edge='#94a3b8'):
                out.append(e.replace('stroke="#334155"', 'stroke="#94a3b8"').replace('<path', '<path stroke-dasharray="4 3"'))
        else:
            out += humanoid(cx, gy, h * px_m, **kw)
        out.append(text(cx, gy + 24, name, 14, col if kw != 'ref' else MUTED, 'middle', 700))
        out.append(text(cx, gy + 42, who, 11.5, MUTED, 'middle'))
        out.append(text(cx, gy + 60, f'{h:.2f} м' + (f' · {m} кг' if m else ''), 12, INK, 'middle'))
    out += legend(70, 400, [('США', US, None)], 12)
    out += legend(150, 400, [('Китай', CN, None)], 12)
    out += legend(240, 400, [('Япония', JP, None)], 12)
    out += legend(340, 400, [('Норвегия и США', EU, None)], 12)
    out.append(text(1080, 400, 'Силуэты условные: показан рост и общий тип, не внешний вид.', 12, MUTED, 'end'))
    write(os.path.join(OUT08, 'humanoid_lineup.svg'), out)


def service_bot(cx, gy, H, fill='#f8fafc', edge=EDGE, accent=BLUE):
    """Колёсный сервисный робот: корпус-колокол, экран, голова."""
    out = [shape(f'M{cx - 0.22 * H:.1f},{gy - 0.04 * H:.1f} Q{cx - 0.2 * H:.1f},{gy - 0.55 * H:.1f} {cx - 0.12 * H:.1f},{gy - 0.62 * H:.1f} '
                 f'L{cx + 0.12 * H:.1f},{gy - 0.62 * H:.1f} Q{cx + 0.2 * H:.1f},{gy - 0.55 * H:.1f} {cx + 0.22 * H:.1f},{gy - 0.04 * H:.1f} z', fill, edge)]
    out.append(shape(f'M{cx - 0.09 * H:.1f},{gy - 0.45 * H:.1f} h{0.18 * H:.1f} v{0.13 * H:.1f} h-{0.18 * H:.1f} z', accent, edge, 1))
    out.append(circle(cx, gy - 0.78 * H, 0.15 * H, fill, edge, 1.6))
    out.append(circle(cx - 0.05 * H, gy - 0.79 * H, 0.025 * H, '#1e293b'))
    out.append(circle(cx + 0.05 * H, gy - 0.79 * H, 0.025 * H, '#1e293b'))
    out.append(shape(f'M{cx - 0.24 * H:.1f},{gy:.1f} h{0.48 * H:.1f} v-{0.05 * H:.1f} h-{0.48 * H:.1f} z', '#475569', edge, 1))
    return out


def bust(cx, gy, H, fill='#fde7d4', edge=EDGE):
    """Андроид-бюст (сидячий робот с лицом)."""
    out = [shape(f'M{cx - 0.4 * H:.1f},{gy:.1f} Q{cx - 0.38 * H:.1f},{gy - 0.42 * H:.1f} {cx:.1f},{gy - 0.45 * H:.1f} '
                 f'Q{cx + 0.38 * H:.1f},{gy - 0.42 * H:.1f} {cx + 0.4 * H:.1f},{gy:.1f} z', '#94a3b8', edge)]
    out.append(f'<ellipse cx="{cx:.1f}" cy="{gy - 0.7 * H:.1f}" rx="{0.17 * H:.1f}" ry="{0.22 * H:.1f}" fill="{fill}" stroke="{edge}" stroke-width="1.6"/>')
    out.append(circle(cx - 0.06 * H, gy - 0.73 * H, 0.022 * H, '#1e293b'))
    out.append(circle(cx + 0.06 * H, gy - 0.73 * H, 0.022 * H, '#1e293b'))
    out.append(f'<path d="M{cx - 0.06 * H:.1f},{gy - 0.6 * H:.1f} q{0.06 * H:.1f},{0.04 * H:.1f} {0.12 * H:.1f},0" fill="none" stroke="{edge}" stroke-width="1.4"/>')
    return out


def hexapod(cx, gy, L, fill=BODY, edge=EDGE):
    """Шестиногий шагающий аппарат, вид сбоку."""
    out = []
    by = gy - 0.45 * L
    for k in range(3):
        x0 = cx - 0.35 * L + k * 0.35 * L
        out += limb([(x0, by + 0.05 * L), (x0 + 0.1 * L, by - 0.08 * L), (x0 + 0.16 * L, gy - 0.01 * L)], 0.035 * L, fill, edge)
        out += limb([(x0, by + 0.05 * L), (x0 - 0.08 * L, by - 0.05 * L), (x0 - 0.12 * L, gy - 0.01 * L)], 0.035 * L, '#cbd5e1', edge)
    out.append(shape(f'M{cx - 0.5 * L:.1f},{by:.1f} h{L:.1f} v{0.14 * L:.1f} h-{L:.1f} z', fill, edge))
    return out


def tilt(parts, cx, cy, deg):
    return [f'<g transform="rotate({deg} {cx:.1f} {cy:.1f})">'] + parts + ['</g>']


def l08_fedor_teleop():
    W, H = 1100, 360
    out = svg_open(W, H)
    out.append(text(550, 28, 'ФЁДОР: копирующее управление и полёт на МКС (2019)', 18, INK, 'middle', 700))
    gy = 290
    out += ground(40, 620, gy)
    op = humanoid(130, gy, 190, 'round', 0.9, '#fef3c7', None)
    out += op
    for (x1, y1, x2, y2) in ((95, gy - 150, 95, gy - 100), (165, gy - 150, 165, gy - 100), (112, gy - 90, 112, gy - 20), (148, gy - 90, 148, gy - 20)):
        out.append(line(x1, y1, x2, y2, PURPLE, 4))
    out.append(text(130, gy + 24, 'оператор', 14, INK, 'middle', 700))
    out.append(text(130, gy + 42, 'в задающем костюме', 12.5, MUTED, 'middle'))
    out += humanoid(520, gy, 190, 'visor', 1.05, '#e2e8f0', '#94a3b8')
    out.append(text(520, gy + 24, 'робот ФЁДОР', 14, INK, 'middle', 700))
    out.append(text(520, gy + 42, '(Skybot F-850)', 12.5, MUTED, 'middle'))
    out.append(arrow(210, 150, 440, 150, BLUE, 2.4))
    out.append(text(325, 140, 'углы суставов оператора', 13, BLUE, 'middle', 700))
    out.append(arrow(440, 200, 210, 200, GREEN, 2.4))
    out.append(text(325, 222, 'видео с камер, усилия', 13, GREEN, 'middle', 700))
    out.append(text(325, 250, 'робот повторяет движения человека', 12.5, MUTED, 'middle'))
    # хронология полёта
    out.append(rect(660, 56, 410, 290, '#f8fafc', '#cbd5e1', 10, 1.4))
    out.append(text(680, 82, 'Полёт «Союз МС-14», 2019 г.', 15, INK, 'start', 700))
    ev = [('22 авг', 'запуск с Байконура; робот в кресле командира'), ('24 авг', 'первая стыковка не удалась'),
          ('27 авг', 'стыковка после перестыковки корабля'), ('27 авг – 6 сен', 'опыты на станции'),
          ('7 сен', 'возвращение на Землю')]
    for k, (d, t) in enumerate(ev):
        y = 118 + k * 46
        out.append(circle(690, y - 5, 6, BLUE if k != 1 else RED))
        if k < len(ev) - 1:
            out.append(line(690, y + 1, 690, y + 35, LIGHT, 2))
        out.append(text(706, y, d, 13.5, INK, 'start', 700))
        out.append(text(706, y + 18, t, 12.5, MUTED))
    write(os.path.join(OUT08, 'fedor_teleop.svg'), out)


def l08_russia_timeline():
    W, H = 1100, 380
    out = svg_open(W, H)
    out.append(text(550, 28, 'Российские шагающие и антропоморфные роботы на одной шкале', 18, INK, 'middle', 700))
    ay = 286

    def X(yr):
        return 70 + (yr - 1970) / 15 * 120 if yr < 1990 else 290 + (yr - 2012) / (2026.5 - 2012) * 780
    out.append(line(60, ay, 240, ay, MUTED, 2))
    out.append(line(290, ay, 1080, ay, MUTED, 2))
    out.append(text(265, ay + 5, '//', 16, MUTED, 'middle', 700))
    for yr in (1970, 1980):
        out.append(line(X(yr), ay, X(yr), ay + 7, MUTED, 1.4))
        out.append(text(X(yr), ay + 24, str(yr), 12, MUTED, 'middle'))
    for yr in range(2014, 2027, 2):
        out.append(line(X(yr), ay, X(yr), ay + 7, MUTED, 1.4))
        out.append(text(X(yr), ay + 24, str(yr), 12, MUTED, 'middle'))
    gy = 196
    ev = [
        (1977, 'шагающий аппарат', 'ИПМ, 1970-е', 'hex', BLUE),
        (2015, 'Промобот', 'колёсный, сервисный', 'service', BLUE),
        (2017, 'ФЁДОР', 'для МЧС и ФПИ', 'fedor', BLUE),
        (2019.65, 'ФЁДОР на МКС', 'август 2019', 'fedor_iss', BLUE),
        (2019.9, 'Robo-C', 'лицо с мимикой', 'bust', BLUE),
        (2025.85, 'Грин (Сбер)', 'GigaChat', 'green', GREEN),
        (2025.88, 'AIDOL', 'упал на показе', 'aidol', RED),
    ]
    for k, (yr, name, sub, kind, col) in enumerate(ev):
        x = 120 + k * 146
        out.append(rect(x - 66, 50, 132, 186, '#f8fafc', '#e2e8f0', 10, 1.2))
        if kind == 'hex':
            out += hexapod(x, gy - 30, 100)
        elif kind == 'service':
            out += service_bot(x, gy, 110)
        elif kind == 'fedor':
            out += humanoid(x, gy, 125, 'visor', 1.0, '#e2e8f0', '#94a3b8')
        elif kind == 'fedor_iss':
            out.append(rect(x - 52, 58, 104, 146, '#eff6ff', '#bfdbfe', 8, 1.2))
            out.append(text(x + 44, 76, 'МКС', 12, BLUE, 'end', 700))
            out += humanoid(x, gy - 18, 100, 'visor', 1.0, '#e2e8f0', '#94a3b8', pose='arms_up')
        elif kind == 'bust':
            out += bust(x, gy, 120)
        elif kind == 'green':
            out += humanoid(x, gy, 125, 'visor', 0.95, '#f0fdf4', '#86efac')
        else:
            out += tilt(humanoid(x, gy, 125, 'visor', 0.95, '#f1f5f9', '#cbd5e1'), x + 10, gy, 24)
        out.append(text(x, gy + 20, name, 13.5, col, 'middle', 700))
        out.append(text(x, gy + 36, sub, 11.5, MUTED, 'middle'))
        out.append(line(x, 236, X(yr), ay - 4, LIGHT, 1.2, '3 3'))
        out.append(circle(X(yr), ay, 5, col))
    out += wrap_lines(60, 340, ['Точки на шкале — примерный год показа или события; Грин и AIDOL показаны в ноябре 2025 г. Силуэты условные.'], 12.5, MUTED, dy=19)
    write(os.path.join(OUT08, 'russia_timeline.svg'), out)


def main():
    print('Лекция 07:')
    l07_course_place()
    print('   время по профилю (поворот):', round(l07_path_vs_trajectory(), 3))
    print('   max κ сглаженной змейки:', round(l07_smoothing_curvature(), 3))
    l07_two_pass()
    print('   трапеция / S-профиль, с:', [round(x, 3) for x in l07_trapezoid_scurve()])
    print('   D* Lite (исходно, A* с нуля, ремонт):', l07_dstar_replanning())
    print('   g после перекрытия ребра:', l07_g_rhs())
    l07_frenet_frame()
    print('   интеграл рывка по T:', [(T, round(J, 2)) for T, J in l07_quintic_family()])
    print('   веер Френе:', l07_frenet_fan())
    l07_covariate_shift()
    l07_mse_vs_modes()
    l07_forward_noising()
    print('   DDPM (слева, через препятствие):', l07_reverse_process())
    l07_flow_vs_diffusion()
    l07_diffusion_policy_arch()
    l07_action_chunks()
    l07_act_arch()
    l07_nomad_arch()
    l07_topological_graph()
    print('Лекция 08:')
    l08_timeline()
    l08_static_vs_dynamic()
    print('   ω LIPM:', round(l08_lipm(), 3))
    l08_capture_band()
    print('   скорость в начале шага LIPM:', round(l08_lipm_walking(), 3))
    l08_raibert()
    l08_classical_stack()
    l08_wbc_qp()
    l08_motion_tracking()
    l08_helix()
    l08_vla_vs_wam()
    l08_frequency_hierarchy()
    l08_course_map()
    l08_bd_path()
    l08_lineup()
    l08_fedor_teleop()
    l08_russia_timeline()


if __name__ == '__main__':
    main()
