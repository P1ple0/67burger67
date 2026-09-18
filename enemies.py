import math
import pyxel
import random


ENEMIES = [(32, 8), (48, 8), (0, 23)]
ENEMY_W = 8
ENEMY_H = 8

class Enemies:
    def __init__(self):
        self.list = [Enemy()]

    def draw(self):
        [e.draw() for e in self.list]

    def update(self, state, player_x, player_y, point_x, point_y):

        for i, enemy in enumerate(self.list):
            enemy.update(player_x, player_y)

            # Уничтожаем противника при соприкосновении с оружием
            if math.dist((point_x, point_y), (enemy.x, enemy.y)) < (ENEMY_W + ENEMY_H) / 2:

                # Увеличиваем счёт
                state.score += 1

                # Добавляем нового врага
                self.list.append(Enemy())

                # Перегенеряем старого врага
                self.list[i] = Enemy()

            # Отнимаем жизни у игрока при столкновении с противником
            if math.dist((player_x, player_y), (enemy.x, enemy.y)) < (ENEMY_W + ENEMY_H) / 2:
                state.hp -= 1

        [e.update(player_x, player_y) for e in self.list]

class Enemy:
    def __init__(self):
        offset = random.randint(50, 200)
        self.x, self.y = random.choice([(-offset, random.randint(0, pyxel.height)),
                                        (pyxel.width+offset, random.randint(0, pyxel.height)),
                                        (random.randint(0, pyxel.width), -offset),
                                        (random.randint(0, pyxel.width), pyxel.height+offset)
                                        ])
        self.u, self.v = random.choice(ENEMIES)
        self.speed = 0.3

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0, u=self.u, v=self.v, w=8, h=8, colkey=6)

    def update(self, player_x, player_y):

        # Приближаемся к игроку
        if self.x < player_x:
            self.x += self.speed
        elif self.x > player_x:
            self.x -= self.speed
        if self.y < player_y:
            self.y += self.speed
        elif self.y > player_y:
            self.y -= self.speed

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
