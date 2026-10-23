import pyxel
import random

import boss
import helpers
import settings


ENEMIES = [(0, 48), (16, 48), (32, 48)]
ENEMY_W = 16
ENEMY_H = 16
ENEMY_STATE_ALIVE = 'ENEMY_STATE_ALIVE'
ENEMY_STATE_KILLED = 'ENEMY_STATE_KILLED'


class Enemies:
    def __init__(self, player):
        self.player = player
        self.list = [Enemy()]
        self.boss = boss.Boss(self.player)

    def draw(self):

        # Рисуем обычных врагов
        [e.draw() for e in self.list]

        # Рисуем босса
        if self.boss.hp > 0:
            self.boss.draw()

    def update(self, state, point_x, point_y):

        # Босс
        if state.level >= settings.BOSS_SHOWS_UP_AFTER_LEVEL and pyxel.frame_count - state.freeze_started > 300 and self.boss.hp > 0:
            self.boss.update(state)

            # Добавляем босовских детенышей
            if pyxel.frame_count % 100 == 0:
                self.list.append(Enemy(xy=[self.boss.x+self.boss.w/2-16, self.boss.y+self.boss.h/2-16],
                                       uv=[48, 80],
                                       speed=0.8))

        # Обычные враги
        for i, enemy in enumerate(self.list):

            # Обновляем врага [если он не заморожен]
            if pyxel.frame_count - state.freeze_started > 300:
                enemy.update(self.player.x, self.player.y)

            # Уничтожаем противника при соприкосновении с оружием
            if helpers.check_circle_collision(x1=point_x, y1=point_y, r1=self.player.orb_size, x2=enemy.x+ENEMY_W/2, y2=enemy.y+ENEMY_H/2, r2=ENEMY_W/2):

                # Обновляем прогресс бар
                state.score += 1
                state.score_total += 1
                state.update_progress_bar()

                if state.level < settings.BOSS_SHOWS_UP_AFTER_LEVEL:

                    # Добавляем нового врага
                    self.list.append(Enemy())

                    # Перегенеряем старого врага
                    self.list[i] = Enemy()

                else:
                    enemy.state = ENEMY_STATE_KILLED

            # Отнимаем жизни у игрока при столкновении с противником
            if helpers.check_circle_collision(x1=self.player.x+self.player.w/2, y1=self.player.y+self.player.h/2, r1=self.player.w/2, x2=enemy.x+ENEMY_W/2, y2=enemy.y+ENEMY_H/2, r2=ENEMY_W/2) and pyxel.frame_count % 20 == 0:
                state.hp -= 1
                self.player.attacked = True

        # Удаляем убитых врагов
        self.list = [e for e in self.list if e.state == ENEMY_STATE_ALIVE]


class Enemy:
    def __init__(self, xy=None, uv=None, speed=None):
        self.state = ENEMY_STATE_ALIVE

        if speed:
            self.speed = speed
        else:
            self.speed = random.uniform(0.1, 0.4)

        self.x = None
        self.y = None
        if xy:
            self.x, self.y = xy
        else:
            self.generate_location()

        if uv:
            self.u, self.v = uv
        else:
            self.u, self.v = random.choice(ENEMIES)

    def generate_location(self):
        offset = random.randint(50, 200)
        self.x, self.y = random.choice([(-offset, random.randint(0, pyxel.height)),
                                        (pyxel.width+offset, random.randint(0, pyxel.height)),
                                        (random.randint(0, pyxel.width), -offset),
                                        (random.randint(0, pyxel.width), pyxel.height+offset)
                                        ])

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
