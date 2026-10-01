import math
import pyxel
import random

import helpers


COORDINATES = {'down': {'u': 0, 'v': 32, 'w': 16, 'h': 16},
               'up': {'u': 16, 'v': 32, 'w': 16, 'h': 16},
               'down-right': {'u': 32, 'v': 32, 'w': 16, 'h': 16},
               'down-left': {'u': 32, 'v': 32, 'w': -16, 'h': 16},
               'up-right': {'u': 48, 'v': 32, 'w': 16, 'h': 16},
               'up-left': {'u': 48, 'v': 32, 'w': -16, 'h': 16},
               }


class Player:
    def __init__(self):
        self.x = pyxel.width // 2 - COORDINATES['down']['w']/2
        self.y = pyxel.height // 2 - COORDINATES['down']['h']/2
        self.u, self.v, self.w, self.h = COORDINATES['down'].values()
        self.speed = 1

        # Orb / Сфера
        self.orb_speed = 6
        self.orb_distance = 20
        self.orb_size = 1
        self.point_index = 0
        self.points = None
        self.refresh_orb()

        self.attacked = False

    def draw(self):

        pyxel.blt(x=self.x, y=self.y, img=0, u=self.u, v=self.v, w=self.w, h=self.h, colkey=6)
        pyxel.circ(x=self.points[self.point_index][0], y=self.points[self.point_index][1], r=self.orb_size, col=random.randint(0, 16))

        # Если игрок теряет жизни:
        if self.attacked:
            pyxel.circ(x=self.x+self.w/2, y=self.y+self.h/2, r=self.w/2, col=pyxel.COLOR_RED)
            self.attacked = False

    def update(self):

        if pyxel.frame_count % self.orb_speed == 0:
            self.point_index += 1
            if self.point_index >= len(self.points):
                self.point_index = 0

        shift_x = 0
        shift_y = 0
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            shift_x = -1
            self.u, self.v, self.w, self.h = COORDINATES['down-left'].values()
        elif pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            shift_x = 1
            self.u, self.v, self.w, self.h = COORDINATES['down-right'].values()
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            shift_y = -1
            self.u, self.v, self.w, self.h = COORDINATES['up'].values()
        elif pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            shift_y = 1
            self.u, self.v, self.w, self.h = COORDINATES['down'].values()

        vx, vy = helpers.get_diagonal_velocity(shift_x, shift_y, self.speed)
        self.x += vx
        self.y += vy

        if self.x < 0:
            self.x = 0
        elif self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.h
        if self.y < 0:
            self.y = 0
        elif self.y > pyxel.height - self.h:
            self.y = pyxel.height - self.h

        # Перегенеряем координаты кружочка, если игрок сдвинулся
        if shift_x or shift_y:
            self.refresh_orb()

    def refresh_orb(self):
        """ Обновляем координаты Сферы """
        self.points = get_circle_edge_coordinates(cx=self.x+abs(self.w/2), cy=self.y+abs(self.h/2), radius=self.orb_distance, num_points=20)

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
