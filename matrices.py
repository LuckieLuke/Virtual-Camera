import numpy as np
from math import sin, cos


def trans(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])


def rotateX(x):
    return np.array([
        [1, 0, 0, 0],
        [0, cos(x), sin(x), 0],
        [0, -sin(x), cos(x), 0],
        [0, 0, 0, 1]
    ])


def rotateY(x):
    return np.array([
        [cos(x), 0, -sin(x), 0],
        [0, 1, 0, 0],
        [sin(x), 0, cos(x), 0],
        [0, 0, 0, 1]
    ])


def rotateZ(x):
    return np.array([
        [cos(x), sin(x), 0, 0],
        [-sin(x), cos(x), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def zoom(x):
    return np.array([
        [x, 0, 0, 0],
        [0, x, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def mvp(width, height):
    return np.array([
        [width/2, 0, 0, (width-1)/2],
        [0, height/2, 0, (height-1)/2],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def mper(l, r, b, t, n, f):
    return np.array([
        [(2 * n) / (r - l), 0, (l + r) / (l - r), 0],
        [0, (2 * n) / (t - b), (b + t) / (b - t), 0],
        [0, 0, (f + n) / (n - f), (2 * f * n) / (f - n)],
        [0, 0, 1, 0]
    ])


def orth(l, r, b, t, n, f):
    return np.array([
        [2 / (r - l), 0, 0, (r + l) / (l - r)],
        [0, 2 / (t - b), 0, (t + b) / (b - t)],
        [0, 0, 2 / (n - f), (n + f) / (f - n)],
        [0, 0, 0, 1],
    ])


def getOrthViewVolume(width, height):
    return {
        'l': -width/2,
        'r': width/2,
        'b': -height/2,
        't': height/2,
        'n': -900,
        'f': -1000
    }


def mg(x, y, z):
    return np.array([
        [x], [y], [z]
    ])


def mp(n, f):
    return np.array([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n+f, -1*f*n],
        [0, 0, 1, 0]
    ])
