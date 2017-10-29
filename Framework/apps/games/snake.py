import numpy as np
import random
from theme import theme
import time
from font import render_text
from apps.games import Game


class Snake(Game):
    def __init__(self, matrix, parent):
        super(Snake, self).__init__(matrix, parent)

        self.particle = [random.randint(0, 34), random.randint(0, 19)]
        self.snake = [[random.randint(0, 34), random.randint(0, 19)]]
        self.direction = [1, 0]
        random.shuffle(self.direction)
        self.length = 3
        self.ingame = False
        self.firstrun = True

    def loop(self):
        if self.ingame:
            if self.keys_down["LEFT"] and not self.last_keys_down["LEFT"]: self.direction = [-1, 0]
            if self.keys_down["RIGHT"] and not self.last_keys_down["RIGHT"]: self.direction = [1, 0]
            if self.keys_down["UP"] and not self.last_keys_down["UP"]: self.direction = [0, -1]
            if self.keys_down["DOWN"] and not self.last_keys_down["DOWN"]: self.direction = [0, 1]
            if self.keys_down["B"] and not self.last_keys_down["B"]:
                self.ingame = False
                self.firstrun = False

            self.frame = np.zeros((20, 35, 3), np.uint8) + theme["snake_background"]
            particle_x, particle_y = self.particle
            self.frame[particle_y, particle_x] = theme["snake_food"]

            newpoint = list(self.snake[-1])
            newpoint[0] = (newpoint[0] + self.direction[0]) % 35
            newpoint[1] = (newpoint[1] + self.direction[1]) % 20
            self.snake.append(newpoint)

            if newpoint in self.snake[:-1]:
                self.ingame = False
                self.firstrun = False

            if newpoint[0] == self.particle[0] and newpoint[1] == self.particle[1]:
                self.length += 1
                self.particle = [random.randint(0, 34), random.randint(0, 19)]

            if len(self.snake) > self.length:
                self.snake.pop(0)

            time.sleep(0.07)

            for point in self.snake:
                point_x, point_y = point
                self.frame[point_y, point_x] = theme["snake_snake"]
        else:
            render_text(self.get_self_frame(), theme["header"], theme["snake_background"], "Snake", 0, 0)
            if self.firstrun:
                render_text(self.get_self_frame(), theme["snake_welcome"], theme["snake_background"], "Welcome", 2, 8)
            else:
                render_text(self.get_self_frame(), theme["snake_lose"], theme["snake_background"], "You lose", 2, 8)
            if self.keys_down["A"] and not self.last_keys_down["A"]:
                self.particle = [random.randint(0, 34), random.randint(0, 19)]
                self.snake = [[random.randint(0, 34), random.randint(0, 19)]]
                self.direction = [1, 0]
                random.shuffle(self.direction)
                self.length = 3
                self.ingame = True

            if self.last_keys_down["B"] and not self.keys_down["B"]:
                self.parent.back()
