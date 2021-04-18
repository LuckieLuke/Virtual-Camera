from tkinter import *
import numpy as np
from matrices import *
from const import *

camera_coords = np.array(
    [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]
)


def move(coords, direction):
    for index, coord in enumerate(coords):
        new_cords1 = np.array(
            [[coord[0][0][0]], [coord[0][1][0]], [coord[0][2][0]], [1]])
        new_cords1 = trans(*MOVE_DIRECTION[direction]).dot(new_cords1)

        new_cords2 = np.array(
            [[coord[1][0][0]], [coord[1][1][0]], [coord[1][2][0]], [1]])
        new_cords2 = trans(*MOVE_DIRECTION[direction]).dot(new_cords2)

        new_cords3 = np.array(
            [[coord[2][0][0]], [coord[2][1][0]], [coord[2][2][0]], [1]])
        new_cords3 = trans(*MOVE_DIRECTION[direction]).dot(new_cords3)

        coords[index] = (new_cords1, new_cords2, new_cords3, coord[3])


def rotate(coords, angle, axis):
    for index, coord in enumerate(coords):
        new_cords1 = np.array(
            [[coord[0][0][0]], [coord[0][1][0]], [coord[0][2][0]], [1]])
        new_cords2 = np.array(
            [[coord[1][0][0]], [coord[1][1][0]], [coord[1][2][0]], [1]])
        new_cords3 = np.array(
            [[coord[2][0][0]], [coord[2][1][0]], [coord[2][2][0]], [1]])

        if axis == 'x':
            new_cords1 = rotateX(angle).dot(new_cords1)
            new_cords2 = rotateX(angle).dot(new_cords2)
            new_cords3 = rotateX(angle).dot(new_cords3)
        elif axis == 'y':
            new_cords1 = rotateY(angle).dot(new_cords1)
            new_cords2 = rotateY(angle).dot(new_cords2)
            new_cords3 = rotateY(angle).dot(new_cords3)
        elif axis == 'z':
            new_cords1 = rotateZ(angle).dot(new_cords1)
            new_cords2 = rotateZ(angle).dot(new_cords2)
            new_cords3 = rotateZ(angle).dot(new_cords3)

        coords[index] = (new_cords1, new_cords2, new_cords3, coord[3])


def zoom(coords, coef):
    for index, coord in enumerate(coords):
        new_cords1 = np.array(
            [[coord[0][0][0]], [coord[0][1][0]], [coord[0][2][0]], [1]])
        new_cords2 = np.array(
            [[coord[1][0][0]], [coord[1][1][0]], [coord[1][2][0]], [1]])
        new_cords3 = np.array(
            [[coord[2][0][0]], [coord[2][1][0]], [coord[2][2][0]], [1]])

        new_cords1 = mzoom(coef).dot(new_cords1)
        new_cords2 = mzoom(coef).dot(new_cords2)
        new_cords3 = mzoom(coef).dot(new_cords3)

        coords[index] = (new_cords1, new_cords2, new_cords3, coord[3])
