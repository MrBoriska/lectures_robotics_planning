#!/usr/bin/env python3
"""
generate_lectures_05_06_diagrams.py

Схемы к лекциям 05 (оптимальное управление, MPC) и 06 (обучение с подкреплением).

Все графики строятся расчётом, без внешних зависимостей:
- функция Гамильтона как функция управления (аффинный и квадратичный случаи);
- точный фазовый портрет задачи быстродействия для двойного интегратора,
  временные зависимости u(t) и функции переключения lambda_2(t);
- сравнение быстродействия, минимума энергии и LQR с насыщением (RK4);
- начальные приближения в одиночной/многократной стрельбе и коллокации;
- портрет разреженности матрицы ККТ многократной стрельбы;
- логарифмический барьер и центральная траектория;
- замкнутый контур MPC с прогнозами (QP решается проекцией градиента);
- веса дисконтирования, усечённая целевая функция PPO;
- фильтр безопасности на основе барьерной функции (CBF).

Запуск: python3 scripts/generate_lectures_05_06_diagrams.py
"""

import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT05 = os.path.join(ROOT, 'assets', 'images', 'lecture-05')
OUT06 = os.path.join(ROOT, 'assets', 'images', 'lecture-06')

# Палитра темы robotics-minimal
INK = '#0f172a'
MUTED = '#475569'
LIGHT = '#94a3b8'
GRID = '#e2e8f0'
BLUE = '#2563eb'
SKY = '#0284c7'
GREEN = '#059669'
AMBER = '#d97706'
RED = '#dc2626'
PURPLE = '#7c3aed'
BG = '#ffffff'
PANEL = '#f8fafc'

SANS = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"
SERIF = "'Times New Roman', 'STIX Two Text', serif"


# ---------------------------------------------------------------------------
# Базовые примитивы SVG
# ---------------------------------------------------------------------------

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def svg_open(w, h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" font-family="{SANS}">',
            f'<rect width="{w}" height="{h}" fill="{BG}"/>',
            '<defs>'
            f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
            f'<marker id="arrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
            f'<marker id="arrR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>'
            f'<marker id="arrG" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker>'
            f'<marker id="arrP" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{PURPLE}"/></marker>'
            f'<marker id="arrA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/></marker>'
            '</defs>']


def rich(s):
    """Разметка индексов: a_t, a_{t+1} -> нижний индекс; e^{-1}, x^T -> верхний."""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c in '_^' and i + 1 < len(s) and s[i + 1] not in ' ,)':
            if s[i + 1] == '{':
                j = s.index('}', i)
                body, i = s[i + 2:j], j + 1
            else:
                body, i = s[i + 1], i + 2
            shift = 'sub' if c == '_' else 'super'
            out.append(f'<tspan baseline-shift="{shift}" font-size="72%">{esc(body)}</tspan>')
        else:
            out.append(esc(c))
            i += 1
    return ''.join(out)


def text(x, y, s, size=15, color=INK, anchor='start', weight=400, italic=False, family=None):
    fam = f' font-family="{family}"' if family else ''
    st = ' font-style="italic"' if italic else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{st}{fam}>{rich(s)}</text>')


def line(x1, y1, x2, y2, color=MUTED, width=1.5, dash=None, marker=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = f' marker-end="url(#{marker})"' if marker else ''
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}"{d}{m}/>')


def polyline(pts, color=BLUE, width=2.2, dash=None, fill='none', opacity=1.0, marker=None):
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = f' marker-end="url(#{marker})"' if marker else ''
    return (f'<polyline points="{p}" fill="{fill}" stroke="{color}" stroke-width="{width}" '
            f'stroke-linejoin="round" stroke-linecap="round" opacity="{opacity}"{d}{m}/>')


def polygon(pts, fill, opacity=1.0, stroke='none'):
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}"/>'


def circle(x, y, r, fill=BLUE, stroke='none', width=1.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def rect(x, y, w, h, fill=PANEL, stroke=GRID, rx=8, width=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"{d}/>')


class Axes:
    """Отображение координат данных в пиксели прямоугольной области."""

    def __init__(self, x0, y0, w, h, xlim, ylim):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xlim, self.ylim = xlim, ylim

    def px(self, x):
        return self.x0 + (x - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * self.w

    def py(self, y):
        return self.y0 + self.h - (y - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * self.h

    def p(self, x, y):
        return (self.px(x), self.py(y))

    def pts(self, xs, ys):
        return [self.p(x, y) for x, y in zip(xs, ys)]

    def frame(self, xticks=(), yticks=(), xlabel='', ylabel='', zero_axes=True, fmt='{:g}',
              tick_size=13):
        out = [rect(self.x0, self.y0, self.w, self.h, fill='#ffffff', stroke=GRID, rx=0, width=1)]
        for t in xticks:
            X = self.px(t)
            out.append(line(X, self.y0, X, self.y0 + self.h, GRID, 1))
            out.append(text(X, self.y0 + self.h + 18, fmt.format(t), tick_size, MUTED, 'middle'))
        for t in yticks:
            Y = self.py(t)
            out.append(line(self.x0, Y, self.x0 + self.w, Y, GRID, 1))
            out.append(text(self.x0 - 8, Y + 4, fmt.format(t), tick_size, MUTED, 'end'))
        if zero_axes:
            if self.ylim[0] < 0 < self.ylim[1]:
                out.append(line(self.x0, self.py(0), self.x0 + self.w, self.py(0), LIGHT, 1.3))
            if self.xlim[0] < 0 < self.xlim[1]:
                out.append(line(self.px(0), self.y0, self.px(0), self.y0 + self.h, LIGHT, 1.3))
        if xlabel:
            out.append(text(self.x0 + self.w, self.y0 + self.h + 36, xlabel, 15, INK, 'end', italic=True, family=SERIF))
        if ylabel:
            out.append(text(self.x0, self.y0 - 10, ylabel, 15, INK, 'start', italic=True, family=SERIF))
        return out

    def clip_id(self, name):
        return (f'<clipPath id="{name}"><rect x="{self.x0}" y="{self.y0}" width="{self.w}" height="{self.h}"/></clipPath>')


def legend(x, y, items, size=14, dy=22):
    out = []
    for i, (label, color, dash) in enumerate(items):
        Y = y + i * dy
        out.append(line(x, Y - 5, x + 26, Y - 5, color, 2.6, dash))
        out.append(text(x + 34, Y, label, size, INK))
    return out


def write(path, parts):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts + ['</svg>']) + '\n')
    print('  ->', os.path.relpath(path, ROOT))


def linspace(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def rk4(f, x, u, h):
    k1 = f(x, u)
    k2 = f([xi + h / 2 * ki for xi, ki in zip(x, k1)], u)
    k3 = f([xi + h / 2 * ki for xi, ki in zip(x, k2)], u)
    k4 = f([xi + h * ki for xi, ki in zip(x, k3)], u)
    return [xi + h / 6 * (a + 2 * b + 2 * c + d) for xi, a, b, c, d in zip(x, k1, k2, k3, k4)]


def dint(x, u):
    """Двойной интегратор: x1' = x2, x2' = u."""
    return [x[1], u]


# ---------------------------------------------------------------------------
# Лекция 05
# ---------------------------------------------------------------------------

def l05_cart_example():
    """Сквозной пример лекции 05: тележка на рельсе и её состояние на фазовой плоскости."""
    W, H = 1100, 310
    out = svg_open(W, H)
    out.append(text(24, 30, 'Сквозной пример: тележка (мобильный робот) должна остановиться точно у отметки x = 0', 18, INK, weight=700))
    # рельс и шкала
    X = lambda v: 110 + (v + 1.2) / 1.6 * 520
    out.append(line(X(-1.25), 200, X(0.35), 200, INK, 3))
    for v in (-1.0, -0.5, 0.0):
        out.append(line(X(v), 200, X(v), 212, INK, 2))
        out.append(text(X(v), 234, f'{v:g} м'.replace('-', '−'), 14, MUTED, 'middle'))
    out.append(line(X(0), 110, X(0), 200, RED, 3, '6 4'))
    out.append(text(X(0) + 8, 120, 'точка остановки', 14, RED, 'start', 700))
    # тележка в x = -1
    cx = X(-1.0)
    out.append(rect(cx - 50, 148, 100, 40, '#dbeafe', BLUE, 6, 2))
    out.append(circle(cx - 30, 192, 8, INK))
    out.append(circle(cx + 30, 192, 8, INK))
    out.append(line(cx, 140, cx, 200, BLUE, 1.5, '3 3'))
    out.append(line(cx + 52, 168, cx + 130, 168, AMBER, 3, marker='arrA'))
    out.append(text(cx + 60, 152, 'u — ускорение, |u| ≤ 1 м/с²', 14, AMBER, 'start', 700))
    out.append(text(cx, 136, 'x₁ — положение', 14, BLUE, 'middle', 700))
    out.append(text(110, 270, 'Состояние: x₁ — положение (м), x₂ = ẋ₁ — скорость (м/с).', 15, INK))
    out.append(text(110, 294, 'Модель: ẋ₁ = x₂,  ẋ₂ = u. Старт: x = (−1; 0). Цель: x = (0; 0).', 15, INK))
    # фазовая плоскость
    a = Axes(760, 70, 290, 190, (-1.4, 0.6), (-0.6, 1.3))
    out += a.frame(xticks=(-1, 0), yticks=(0, 1), xlabel='x₁', ylabel='x₂ (фазовая плоскость)')
    out.append(circle(*a.p(-1, 0), 7, BLUE, '#fff', 2))
    out.append(text(a.px(-1) + 4, a.py(0) + 24, 'старт', 14, BLUE, 'middle', 700))
    out.append(circle(*a.p(0, 0), 7, GREEN, '#fff', 2))
    out.append(text(a.px(0) + 10, a.py(0) + 24, 'цель', 14, GREEN, 'start', 700))
    ts = linspace(0, 2, 60)
    pts = []
    for t in ts:
        if t <= 1:
            pts.append(a.p(-1 + t * t / 2, t))
        else:
            tau = t - 1
            pts.append(a.p(-0.5 + tau - tau * tau / 2, 1 - tau))
    out.append(polyline(pts, PURPLE, 2.2, '6 4'))
    out.append(text(a.px(-0.5), a.py(1.0) - 10, 'одно из движений', 13, PURPLE, 'middle'))
    write(os.path.join(OUT05, 'cart_example.svg'), out)


def l05_hamiltonian_vs_u():
    W, H = 1000, 400
    out = svg_open(W, H)
    out.append(text(24, 30, 'Где находится наибольшее значение функции на отрезке −1 ≤ u ≤ 1 (голубая полоса)', 18, INK, weight=700))

    # (а) аффинная по u динамика: H = h0 + sigma*u
    a = Axes(70, 70, 380, 250, (-1.5, 1.5), (-1.6, 1.6))
    out += a.frame(xticks=(-1, 0, 1), yticks=(-1, 0, 1), xlabel='u', ylabel='F(u)')
    out.append(polygon([a.p(-1, -1.6), a.p(1, -1.6), a.p(1, 1.6), a.p(-1, 1.6)], '#dbeafe', 0.45))
    for sig, col, lab in ((0.9, BLUE, 'наклон > 0'), (-0.6, RED, 'наклон < 0')):
        us = linspace(-1.5, 1.5, 2)
        out.append(polyline(a.pts(us, [0.1 + sig * u for u in us]), col, 1.4, '5 4', opacity=0.6))
        us = linspace(-1, 1, 2)
        out.append(polyline(a.pts(us, [0.1 + sig * u for u in us]), col, 2.8))
        ustar = 1 if sig > 0 else -1
        X, Y = a.p(ustar, 0.1 + sig * ustar)
        out.append(circle(X, Y, 6, col, '#fff', 2))
        out.append(text(X + 10, Y - 12, f'{lab}:  u* = {ustar:+d}', 14, col, 'start', 600))
    out.append(text(a.x0 + a.w / 2, a.y0 + a.h + 58, '(а) Прямая F = c + σu: производная σ нигде не равна нулю,', 14, MUTED, 'middle'))
    out.append(text(a.x0 + a.w / 2, a.y0 + a.h + 77, 'наибольшее значение — на конце отрезка: u* = +1 или −1', 14, MUTED, 'middle'))

    # (б) строго вогнутая по u функция: H = h0 + sigma*u - r u^2 / 2
    b = Axes(580, 70, 380, 250, (-1.5, 1.5), (-1.6, 1.6))
    out += b.frame(xticks=(-1, 0, 1), yticks=(-1, 0, 1), xlabel='u', ylabel='F(u)')
    out.append(polygon([b.p(-1, -1.6), b.p(1, -1.6), b.p(1, 1.6), b.p(-1, 1.6)], '#dbeafe', 0.45))
    r = 1.0
    out.append(b.clip_id('clipH'))
    out.append('<g clip-path="url(#clipH)">')
    for sig, col, h0 in ((0.5, GREEN, 0.2), (1.6, AMBER, -0.2)):
        us = linspace(-1.5, 1.5, 120)
        out.append(polyline(b.pts(us, [h0 + sig * u - r * u * u / 2 for u in us]), col, 1.4, '5 4', opacity=0.6))
        us = linspace(-1, 1, 80)
        out.append(polyline(b.pts(us, [h0 + sig * u - r * u * u / 2 for u in us]), col, 2.8))
        uu = sig / r
        if abs(uu) <= 1.5:
            out.append(circle(*b.p(uu, h0 + sig * uu - r * uu * uu / 2), 4, '#fff', col, 2))
        ustar = max(-1.0, min(1.0, uu))
        X, Y = b.p(ustar, h0 + sig * ustar - r * ustar ** 2 / 2)
        out.append(circle(X, Y, 6, col, '#fff', 2))
    out.append('</g>')
    out.append(text(b.px(0.55), b.py(-0.6), 'вершина внутри: u* = 0.5', 14, GREEN, 'middle', 600))
    out.append(text(b.px(0.35), b.py(1.3), 'вершина вне отрезка: u* = 1', 14, AMBER, 'middle', 600))
    out.append(text(b.x0 + b.w / 2, b.y0 + b.h + 58, '(б) Парабола F = c + σu − u²/2: если вершина u = σ внутри,', 14, MUTED, 'middle'))
    out.append(text(b.x0 + b.w / 2, b.y0 + b.h + 77, 'то F′(u*) = 0; если вне — максимум на ближайшем конце', 14, MUTED, 'middle'))
    write(os.path.join(OUT05, 'pmp_hamiltonian_vs_u.svg'), out)


def time_optimal_arc(x10, x20):
    """Аналитическое решение задачи быстродействия для двойного интегратора.

    Возвращает (u1, t_s, T, x1s, x2s): управление на первом участке, момент
    переключения, полное время и точку переключения на кривой Γ.
    """
    s = x10 + 0.5 * x20 * abs(x20)
    u1 = -1.0 if s > 0 else 1.0
    if s == 0:
        return (-math.copysign(1, x20), 0.0, abs(x20), x10, x20)
    # первый участок: x1 − x2²/(2 u1) = C
    C = x10 - x20 ** 2 / (2 * u1)
    # пересечение с ветвью Γ, где u2 = -u1: x1 = x2^2/(2 u2)
    u2 = -u1
    # C + x2^2/(2u1) = x2^2/(2u2)  ->  x2^2 (1/(2u2) - 1/(2u1)) = C -> x2^2 * (u1 - u2)/(2 u1 u2) = C
    x2s_sq = C * 2 * u1 * u2 / (u1 - u2)
    x2s = -u2 * math.sqrt(x2s_sq)  # на ветви Γ с управлением u2 скорость имеет знак −u2
    x1s = x2s ** 2 / (2 * u2)
    t_s = (x2s - x20) / u1
    T = t_s + abs(x2s)
    return (u1, t_s, T, x1s, x2s)


def l05_time_optimal_phase():
    W, H = 1100, 520
    out = svg_open(W, H)
    out.append(text(24, 30, 'Задача быстродействия для двойного интегратора: ẍ = u, |u| ≤ 1', 18, INK, weight=700))

    a = Axes(70, 66, 520, 400, (-3, 3), (-2.4, 2.4))
    out.append(a.clip_id('clipPP'))
    # области постоянного управления
    xs = linspace(-2.4, 2.4, 200)
    out.append('<g clip-path="url(#clipPP)">')
    # область u = −1 лежит справа от Γ, область u = +1 — слева
    pts_minus = [a.p(max(-3.0, min(3.0, -0.5 * v * abs(v))), v) for v in xs]
    out.append(polygon(pts_minus + [a.p(3, 2.4), a.p(3, -2.4)], '#fee2e2', 0.7))
    out.append(polygon(pts_minus + [a.p(-3, 2.4), a.p(-3, -2.4)], '#dbeafe', 0.7))
    out.append('</g>')
    out += a.frame(xticks=(-2, -1, 0, 1, 2), yticks=(-2, -1, 0, 1, 2), xlabel='x₁ = x', ylabel='x₂ = ẋ')
    out.append('<g clip-path="url(#clipPP)">')
    # семейства фазовых траекторий: x1 = x2^2/(2u) + C
    vs = linspace(-2.4, 2.4, 120)
    for C in (-2.5, -1.5, -0.5, 0.5, 1.5, 2.5):
        out.append(polyline(a.pts([v * v / 2 + C for v in vs], vs), BLUE, 1.0, '4 4', opacity=0.45))
        out.append(polyline(a.pts([-v * v / 2 + C for v in vs], vs), RED, 1.0, '4 4', opacity=0.45))
    out.append('</g>')
    # кривая переключения Γ
    vn = linspace(-2.2, 0, 60)
    vp = linspace(0, 2.2, 60)
    out.append(polyline(a.pts([v * v / 2 for v in vn], vn), INK, 3.2))
    out.append(polyline(a.pts([-v * v / 2 for v in vp], vp), INK, 3.2))
    out.append(text(a.px(0.95), a.py(-1.95), 'Γ₊ (u = +1)', 14, INK, 'end', 700))
    out.append(text(a.px(-0.95), a.py(1.8), 'Γ₋ (u = −1)', 14, INK, 'start', 700))
    out.append(text(a.px(2.95), a.py(2.15), 'u* = −1', 15, RED, 'end', 700))
    out.append(text(a.px(-2.95), a.py(-2.25), 'u* = +1', 15, BLUE, 'start', 700))

    # две оптимальные траектории (аналитически)
    traj_info = []
    for (x10, x20), col in (((-1.0, 0.0), '#1d4ed8'), ((2.0, 1.0), '#b91c1c')):
        u1, ts, T, x1s, x2s = time_optimal_arc(x10, x20)
        t1 = linspace(0, ts, 60)
        p1 = [(x10 + x20 * t + u1 * t * t / 2, x20 + u1 * t) for t in t1]
        t2 = linspace(0, T - ts, 60)
        p2 = [(x1s + x2s * t - u1 * t * t / 2, x2s - u1 * t) for t in t2]
        out.append(polyline([a.p(*q) for q in p1], col, 3.0))
        out.append(polyline([a.p(*q) for q in p2], GREEN, 3.0))
        mid = p1[len(p1) // 2]
        nxt = p1[len(p1) // 2 + 2]
        out.append(line(*a.p(*mid), *a.p(*nxt), col, 3, marker='arrR' if col == '#b91c1c' else 'arrB'))
        out.append(circle(*a.p(x10, x20), 6, col, '#fff', 2))
        out.append(circle(*a.p(x1s, x2s), 6, AMBER, '#fff', 2))
        traj_info.append((x10, x20, u1, ts, T, x1s, x2s))
    out.append(text(a.px(-1.0) - 8, a.py(0.0) + 24, 'A (−1; 0)', 14, '#1d4ed8', 'end', 700))
    out.append(text(a.px(2.0) + 10, a.py(1.0) - 10, 'B (2; 1)', 14, '#b91c1c', 'start', 700))
    out.append(circle(*a.p(0, 0), 6, GREEN, '#fff', 2))

    # временные зависимости для траектории A
    x10, x20, u1, ts, T, x1s, x2s = traj_info[0]
    b = Axes(680, 66, 380, 160, (0, 2.4), (-1.3, 1.3))
    out += b.frame(xticks=(0, 0.5, 1, 1.5, 2), yticks=(-1, 0, 1), xlabel='', ylabel='состояние, траектория A')
    tt = linspace(0, T, 200)
    xs1, xs2 = [], []
    for t in tt:
        if t <= ts:
            xs1.append(x10 + x20 * t + u1 * t * t / 2)
            xs2.append(x20 + u1 * t)
        else:
            tau = t - ts
            xs1.append(x1s + x2s * tau - u1 * tau * tau / 2)
            xs2.append(x2s - u1 * tau)
    out.append(polyline(b.pts(tt, xs1), INK, 2.4))
    out.append(polyline(b.pts(tt, xs2), SKY, 2.4, '7 4'))
    out += legend(b.x0 + b.w - 100, b.y0 + b.h - 34, [('x₁(t)', INK, None), ('x₂(t)', SKY, '7 4')], 14)

    c = Axes(680, 290, 380, 160, (0, 2.4), (-1.6, 1.6))
    out += c.frame(xticks=(0, 0.5, 1, 1.5, 2), yticks=(-1, 0, 1), xlabel='t', ylabel='управление и функция переключения')
    out.append(polyline([c.p(0, u1), c.p(ts, u1), c.p(ts, -u1), c.p(T, -u1)], RED, 2.8))
    lam = [(t - ts) / (T - ts) * (-u1) for t in tt]
    out.append(polyline(c.pts(tt, lam), PURPLE, 2.4, '7 4'))
    out.append(line(c.px(ts), c.y0, c.px(ts), c.y0 + c.h, AMBER, 1.6, '3 3'))
    out.append(text(c.px(ts + 0.04), c.py(-1.3), f't_s = {ts:.2f}', 14, AMBER, 'start', 700))
    out.append(line(c.px(T), c.y0, c.px(T), c.y0 + c.h, GREEN, 1.6, '3 3'))
    out.append(text(c.px(T - 0.04), c.py(0.25), f'T* = {T:.2f}', 14, GREEN, 'end', 700))
    out += legend(c.px(1.04), c.y0 + 22, [('u*(t)', RED, None), ('σ(t) = λ₂(t)', PURPLE, '7 4')], 14)
    write(os.path.join(OUT05, 'time_optimal_phase_portrait.svg'), out)
    return traj_info


def l05_criteria_comparison():
    """Перевод из (−1, 0) в (0, 0): быстродействие, минимум энергии, LQR с насыщением."""
    W, H = 1100, 430
    out = svg_open(W, H)
    out.append(text(24, 30, 'Подъезд к точке остановки из x = −1 м, ẋ = 0 при |u| ≤ 1: три критерия качества', 18, INK, weight=700))
    d, Tbb = 1.0, 2.0
    Te = 2.5
    dt = 0.002
    tt = [i * dt for i in range(int(8.0 / dt) + 1)]

    def u_bb(t):
        return 1.0 if t < 1.0 else (-1.0 if t < 2.0 else 0.0)

    def u_en(t):
        return (6 * d / Te ** 2) * (1 - 2 * t / Te) if t < Te else 0.0

    k1, k2 = 1.0, math.sqrt(3.0)  # LQR: Q = diag(1, 1), R = 1  =>  K = [1, sqrt(3)]

    def sim(ctrl, feedback=False):
        x = [-1.0, 0.0]
        X1, U = [], []
        energy = 0.0
        for t in tt:
            u = max(-1.0, min(1.0, -k1 * x[0] - k2 * x[1])) if feedback else ctrl(t)
            X1.append(x[0])
            U.append(u)
            energy += u * u * dt
            x = rk4(dint, x, u, dt)
        return X1, U, energy

    xb, ub, eb = sim(u_bb)
    xe, ue, ee = sim(u_en)
    xl, ul, el = sim(None, True)

    a = Axes(70, 66, 440, 270, (0, 8), (-1.1, 0.15))
    out += a.frame(xticks=(0, 2, 4, 6, 8), yticks=(-1, -0.5, 0), xlabel='t', ylabel='x(t)')
    out.append(polyline(a.pts(tt, xb), RED, 2.6))
    out.append(polyline(a.pts(tt, xe), BLUE, 2.6, '8 4'))
    out.append(polyline(a.pts(tt, xl), GREEN, 2.6, '2 4'))

    b = Axes(600, 66, 440, 270, (0, 8), (-1.3, 1.3))
    out += b.frame(xticks=(0, 2, 4, 6, 8), yticks=(-1, 0, 1), xlabel='t', ylabel='u(t)')
    out.append(line(b.x0, b.py(1), b.x0 + b.w, b.py(1), AMBER, 1.3, '4 3'))
    out.append(line(b.x0, b.py(-1), b.x0 + b.w, b.py(-1), AMBER, 1.3, '4 3'))
    out.append(polyline(b.pts(tt, ub), RED, 2.6))
    out.append(polyline(b.pts(tt, ue), BLUE, 2.6, '8 4'))
    out.append(polyline(b.pts(tt, ul), GREEN, 2.6, '2 4'))

    # время входа в окрестность |x| < 0.02
    def settle(xs):
        for i in range(len(xs) - 1, -1, -1):
            if abs(xs[i]) > 0.02:
                return tt[min(i + 1, len(tt) - 1)]
        return 0.0

    rows = [
        (f'Быстродействие: T = {Tbb:.1f}, ∫u²dt = {eb:.2f}', RED, None),
        (f'Минимум энергии при T = {Te:.1f}: ∫u²dt = {ee:.2f}', BLUE, '8 4'),
        (f'LQR (Q = I, R = 1) с насыщением: |x| < 0.02 при t > {settle(xl):.1f}', GREEN, '2 4'),
    ]
    out += legend(80, 384, rows[:2], 14)
    out += legend(600, 384, rows[2:], 14)
    write(os.path.join(OUT05, 'criteria_comparison.svg'), out)
    return eb, ee, settle(xl)


def l05_transcription_guesses():
    """Начальное приближение в трёх методах прямой транскрипции.

    Задача: двойной интегратор, x(0) = (0, 0), x(T) = (1, 0), T = 2, N = 4 интервала.
    Во всех трёх случаях показано состояние до первой итерации решателя NLP.
    """
    W, H = 1100, 400
    out = svg_open(W, H)
    out.append(text(24, 30, 'Начальное приближение в методах прямой транскрипции: x(0) = 0, x(2) = 1, N = 4', 18, INK, weight=700))
    T, N = 2.0, 4
    h = T / N
    tk = [k * h for k in range(N + 1)]
    panels = []
    for i, title in enumerate(('Одиночная стрельба', 'Многократная стрельба', 'Коллокация Эрмита–Симпсона')):
        ax = Axes(60 + i * 360, 100, 300, 200, (0, 2), (-0.2, 1.2))
        out += ax.frame(xticks=(0, 0.5, 1, 1.5, 2), yticks=(0, 0.5, 1), xlabel='t', fmt='{:g}', tick_size=12)
        out.append(text(ax.x0, 66, title, 16, INK, 'start', 700))
        out.append(text(ax.x0, 88, 'положение x_1(t)', 13, MUTED, 'start', 400, True, SERIF))
        out.append(circle(*ax.p(2, 1), 6, '#fff', GREEN, 2.4))
        panels.append(ax)

    # (1) одиночная стрельба: задано только управление, траектория получается интегрированием
    ax = panels[0]
    uk = [0.4, 0.1, -0.1, -0.2]
    x = [0.0, 0.0]
    pts = [ax.p(0, 0)]
    for k in range(N):
        for j in range(20):
            x = rk4(dint, x, uk[k], h / 20)
            pts.append(ax.p(tk[k] + (j + 1) * h / 20, x[0]))
    out.append(polyline(pts, BLUE, 2.6))
    out.append(circle(*ax.p(0, 0), 5, BLUE))
    out.append(line(*ax.p(2, x[0]), *ax.p(2, 1), RED, 2, '4 3'))
    out.append(text(ax.px(1.95), ax.py((x[0] + 1) / 2) + 4, 'невязка x(T) − x_f', 13, RED, 'end', 600))
    out.append(text(ax.x0, ax.y0 + ax.h + 44, 'переменные NLP: u_0 … u_{N−1};', 13, MUTED))
    out.append(text(ax.x0, ax.y0 + ax.h + 62, 'x_k вычисляются интегрированием от x_0', 13, MUTED))

    # одинаковое для (2) и (3) грубое приближение узлов: линейная интерполяция положения, скорость 0
    pos = [k / N for k in range(N + 1)]

    # (2) многократная стрельба: интегрирование на каждом интервале от своего узла
    ax = panels[1]
    for k in range(N):
        x = [pos[k], 0.0]
        pts = [ax.p(tk[k], x[0])]
        for j in range(20):
            x = rk4(dint, x, 0.15, h / 20)
            pts.append(ax.p(tk[k] + (j + 1) * h / 20, x[0]))
        out.append(polyline(pts, BLUE, 2.6))
        out.append(line(*ax.p(tk[k + 1], x[0]), *ax.p(tk[k + 1], pos[k + 1]), RED, 2.2, '4 3'))
    for k in range(N + 1):
        out.append(circle(*ax.p(tk[k], pos[k]), 5, BLUE, '#fff', 1.5))
    out.append(text(ax.px(0.05), ax.py(1.0), 'дефекты x_{k+1} − F(x_k, u_k)', 13, RED, 'start', 600))
    out.append(text(ax.x0, ax.y0 + ax.h + 44, 'переменные NLP: x_0 … x_N, u_0 … u_{N−1};', 13, MUTED))
    out.append(text(ax.x0, ax.y0 + ax.h + 62, 'узлы задаются независимо, интегратор на интервале', 13, MUTED))

    # (3) коллокация: кубический сплайн Эрмита по тем же узлам (x_1 = pos, x_2 = 0)
    ax = panels[2]
    for k in range(N):
        p0, p1 = pos[k], pos[k + 1]
        pts = []
        for j in range(31):
            s_ = j / 30
            pts.append(ax.p(tk[k] + s_ * h, p0 + (p1 - p0) * (3 * s_ ** 2 - 2 * s_ ** 3)))
        out.append(polyline(pts, BLUE, 2.6))
        # средняя точка: наклон сплайна 1.5 (p1 − p0)/h против f = x_2(c) = 0
        tc, pc = tk[k] + h / 2, (p0 + p1) / 2
        sl = 1.5 * (p1 - p0) / h
        dtc = 0.13
        out.append(line(*ax.p(tc - dtc, pc - sl * dtc), *ax.p(tc + dtc, pc + sl * dtc), PURPLE, 2.0))
        out.append(line(*ax.p(tc - dtc, pc), *ax.p(tc + dtc, pc), RED, 2.2, '4 3'))
        out.append(circle(*ax.p(tc, pc), 4, AMBER))
    for k in range(N + 1):
        out.append(circle(*ax.p(tk[k], pos[k]), 5, BLUE, '#fff', 1.5))
    out.append(text(ax.px(0.05), ax.py(1.08), 'в средней точке: наклон сплайна', 13, PURPLE, 'start', 600))
    out.append(text(ax.px(0.05), ax.py(0.92), 'против f(x_c, u_c) = x_2(t_c) = 0', 13, RED, 'start', 600))
    out.append(text(ax.x0, ax.y0 + ax.h + 44, 'переменные NLP: x_k, u_k, u_c; дефекты —', 13, MUTED))
    out.append(text(ax.x0, ax.y0 + ax.h + 62, 'алгебраические, интегратор не вызывается', 13, MUTED))
    write(os.path.join(OUT05, 'transcription_initial_guess.svg'), out)


def l05_kkt_sparsity():
    """Портрет разреженности матрицы ККТ многократной стрельбы (n = 3, m = 2, N = 6)."""
    n, m, N = 3, 2, 6
    nv = N * (n + m) + n          # x0,u0,...,x_{N-1},u_{N-1},x_N
    nc = (N + 1) * n              # x0 - xhat = 0, x_{k+1} - F = 0
    dim = nv + nc

    def xidx(k):
        return k * (n + m)

    def uidx(k):
        return k * (n + m) + n

    M = [[0] * dim for _ in range(dim)]
    # Гессиан лагранжиана: плотные блоки по стадиям
    for k in range(N):
        b0 = xidx(k)
        for i in range(n + m):
            for j in range(n + m):
                M[b0 + i][b0 + j] = 1
    for i in range(n):
        for j in range(n):
            M[xidx(N) + i][xidx(N) + j] = 1
    # Якобиан ограничений G (строки nv + ...)
    for i in range(n):
        M[nv + i][xidx(0) + i] = 2
    for k in range(N):
        r0 = nv + (k + 1) * n
        for i in range(n):
            for j in range(n):
                M[r0 + i][xidx(k) + j] = 2
            for j in range(m):
                M[r0 + i][uidx(k) + j] = 2
            M[r0 + i][xidx(k + 1) + i] = 2
    for i in range(nc):
        for j in range(nv):
            if M[nv + i][j]:
                M[j][nv + i] = 2
    nnz = sum(1 for r in M for v in r if v)

    # перестановка: (λ_0, x_0, u_0, λ_1, x_1, u_1, ..., λ_N, x_N)
    order = []
    for k in range(N + 1):
        order += [nv + k * n + i for i in range(n)]
        order += [xidx(k) + i for i in range(n)]
        if k < N:
            order += [uidx(k) + i for i in range(m)]
    P = [[M[i][j] for j in order] for i in order]
    bw = max(abs(i - j) for i in range(dim) for j in range(dim) if P[i][j])

    W, H = 1100, 540
    out = svg_open(W, H)
    out.append(text(24, 30, f'Матрица ККТ многократной стрельбы: n = {n}, m = {m}, N = {N}, размер {dim}×{dim}', 18, INK, weight=700))
    cell = 7.0
    for p, (Mat, title, sub) in enumerate((
            (M, 'Блочная запись [∇²L  Gᵀ; G  0]', 'гессиан — блочно-диагональный, G — блочно-двухдиагональный'),
            (P, 'После перестановки по стадиям (λ_k, x_k, u_k)', f'ленточная матрица, полуширина ленты {bw}'))):
        x0 = 60 + p * 540
        y0 = 90
        out.append(text(x0, 70, title, 15, INK, 'start', 700))
        out.append(rect(x0 - 1, y0 - 1, dim * cell + 2, dim * cell + 2, '#fff', GRID, 0, 1))
        for i in range(dim):
            for j in range(dim):
                v = Mat[i][j]
                if v:
                    col = BLUE if v == 1 else AMBER
                    out.append(f'<rect x="{x0 + j * cell:.1f}" y="{y0 + i * cell:.1f}" width="{cell - 1:.1f}" height="{cell - 1:.1f}" fill="{col}"/>')
        out.append(text(x0, y0 + dim * cell + 24, sub, 13, MUTED))
    out.append(f'<rect x="60" y="{90 + dim * cell + 38}" width="12" height="12" fill="{BLUE}"/>')
    out.append(text(78, 90 + dim * cell + 49, 'вторые производные лагранжиана', 13, INK))
    out.append(f'<rect x="330" y="{90 + dim * cell + 38}" width="12" height="12" fill="{AMBER}"/>')
    out.append(text(348, 90 + dim * cell + 49, 'якобиан ограничений динамики', 13, INK))
    out.append(text(600, 90 + dim * cell + 49,
                    f'ненулевых элементов: {nnz} из {dim * dim} ({100 * nnz / dim / dim:.0f} %)', 13, INK))
    write(os.path.join(OUT05, 'kkt_sparsity_multiple_shooting.svg'), out)
    return dim, nnz, bw


def l05_barrier():
    """min (x−2)² при x ≤ 1: логарифмический барьер и центральная траектория."""
    W, H = 640, 470
    out = svg_open(W, H)
    out.append(text(20, 28, 'Барьерная задача: min (x − 2)² − μ ln(1 − x)', 17, INK, weight=700))
    a = Axes(70, 66, 520, 280, (-0.5, 1.15), (0, 6.5))
    out.append(a.clip_id('clipB'))
    out += a.frame(xticks=(-0.5, 0, 0.5, 1), yticks=(0, 2, 4, 6), xlabel='x', ylabel='φ_μ(x)')
    out.append(polygon([a.p(1, 0), a.p(1.15, 0), a.p(1.15, 6.5), a.p(1, 6.5)], '#fee2e2', 0.8))
    out.append(text(a.px(1.075), a.py(5.9), 'x > 1', 13, RED, 'middle', 600))
    xs = linspace(-0.5, 1.15, 200)
    out.append('<g clip-path="url(#clipB)">')
    out.append(polyline(a.pts(xs, [(x - 2) ** 2 for x in xs]), LIGHT, 2.0, '6 4'))
    cols = [PURPLE, BLUE, SKY, GREEN]
    mus = [1.0, 0.3, 0.1, 0.03]
    star = []
    for mu, col in zip(mus, cols):
        xs2 = linspace(-0.5, 1 - 1e-4, 400)
        out.append(polyline(a.pts(xs2, [(x - 2) ** 2 - mu * math.log(1 - x) for x in xs2]), col, 2.4))
        s_ = (-1 + math.sqrt(1 + 2 * mu)) / 2      # 1 − x*(μ): корень 2s² + 2s − μ = 0
        xstar = 1 - s_
        star.append((mu, xstar, mu / s_))
        out.append(circle(*a.p(xstar, (xstar - 2) ** 2 - mu * math.log(s_)), 5, col, '#fff', 1.8))
    out.append('</g>')
    out.append(line(a.px(1), a.y0, a.px(1), a.y0 + a.h, RED, 1.6))
    out.append(circle(*a.p(1, 1), 6, INK, '#fff', 2))
    out.append(text(a.px(0.97), a.py(0.55), 'x* = 1', 13, INK, 'end', 700))
    out.append(text(a.px(-0.45), a.py(0.6), 'пунктир: (x − 2)² без ограничения', 13, MUTED))
    yb = 400
    for i, (mu, xstar, z) in enumerate(star):
        X = 70 + i * 135
        out.append(line(X, yb - 5, X + 22, yb - 5, cols[i], 3))
        out.append(text(X + 28, yb, f'μ = {mu:g}', 13, cols[i], 'start', 700))
        out.append(text(X, yb + 20, f'x*(μ) = {xstar:.3f}', 13, INK))
        out.append(text(X, yb + 39, f'z(μ) = {z:.3f}', 13, INK))
    out.append(text(70, yb + 62, 'z(μ) = μ / (1 − x*) — оценка множителя; при μ → 0: x* → 1, z → 2', 13, MUTED))
    write(os.path.join(OUT05, 'barrier_central_path.svg'), out)
    return star


def solve_box_qp(Hm, g, lo, hi, iters=3000):
    """min ½ Uᵀ H U + gᵀ U, lo ≤ U ≤ hi — проекция градиента с шагом 1/L."""
    n = len(g)
    v = [1.0] * n
    for _ in range(100):
        w = [sum(Hm[i][j] * v[j] for j in range(n)) for i in range(n)]
        nrm = math.sqrt(sum(x * x for x in w))
        v = [x / nrm for x in w]
    L = nrm
    U = [0.0] * n
    for _ in range(iters):
        grad = [sum(Hm[i][j] * U[j] for j in range(n)) + g[i] for i in range(n)]
        U = [min(hi, max(lo, U[i] - grad[i] / L)) for i in range(n)]
    return U


def l05_mpc_receding():
    """MPC для двойного интегратора с |u| ≤ 1 при рассогласовании модели и объекта.

    Модель регулятора: x2' = u. Объект: x2' = 0.7 u (привод слабее модели),
    в момент t = 4 с — толчок, мгновенно добавляющий скорость +1.5.
    Для сравнения тот же объект управляется без обратной связи: план на 10 с,
    рассчитанный один раз в начальный момент, исполняется вслепую.
    """
    dt, Np = 0.25, 10
    gain_plant = 0.7
    push_step, push_dv = 16, 1.5
    steps = 40
    A = [[1, dt], [0, 1]]
    B = [dt * dt / 2, dt]
    q1, q2, r = 1.0, 0.1, 0.05
    Pf = [[5.0, 1.5], [1.5, 2.0]]

    def mat_vec(M_, v):
        return [sum(M_[i][j] * v[j] for j in range(len(v))) for i in range(len(M_))]

    Apow = [[[1, 0], [0, 1]]]
    for _ in range(steps):
        Pm = Apow[-1]
        Apow.append([[sum(A[i][l] * Pm[l][j] for l in range(2)) for j in range(2)] for i in range(2)])

    def S(k, j):  # влияние u_j на x_k при k > j
        return mat_vec(Apow[k - 1 - j], B)

    def qp(x0, n):
        """Конденсированная QP: min Σ x_kᵀQx_k + r u_k² + x_Nᵀ P_f x_N при |u_k| ≤ 1."""
        Hm = [[0.0] * n for _ in range(n)]
        g = [0.0] * n
        for k in range(1, n + 1):
            Q = Pf if k == n else [[q1, 0], [0, q2]]
            free = mat_vec(Apow[k], x0)
            cols = [S(k, j) if j < k else [0, 0] for j in range(n)]
            for i in range(n):
                Qi = mat_vec(Q, cols[i])
                g[i] += sum(Qi[l] * free[l] for l in range(2))
                for j in range(n):
                    Hm[i][j] += sum(Qi[l] * cols[j][l] for l in range(2))
        for i in range(n):
            Hm[i][i] += r
        U = solve_box_qp(Hm, g, -1.0, 1.0)
        pred, x = [x0], x0
        for u in U:
            x = [x[0] + dt * x[1] + B[0] * u, x[1] + B[1] * u]
            pred.append(x)
        return U, pred

    def plant(x, u):
        return [x[0] + dt * x[1] + gain_plant * B[0] * u, x[1] + gain_plant * B[1] * u]

    x = [2.5, 0.0]
    X, Uapp, preds = [x], [], {}
    for k in range(steps):
        if k == push_step:
            x = [x[0], x[1] + push_dv]
            X[-1] = x
        U, pred = qp(x, Np)
        if k in (0, 4, push_step):
            preds[k] = pred
        u = U[0]
        Uapp.append(u)
        x = plant(x, u)
        X.append(x)

    # без обратной связи: один план на весь интервал
    Uol, _ = qp([2.5, 0.0], steps)
    x = [2.5, 0.0]
    Xol = [x]
    for k in range(steps):
        if k == push_step:
            x = [x[0], x[1] + push_dv]
            Xol[-1] = x
        x = plant(x, Uol[k])
        Xol.append(x)

    W, H = 1100, 480
    out = svg_open(W, H)
    out.append(text(24, 30, f'Скользящий горизонт: Δt = {dt} с, N = {Np}, |u| ≤ 1; объект: ẍ = 0.7u, толчок при t = 4 с', 18, INK, weight=700))
    tmax = steps * dt + 0.1
    a = Axes(70, 76, 960, 220, (0, tmax), (-0.6, 4.6))
    out += a.frame(xticks=list(range(0, 11)), yticks=(0, 1, 2, 3, 4), xlabel='t, с', ylabel='положение x_1')
    out.append(a.clip_id('clipMPC'))
    out.append('<g clip-path="url(#clipMPC)">')
    tsx = [i * dt for i in range(len(X))]
    out.append(polyline(a.pts(tsx, [p[0] for p in Xol]), RED, 2.4, '3 4'))
    out.append('</g>')
    cols = {0: PURPLE, 4: AMBER, push_step: SKY}
    for k, pred in preds.items():
        ts = [(k + i) * dt for i in range(len(pred))]
        out.append(polyline(a.pts(ts, [p[0] for p in pred]), cols[k], 2.0, '6 4'))
        for t_, p in zip(ts, pred):
            out.append(circle(*a.p(t_, p[0]), 2.6, cols[k]))
        out.append(line(a.px(k * dt), a.y0, a.px(k * dt), a.y0 + a.h, cols[k], 1, '2 3'))
    out.append(text(a.px(2.5) - 6, a.py(preds[0][-1][0]) + 20, 'прогноз при k = 0', 13, PURPLE, 'end', 600))
    out.append(text(a.px(3.0), a.py(0.45), 'прогноз при k = 4', 13, AMBER, 'start', 600))
    out.append(text(a.px(5.0), a.py(-0.35), f'прогноз при k = {push_step} (сразу после толчка)', 13, SKY, 'start', 600))
    out.append(polyline(a.pts(tsx, [p[0] for p in X]), INK, 3.0))
    out.append(text(a.px(0.15), a.py(4.3), 'MPC: фактическая траектория объекта', 14, INK, 'start', 700))
    out.append(text(a.px(6.2), a.py(3.6), 'без обратной связи: первый план исполняется вслепую', 14, RED, 'start', 700))

    b = Axes(70, 340, 960, 100, (0, tmax), (-1.25, 1.25))
    out += b.frame(xticks=list(range(0, 11)), yticks=(-1, 0, 1), xlabel='t, с', ylabel='применённое управление u_0*')
    stair = []
    for k, u in enumerate(Uapp):
        stair += [b.p(k * dt, u), b.p((k + 1) * dt, u)]
    out.append(polyline(stair, INK, 2.4))
    write(os.path.join(OUT05, 'mpc_receding_horizon.svg'), out)
    return X[-1], Xol[-1]


# ---------------------------------------------------------------------------
# Лекция 06
# ---------------------------------------------------------------------------

def box(x, y, w, h, title, lines_, color=BLUE, fill='#eff6ff', tsize=16, lsize=14):
    out = [rect(x, y, w, h, fill, color, 10, 2)]
    out.append(text(x + w / 2, y + 26, title, tsize, color, 'middle', 700))
    for i, s in enumerate(lines_):
        out.append(text(x + w / 2, y + 50 + i * 21, s, lsize, INK, 'middle'))
    return out


def l06_rl_loop():
    W, H = 1000, 330
    out = svg_open(W, H)
    out += box(60, 70, 300, 150, 'Агент (регулятор)', ['выбирает действие a_t', 'по политике π(a | s)', 'и учится на опыте'], BLUE, '#eff6ff')
    out += box(640, 70, 300, 150, 'Среда (робот и мир)', ['переходит в новое', 'состояние s_{t+1}', 'и выдаёт награду r_{t+1}'], INK, PANEL)
    out.append(line(360, 110, 636, 110, BLUE, 2.4, marker='arrB'))
    out.append(text(498, 100, 'действие a_t', 15, BLUE, 'middle', 700))
    out.append(polyline([(790, 220), (790, 280), (210, 280), (210, 224)], GREEN, 2.4, marker='arrG'))
    out.append(text(500, 272, 'новое состояние s_{t+1} и награда r_{t+1}', 15, GREEN, 'middle', 700))
    out.append(text(500, 40, 'Один такт: s_t → a_t → (r_{t+1}, s_{t+1}); эпизод — последовательность тактов от начала до конца попытки', 16, INK, 'middle', 600))
    write(os.path.join(OUT06, 'rl_interaction_loop.svg'), out)


def l06_corridor():
    """Сквозной пример лекции 06: коридор из пяти клеток, цель справа.

    Награда +10 за вход в цель, 0 за остальные шаги, γ = 0.9, действия «влево» и
    «вправо» (у левой стены действие «влево» оставляет робота на месте).
    Ценности V* и Q* вычисляются итерацией по ценности.
    """
    gamma, R = 0.9, 10.0
    n = 4  # нетерминальные клетки 1..4, клетка 5 — цель
    V = [0.0] * (n + 2)

    def step(s, a):
        s2 = max(1, s - 1) if a == 'L' else s + 1
        return s2, (R if s2 == n + 1 else 0.0)

    hist = [V[1:n + 1]]
    for _ in range(20):
        V2 = V[:]
        for s in range(1, n + 1):
            vals = []
            for a in 'LR':
                s2, r = step(s, a)
                vals.append(r + gamma * (0.0 if s2 == n + 1 else V[s2]))
            V2[s] = max(vals)
        V = V2
        hist.append(V[1:n + 1])
    Q = {}
    for s in range(1, n + 1):
        for a in 'LR':
            s2, r = step(s, a)
            Q[(s, a)] = r + gamma * (0.0 if s2 == n + 1 else V[s2])

    W, H = 1100, 275
    out = svg_open(W, H)
    out.append(text(24, 30, 'Сквозной пример: робот в коридоре. Награда +10 за вход в цель, иначе 0; γ = 0.9', 18, INK, weight=700))
    x0, y0, cw, ch = 60, 70, 190, 130
    for i in range(1, n + 2):
        x = x0 + (i - 1) * (cw + 10)
        goal = i == n + 1
        out.append(rect(x, y0, cw, ch, '#ecfdf5' if goal else '#ffffff', GREEN if goal else LIGHT, 8, 2))
        out.append(text(x + 10, y0 + 22, f'клетка {i}', 14, MUTED))
        if goal:
            out.append(text(x + cw / 2, y0 + 62, 'ЦЕЛЬ', 20, GREEN, 'middle', 700))
            out.append(text(x + cw / 2, y0 + 90, 'эпизод завершается', 13, GREEN, 'middle'))
            continue
        out.append(text(x + cw / 2, y0 + 64, f'V* = {V[i]:.2f}', 20, BLUE, 'middle', 700))
        out.append(text(x + 12, y0 + 112, f'← {Q[(i, "L")]:.2f}', 15, MUTED, 'start'))
        out.append(text(x + cw - 12, y0 + 112, f'{Q[(i, "R")]:.2f} →', 15, GREEN, 'end', 700))
    # робот в клетке 1
    out.append(circle(x0 + cw - 30, y0 + 28, 11, AMBER, '#fff', 2))
    out.append(text(x0 + cw - 30, y0 + 33, 'Р', 12, '#fff', 'middle', 700))
    out.append(text(60, y0 + ch + 34, 'В каждой клетке: V* — ценность клетки; внизу Q*(s, ←) и Q*(s, →) — ценности двух действий.', 15, INK))
    out.append(text(60, y0 + ch + 58, 'Оптимальное действие — с большей ценностью (зелёное): везде «вправо». У стены «влево» оставляет робота на месте.', 15, INK))
    write(os.path.join(OUT06, 'corridor_values.svg'), out)
    return hist, Q


def l06_discount():
    W, H = 640, 400
    out = svg_open(W, H)
    out.append(text(20, 28, 'Вес награды через k тактов: γᵏ', 17, INK, weight=700))
    a = Axes(70, 56, 530, 260, (0, 400), (0, 1.05))
    out += a.frame(xticks=(0, 100, 200, 300, 400), yticks=(0, 0.5, 1), xlabel='k', ylabel='γᵏ')
    cols = [(0.9, RED), (0.99, BLUE), (0.995, GREEN)]
    for g, col in cols:
        ks = list(range(0, 401, 2))
        out.append(polyline(a.pts(ks, [g ** k for k in ks]), col, 2.6))
        hzn = 1 / (1 - g)
        out.append(line(a.px(hzn), a.py(0), a.px(hzn), a.py(g ** hzn), col, 1.3, '3 3'))
        out.append(circle(*a.p(hzn, g ** hzn), 4.5, col, '#fff', 1.8))
    out += legend(360, 96, [('γ = 0.9:   1/(1−γ) = 10', RED, None),
                            ('γ = 0.99:  1/(1−γ) = 100', BLUE, None),
                            ('γ = 0.995: 1/(1−γ) = 200', GREEN, None)], 14)
    out.append(text(70, 362, 'Точки: k = 1/(1−γ), где γᵏ ≈ e⁻¹ ≈ 0.37.', 14, MUTED))
    out.append(text(70, 382, 'При частоте политики 50 Гц и γ = 0.99 это ≈ 100 тактов ≈ 2 с.', 14, MUTED))
    write(os.path.join(OUT06, 'discount_horizon.svg'), out)


def l06_taxonomy():
    W, H = 1100, 430
    out = svg_open(W, H)
    out.append(text(550, 32, 'Основные семейства методов обучения с подкреплением', 18, INK, 'middle', 700))

    def node(x, y, w, h, title, sub, color, fill):
        o = [rect(x, y, w, h, fill, color, 8, 1.8)]
        o.append(text(x + w / 2, y + 24, title, 15, color, 'middle', 700))
        for i, s in enumerate(sub):
            o.append(text(x + w / 2, y + 46 + i * 19, s, 13, INK, 'middle'))
        return o

    out += node(420, 52, 260, 50, 'Обучение с подкреплением', [], INK, PANEL)
    out.append(polyline([(550, 102), (550, 118), (295, 118), (295, 134)], LIGHT, 1.8))
    out.append(polyline([(550, 118), (860, 118), (860, 134)], LIGHT, 1.8))
    out += node(105, 134, 380, 50, 'Без модели среды (model-free)', [], BLUE, '#eff6ff')
    out += node(670, 134, 380, 50, 'С моделью среды (model-based)', [], AMBER, '#fffbeb')
    mf = [('На основе ценности', ['Q-learning, DQN', 'политика: argmax_a Q', 'конечное множество A']),
          ('Градиент политики', ['REINFORCE', 'π_θ(a|s) напрямую', 'высокая дисперсия']),
          ('Актор–критик', ['A2C, PPO (on-policy)', 'DDPG, TD3, SAC', '(off-policy)'])]
    for i, (t, s) in enumerate(mf):
        x = 30 + i * 180
        out.append(polyline([(295, 184), (295, 200), (x + 85, 200), (x + 85, 214)], LIGHT, 1.6))
        out += node(x, 214, 170, 108, t, s, BLUE, '#ffffff')
    mb = [('Известная модель', ['динамическое', 'программирование,', 'MCTS, MPC (лекция 05)']),
          ('Обучаемая модель', ['Dyna, MBPO, PETS,', 'Dreamer: обучение', 'политики «в модели»'])]
    for i, (t, s) in enumerate(mb):
        x = 670 + i * 200
        out.append(polyline([(860, 184), (860, 200), (x + 90, 200), (x + 90, 214)], LIGHT, 1.6))
        out += node(x, 214, 180, 108, t, s, AMBER, '#ffffff')
    out.append(text(30, 352, 'Ось «on-policy / off-policy»: используются ли для обновления только данные текущей политики', 14, MUTED))
    out.append(text(30, 372, '(PPO) или любой накопленный опыт из буфера (DQN, SAC). Off-policy методы экономнее по данным,', 14, MUTED))
    out.append(text(30, 392, 'on-policy методы проще и устойчивее при массово-параллельной симуляции.', 14, MUTED))
    write(os.path.join(OUT06, 'rl_method_families.svg'), out)


def l06_actor_critic():
    W, H = 1000, 360
    out = svg_open(W, H)
    out += box(40, 60, 290, 120, 'Актор π_θ(a | s)', ['выдаёт действие a_t', 'обновление: ∇_θ log π_θ(a_t|s_t) · Â_t'], BLUE, '#eff6ff', 16, 14)
    out += box(670, 60, 290, 120, 'Критик V_φ(s)', ['оценивает ценность состояния', 'обновление: min (V_φ(s_t) − ŷ_t)²'], GREEN, '#ecfdf5', 16, 14)
    out += box(355, 230, 290, 100, 'Среда', ['s_{t+1} ~ P(· | s_t, a_t)', 'r_{t+1}'], INK, PANEL, 16, 14)
    out.append(polyline([(185, 180), (185, 280), (351, 280)], BLUE, 2.2, marker='arrB'))
    out.append(text(192, 262, 'a_t', 15, BLUE, 'start', 700))
    out.append(polyline([(649, 280), (815, 280), (815, 184)], GREEN, 2.2, marker='arrG'))
    out.append(text(808, 262, 's_{t+1}, r_{t+1}', 15, GREEN, 'end', 700))
    out += box(370, 70, 260, 100, 'TD-ошибка', ['δ_t = r_{t+1} + γV_φ(s_{t+1}) − V_φ(s_t)', 'Â_t = Σ (γλ)ˡ δ_{t+l}  (GAE)'], PURPLE, '#f5f3ff', 16, 13)
    out.append(line(666, 120, 634, 120, PURPLE, 2.2, marker='arrP'))
    out.append(line(366, 120, 334, 120, PURPLE, 2.2, marker='arrP'))
    out.append(text(500, 34, 'Схема актор–критик: критик снижает дисперсию оценки градиента политики', 17, INK, 'middle', 700))
    write(os.path.join(OUT06, 'actor_critic_scheme.svg'), out)


def l06_ppo_clip():
    W, H = 1000, 430
    out = svg_open(W, H)
    out.append(text(24, 30, 'Усечённая целевая функция PPO для одного перехода: L = min(ρÂ, clip(ρ, 1−ε, 1+ε)Â), ε = 0.2', 17, INK, weight=700))
    eps = 0.2
    for p, (A, title) in enumerate(((1.0, 'Â > 0: действие лучше среднего'), (-1.0, 'Â < 0: действие хуже среднего'))):
        a = Axes(80 + p * 480, 70, 380, 230, (0, 2), (-2.1, 2.1))
        out += a.frame(xticks=(0, 0.5, 0.8, 1, 1.2, 1.5, 2), yticks=(-2, -1, 0, 1, 2), xlabel='ρ = π_θ / π_{old}', ylabel='L(ρ)', fmt='{:g}', tick_size=12)
        out.append(polygon([a.p(1 - eps, -2.1), a.p(1 + eps, -2.1), a.p(1 + eps, 2.1), a.p(1 - eps, 2.1)], '#dbeafe', 0.5))
        rs = linspace(0, 2, 400)
        out.append(polyline(a.pts(rs, [r_ * A for r_ in rs]), LIGHT, 2.0, '6 4'))
        L = [min(r_ * A, max(1 - eps, min(1 + eps, r_)) * A) for r_ in rs]
        out.append(polyline(a.pts(rs, L), RED if A < 0 else GREEN, 3.0))
        out.append(circle(*a.p(1, A), 5, INK, '#fff', 2))
        out.append(text(a.x0 + a.w / 2, a.y0 + a.h + 62, title, 15, INK, 'middle', 700))
        if A > 0:
            out.append(text(a.px(1.6), a.py(1.2) - 10, 'рост ρ выше 1+ε', 13, GREEN, 'middle', 600))
            out.append(text(a.px(1.6), a.py(1.2) + 8, 'не увеличивает L', 13, GREEN, 'middle', 600))
        else:
            out.append(text(a.px(0.42), a.py(-0.8) + 26, 'снижение ρ ниже 1−ε', 13, RED, 'middle', 600))
            out.append(text(a.px(0.42), a.py(-0.8) + 44, 'не увеличивает L', 13, RED, 'middle', 600))
    out += legend(80, 396, [('без усечения: ρÂ', LIGHT, '6 4')], 13)
    out.append(text(290, 396, 'Полоса — [1−ε, 1+ε]. Градиент L по θ равен нулю только на горизонтальных', 13, MUTED))
    out.append(text(290, 415, 'участках: при Â > 0 и ρ > 1+ε, при Â < 0 и ρ < 1−ε.', 13, MUTED))
    write(os.path.join(OUT06, 'ppo_clipped_objective.svg'), out)


def l06_teacher_student():
    W, H = 1100, 400
    out = svg_open(W, H)
    out.append(text(550, 30, 'Обучение с привилегированной информацией (учитель–ученик)', 18, INK, 'middle', 700))
    out.append(rect(20, 50, 1060, 150, '#eff6ff', BLUE, 12, 1.4, '6 4'))
    out.append(text(36, 74, 'Этап 1. Симулятор, RL (PPO)', 15, BLUE, 'start', 700))
    out += box(40, 88, 300, 96, 'Привилегированные данные', ['карта высот, силы контакта,', 'трение, масса груза'], AMBER, '#fffbeb', 14, 13)
    out += box(400, 88, 300, 96, 'Учитель π_T(a | o_t, e_t)', ['e_t — скрытые параметры среды', 'обучается максимизацией J'], BLUE, '#ffffff', 14, 13)
    out.append(line(340, 136, 396, 136, AMBER, 2.2, marker='arrA'))
    out += box(760, 88, 300, 96, 'Учитель → действие a_t^T', ['используется как разметка', 'на втором этапе'], BLUE, '#ffffff', 14, 13)
    out.append(line(700, 136, 756, 136, BLUE, 2.2, marker='arrB'))

    out.append(rect(20, 222, 1060, 160, '#ecfdf5', GREEN, 12, 1.4, '6 4'))
    out.append(text(36, 246, 'Этап 2. Симулятор, обучение с учителем (дистилляция, DAgger)', 15, GREEN, 'start', 700))
    out += box(40, 262, 300, 100, 'История бортовых данных', ['o_{t−H:t} = (q, q̇, ω, g, a_{t−1})', 'только то, что есть на роботе'], INK, '#ffffff', 14, 13)
    out += box(400, 262, 300, 100, 'Ученик π_S(a | o_{t−H:t})', ['ẑ_t = g_ψ(o_{t−H:t}) — оценка e_t', 'рекуррентная или свёрточная сеть'], GREEN, '#ffffff', 14, 13)
    out.append(line(340, 312, 396, 312, INK, 2.2, marker='arr'))
    out += box(760, 262, 300, 100, 'Функция потерь', ['‖π_S − a_t^T‖² + β‖ẑ_t − z_t^T‖²', 'действия берутся у ученика'], PURPLE, '#ffffff', 14, 13)
    out.append(line(700, 312, 756, 312, GREEN, 2.2, marker='arrG'))
    out.append(polyline([(910, 184), (910, 258)], BLUE, 2.0, '5 4', marker='arrB'))
    write(os.path.join(OUT06, 'teacher_student_privileged.svg'), out)


def l06_cbf_filter():
    """Фильтр безопасности: ṗ = u, h(p) = ‖p − o‖² − R², ḣ ≥ −α h."""
    o = (0.0, 0.0)
    R = 1.0
    alpha = 2.0
    goal = (3.0, 0.35)
    dt = 0.01

    def nominal(p):
        dx, dy = goal[0] - p[0], goal[1] - p[1]
        nrm = math.hypot(dx, dy)
        k = min(1.0, nrm) / max(nrm, 1e-9)
        return (dx * k, dy * k)

    def filt(p, u):
        hx, hy = p[0] - o[0], p[1] - o[1]
        hval = hx * hx + hy * hy - R * R
        a = (2 * hx, 2 * hy)
        lhs = a[0] * u[0] + a[1] * u[1] + alpha * hval
        if lhs >= 0:
            return u, False
        s = lhs / (a[0] ** 2 + a[1] ** 2)
        return (u[0] - s * a[0], u[1] - s * a[1]), True

    def run(use_filter):
        p = (-3.0, 0.0)
        pts = [p]
        active = []
        for _ in range(1500):
            u = nominal(p)
            act = False
            if use_filter:
                u, act = filt(p, u)
            p = (p[0] + dt * u[0], p[1] + dt * u[1])
            pts.append(p)
            active.append(act)
            if math.hypot(p[0] - goal[0], p[1] - goal[1]) < 0.02:
                break
        return pts, active

    raw, _ = run(False)
    safe, act = run(True)
    hmin = min(math.hypot(x, y) ** 2 - R * R for x, y in safe)

    W, H = 640, 470
    out = svg_open(W, H)
    out.append(text(20, 28, 'Фильтр безопасности на основе CBF: ṗ = u', 17, INK, weight=700))
    a = Axes(40, 50, 560, 300, (-3.3, 3.3), (-1.75, 1.75))
    out += a.frame(xticks=(-3, -2, -1, 0, 1, 2, 3), yticks=(-1, 0, 1), xlabel='p_x', ylabel='p_y')
    out.append(f'<ellipse cx="{a.px(0):.1f}" cy="{a.py(0):.1f}" rx="{a.px(R) - a.px(0):.1f}" ry="{a.py(0) - a.py(R):.1f}" fill="#fee2e2" stroke="{RED}" stroke-width="2"/>')
    out.append(text(a.px(0), a.py(0) + 5, 'h(p) < 0', 14, RED, 'middle', 700))
    out.append(polyline([a.p(*q) for q in raw], LIGHT, 2.4, '7 5'))
    out.append(polyline([a.p(*q) for q in safe], BLUE, 3.0))
    seg = [a.p(*safe[i]) for i in range(len(act)) if act[i]]
    if seg:
        out.append(polyline(seg, AMBER, 4.2, opacity=0.85))
    out.append(circle(*a.p(-3, 0), 6, INK, '#fff', 2))
    out.append(circle(*a.p(*goal), 6, GREEN, '#fff', 2))
    out.append(text(a.px(-3) + 8, a.py(0) - 12, 'старт', 13, INK))
    out.append(text(a.px(goal[0]) - 4, a.py(goal[1]) - 12, 'цель', 13, GREEN, 'end'))
    out += legend(48, 408, [('без фильтра (u = u_ном)', LIGHT, '7 5'), ('с фильтром', BLUE, None)], 13, 22)
    out += legend(330, 408, [('ограничение ḣ ≥ −αh активно', AMBER, None)], 13, 22)
    out.append(text(330, 430, f'α = {alpha:g}; min h вдоль пути = {hmin:.3f} > 0', 13, MUTED))
    write(os.path.join(OUT06, 'cbf_safety_filter.svg'), out)
    return hmin


def main():
    print('Лекция 05:')
    l05_cart_example()
    l05_hamiltonian_vs_u()
    info = l05_time_optimal_phase()
    for x10, x20, u1, ts, T, x1s, x2s in info:
        print(f'   траектория из ({x10}, {x20}): u1 = {u1:+.0f}, t_s = {ts:.4f}, T* = {T:.4f}, точка переключения ({x1s:.4f}, {x2s:.4f})')
    print('   энергия/время установления:', l05_criteria_comparison())
    l05_transcription_guesses()
    print('   ККТ (размер, ненули, полуширина):', l05_kkt_sparsity())
    print('   центральная траектория:', l05_barrier())
    print('   MPC: конец (MPC, без обратной связи):', l05_mpc_receding())
    print('Лекция 06:')
    l06_rl_loop()
    hist, Q = l06_corridor()
    print('   коридор, итерации по ценности:', [[round(v, 3) for v in h] for h in hist[:6]])
    l06_discount()
    l06_taxonomy()
    l06_actor_critic()
    l06_ppo_clip()
    l06_teacher_student()
    print('   CBF min h =', l06_cbf_filter())


if __name__ == '__main__':
    main()
