import pyxel
import random

STATE_SELECT_UPDATE = 'STATE_SELECT_UPDATE'
UPDATES = ['INCREASE\nWALK\nSPEED',
           'INCREASE\nHP',
           'INCREASE\nORB\nSIZE',
           'INCREASE\nORB\nDISTANCE',
           'INCREASE\nORB\nSPEED'
           ]

class State:
    def __init__(self, player):
        self.player = player
        self.state = None
        self.level = 1
        self.score_for_level = 2 ** self.level
        self.score = 0
        self.score_total = 0
        self.hp = 3

        # Параметры прогресс-бара
        self.w = 0
        self.h = 9
        self.update_progress_bar()
        self.updates = random.sample(UPDATES, 3)
        self.block = 50

        # Доска достижение
        self.board = None

    def draw(self):

        # Заполняем прогресс-бар
        pyxel.rect(x=0, y=pyxel.height-self.h, w=pyxel.width, h=self.h, col=pyxel.COLOR_GRAY)
        pyxel.rect(x=0, y=pyxel.height-self.h, w=self.w, h=self.h, col=pyxel.COLOR_RED)

        # Рисуем рамку прогресс-бара
        pyxel.rectb(x=0, y=pyxel.height-self.h, w=pyxel.width, h=self.h, col=pyxel.COLOR_RED)
        pyxel.text(x=pyxel.width/2-20, y=pyxel.height-7, s=f'LEVEL: {self.level}', col=pyxel.COLOR_BLACK)

        # Выбор апдейтов
        if self.state == STATE_SELECT_UPDATE:
            for i in range(3):
                x = pyxel.width/2-self.block*1.5+i*self.block
                y = pyxel.height/2-self.block/2
                pyxel.rect(x=x, y=y, w=self.block, h=self.block, col=pyxel.COLOR_RED)
                pyxel.rectb(x=x, y=y, w=self.block, h=self.block, col=pyxel.COLOR_PURPLE)
                pyxel.text(x=x+2, y=y+2, s=f'[{i+1}]', col=pyxel.COLOR_PURPLE)
                pyxel.text(x=x+2, y=y+12, s=self.updates[i], col=pyxel.COLOR_PURPLE)

            if any([pyxel.btnp(pyxel.KEY_1), pyxel.btnp(pyxel.KEY_2), pyxel.btnp(pyxel.KEY_3)]):
                self.score = 0
                self.level += 1
                self.score_for_level = 2 ** self.level
                one_block = pyxel.width / self.score_for_level
                self.w = one_block * self.score
                self.state = None
                update = {}

                if pyxel.btnp(pyxel.KEY_1):
                    update = self.updates[0]
                elif pyxel.btnp(pyxel.KEY_2):
                    update = self.updates[1]
                elif pyxel.btnp(pyxel.KEY_3):
                    update = self.updates[2]

                update_index = UPDATES.index(update)
                if update_index == 0:
                    self.player.speed += 0.25
                elif update_index == 1:
                    self.hp += 1
                elif update_index == 2:
                    self.player.orb_size += 1
                    self.player.refresh_orb()
                elif update_index == 3:
                    self.player.orb_distance += 8
                    self.player.refresh_orb()
                elif update_index == 4:
                    self.player.orb_speed -= 1

                self.updates = random.sample(UPDATES, 3)

    def update_progress_bar(self):
        """ Увеличиваем счёт """

        # Просчитываем ширину прогресс бара
        one_block = pyxel.width / self.score_for_level
        self.w = one_block * self.score

        # Рисуем обновления, когда достигли уровня
        if self.score == self.score_for_level:
            self.state = STATE_SELECT_UPDATE
