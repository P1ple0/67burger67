import pyxel
import random

from state import State
from player import Player
from enemies import Enemies
import scoreboard

"""
ЕЛИСЕЮ: Нарисовать большого монстра (возможно, червяка, пускающего маленьких червяков)
ЕЛИСЕЮ: Нарисовать обводку от сердца
ЕЛИСЕЮ: Придумать название игры
ЕЛИСЕЮ: Нарисовать картинку для обложки
- Добавить рост здоровья
- Добавить Начальный экран
- Добавить дополнительные абилки:
    INCREASE\nHP\nREGENERATION\nSPEED
    ADD\nONE\nORB
    DESTROY\nALL\nENEMIES
    FREEZE\nALL\nENEMIES
    BECOME\nINVINSIBLE
- Сделать веб-билд, зааплоадить на итч
"""


class App:
    def __init__(self):
        pyxel.init(400, 300, display_scale=3)  # 320x200
        pyxel.load("data.pyxres")
        self.font = pyxel.Font("notcourier.ttf", 30)
        self.player = Player()
        self.state = State(self.player)
        self.enemies = Enemies(self.player)

        self.flowers = []
        for i in range(100):
            x = random.randint(0, pyxel.width)
            y = random.randint(0, pyxel.height)
            c = random.choice([(48, 16), (56, 16), (48, 24), (56, 24)])
            self.flowers.append([x, y, c[0], c[1]])

        pyxel.run(self.update, self.draw)

    def update(self):

        if self.state.state is None:
            if self.state.hp > 0:
                self.player.update()
                self.enemies.update(self.state,
                                    self.player.points[self.player.point_index][0], self.player.points[self.player.point_index][1])
            else:
                if pyxel.btn(pyxel.KEY_SPACE):
                    self.player = Player()
                    self.state = State(self.player)
                    self.enemies = Enemies(self.player)

    def draw(self):

        if self.state.hp > 0:
            pyxel.cls(pyxel.COLOR_LIME)

            for (x, y, u, v) in self.flowers:
                pyxel.blt(x=x, y=y, img=0, u=u, v=v, w=8, h=8, colkey=11)

            self.enemies.draw()
            self.player.draw()
            self.state.draw()

            # Рисуем жизни
            for i in range(self.state.hp):
                pyxel.blt(x=i*20, y=1, img=0, u=0, v=64, w=16, h=16, colkey=pyxel.COLOR_LIGHT_BLUE)

        else:
            pyxel.cls(pyxel.COLOR_BLACK)

            # Если игрок умер, сохраняем его статистику
            if not self.state.board:
                self.state.board = scoreboard.save(self.state.level, self.state.score_total)

            # pyxel.text(x=50, y=pyxel.height/2-35, s='G A M E  O V E R', col=pyxel.COLOR_RED, font=self.font)
            pyxel.text(x=50, y=10, s='#     Name            Date                         Level           Score', col=pyxel.COLOR_DARK_BLUE)
            pyxel.text(x=50, y=20, s='-'*75, col=pyxel.COLOR_DARK_BLUE)
            for i, stat in enumerate(self.state.board):
                color = pyxel.COLOR_YELLOW
                if stat.get('current'):
                    color = pyxel.COLOR_RED

                pyxel.text(x=50, y=30+i*10, s=f'{str(i+1).zfill(2)}.   {stat['name']}       {stat['date']}          {stat['level']}               {stat['score']}', col=color)
            pyxel.text(x=110, y=pyxel.height-40, s='P r e s s   [ S P A C E ]   t o   s t a r t', col=pyxel.COLOR_GREEN)

App()
