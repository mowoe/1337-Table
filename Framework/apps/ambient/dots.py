from apps.ambient import Ambient
import math
import random
import colorsys
import numpy as np


class Dots(Ambient):
    def __init__(self, matrix, parent):
        super(Dots, self).__init__(matrix, parent)

        self.active_dot = [10, 10]
        self.active_dot_dest_size = 5
        self.active_dot_size = 0
        self.h = 0.42

    def loop(self):

        if self.active_dot_size > 0:
            for i in range(0, self.active_dot_size):
                for n in range(0, 360):
                    s = math.sin((n / 360.) * (math.pi * 2))
                    c = math.cos((n / 360.) * (math.pi * 2))
                    x = int(self.active_dot[0] + (i * c))
                    y = int(self.active_dot[1] + (i * s))
                    if x >= 0 and x < 35:
                        if y >= 0 and y < 20:
                            a = i / float(self.active_dot_dest_size)
                            dot_color = np.array(tuple(map(lambda x: int(x * 255), colorsys.hsv_to_rgb(self.h, 1, a))))
                            self.frame[y, x] = dot_color
        if self.active_dot_size < self.active_dot_dest_size:
            self.active_dot_size += 1
        else:
            self.active_dot_dest_size = random.randint(0, 10)
            self.active_dot_size = 0
            self.active_dot = [random.randint(0, 34), random.randint(0, 19)]
            self.h = random.randint(0, 255) / 255.

        if self.is_key_up("B"):
            self.parent.back()
