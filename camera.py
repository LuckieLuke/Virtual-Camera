from matrices import *
import utils
from tkinter import *
from functools import cmp_to_key


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
                            fill='blue',
                            outline='red'
                        )
                    )
        self.render()
        self.root.mainloop()

    def key_pressed(self, event):
        if event.char == 'd':
            utils.move(self.triangles_coords, 'left')
            # utils.move_cam('right')
        elif event.char == 'a':
            utils.move(self.triangles_coords, 'right')
            # utils.move_cam('left')
        elif event.char == 's':
            utils.move(self.triangles_coords, 'up')
            # utils.move_cam('down')
        elif event.char == 'w':
            utils.move(self.triangles_coords, 'down')
            # utils.move_cam('up')
        elif event.char == 'c':
            utils.move(self.triangles_coords, 'front')
            # utils.move_cam('back')
        elif event.char == 'f':
            utils.move(self.triangles_coords, 'back')
            # utils.move_cam('front')
        elif event.char == 'q':
            utils.rotate(self.triangles_coords, -0.01, 'z')
            #utils.rotate_cam(0.01, 'z')
        elif event.char == 'e':
            utils.rotate(self.triangles_coords, 0.01, 'z')
            #utils.rotate_cam(-0.01, 'z')
        elif event.char == 'r':
            utils.rotate(self.triangles_coords, -0.01, 'x')
            #utils.rotate_cam(0.01, 'x')
        elif event.char == 't':
            utils.rotate(self.triangles_coords, 0.01, 'x')
            #utils.rotate_cam(-0.01, 'x')
        elif event.char == 'h':
            utils.rotate(self.triangles_coords, -0.01, 'y')
            #utils.rotate_cam(0.01, 'y')
        elif event.char == 'g':
            utils.rotate(self.triangles_coords, 0.01, 'y')
            #utils.rotate_cam(-0.01, 'y')
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
        # screen_triangles = []

        # for index, coord in enumerate(self.triangles_coords):
        #     screen_coords_a = M.dot(coord[0])
        #     screen_coords_b = M.dot(coord[1])
        #     screen_coords_c = M.dot(coord[2])

        #     screen_triangles.append(
        #         (screen_coords_a, screen_coords_b, screen_coords_c, self.triangles[index]))

        self.triangles_coords = sorted(
            self.triangles_coords, key=cmp_to_key(is_closer))
        # for triangle in self.triangles_coords:
        #     print(triangle[3])
        # print(self.triangles_coords)

        # print(screen_triangles)
        # print(self.triangles)

        self.my_canvas.delete("all")

        for index, coord in enumerate(self.triangles_coords):
            screen_coords_a = M.dot(coord[0])
            screen_coords_b = M.dot(coord[1])
            screen_coords_c = M.dot(coord[2])
            # print(screen_triangle[3])
            # self.my_canvas.coords(self.triangles[screen_triangle[3]-1], [
            #     int(screen_triangle[0][0] / screen_triangle[0][3]),
            #     int(screen_triangle[0][1] / screen_triangle[0][3]),
            #     int(screen_triangle[1][0] / screen_triangle[1][3]),
            #     int(screen_triangle[1][1] / screen_triangle[1][3]),
            #     int(screen_triangle[2][0] / screen_triangle[2][3]),
            #     int(screen_triangle[2][1] / screen_triangle[2][3])
            # ])

            self.my_canvas.create_polygon(
                int(screen_coords_a[0] / screen_coords_a[3]),
                int(screen_coords_a[1] / screen_coords_a[3]),
                int(screen_coords_b[0] / screen_coords_b[3]),
                int(screen_coords_b[1] / screen_coords_b[3]),
                int(screen_coords_c[0] / screen_coords_c[3]),
                int(screen_coords_c[1] / screen_coords_c[3]),
                fill='blue',
                outline='red'
            )


def is_closer(plane, check, *zapychadelko):
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
        utils.camera_coords[0][3] + b*utils.camera_coords[1][3] + c*utils.camera_coords[2][3] - d >= 0 else -1

    tr_dir1 = a*cp1[0] + b*cp1[1] + c*cp1[2] - d
    tr_dir2 = a*cp2[0] + b*cp2[1] + c*cp2[2] - d
    tr_dir3 = a*cp3[0] + b*cp3[1] + c*cp3[2] - d

    results = [np.round(x, 6) for x in [tr_dir1, tr_dir2, tr_dir3]]

    # if plane[3] == 10 and check[3] == 25:
    #     print(f'{tr_dir1} {tr_dir2} {tr_dir3}')

    if not any(results):
        return 0

    # print(results)
    check = [x for x in results if x != 0]
    if cam_dir * check[0] < 0:
        return 1
    return -1
