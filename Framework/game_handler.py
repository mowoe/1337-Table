import time
from theme import theme
from font import render_text
import numpy as np

from apps.games import conf


class GameHandler(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8) + theme["background"]

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

        self.games = {
        }

        for key in conf.apps.keys():
            self.games.update({key: conf.apps[key]})

        self.keys = self.games.keys()
        self.index = 0

        self.active = self
        self.back_time = time.time()

    def activation(self):
        self.active = self
        self.back_time = time.time()

    def back(self):
        self.active = self
        self.back_time = time.time()

    def self_update(self, keys_down):
        self.active.self_self_update(keys_down)

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

        self.frame = np.zeros((20, 35, 3), np.uint8) + theme["background"]
        render_text(self.get_frame(), theme["header"], theme["background"], "Games", 0, 0)
        render_text(self.get_frame(), theme["text"], theme["background"], self.keys[self.index], 2, 8)
        a = "<"
        b = ">"
        if self.index == 0:
            a = " "
        if self.index == len(self.keys) - 1:
            b = " "
        render_text(self.frame, theme["elements"], theme["background"], "%s      %s" % (a, b), 2, 14)

        if self.keys_down["LEFT"] and not self.last_keys_down["LEFT"]:
            self.back_time = time.time()
            if self.index > 0:
                self.index -= 1

        if self.keys_down["RIGHT"] and not self.last_keys_down["RIGHT"]:
            self.back_time = time.time()
            if self.index < len(self.keys) - 1:
                self.index += 1

        if self.keys_down["A"] and not self.last_keys_down["A"]:
            self.active = self.games[self.keys[self.index]](self.matrix, self)

        if self.keys_down["B"] and not self.last_keys_down["B"]:
            self.parent.back()

        if time.time() - self.back_time > self.parent.standby_timeout:
            self.parent.standby()
        else:
            tleft = time.time() - self.back_time
            if tleft > 0:
                tleft /= float(self.parent.standby_timeout)
                r = int(tleft * 255)
                g = 255 - r
                b = 0
                self.frame[18, 1] = (r, g, b)

        time.sleep(0.05)

    def get_self_frame(self):
        return self.frame

    def get_frame(self):
        return self.active.get_self_frame()
