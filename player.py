import math
import pyxel


class Player:
    def __init__(self):
        self.x = pyxel.width // 2
        self.y = pyxel.height // 2
        self.u = 16
        self.v = 0
        self.w = 8
        self.h = 12
        self.speed = 1
        self.points = get_circle_edge_coordinates(cx=self.x+self.w/2, cy=self.y+self.h/2, radius=20, num_points=20)
        self.point_index = 0

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0, u=self.u, v=self.v, w=self.w, h=12, colkey=6)
        pyxel.circ(self.points[self.point_index][0], self.points[self.point_index][1], r=1, col=pyxel.COLOR_RED)

    def update(self):

        if pyxel.frame_count % 6 == 0:
            self.point_index += 1
            if self.point_index >= len(self.points):
                self.point_index = 0

        x_tmp = self.x
        y_tmp = self.y

        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.u = 24
            self.v = 0
            self.w = -8
        elif pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.u = 24
            self.v = 0
            self.w = 8
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
            self.u = 16
            self.v = 16
            self.w = 8
        elif pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
            self.u = 16
            self.v = 0
            self.w = 8

        if self.x < 0:
            self.x = 0
        elif self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.h
        if self.y < 0:
            self.y = 0
        elif self.y > pyxel.height - self.h:
            self.y = pyxel.height - self.h

        # Перегенеряем координаты кружочка, если игрок сдвинулся
        if x_tmp != self.x or y_tmp != self.y:
            self.points = get_circle_edge_coordinates(cx=self.x+self.w/2, cy=self.y+self.h/2, radius=20, num_points=10)


def get_circle_edge_coordinates(cx, cy, radius, num_points=20):
    coordinates = []
    for i in range(num_points):
        # Calculate the angle for the current point
        angle = 2 * math.pi * i / num_points

        # Trigonometry formula for circle coordinates
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)

        coordinates.append((x, y))
    return coordinates
