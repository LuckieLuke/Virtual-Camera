from tkinter import *
import numpy as np
from matrices import *
from const import *
import math

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


def move_cam(direction):
    global camera_coords

    column, coef = None, None
    if direction in ['up', 'down']:
        coef = 3 if direction == 'down' else -3
        column = camera_coords[:, 1]
    elif direction in ['left', 'right']:
        coef = 3 if direction == 'right' else -3
        column = camera_coords[:, 0]
    else:
        coef = 3 if direction == 'front' else -3
        column = camera_coords[:, 2]

    column = column * coef
    for i in range(4):
        camera_coords[i, 3] += column[i]


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


def rotate_cam(angle, axis):
    global camera_coords

    cam_rot = np.array([
        [*camera_coords[0, :3], 0],
        [*camera_coords[1, :3], 0],
        [*camera_coords[2, :3], 0],
        [0, 0, 0, 0],
    ])

    if axis == 'x':
        cam_rot = rotateX(angle).dot(cam_rot)
    elif axis == 'y':
        cam_rot = rotateY(angle).dot(cam_rot)
    elif axis == 'z':
        cam_rot = rotateZ(angle).dot(cam_rot)

    x, y, z = camera_coords[0, 3], camera_coords[1, 3], camera_coords[2, 3]
    camera_coords = np.array([
        [*cam_rot[0, :3], x],
        [*cam_rot[1, :3], y],
        [*cam_rot[2, :3], z],
        [0, 0, 0, 1],
    ])

    angle = math.asin(camera_coords[2][0]) * 180 / math.pi
    print(angle)


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
