import math
from matrices import *
import utils
from tkinter import *


class Camera():
    def __init__(self):
        self.rendered = False
        self.root = Tk()
        self.root.title('Virtual Camera')
        self.root.geometry('1000x800')

        self.my_canvas = Canvas(self.root, width=900, height=700, bg='white')
        self.my_canvas.pack(pady=70)

        w = Label(self.root, text='''Keys:
        WSADCF - walking around (up, down, left, right, front, back)
        QERTGH - rotating, PL - zoom
        ''')
        w.place(x=300, y=0)

        self.triangles = []
        self.triangles_coords = []
        self.root.bind('<Key>', self.key_pressed)

        with open('coords.txt', 'r') as file:
            for index, line in enumerate(file.readlines()):
                if line[0] != '#':
                    coords = [int(x) for x in line.split()]
                    a = np.array([[*coords[:3], 1]]).T
                    b = np.array([[*coords[3:6], 1]]).T
                    c = np.array([[*coords[6:], 1]]).T

                    self.triangles_coords.append((a, b, c, index))

                    self.triangles.append(
                        self.my_canvas.create_polygon(
                            a[0][0], a[1][0],
                            b[0][0], b[1][0],
                            c[0][0], c[1][0],
                            fill='green',
                            outline='red'
                        )
                    )
        self.render()
        self.root.mainloop()

    def key_pressed(self, event):
        if event.char == 'd':
            utils.move(self.triangles_coords, 'left')
        elif event.char == 'a':
            utils.move(self.triangles_coords, 'right')
        elif event.char == 's':
            utils.move(self.triangles_coords, 'up')
        elif event.char == 'w':
            utils.move(self.triangles_coords, 'down')
        elif event.char == 'c':
            utils.move(self.triangles_coords, 'front')
        elif event.char == 'f':
            utils.move(self.triangles_coords, 'back')
        elif event.char == 'q':
            utils.rotate(self.triangles_coords, -0.05, 'z')
        elif event.char == 'e':
            utils.rotate(self.triangles_coords, 0.05, 'z')
        elif event.char == 'r':
            utils.rotate(self.triangles_coords, -0.05, 'x')
        elif event.char == 't':
            utils.rotate(self.triangles_coords, 0.05, 'x')
        elif event.char == 'h':
            utils.rotate(self.triangles_coords, -0.05, 'y')
        elif event.char == 'g':
            utils.rotate(self.triangles_coords, 0.05, 'y')
        elif event.char == 'p':
            utils.zoom(self.triangles_coords, 2)
        elif event.char == 'l':
            utils.zoom(self.triangles_coords, 0.5)
        self.render()

    def render(self):
        MVP = mvp(900, 700)
        orth_view = getOrthViewVolume(900, 700)
        Morth = orth(
            orth_view['l'],
            orth_view['r'],
            orth_view['b'],
            orth_view['t'],
            orth_view['n'],
            orth_view['f'],
        )
        P = mp(
            orth_view['n'],
            orth_view['f']
        )

        M = Morth.dot(P)
        M = MVP.dot(M)

        self.triangles_coords = posortuj(self.triangles_coords)

        self.my_canvas.delete("all")

        for coord in self.triangles_coords:
            screen_coords_a = M.dot(coord[0])
            screen_coords_b = M.dot(coord[1])
            screen_coords_c = M.dot(coord[2])
            color = 'blue'
            if coord[3] < 37:
                color = 'green'
            if coord[3] < 25:
                color = 'pink'
            if coord[3] < 13:
                color = 'yellow'

            self.my_canvas.create_polygon(
                int(screen_coords_a[0] / screen_coords_a[3]),
                int(screen_coords_a[1] / screen_coords_a[3]),
                int(screen_coords_b[0] / screen_coords_b[3]),
                int(screen_coords_b[1] / screen_coords_b[3]),
                int(screen_coords_c[0] / screen_coords_c[3]),
                int(screen_coords_c[1] / screen_coords_c[3]),
                fill=color,
                outline='red'
            )

            maxs = find_max(coord)
            not_to_draw = []

            if maxs == 'ab':
                not_to_draw = [
                    int(screen_coords_a[0] / screen_coords_a[3]),
                    int(screen_coords_a[1] / screen_coords_a[3]),
                    int(screen_coords_b[0] / screen_coords_b[3]),
                    int(screen_coords_b[1] / screen_coords_b[3])
                ]
            elif maxs == 'bc':
                not_to_draw = [
                    int(screen_coords_b[0] / screen_coords_b[3]),
                    int(screen_coords_b[1] / screen_coords_b[3]),
                    int(screen_coords_c[0] / screen_coords_c[3]),
                    int(screen_coords_c[1] / screen_coords_c[3])
                ]
            else:
                not_to_draw = [
                    int(screen_coords_a[0] / screen_coords_a[3]),
                    int(screen_coords_a[1] / screen_coords_a[3]),
                    int(screen_coords_c[0] / screen_coords_c[3]),
                    int(screen_coords_c[1] / screen_coords_c[3])
                ]

            self.my_canvas.create_line(not_to_draw, fill=color)


def find_max(triangle):
    ax, ay, az, _ = triangle[0]
    bx, by, bz, _ = triangle[1]
    cx, cy, cz, _ = triangle[2]

    len_ab = math.sqrt((ax-bx)**2 + (ay-by)**2 + (az-bz)**2)
    len_bc = math.sqrt((bx-cx)**2 + (by-cy)**2 + (bz-cz)**2)
    len_ca = math.sqrt((cx-ax)**2 + (cy-ay)**2 + (cz-az)**2)

    if len_ab > len_bc and len_ab > len_ca:
        return 'ab'
    elif len_bc > len_ab and len_bc > len_ca:
        return 'bc'
    else:
        return 'cz'


def is_closer(plane, check):
    p1 = np.array(plane[0])
    p2 = np.array(plane[1])
    p3 = np.array(plane[2])

    cp1 = np.array(check[0])
    cp2 = np.array(check[1])
    cp3 = np.array(check[2])

    v1 = p3 - p1
    v2 = p2 - p1

    cp = np.cross(np.concatenate(v1[:3]), np.concatenate(v2[:3]))
    a, b, c = cp

    d = np.dot(cp, p3[:3])

    cam_dir = 1 if a * \
        utils.camera_coords[0][3] + b*utils.camera_coords[1][3] + c*utils.camera_coords[2][3] - d > 0 else -1

    tr_dir1 = a*(cp1[0]/1e5) + b*(cp1[1]/1e5) + c*(cp1[2]/1e5) - d/1e5
    tr_dir2 = a*(cp2[0]/1e5) + b*(cp2[1]/1e5) + c*(cp2[2]/1e5) - d/1e5
    tr_dir3 = a*(cp3[0]/1e5) + b*(cp3[1]/1e5) + c*(cp3[2]/1e5) - d/1e5

    results = [np.round(x, 6) for x in [tr_dir1, tr_dir2, tr_dir3]]

    for i in range(len(results)):
        if results[i] > 0:
            results[i] = 1
        elif results[i] == 0:
            results[i] = 0
        else:
            results[i] = -1

    if not any(results):
        return 1

    check = [x for x in results if x != 0]
    if cam_dir * check[0] < 0:
        return 1
    return -1


def posortuj(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if is_closer(arr[j], arr[j+1]) == 1:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
