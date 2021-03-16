from matrices import *
from utils import *
from tkinter import *


class Camera():
    def __init__(self):
        self.rendered = False
        self.root = Tk()
        self.root.title('Virtual Camera')
        self.root.geometry('1000x800')

        self.my_canvas = Canvas(self.root, width=900, height=700, bg='white')
        self.my_canvas.pack(pady=50)

        self.lines = []
        self.lines_coords = []
        self.root.bind('<Key>', self.key_pressed)

        with open('coords.txt', 'r') as file:
            for line in file.readlines():
                if line[0] != '#':
                    coords = [int(x) for x in line.split()]
                    start = np.array([[*coords[:3], 1]]).T
                    end = np.array([[*coords[3:], 1]]).T

                    self.lines_coords.append((start, end))
                    if start[2][0] == -50 and end[2][0] == -50:
                        color = "red"
                    elif start[2][0] == -100 and end[2][0] == -100:
                        color = "green"
                    else:
                        color = "blue"
                    if start[0][0] == 20 and start[1][0] == 20 and start[2][0] == -50 and end[0][0] == 20 and end[1][0] == 70 and end[2][0] == -50:
                        color = "black"
                    self.lines.append(
                        self.my_canvas.create_line(start[0][0], start[1][0], end[0][0], end[1][0], fill=color))
        self.render()
        self.root.mainloop()

    def key_pressed(self, event):
        w = Label(self.root, text='Key pressed: ' + event.char)
        w.place(x=300, y=0)
        if event.char == 'a':
            move(self.lines_coords, 'left')
        elif event.char == 'd':
            move(self.lines_coords, 'right')
        elif event.char == 'w':
            move(self.lines_coords, 'up')
        elif event.char == 's':
            move(self.lines_coords, 'down')
        elif event.char == 'c':
            move(self.lines_coords, 'front')
        elif event.char == 'f':
            move(self.lines_coords, 'back')
        elif event.char == 'q':
            rotate(self.lines_coords, -0.01, 'z')
        elif event.char == 'e':
            rotate(self.lines_coords, 0.01, 'z')
        elif event.char == 'r':
            rotate(self.lines_coords, -0.01, 'x')
        elif event.char == 't':
            rotate(self.lines_coords, 0.01, 'x')
        elif event.char == 'h':
            rotate(self.lines_coords, -0.01, 'y')
        elif event.char == 'g':
            rotate(self.lines_coords, 0.01, 'y')
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
        Mcam = np.array([
            [1, 0, 0, -450],
            [0, 1, 0, -350],
            [0, 0, 1, -500],
            [0, 0, 0, 1]
        ])

        M = P.dot(Mcam)
        M = Morth.dot(M)
        M = MVP.dot(M)

        for index, coord in enumerate(self.lines_coords):
            screen_coords_a = M.dot(coord[0])
            screen_coords_b = M.dot(coord[1])

            self.my_canvas.coords(self.lines[index], [
                int(screen_coords_a[0] / screen_coords_a[3]),
                int(screen_coords_a[1] / screen_coords_a[3]),
                int(screen_coords_b[0] / screen_coords_b[3]),
                int(screen_coords_b[1] / screen_coords_b[3])
            ])
