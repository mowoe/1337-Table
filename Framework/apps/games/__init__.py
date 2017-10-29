import numpy as np
from theme import theme
import time


class Game(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8) + theme["background"]

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

    def loop(self): pass

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

        self.loop()

        time.sleep(0.03)

    def get_self_frame(self):
        return self.frame
