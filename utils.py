from tkinter import *
import numpy as np
from matrices import *
from const import *


def move(coords, direction):
    for index, coord in enumerate(coords):
        new_cords1 = np.array(
            [[coord[0][0][0]], [coord[0][1][0]], [coord[0][2][0]], [1]])
        new_cords1 = trans(*MOVE_DIRECTION[direction]).dot(new_cords1)

        new_cords2 = np.array(
            [[coord[1][0][0]], [coord[1][1][0]], [coord[1][2][0]], [1]])
        new_cords2 = trans(*MOVE_DIRECTION[direction]).dot(new_cords2)

        coords[index] = (new_cords1, new_cords2)


def rotate(coords, angle, axis):
    for index, coord in enumerate(coords):
        new_cords1 = np.array(
            [[coord[0][0][0]], [coord[0][1][0]], [coord[0][2][0]], [1]])
        new_cords2 = np.array(
            [[coord[1][0][0]], [coord[1][1][0]], [coord[1][2][0]], [1]])

        if axis == 'x':
            new_cords1 = rotateX(angle).dot(new_cords1)
            new_cords2 = rotateX(angle).dot(new_cords2)
        elif axis == 'y':
            new_cords1 = rotateY(angle).dot(new_cords1)
            new_cords2 = rotateY(angle).dot(new_cords2)
        elif axis == 'z':
            new_cords1 = rotateZ(angle).dot(new_cords1)
            new_cords2 = rotateZ(angle).dot(new_cords2)

        coords[index] = (new_cords1, new_cords2)


def move_vect(vect, direction):
    vect = trans(*MOVE_DIRECTION[direction]).dot(vect.T)
