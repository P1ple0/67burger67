import pyxel
import random

import helpers


class Boss:
    def __init__(self, player):

        self.player = player

        offset = 500
        self.x, self.y = random.choice([(-offset, random.randint(0, pyxel.height)),
                                        (pyxel.width+offset, random.randint(0, pyxel.height)),
                                        (random.randint(0, pyxel.width), -offset),
                                        (random.randint(0, pyxel.width), pyxel.height+offset)
                                        ])
        self.u = 0
        self.v = 80
        self.w = 48
        self.h = 32
        self.speed = 0.4
        self.hp = 100
        self.hp_max = self.hp

    def draw(self):

        # Рисуем босса
        pyxel.blt(x=self.x, y=self.y, img=0, u=self.u, v=self.v, w=self.w, h=self.h, colkey=6)

        # Рисуем цифрами HP босса
        pyxel.text(x=self.x+self.w/2-5, y=self.y-8, s=str(int(self.hp)), col=pyxel.COLOR_RED)

        # # Рисуем фон HP босса
        # pyxel.rect(x=self.x, y=self.y-8, w=self.w, h=5, col=pyxel.COLOR_GRAY)
        #
        # # Рисуем рамку НР босса
        # pyxel.rectb(x=self.x, y=self.y-8, w=self.w, h=5, col=pyxel.COLOR_RED)
        #
        # # Заполняем жизнями HP босса
        # pyxel.rect(x=self.x, y=self.y-8, w=self.hp, h=5, col=pyxel.COLOR_RED)

    def update(self, state):

        # Приближаемся к игроку
        shift_x = 0
        shift_y = 0
        if self.x < self.player.x:
            shift_x = 1
        elif self.x > self.player.x:
            shift_x = -1
        if self.y < self.player.y:
            shift_y = 1
        elif self.y > self.player.y:
            shift_y = -1

        vx, vy = helpers.get_diagonal_velocity(shift_x, shift_y, self.speed)
        self.x += vx
        self.y += vy

        if pyxel.frame_count % 5 == 0:
            self.x = random.choice([self.x-1, self.x, self.x+1])
            self.y = random.choice([self.y-1, self.y, self.y+1])

        if self.x < 0:
            self.x = 0
        elif self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.w
        if self.y < 0:
            self.y = 0
        elif self.y > pyxel.height - self.h:
            self.y = pyxel.height - self.h


        # Отнимаем у босса жизнь при соприкосновении с оружием
        if any([helpers.check_circle_collision(x1=self.player.points[self.player.point_index][0], y1=self.player.points[self.player.point_index][1], r1=self.player.orb_size, x2=self.x+16, y2=self.y+16, r2=16),
                helpers.check_circle_collision(x1=self.player.points[self.player.point_index][0], y1=self.player.points[self.player.point_index][1], r1=self.player.orb_size, x2=self.x+24, y2=self.y+16, r2=16),
                helpers.check_circle_collision(x1=self.player.points[self.player.point_index][0], y1=self.player.points[self.player.point_index][1], r1=self.player.orb_size, x2=self.x+32, y2=self.y+16, r2=16)]
               ):
            self.hp -= 1

        # Отнимаем жизни у игрока при столкновении с противником
        if pyxel.frame_count % 20 == 0 and\
           any([helpers.check_circle_collision(x1=self.player.x+self.player.w/2, y1=self.player.y+self.player.h/2, r1=self.player.orb_size, x2=self.x+16, y2=self.y+16, r2=16),
                 helpers.check_circle_collision(x1=self.player.x+self.player.w/2, y1=self.player.y+self.player.h/2, r1=self.player.orb_size, x2=self.x+24, y2=self.y+16, r2=16),
                 helpers.check_circle_collision(x1=self.player.x+self.player.w/2, y1=self.player.y+self.player.h/2, r1=self.player.orb_size, x2=self.x+32, y2=self.y+16, r2=16)]
              ):
            state.hp -= 1
            self.player.attacked = True
