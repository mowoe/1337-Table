import numpy as np
from Framework.theme import theme
import time


class Game(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8) + theme["background"]

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

    def loop(self): pass

    def is_key_down(self, key):
        return self.keys_down[key] and not self.last_keys_down[key]

    def is_key_pressed(self, key):
        return self.keys_down[key]

    def is_key_up(self, key):
        return self.last_keys_down[key] and not self.keys_down[key]

    def clear(self):
        self.frame = np.zeros((20, 35, 3), np.uint8) + theme["background"]

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

        self.loop()

        time.sleep(0.03)

    def get_self_frame(self):
        return self.frame
