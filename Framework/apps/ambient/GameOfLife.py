import random
import numpy as np
import time
import colorsys

from apps.ambient import Ambient

class GameOfLife(Ambient):
    def __init__(self, matrix, parent):
        super(GameOfLife, self).__init__(matrix, parent)

        self.nullhash = hash(str(np.zeros((20, 35))))
        self.pop = np.random.randint(0, 2, (20, 35))
        self.show_pop(self.pop, (0, 0, 0))
        self.lastten = []
        self.h = 0

    def show_pop(self, pop, c):
        tmp = (pop[..., None] * c)
        self.frame = tmp

    def do_life(self, pop):
        sr, sm, sl = (slice(1, None), slice(0, None), slice(0, -1))
        slices = [(sl, sl), (sl, sm), (sl, sr),
                  (sm, sl), (sm, sr),
                  (sr, sl), (sr, sm), (sr, sr)]
        nbr = np.zeros_like(pop)
        nbr[sl, sl] += pop[sr, sr]
        nbr[sl, sm] += pop[sr, sm]
        nbr[sl, sr] += pop[sr, sl]
        nbr[sm, sl] += pop[sm, sr]
        nbr[sm, sr] += pop[sm, sl]
        nbr[sr, sl] += pop[sl, sr]
        nbr[sr, sm] += pop[sl, sm]
        nbr[sr, sr] += pop[sl, sl]
        born = (nbr == 3) & (pop == 0)
        notdied = (nbr > 1) & (nbr < 4)
        pop &= notdied
        pop |= born

    def generation(self):
        self.h = (self.h + 1) % 255
        c = tuple(map(lambda x: int(x * 255), colorsys.hsv_to_rgb(self.h / 255., 1, 1)))
        self.do_life(self.pop)
        self.show_pop(self.pop, c)
        self.lastten.append(hash(str(self.pop)))
        if len(self.lastten) > 15:
            self.lastten.pop(0)
        if hash(str(self.pop)) in self.lastten[:-1]:
            rx = random.randint(1, self.pop.shape[1] - 1)
            ry = random.randint(1, self.pop.shape[0] - 1)
            self.pop[ry, rx] = 1 - self.pop[ry, rx]
            print "spawned new"
        if sum(map(sum, self.pop)) < 10:
            self.pop = np.random.randint(0, 2, (20, 35))
        time.sleep(0.1)

    def loop(self):
        self.generation()
        if self.last_keys_down["B"] and not self.keys_down["B"]:
            self.parent.back()