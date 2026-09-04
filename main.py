import math
import pyxel
import random

ANIMALS = [(32, 8), (48, 8), (0, 23)]
ANIMAL_W = 8
ANIMAL_H = 8
PLAYER_W = 8
PLAYER_H = 12

class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("data.pyxres")
        self.x = pyxel.width // 2
        self.y = pyxel.height // 2
        self.u = 16
        self.v = 0
        self.w = 8
        self.speed = 1
        self.score = 0
        self.bot_x = random.randint(0, pyxel.width - ANIMAL_W)
        self.bot_y = random.randint(0, pyxel.height - ANIMAL_H)
        self.bot_u, self.bot_v = random.choice(ANIMALS)

        self.flowers = []
        for i in range(30):
            x = random.randint(0, pyxel.width)
            y = random.randint(0, pyxel.height)
            c = random.choice([(48, 16), (56, 16), (48, 24), (56, 24)])
            self.flowers.append([x, y, c[0], c[1]])


        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.cls(0)
        if pyxel.btn(pyxel.KEY_A):
            self.x -= self.speed
            self.u = 24
            self.v = 0
            self.w = -8
        elif pyxel.btn(pyxel.KEY_D):
            self.x += self.speed
            self.u = 24
            self.v = 0
            self.w = 8
        if pyxel.btn(pyxel.KEY_W):
            self.y -= self.speed
            self.u = 16
            self.v = 16
            self.w = 8
        elif pyxel.btn(pyxel.KEY_S):
            self.y += self.speed
            self.u = 16
            self.v = 0
            self.w = 8

        if self.x < 0:
            self.x = 0
        elif self.x > pyxel.width - PLAYER_W:
            self.x = pyxel.width - PLAYER_W
        if self.y < 0:
            self.y = 0
        elif self.y > pyxel.height - PLAYER_H:
            self.y = pyxel.height - PLAYER_H

        if math.dist((self.x, self.y), (self.bot_x, self.bot_y)) < (ANIMAL_W+ANIMAL_H)/2:
            self.score += 1
            self.bot_x = random.randint(0, pyxel.width - ANIMAL_W)
            self.bot_y = random.randint(0, pyxel.height - ANIMAL_H)
            self.bot_u, self.bot_v = random.choice(ANIMALS)

        if pyxel.frame_count % 5 == 0:
            self.bot_x = random.choice([self.bot_x-1, self.bot_x, self.bot_x+1])
            self.bot_y = random.choice([self.bot_y-1, self.bot_y, self.bot_y+1])

        if self.bot_x < 0:
            self.bot_x = 0
        elif self.bot_x > pyxel.width - ANIMAL_W:
            self.bot_x = pyxel.width - ANIMAL_W
        if self.bot_y < 0:
            self.bot_y = 0
        elif self.bot_y > pyxel.height - ANIMAL_H:
            self.bot_y = pyxel.height - ANIMAL_H

    def draw(self):
        pyxel.cls(11)

        for (x, y, u, v) in self.flowers:
            pyxel.blt(x=x, y=y, img=0, u=u, v=v, w=8, h=8, colkey=11)

        pyxel.blt(x=self.bot_x, y=self.bot_y, img=0, u=self.bot_u, v=self.bot_v, w=8, h=8, colkey=6)
        pyxel.blt(x=self.x, y=self.y, img=0, u=self.u, v=self.v, w=self.w, h=12, colkey=6)
        pyxel.text(x=1, y=1, s=str(self.score), col=pyxel.COLOR_RED)


App()
