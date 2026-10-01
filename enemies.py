import pyxel
import random

import helpers


ENEMIES = [(0, 48), (16, 48), (32, 48)]
ENEMY_W = 16
ENEMY_H = 16

class Enemies:
    def __init__(self, player):
        self.player = player
        self.list = [Enemy()]

    def draw(self):
        [e.draw() for e in self.list]

    def update(self, state, point_x, point_y):

        for i, enemy in enumerate(self.list):
            enemy.update(self.player.x, self.player.y)

            # Уничтожаем противника при соприкосновении с оружием
            if check_circle_collision(x1=point_x, y1=point_y, r1=self.player.orb_size, x2=enemy.x+ENEMY_W/2, y2=enemy.y+ENEMY_H/2, r2=ENEMY_W/2):

                # Обновляем прогресс бар
                state.score += 1
                state.score_total += 1
                state.update_progress_bar()

                # Добавляем нового врага
                self.list.append(Enemy())

                # Перегенеряем старого врага
                self.list[i] = Enemy()

            # Отнимаем жизни у игрока при столкновении с противником
            if check_circle_collision(x1=self.player.x+self.player.w/2, y1=self.player.y+self.player.h/2, r1=self.player.w/2, x2=enemy.x+ENEMY_W/2, y2=enemy.y+ENEMY_H/2, r2=ENEMY_W/2) and pyxel.frame_count % 20 == 0:
                state.hp -= 1
                self.player.attacked = True

        [e.update(self.player.x, self.player.y) for e in self.list]

class Enemy:
    def __init__(self):
        offset = random.randint(50, 200)
        self.x, self.y = random.choice([(-offset, random.randint(0, pyxel.height)),
                                        (pyxel.width+offset, random.randint(0, pyxel.height)),
                                        (random.randint(0, pyxel.width), -offset),
                                        (random.randint(0, pyxel.width), pyxel.height+offset)
                                        ])
        self.u, self.v = random.choice(ENEMIES)
        self.speed = random.uniform(0.1, 0.4)

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0, u=self.u, v=self.v, w=16, h=16, colkey=6)

    def update(self, player_x, player_y):

        # Приближаемся к игроку
        shift_x = 0
        shift_y = 0
        if self.x < player_x:
            shift_x = 1
        elif self.x > player_x:
            shift_x = -1
        if self.y < player_y:
            shift_y = 1
        elif self.y > player_y:
            shift_y = -1

        vx, vy = helpers.get_diagonal_velocity(shift_x, shift_y, self.speed)
        self.x += vx
        self.y += vy

        if pyxel.frame_count % 5 == 0:
            self.x = random.choice([self.x-1, self.x, self.x+1])
            self.y = random.choice([self.y-1, self.y, self.y+1])

        if self.x < 0:
            self.x = 0
        elif self.x > pyxel.width - ENEMY_W:
            self.x = pyxel.width - ENEMY_W
        if self.y < 0:
            self.y = 0
        elif self.y > pyxel.height - ENEMY_H:
            self.y = pyxel.height - ENEMY_H


def check_circle_collision(x1, y1, r1, x2, y2, r2):
    """
    Returns True if two circles are colliding, False otherwise.
    Optimized to avoid using square root operations.
    """
    dx = x1 - x2
    dy = y1 - y2
    squared_distance = (dx ** 2) + (dy ** 2)

    radii_sum = r1 + r2
    squared_radii_sum = radii_sum ** 2

    return squared_distance <= squared_radii_sum


