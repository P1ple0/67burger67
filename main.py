import pyxel
import random

from state import State
from player import Player
from enemies import Enemies


class App:
    def __init__(self):
        pyxel.init(320, 240)
        pyxel.load("data.pyxres")
        self.font = pyxel.Font("notcourier.ttf", 30)
        self.state = State()
        self.player = Player()
        self.enemies = Enemies()

        self.flowers = []
        for i in range(100):
            x = random.randint(0, pyxel.width)
            y = random.randint(0, pyxel.height)
            c = random.choice([(48, 16), (56, 16), (48, 24), (56, 24)])
            self.flowers.append([x, y, c[0], c[1]])

        pyxel.run(self.update, self.draw)

    def update(self):

        if self.state.hp > 0:
            self.player.update()
            self.enemies.update(self.state,
                                self.player.x, self.player.y,
                                self.player.points[self.player.point_index][0], self.player.points[self.player.point_index][1])
        else:
            if pyxel.btn(pyxel.KEY_SPACE):
                self.state.hp = 3
                self.state.score = 0
                self.enemies = Enemies()

    def draw(self):

        if self.state.hp > 0:
            pyxel.cls(pyxel.COLOR_LIME)

            for (x, y, u, v) in self.flowers:
                pyxel.blt(x=x, y=y, img=0, u=u, v=v, w=8, h=8, colkey=11)

            self.enemies.draw()
            self.player.draw()
            pyxel.text(x=1, y=1, s=str(self.state.score), col=pyxel.COLOR_RED)

        else:
            pyxel.cls(pyxel.COLOR_BLACK)
            pyxel.text(x=15, y=pyxel.height/2-35, s='G A M E  O V E R', col=pyxel.COLOR_RED, font=self.font)
            pyxel.text(x=130, y=pyxel.height-80, s=f'S C O R E:  {self.state.score}', col=pyxel.COLOR_YELLOW)
            pyxel.text(x=70, y=pyxel.height-40, s='P r e s s   [ S P A C E ]   t o   s t a r t', col=pyxel.COLOR_GREEN)

App()
