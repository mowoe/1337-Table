import numpy as np
import random
import bresenham
from theme import theme
import time
from apps.games import Game


class Pong(Game):
    def __init__(self, matrix, parent):
        super(Pong, self).__init__(matrix, parent)

        self.paddle_a = 11
        self.paddle_b = 11
        self.paddle_a_range = []
        self.paddle_b_range = []

        self.ball = [17, 10]
        self.ball_dest = [1, random.randint(7, 13)]
        self.ball_curve = self.curve()

    def curve(self):
        x0, y0 = self.ball
        x1, y1 = self.ball_dest
        return list(bresenham(x0, y0, x1, y1))

    def draw_paddles(self):
        self.paddle_a_range = []
        self.paddle_b_range = []
        for i in range(-2, 3):
            self.frame[self.paddle_a + i, 2] = theme["pong_paddle"]
            self.paddle_a_range.append(self.paddle_a + i)
            self.frame[self.paddle_b + i, -3] = theme["pong_paddle"]
            self.paddle_b_range.append(self.paddle_b + i)

    def draw_ball(self):
        ball_x, ball_y = self.ball
        self.frame[ball_y, ball_x] = theme["pong_ball"]

    def loop(self):
        self.frame = np.zeros((20, 35, 3), np.uint8)

        if self.keys_down["UP"]:
            self.paddle_a -= 1
            if self.paddle_a < 2:
                self.paddle_a += 1
        if self.keys_down["DOWN"]:
            self.paddle_a += 1
            if self.paddle_a > 17:
                self.paddle_a -= 1
        if self.keys_down["B"] and not self.last_keys_down["B"]:
            self.parent.back()

        self.draw_paddles()
        self.draw_ball()

        self.ball = self.ball_curve.pop(0)

        if self.ball[0] == 2:  # Paddle check
            if self.ball[1] in self.paddle_a_range:
                self.ball_dest = [33, random.randint(7, 13)]
                self.ball_curve = self.curve()

        if self.ball[0] == 1:  # Lose check
            self.ball = [17, 10]
            self.ball_dest = [1, random.randint(7, 13)]
            self.ball_curve = self.curve()
            time.sleep(1)

        if self.ball[0] == 32:  # Paddle check
            if self.ball[1] in self.paddle_b_range:
                self.ball_dest = [1, random.randint(7, 13)]
                self.ball_curve = self.curve()

        if self.ball[0] == 33:  # Lose check
            self.ball = [17, 10]
            self.ball_dest = [33, random.randint(7, 13)]
            self.ball_curve = self.curve()
            time.sleep(1)
