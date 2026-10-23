#!/usr/bin/env python3
"""
generate_slide_figures.py

Схемы для слайдов, где раньше был только короткий текст: каждая показывает
то, о чём говорит слайд, и строится расчётом.

Лекция 01:
- путь и траектория: одна кривая, на траектории — отметки времени по
  профилю скорости (два прохода, как в лекции 02);
- глобальный и локальный планировщик: путь по известной карте и окно
  локального планировщика с лучами дальномера и новым препятствием.
Лекция 05:
- семейства парабол x1 = ±x2²/2 + C при u = ±1 и две половины, ведущие в цель.
Лекция 07:
- задача движения по дороге: варианты «затормозить» и «перестроиться»;
- продольное движение: полиномы 4-й степени к целевой скорости;
- проверка столкновения во времени на плоскости (t, s);
- поведенческое клонирование и RL: откуда берётся сигнал обучения;
- генератор: одномерный шум превращается в один из двух объездов;
- наведение по стоимости: DDPM с тем же точным счётом, что в лекции 07,
  и новым препятствием при разных λ.
Лекция 08:
- от языковой модели к модели «зрение–язык–действие».

Запуск: python3 scripts/generate_slide_figures.py
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_lectures_05_06_diagrams import (  # noqa: E402
    svg_open, text, line, polyline, circle, rect, Axes, legend, write,
    linspace, box, INK, MUTED, LIGHT, GRID, BLUE, GREEN, AMBER, RED, PURPLE,
    PANEL, ROOT, SERIF,
)
from generate_lectures_07_08_diagrams import (  # noqa: E402
    arrow, wrap_lines, bspline, resample, two_pass, RefLine, quintic, pev,
    score, abar, scene_axes, draw_scene, XS, M_PTS,
)

OUT01 = os.path.join(ROOT, 'assets', 'images', 'lecture-01')
OUT05 = os.path.join(ROOT, 'assets', 'images', 'lecture-05')
OUT07 = os.path.join(ROOT, 'assets', 'images', 'lecture-07')
OUT08 = os.path.join(ROOT, 'assets', 'images', 'lecture-08')


# ===========================================================================
# Лекция 01
# ===========================================================================

def l01_path_vs_trajectory():
    """Одна кривая: слева — путь с отметками длины, справа — те же точки во времени."""
    ctrl = [(0, 0), (5, 0), (7, 1), (7, 5)]
    vmax, at, an = 1.5, 0.6, 0.5
    pts, kap = bspline(ctrl)
    xy, kk, ds, L = resample(pts, kap)
    vlim = [min(vmax, math.sqrt(an / k) if k > 1e-6 else 1e9) for k in kk]
    _, _, v, T = two_pass(vlim, ds, at)
    # время прихода в каждую точку
    tt = [0.0]
    for i in range(len(v) - 1):
        vv = v[i] + v[i + 1]
        tt.append(tt[-1] + (2 * ds / vv if vv > 1e-9 else 0))
    W, H = 1100, 330
    out = svg_open(W, H)
    obst = [(1.6, 1.4, 3.6, 4.6), (8.4, -0.6, 9.4, 3.2)]

    def panel(a, title):
        res = [text(a.x0 + a.w / 2, 26, title, 16, INK, 'middle', 700)]
        res.append(rect(a.x0, a.y0, a.w, a.h, '#ffffff', GRID, 6, 1))
        for x0, y0, x1, y1 in obst:
            res.append(rect(a.px(x0), a.py(y1), a.px(x1) - a.px(x0), a.py(y0) - a.py(y1), '#e2e8f0', LIGHT, 3, 1))
        res.append(polyline([a.p(*p) for p in xy], BLUE, 3.2))
        res.append(circle(*a.p(*xy[0]), 7, INK))
        res.append(circle(*a.p(*xy[-1]), 7, GREEN))
        res.append(text(a.px(xy[0][0]), a.py(xy[0][1]) + 26, 'старт', 13, INK, 'middle'))
        res.append(text(a.px(xy[-1][0]) - 12, a.py(xy[-1][1]) + 5, 'цель', 13, GREEN, 'end'))
        return res

    a = Axes(30, 44, 500, 240, (-0.8, 10), (-1, 5.6))
    out += panel(a, 'Путь σ(s): только геометрия')
    for s_mark in range(1, int(L) + 1):
        i = min(len(xy) - 1, round(s_mark / ds))
        out.append(circle(*a.p(*xy[i]), 4.5, '#fff', BLUE, 2))
    for s_mark in (2, 4, 6, 8):
        i = min(len(xy) - 1, round(s_mark / ds))
        dx = 0 if s_mark < 6 else 14
        dy = 22 if s_mark < 6 else 5
        out.append(text(a.px(xy[i][0]) + dx, a.py(xy[i][1]) + dy, f's = {s_mark} м', 13, BLUE, 'middle' if s_mark < 6 else 'start'))
    out.append(text(a.x0 + a.w / 2, a.y0 + a.h + 26, 'Отметки через 1 м длины: равномерные, времени нет', 14, MUTED, 'middle'))

    b = Axes(570, 44, 500, 240, (-0.8, 10), (-1, 5.6))
    out += panel(b, 'Траектория τ(t): тот же путь и время')
    k, tm = 0, 0.0
    while tm <= T + 1e-9:
        while k < len(tt) - 1 and tt[k] < tm:
            k += 1
        out.append(circle(*b.p(*xy[k]), 4.5, AMBER, '#fff', 1.2))
        tm += 1.0
    for t_mark in (2, 5, 8, 10):
        j = min(range(len(tt)), key=lambda q: abs(tt[q] - t_mark))
        dx = 0 if xy[j][0] < 6.5 else 14
        dy = 22 if xy[j][0] < 6.5 else 5
        out.append(text(b.px(xy[j][0]) + dx, b.py(xy[j][1]) + dy, f't = {t_mark} с', 13, AMBER, 'middle' if dx == 0 else 'start', 700))
    out.append(text(b.x0 + b.w / 2, b.y0 + b.h + 26, f'Отметки через 1 с: в повороте гуще (медленнее); весь путь за {T:.1f} с', 14, MUTED, 'middle'))
    write(os.path.join(OUT01, 'path_vs_trajectory_timing.svg'), out)
    return T


def l01_global_local():
    """Глобальный путь по известной карте и окно локального планировщика."""
    W, H = 1100, 340
    out = svg_open(W, H)
    a = Axes(30, 40, 640, 270, (0, 32), (0, 13.5))
    out.append(rect(a.x0, a.y0, a.w, a.h, '#ffffff', GRID, 6, 1))
    walls = [(6, 0, 7, 8), (13, 5.5, 14, 13.5), (20, 0, 21, 8), (26, 5.5, 27, 13.5)]
    for x0, y0, x1, y1 in walls:
        out.append(rect(a.px(x0), a.py(y1), a.px(x1) - a.px(x0), a.py(y0) - a.py(y1), '#cbd5e1', MUTED, 2, 1))
    route = [(2, 3), (4.5, 9.5), (9.5, 10.5), (12, 3.5), (16, 3), (18.5, 10), (23.5, 10.5), (25.5, 3.5), (30, 3.5)]
    out.append(polyline([a.p(*p) for p in route], BLUE, 3, '9 6'))
    out.append(circle(*a.p(*route[0]), 7, INK))
    out.append(circle(*a.p(*route[-1]), 7, GREEN))
    out.append(text(a.px(route[0][0]), a.py(route[0][1]) + 26, 'старт', 13, INK, 'middle'))
    out.append(text(a.px(route[-1][0]), a.py(route[-1][1]) + 26, 'цель', 13, GREEN, 'middle'))
    # робот на маршруте, окно 6 x 6 м перед ним
    rx, ry = 15.0, 3.25
    win = (rx - 0.6, ry - 2.6, rx + 4.2, ry + 3.4)
    out.append(rect(a.px(win[0]), a.py(win[3]), a.px(win[2]) - a.px(win[0]), a.py(win[1]) - a.py(win[3]), '#f0f9ff', BLUE, 4, 2))
    ox, oy, orad = 17.3, 3.2, 0.6
    # лучи дальномера: точное пересечение с кругом нового препятствия и краем окна
    for k in range(-60, 61, 8):
        th = math.radians(k)
        dx, dy = math.cos(th), math.sin(th)
        best = 3.9
        fx, fy = rx - ox, ry - oy
        bq = 2 * (fx * dx + fy * dy)
        cq = fx * fx + fy * fy - orad * orad
        disc = bq * bq - 4 * cq
        hit = False
        if disc >= 0:
            t1 = (-bq - math.sqrt(disc)) / 2
            if 0 < t1 < best:
                best, hit = t1, True
        out.append(line(*a.p(rx, ry), *a.p(rx + best * dx, ry + best * dy), RED if hit else '#fca5a5', 1.2 if hit else 0.8))
        if hit:
            out.append(circle(*a.p(rx + best * dx, ry + best * dy), 2.5, RED))
    out.append(circle(*a.p(ox, oy), orad * a.w / 32, '#fef3c7', AMBER, 2))
    # локальная траектория: огибает препятствие и возвращается к маршруту
    loc = [(rx, ry)] + [(rx + 3.9 * t, ry + 1.45 * math.sin(math.pi * min(1, t * 1.15)) * (1 - t) * 1.9) for t in linspace(0.05, 1, 30)]
    out.append(polyline([a.p(*p) for p in loc], GREEN, 3.2, marker='arrG'))
    out.append(circle(*a.p(rx, ry), 7, BLUE, '#fff', 2))
    # легенда и сравнение
    x0 = 700
    out.append(line(x0, 62, x0 + 34, 62, BLUE, 3, '9 6'))
    out.append(text(x0 + 44, 67, 'Глобальный путь σ(s)', 16, BLUE, 'start', 700))
    out += wrap_lines(x0 + 44, 92, ['по всей известной карте, от старта до цели;', 'пересчёт редко: 0.2–2 Гц или по запросу'], 14, INK, dy=20)
    out.append(rect(x0, 150, 34, 22, '#f0f9ff', BLUE, 3, 2))
    out.append(text(x0 + 44, 167, 'Окно 2–8 м вокруг робота', 16, BLUE, 'start', 700))
    out += wrap_lines(x0 + 44, 192, ['видит только то, что сейчас измерил датчик', '(лучи); пересчёт 20–50 Гц. Жёлтый круг —', 'новое препятствие, которого нет на карте'], 14, INK, dy=20)
    out.append(line(x0, 266, x0 + 34, 266, GREEN, 3.2, marker='arrG'))
    out.append(text(x0 + 44, 271, 'Локальная траектория', 16, GREEN, 'start', 700))
    out += wrap_lines(x0 + 44, 296, ['обходит новое препятствие и возвращается', 'к глобальному пути; на выходе (v, ω)'], 14, INK, dy=20)
    write(os.path.join(OUT01, 'global_vs_local.svg'), out)


# ===========================================================================
# Лекция 05
# ===========================================================================

def l05_parabola_families():
    W, H = 1100, 350
    out = svg_open(W, H)

    def panel(a, u, color, title, half_label):
        res = [text(a.x0 + a.w / 2, 26, title, 16, INK, 'middle', 700)]
        res += a.frame(xticks=(-2, -1, 0, 1, 2), yticks=(-2, -1, 0, 1, 2), xlabel='x₁ (положение)', ylabel='x₂ (скорость)')
        cid = 'pf' + ('p' if u > 0 else 'm')
        res.append(a.clip_id(cid))
        res.append(f'<g clip-path="url(#{cid})">')
        for C in (-3, -2, -1, 1, 2, 3):
            pts = [a.p(u * x2 * x2 / 2 + C, x2) for x2 in linspace(-2.6, 2.6, 80)]
            res.append(polyline(pts, color, 1.4, opacity=0.45))
        res.append(polyline([a.p(u * x2 * x2 / 2, x2) for x2 in linspace(-2.6, 2.6, 80)], color, 1.4, opacity=0.45))
        # половина параболы с C = 0, по которой тележка приходит в (0, 0)
        half = [a.p(u * x2 * x2 / 2, x2) for x2 in (linspace(-2.6, 0, 60) if u > 0 else linspace(2.6, 0, 60))]
        res.append(polyline(half, GREEN, 4))
        # стрелки направления: x2 растёт при u = +1 и убывает при u = −1
        for C in (-2, 0, 2):
            for x2 in (-1.4, 1.4):
                if abs(u * x2 * x2 / 2 + C) > 2.3:
                    continue
                y0, y1 = x2 - 0.15 * u, x2 + 0.15 * u
                p0, p1 = a.p(u * y0 * y0 / 2 + C, y0), a.p(u * y1 * y1 / 2 + C, y1)
                res.append(line(*p0, *p1, GREEN if C == 0 and x2 * u < 0 else color, 2.2, marker='arrG' if C == 0 and x2 * u < 0 else ('arrB' if u > 0 else 'arrR')))
        res.append('</g>')
        res.append(circle(a.px(0), a.py(0), 6, INK))
        lx, ly = (-0.15, -1.75) if u > 0 else (0.15, 1.6)
        res.append(text(a.px(lx), a.py(ly), half_label, 15, GREEN, 'end' if u > 0 else 'start', 700))
        return res

    a = Axes(70, 50, 400, 230, (-2.6, 2.6), (-2.4, 2.4))
    out += panel(a, 1, BLUE, 'u = +1:  x₁ = x₂²/2 + C, движение вверх', 'Γ₊ (C = 0, x₂ < 0)')
    b = Axes(620, 50, 400, 230, (-2.6, 2.6), (-2.4, 2.4))
    out += panel(b, -1, RED, 'u = −1:  x₁ = −x₂²/2 + C, движение вниз', 'Γ₋ (C = 0, x₂ > 0)')
    out.append(text(550, 342, 'Константа C сдвигает параболу вдоль x₁. В цель (0, 0) приходят только зелёные половины с C = 0.', 14, MUTED, 'middle'))
    write(os.path.join(OUT05, 'parabola_families.svg'), out)


# ===========================================================================
# Лекция 07
# ===========================================================================

ROAD = RefLine([(-6, 0), (0, 0), (18, 0.5), (34, 4.5), (50, 6.5), (70, 5.5)])


def car_svg(a, ref, s, d, fill, sc):
    _, _, th = ref.at(s)
    X, Y = a.p(*ref.xy(s, d))
    return (f'<g transform="translate({X:.1f},{Y:.1f}) rotate({-math.degrees(th):.1f})">'
            f'<rect x="{-2.25 * sc:.1f}" y="{-0.9 * sc:.1f}" width="{4.5 * sc:.1f}" height="{1.8 * sc:.1f}" rx="3" fill="{fill}"/></g>')


def l07_road_task():
    W, H = 1100, 300
    out = svg_open(W, H)
    a = Axes(20, 30, 1060, 250, (-11, 66), (-5, 11.5))
    sc = a.w / 77
    out.append(a.clip_id('rtc'))
    out.append('<g clip-path="url(#rtc)">')
    for d, col, wdt, dash in ((-1.75, MUTED, 2.2, None), (5.25, MUTED, 2.2, None), (1.75, LIGHT, 1.6, '12 10')):
        out.append(polyline([a.p(*ROAD.xy(s, d)) for s in linspace(-6, 72, 160)], col, wdt, dash))
    # «держись в 0.5 м левее середины полосы»: в (x, y) это кривая
    out.append(polyline([a.p(*ROAD.xy(s, 0.5)) for s in linspace(-6, 72, 160)], PURPLE, 1.8, '4 4'))
    ego, slow, other = 2.0, 30.0, 61.0
    # вариант 1: затормозить и встать за машиной
    stop = slow - 9
    out.append(polyline([a.p(*ROAD.xy(s, 0)) for s in linspace(ego + 2.5, stop, 40)], AMBER, 3.4, marker='arrA'))
    # вариант 2: перестроиться (полином 5-й степени по d), обогнать и вернуться
    out_c = quintic(0, 0, 0, 3.5, 0, 0, 1.0)
    back_c = quintic(3.5, 0, 0, 0, 0, 0, 1.0)
    path = []
    for s in linspace(ego + 2.5, 64, 140):
        if s < 14:
            d = 0
        elif s < 24:
            d = pev(out_c, (s - 14) / 10)[0]
        elif s < 38:
            d = 3.5
        elif s < 50:
            d = pev(back_c, (s - 38) / 12)[0]
        else:
            d = 0
        path.append(a.p(*ROAD.xy(s, d)))
    out.append(polyline(path, GREEN, 3.4, marker='arrG'))
    out.append(car_svg(a, ROAD, slow, 0, RED, sc))
    out.append(car_svg(a, ROAD, other, 3.5, MUTED, sc))
    out.append(car_svg(a, ROAD, ego, 0, BLUE, sc))
    out.append('</g>')
    ex, ey = a.p(*ROAD.xy(ego, 0))
    out.append(text(ex, ey + 30, 'робот', 14, BLUE, 'middle', 700))
    sx, sy = a.p(*ROAD.xy(slow, -1.75))
    out.append(text(sx, sy + 22, 'медленная машина', 14, RED, 'middle', 700))
    oxp, oyp = a.p(*ROAD.xy(other, 5.25))
    out.append(text(oxp, oyp - 12, 'соседняя полоса: тоже движутся', 14, MUTED, 'middle', 700))
    bx, by = a.p(*ROAD.xy(stop - 4, -1.75))
    out.append(text(bx, by + 22, '1. затормозить', 14, AMBER, 'middle', 700))
    gx, gy = a.p(*ROAD.xy(28, 3.5))
    out.append(text(gx - 40, gy - 18, '2. перестроиться, обогнать, вернуться', 14, GREEN, 'end', 700))
    px_, py_ = a.p(*ROAD.xy(58, -1.75))
    out.append(text(px_, py_ + 24, 'пунктир: «0.5 м левее середины» — в (x, y) кривая', 13, PURPLE, 'middle', 700))
    out.append(text(30, 296, 'Выбор пересчитывается каждые 0.1 с: машины сдвинулись, и лучший вариант мог смениться.', 14, MUTED))
    write(os.path.join(OUT07, 'road_task.svg'), out)


def quartic_speed(v0, a0, vT, T):
    """s(t) = c0 + … + c4 t⁴: s(0) = 0, ṡ(0) = v0, s̈(0) = a0, ṡ(T) = vT, s̈(T) = 0."""
    c1, c2 = v0, a0 / 2
    # 3c3 T² + 4c4 T³ = vT − c1 − 2c2 T;  6c3 T + 12c4 T² = −2c2
    r1, r2 = vT - c1 - 2 * c2 * T, -2 * c2
    det = 3 * T * T * 12 * T * T - 4 * T ** 3 * 6 * T
    c3 = (r1 * 12 * T * T - 4 * T ** 3 * r2) / det
    c4 = (3 * T * T * r2 - 6 * T * r1) / det
    return [0.0, c1, c2, c3, c4]


def qev(c, t, T, vT):
    """Положение, скорость, ускорение; после T — равномерно со скоростью vT."""
    tt = min(t, T)
    s = sum(c[k] * tt ** k for k in range(5))
    v = sum(k * c[k] * tt ** (k - 1) for k in range(1, 5))
    acc = sum(k * (k - 1) * c[k] * tt ** (k - 2) for k in range(2, 5))
    if t > T:
        s += vT * (t - T)
        acc = 0.0
    return s, v, acc


def l07_longitudinal():
    v0, vT = 10.0, 15.0
    W, H = 1100, 340
    out = svg_open(W, H)
    out.append(text(550, 26, f'Продольная цель — скорость: разгон с v₀ = {v0:g} до v_T = {vT:g} м/с полиномом 4-й степени за разное T', 16, INK, 'middle', 700))
    a = Axes(70, 66, 440, 200, (0, 6), (9, 16))
    out += a.frame(xticks=range(0, 7), yticks=(10, 12, 14, 16), xlabel='t, с', ylabel='скорость ṡ(t), м/с')
    b = Axes(620, 66, 440, 200, (0, 6), (-0.5, 4))
    out += b.frame(xticks=range(0, 7), yticks=(0, 1, 2, 3, 4), xlabel='t, с', ylabel='ускорение s̈(t), м/с²')
    cols = [RED, AMBER, GREEN, BLUE]
    peaks = []
    for T, c in zip((2, 3, 4, 5), cols):
        co = quartic_speed(v0, 0.0, vT, T)
        ts = linspace(0, 6, 120)
        out.append(polyline([a.p(t, qev(co, t, T, vT)[1]) for t in ts], c, 2.6))
        out.append(polyline([b.p(t, qev(co, t, T, vT)[2]) for t in ts], c, 2.4))
        peaks.append((T, max(qev(co, t, T, vT)[2] for t in ts)))
    out.append(line(a.px(0), a.py(vT), a.px(6), a.py(vT), LIGHT, 1.2, '6 5'))
    out.append(text(a.px(0.1), a.py(vT) - 8, 'v_T', 14, MUTED, 'start', 700))
    for k, ((T, p), c) in enumerate(zip(peaks, cols)):
        out += legend(70 + k * 250, 330, [(f'T = {T} с: пик ускорения {p:.1f} м/с²', c, None)], 13)
    out.append(text(b.px(5.9), b.py(3.6), 'Конечное положение s(T) не задано:', 13, MUTED, 'end'))
    out.append(text(b.px(5.9), b.py(3.6) + 18, 'у каждого T своё', 13, MUTED, 'end'))
    write(os.path.join(OUT07, 'longitudinal_quartic.svg'), out)
    return peaks


def l07_st_collision():
    """Плоскость (t, s): машина впереди в той же полосе и продольные варианты робота."""
    v0, lead0, vlead, gap = 12.0, 30.0, 6.0, 10.0
    T, Th = 4.0, 6.0
    W, H = 1100, 330
    out = svg_open(W, H)
    a = Axes(70, 40, 620, 250, (0, Th), (0, 90))
    out += a.frame(xticks=range(0, 7), yticks=(0, 20, 40, 60, 80), xlabel='t, с', ylabel='s, м (вдоль полосы)')
    ts = linspace(0, Th, 120)
    lead = [lead0 + vlead * t for t in ts]
    top = [a.p(t, s + 2.25) for t, s in zip(ts, lead)]
    low = [a.p(t, s - 2.25 - gap) for t, s in zip(ts, lead)]
    out.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in top + low[::-1])}" fill="#fee2e2" stroke="none"/>')
    out.append(polyline([a.p(t, s) for t, s in zip(ts, lead)], RED, 3))
    res = []
    for vT in (2, 4, 6, 8, 10, 12, 14):
        co = quartic_speed(v0, 0.0, vT, T)
        traj = [qev(co, t, T, vT)[0] for t in ts]
        hit = any(s + 2.25 > l - 2.25 - gap for s, l in zip(traj, lead))
        res.append((vT, hit))
        out.append(polyline([a.p(t, s) for t, s in zip(ts, traj)], '#fca5a5' if hit else GREEN, 2.6 if not hit else 1.8))
        if not hit:
            out.append(text(a.px(Th) + 6, a.py(traj[-1]) + 5, f'{vT} м/с', 13, GREEN, 'start', 700))
    ok = [v for v, h in res if not h]
    bad = [v for v, h in res if h]
    out.append(text(a.px(0.4), a.py(lead0 + vlead * 0.4 + 2.25) - 26, 'машина впереди, прогноз:', 13, RED, 'start', 700))
    out.append(text(a.px(0.4), a.py(lead0 + vlead * 0.4 + 2.25) - 10, f's = {lead0:g} + {vlead:g}·t', 13, RED, 'start'))
    out.append(text(a.px(0.15), a.py(lead0 - gap + 1.5), f'полоса: машина + зазор {gap:g} м', 13, RED, 'start'))
    x0 = 760
    out += wrap_lines(x0, 70, ['Робот: s(0) = 0, ṡ(0) = 12 м/с; 7 вариантов', 'с целевой скоростью v_T = 2 … 14 м/с,', 'T = 4 с (полином 4-й степени).'], 14, INK, dy=21)
    out.append(line(x0, 150, x0 + 30, 150, '#fca5a5', 2.4))
    out.append(text(x0 + 40, 155, f'в красной полосе: v_T = {bad[0]} … {bad[-1]} м/с', 14, RED, 'start', 700))
    out.append(line(x0, 180, x0 + 30, 180, GREEN, 2.6))
    out.append(text(x0 + 40, 185, f'допустимы: v_T = {", ".join(map(str, ok))} м/с', 14, GREEN, 'start', 700))
    out += wrap_lines(x0, 225, ['Столкновение — это пересечение во времени:', 'в момент t робот там же, где будет машина', 'в момент t. Обгон проверяется так же,', 'по полосе соседней полосы.'], 14, INK, dy=21)
    write(os.path.join(OUT07, 'st_collision.svg'), out)
    return ok, bad


def l07_bc_vs_rl():
    W, H = 1100, 300
    out = svg_open(W, H)
    out.append(text(20, 30, 'Поведенческое клонирование: сигнал обучения — действие человека', 16, PURPLE, 'start', 700))
    y = 48
    out += box(20, y, 220, 84, 'Человек управляет', ['пульт, VR, мокап'], INK, PANEL, 15, 13)
    out += box(300, y, 240, 84, 'Демонстрации', ['пары (o_i, a_i) на каждом', 'такте записи'], PURPLE, '#faf5ff', 15, 13)
    out += box(600, y, 230, 84, 'Регрессия', ['min Σ ‖a_i − π_θ(o_i)‖²', 'по весам θ'], PURPLE, '#faf5ff', 15, 13)
    out += box(890, y, 190, 84, 'Политика π_θ', ['робот: o → a'], BLUE, '#eff6ff', 15, 13)
    for x1, x2 in ((240, 296), (540, 596), (830, 886)):
        out.append(arrow(x1, y + 42, x2, y + 42, PURPLE, 2.2))
    out.append(text(20, 172, 'RL (лекция 06): сигнал обучения — награда за собственные пробы', 16, GREEN, 'start', 700))
    y = 190
    out += box(20, y, 220, 84, 'Политика π_θ', ['выбирает действие'], BLUE, '#eff6ff', 15, 13)
    out += box(300, y, 240, 84, 'Среда / симулятор', ['новое состояние', 'и награда r'], INK, PANEL, 15, 13)
    out += box(600, y, 230, 84, 'Оценка проб', ['какие действия дали', 'большую сумму наград'], GREEN, '#ecfdf5', 15, 13)
    out.append(arrow(240, y + 42, 296, y + 42, GREEN, 2.2))
    out.append(arrow(540, y + 42, 596, y + 42, GREEN, 2.2))
    out.append(polyline([(715, y + 84), (715, y + 102), (130, y + 102), (130, y + 88)], GREEN, 2.2, marker='arrG'))
    out.append(text(420, y + 98, 'обновление θ, новые пробы', 13, GREEN, 'middle'))
    out += wrap_lines(870, y + 22, ['Нужны: награда и', 'миллионы проб.', 'В BC — ни того,', 'ни другого.'], 14, MUTED, dy=20)
    write(os.path.join(OUT07, 'bc_vs_rl.svg'), out)


def l07_noise_to_modes():
    """Одномерный генератор: шум N(0, 1) → смесь N(±1.5, 0.2²) монотонным отображением квантилей."""
    mus, sig = (-1.5, 1.5), 0.2
    phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))

    def cdf_data(x):
        return sum(0.5 * phi((x - m) / sig) for m in mus)

    def inv_data(p):
        lo, hi = -4.0, 4.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if cdf_data(mid) < p:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    rng = random.Random(3)
    zs = sorted(rng.gauss(0, 1) for _ in range(16))
    acts = [inv_data(phi(z)) for z in zs]
    W, H = 1100, 350
    out = svg_open(W, H)
    a = Axes(140, 40, 800, 80, (-3, 3), (0, 0.45))
    b = Axes(140, 200, 800, 80, (-3, 3), (0, 1.1))
    gauss = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
    mix = lambda x: sum(0.5 * math.exp(-(x - m) ** 2 / (2 * sig * sig)) / (sig * math.sqrt(2 * math.pi)) for m in mus)
    xs = linspace(-3, 3, 240)
    out.append(line(a.x0, a.py(0), a.x0 + a.w, a.py(0), LIGHT, 1.2))
    out.append(line(b.x0, b.py(0), b.x0 + b.w, b.py(0), LIGHT, 1.2))
    out.append(polyline([a.p(x, gauss(x)) for x in xs], MUTED, 2.4))
    out.append(polyline([b.p(x, mix(x)) for x in xs], GREEN, 2.4))
    for z, act in zip(zs, acts):
        out.append(line(a.px(z), a.py(0), b.px(act), b.py(0), '#93c5fd', 1.2))
        out.append(circle(a.px(z), a.py(0), 4, BLUE))
        out.append(circle(b.px(act), b.py(0), 4.5, GREEN))
    # препятствие в середине: среднее демонстраций (ответ MSE) попадает в него
    out.append(rect(b.px(-0.6), b.py(1.1), b.px(0.6) - b.px(-0.6), b.py(0) - b.py(1.1), '#fee2e2', RED, 3, 1.2, '4 3'))
    out.append(circle(b.px(0), b.py(0), 6, RED))
    out.append(text(b.px(0), b.py(1.1) - 6, 'препятствие', 13, RED, 'middle', 700))
    out.append(text(b.px(0), b.py(0) + 22, 'среднее (ответ MSE)', 13, RED, 'middle', 700))
    for x in (-2, -1, 0, 1, 2):
        out.append(text(b.px(x), b.py(0) + 40, f'{x:+g}' if x else '0', 12, MUTED, 'middle'))
    out += wrap_lines(20, 70, ['Шум', 'z ~ N(0, 1)'], 15, INK, weight=700)
    out += wrap_lines(20, 230, ['Действие a:', 'смещение', 'объезда, м'], 15, INK, weight=700)
    left = sum(1 for v in acts if v < 0)
    out += wrap_lines(960, 140, ['генератор:', 'каждый шум →', 'свой вариант'], 14, BLUE, weight=700, dy=19)
    out.append(text(550, 342, f'16 выборок шума дали {left} объездов слева и {16 - left} справа, ни одного через середину (одномерный пример)', 14, MUTED, 'middle'))
    write(os.path.join(OUT07, 'noise_to_modes.svg'), out)
    return left


NEW_OBS = (1.4, 1.25, 0.55)   # новое препятствие: x, y, радиус (на пути объезда слева)


def guided_ddpm(K, n, seed, lam, margin=0.35):
    """DDPM с точной функцией оценки и наведением y ← y − λ∇c(y)."""
    ox, oy, r = NEW_OBS
    R = r + margin
    rng = random.Random(seed)
    ys = [[rng.gauss(0, 1) for _ in range(M_PTS)] for _ in range(n)]
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
            if lam > 0:
                # c(y) = Σ max(0, R − dist)², dist — от точки (x_i, y_i) до центра препятствия
                for i in range(M_PTS):
                    dx, dy = XS[i] - ox, mean[i] - oy
                    dist = math.hypot(dx, dy)
                    if dist < R:
                        grad = -2 * (R - dist) * dy / max(dist, 1e-6)
                        mean[i] -= lam * grad
            if k - 1 > 0:
                sig = math.sqrt((1 - abp) / (1 - ab) * beta)
                mean = [m + sig * rng.gauss(0, 1) for m in mean]
            new.append(mean)
        ys = new
    return ys


def l07_guidance():
    K, n = 20, 12
    ox, oy, r = NEW_OBS
    W, H = 1100, 300
    out = svg_open(W, H)
    stats = []
    for k, lam in enumerate((0.0, 1.0, 5.0)):
        ys = guided_ddpm(K, n, 6, lam)
        a = scene_axes(20 + k * 362, 50, 336, 200)
        out.append(rect(a.x0, a.y0, a.w, a.h, '#ffffff', GRID, 6, 1))
        out += draw_scene(a, ys, BLUE, 1.6, 0.85)
        out.append(f'<circle cx="{a.px(ox):.1f}" cy="{a.py(oy):.1f}" r="{r * a.w / 10:.1f}" fill="#fef3c7" stroke="{AMBER}" stroke-width="2"/>')
        hits = sum(1 for y in ys if any(math.hypot(XS[i] - ox, y[i] - oy) < r for i in range(M_PTS)))
        old = sum(1 for y in ys if any(math.hypot(XS[i], y[i]) < 0.9 for i in range(M_PTS)))
        peak = max(max(abs(v) for v in y) for y in ys)
        stats.append((lam, hits, old, round(peak, 2)))
        out.append(text(a.x0 + a.w / 2, 38, f'λ = {lam:g}', 16, INK, 'middle', 700))
        cap = {0: (f'без наведения: {hits} из {n} задевают новое', AMBER),
               1: (f'наведение: задевают новое {hits}, старое {old}', GREEN if hits + old == 0 else AMBER),
               2: (f'слишком сильно: {old} задевают старое', RED)}[k]
        out.append(text(a.x0 + a.w / 2, 272, cap[0], 14, cap[1], 'middle', 700))
    out.append(text(550, 294, 'Красный круг — препятствие из демонстраций, жёлтый — новое. Модель и выборки шума одни и те же, меняется только λ.', 13, MUTED, 'middle'))
    write(os.path.join(OUT07, 'guidance_lambda.svg'), out)
    return stats


# ===========================================================================
# Лекция 08
# ===========================================================================

def l08_llm_vlm_vla():
    W, H = 1100, 300
    out = svg_open(W, H)
    cols = [
        ('LLM: языковая модель', PURPLE, '#faf5ff', ['текст'], ['текст']),
        ('VLM: «зрение–язык»', BLUE, '#eff6ff', ['изображение', 'текст'], ['текст']),
        ('VLA: «зрение–язык–действие»', GREEN, '#ecfdf5', ['кадры камер', 'команда', 'состояние робота'], ['пакет действий', 'a_t … a_{t+H}']),
    ]
    x = 20
    for i, (title, c, fill, ins, outs) in enumerate(cols):
        w = 330
        out.append(rect(x, 40, w, 230, fill, c, 10, 2))
        out.append(text(x + w / 2, 66, title, 16, c, 'middle', 700))
        for j, s in enumerate(ins):
            out.append(rect(x + 16, 86 + j * 44, 120, 34, '#ffffff', GRID, 6, 1.2))
            out.append(text(x + 76, 108 + j * 44, s, 13, INK, 'middle'))
        mid = 86 + (len(ins) * 44 - 10) / 2
        out.append(arrow(x + 140, mid, x + 186, mid, c, 2.2))
        out.append(rect(x + 190, mid - 22 * len(outs) + 5, 124, 22 * len(outs) + 12, '#ffffff', c, 6, 1.6))
        for j, s in enumerate(outs):
            out.append(text(x + 252, mid - 22 * len(outs) + 26 + j * 22, s, 13, c, 'middle', 700))
        if i < 2:
            out.append(arrow(x + w + 2, 155, x + w + 24, 155, MUTED, 2))
        x += w + 26
    out += wrap_lines(36, 244, ['«убери посуду» → план словами'], 13, MUTED)
    out += wrap_lines(392, 244, ['«где ручка двери?» → ответ'], 13, MUTED)
    out += wrap_lines(748, 232, ['RT-2 (2023), OpenVLA (2024), π₀ (2024):', 'π₀ строит действия согласованием потоков'], 13, MUTED, dy=18)
    out.append(text(550, 294, 'Каждый шаг добавляет вход или выход. VLA получают дообучением VLM на записях действий робота', 14, MUTED, 'middle'))
    write(os.path.join(OUT08, 'llm_vlm_vla.svg'), out)


# ---------------------------------------------------------------------------
# Лекция 08: обучение ZEST
# ---------------------------------------------------------------------------

def l08_zest_training():
    """Схема двух приёмов ZEST; числа условные, как в задаче, а не из статьи."""
    W, H = 1100, 350
    out = svg_open(W, H)
    out.append(text(275, 24, 'Адаптивная выборка: чаще там, где ошибается', 16, INK, 'middle', 700))
    out.append(text(830, 24, 'Учебный план: вспомогательная сила убывает', 16, INK, 'middle', 700))
    segs = ['ходьба', 'поворот', 'присед', 'ползком', 'кувырок']
    err = [0.02, 0.04, 0.10, 0.25, 0.40]
    tot = sum(err)
    a = Axes(70, 56, 440, 200, (0, len(segs)), (0, 0.6))
    out += a.frame(yticks=(0, 0.2, 0.4, 0.6), ylabel='доля', fmt='{:g}')
    for i, (sname, e) in enumerate(zip(segs, err)):
        x = a.px(i + 0.18)
        wbar = (a.px(1) - a.px(0)) * 0.3
        out.append(rect(x, a.py(1 / len(segs)), wbar, a.py(0) - a.py(1 / len(segs)), '#cbd5e1', 'none', 2, 0))
        out.append(rect(x + wbar + 2, a.py(e / tot), wbar, a.py(0) - a.py(e / tot), PURPLE, 'none', 2, 0))
        out.append(text(a.px(i + 0.5), a.py(0) + 18, sname, 13, INK, 'middle'))
    out += legend(80, 312, [('поровну (без адаптации)', '#cbd5e1', None)], 13)
    out += legend(300, 312, [('∝ доле падений на фрагменте', PURPLE, None)], 13)
    b = Axes(630, 56, 420, 200, (0, 1), (0, 1.05))
    out += b.frame(xticks=(0, 0.5, 1), yticks=(0, 0.5, 1), xlabel='ход обучения', ylabel='сила / успех', fmt='{:g}')
    xs = linspace(0, 1, 100)
    succ = [1 / (1 + math.exp(-12 * (x - 0.45))) for x in xs]
    out.append(polyline([b.p(x, 1 - sv) for x, sv in zip(xs, succ)], AMBER, 2.8))
    out.append(polyline([b.p(x, sv) for x, sv in zip(xs, succ)], GREEN, 2.6, '7 4'))
    out.append(text(b.px(0.08), b.py(0.93), 'поддержка корпуса', 13, AMBER, 'start', 700))
    out.append(text(b.px(0.97), b.py(0.88), 'успех без поддержки', 13, GREEN, 'end', 700))
    out.append(text(840, 322, 'Силу уменьшают по мере того, как политика справляется сама', 13, MUTED, 'middle'))
    out.append(text(550, 344, 'Схема принципа; числа условные', 12, LIGHT, 'middle'))
    write(os.path.join(OUT08, 'zest_training.svg'), out)


def main():
    print('Дополнительные схемы слайдов:')
    print('   лекция 01, время пути:', round(l01_path_vs_trajectory(), 2))
    l01_global_local()
    l05_parabola_families()
    l07_road_task()
    print('   продольные полиномы (T, пик ускорения):', [(T, round(p, 2)) for T, p in l07_longitudinal()])
    print('   проверка (t, s): допустимы / столкновение:', l07_st_collision())
    l07_bc_vs_rl()
    print('   генератор 1D, объездов слева:', l07_noise_to_modes())
    print('   наведение (λ, задели новое, задели старое, max|y|):', l07_guidance())
    l08_llm_vlm_vla()
    l08_zest_training()


if __name__ == '__main__':
    main()
