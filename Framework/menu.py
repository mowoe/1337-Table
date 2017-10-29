import numpy as np
import time
from font import font_5x3
import random
import colorsys
from bresenham import bresenham
import telegram
from telegram.error import NetworkError, Unauthorized
import threading
import subprocess
from PIL import Image

theme = {
    "header": (0, 255, 255),
    "text": (0, 127, 255),
    "elements": (0, 127, 255),
    "background": (0, 0, 0),
    "snake_food": (255, 0, 0),
    "snake_snake": (255, 255, 255),
    "snake_background": (0, 0, 0),
    "snake_lose": (255, 0, 0),
    "snake_welcome": (0, 255, 0),
    "pong_paddle": (255, 255, 255),
    "pong_ball": (255, 0, 0),
    "clock_color": (127, 255, 0),
}


class TelegramBotThread(threading.Thread):
    def __init__(self, parent):
        super(TelegramBotThread, self).__init__()
        self.daemon = True

        self.parent = parent

        # self.bot = telegram.Bot('357068228:AAHZmriAYgH1ywcFX4JOuOEp5t7BZFFzZ1U')
        self.bot = telegram.Bot('453991406:AAG_pYzmFSQT4gYnAcI4GNECMGXd0ZXlyYo')  # Backup
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None

    def echo(self):
        for update in self.bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1
            if update.message:
                if len(update.message.photo) > 0:
                    self.parent.new_photo = True
                    photo_file = self.bot.get_file(update.message.photo[-1].file_id)
                    self.parent.photo = photo_file["file_path"]
                else:
                    self.parent.new_text = True
                    self.parent.text = update.message.text.strip()

    def run(self):
        while 1:
            try:
                self.echo()
            except NetworkError:
                time.sleep(1)
            except Unauthorized:
                self.update_id += 1


class Telegram(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

        self.last_text = self.text = ""
        self.new_text = self.new_photo = False
        self.photo = ""
        self.show_mode = "text"
        self.actual_render = self.frame
        self.shift = 0
        self.imshowframe = np.zeros((20, 35, 3), np.uint8)

        self.bot = TelegramBotThread(self)
        self.bot.start()

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

        if self.keys_down["B"] and not self.last_keys_down["B"]: pass

        if len(self.text) > 0:
            self.frame = np.zeros((20, 35, 3), np.uint8)

            if self.new_text:
                if len(self.text) >= 9:
                    self.text += "  --  "
                self.actual_render = np.zeros((20, 4 * len(self.text), 3), np.uint8)
                render_text(self.actual_render, (255, 255, 255), (0, 0, 0), self.text, 1, 8)
                self.new_text = False
                self.show_mode = "text"
            elif self.new_photo:
                self.new_photo = False
                self.show_mode = "photo"
                ext = self.photo.split(".")[-1]
                print "started download"
                if subprocess.call(["wget", "-O", "/tmp/image.%s" % ext, self.photo]) == 0:
                    print "finished download"
                    im = Image.open("/tmp/image.%s" % ext)
                    im.thumbnail((35, 20), Image.ANTIALIAS)
                    data = list(im.getdata())
                    width, height = im.size
                    tmp = np.zeros((height, width, 3))
                    i = 0
                    for y in range(0, height):
                        for x in range(0, width):
                            tmp[y, x] = data[i]
                            i += 1
                    self.imshowframe = np.zeros((20, 35, 3), dtype=np.uint8)
                    x = (35 / 2) - (width / 2)
                    y = (20 / 2) - (height / 2)
                    print tmp.shape
                    self.imshowframe[y:y+height, x:x+width] = np.uint8(tmp)
                else:
                    self.show_mode = ""
                    self.text = "Failed to show image"
                    self.new_text = True

            if self.show_mode == "text":
                if self.actual_render.shape[1] <= 35:
                    x = (35 / 2) - (self.actual_render.shape[1] / 2)
                    self.frame[0:20, x:x + self.actual_render.shape[1]] = self.actual_render
                else:
                    self.frame = np.zeros((20, 35, 3), np.uint8)
                    self.frame[0:20, 0:35] = self.actual_render[0:20, 0:35]
                    self.actual_render = np.roll(self.actual_render, -1, 1)
                    time.sleep(0.1)

            if self.show_mode == "photo":
                self.frame = np.zeros((20, 35, 3), np.uint8)
                self.frame = np.array(self.imshowframe)
                time.sleep(0.1)



        time.sleep(0.03)

    def get_self_frame(self):
        return self.frame


class Clock(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down
        t = time.localtime()
        "%02d:%02d" % (t.tm_hour, t.tm_min)

        if self.keys_down["B"] and not self.last_keys_down["B"]: self.parent.back()
        time.sleep(0.03)

    def get_self_frame(self):
        return self.frame


class Settings(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

        self.options = {
            "Invert": self.matrix.do_invert,
            "Flip": self.matrix.do_flip,
            "Menu": self.parent.back
        }

        self.keys = self.options.keys()
        self.index = 0

    def self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

        self.frame = np.zeros((20, 35, 3), np.uint8) + theme["background"]
        render_text(self.get_frame(), theme["header"], theme["background"], "Settings", 0, 0)
        render_text(self.get_frame(), theme["text"], theme["background"], self.keys[self.index], 2, 8)
        a = "<"
        b = ">"
        if self.index == 0:
            a = " "
        if self.index == len(self.keys) - 1:
            b = " "
        render_text(self.frame, theme["elements"], theme["background"], "%s      %s" % (a, b), 2, 14)

        if self.keys_down["LEFT"] and not self.last_keys_down["LEFT"]:
            if self.index > 0:
                self.index -= 1

        if self.keys_down["RIGHT"] and not self.last_keys_down["RIGHT"]:
            if self.index < len(self.keys) - 1:
                self.index += 1

        if self.keys_down["A"] and not self.last_keys_down["A"]:
            self.options[self.keys[self.index]]()

    def get_frame(self):
        return self.frame


class GameOfLife(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

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

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down
        self.generation()
        if self.keys_down["B"] and not self.last_keys_down["B"]:
            self.parent.back()
        time.sleep(0.03)

    def get_self_frame(self):
        return self.frame


class Pong(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

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

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

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

        time.sleep(0.03)

    def get_self_frame(self):
        return self.frame


class Ambient(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

        self.games = {
            "menu": None,
            "GoL": GameOfLife,
            "Tele": Telegram
        }
        self.keys = self.games.keys()
        self.index = 0

        self.active = self

    def back(self):
        self.active = self

    def self_update(self, keys_down):
        self.active.self_self_update(keys_down)

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

        self.frame = np.zeros((20, 35, 3), np.uint8) + theme["background"]
        render_text(self.get_frame(), theme["header"], theme["background"], "Ambient", 0, 0)
        render_text(self.get_frame(), theme["text"], theme["background"], self.keys[self.index], 2, 8)
        a = "<"
        b = ">"
        if self.index == 0:
            a = " "
        if self.index == len(self.keys) - 1:
            b = " "
        render_text(self.frame, (0, 127, 200), (0, 0, 0), "%s      %s" % (a, b), 2, 14)
        if self.keys_down["LEFT"] and not self.last_keys_down["LEFT"]:
            if self.index > 0:
                self.index -= 1

        if self.keys_down["RIGHT"] and not self.last_keys_down["RIGHT"]:
            if self.index < len(self.keys) - 1:
                self.index += 1

        if self.keys_down["A"] and not self.last_keys_down["A"]:
            if not self.keys[self.index] == "menu":
                self.active = self.games[self.keys[self.index]](self.matrix, self)
            else:
                self.parent.back()

        time.sleep(0.05)

    def get_self_frame(self):
        return self.frame

    def get_frame(self):
        return self.active.get_self_frame()


class Snake(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

        self.particle = [random.randint(0, 34), random.randint(0, 19)]
        self.snake = [[random.randint(0, 34), random.randint(0, 19)]]
        self.direction = [1, 0]
        random.shuffle(self.direction)
        self.length = 3
        self.ingame = False
        self.firstrun = True

    def self_self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

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

            time.sleep(0.1)

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
            if self.keys_down["B"] and not self.last_keys_down["B"]:
                self.parent.back()

    def get_self_frame(self):
        return self.frame


class Games(object):
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

        self.games = {
            "menu": None,
            "snake": Snake,
            "pong": Pong,
        }
        self.keys = self.games.keys()
        self.index = 0

        self.active = self

    def back(self):
        self.active = self

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
        render_text(self.frame, (0, 127, 200), (0, 0, 0), "%s      %s" % (a, b), 2, 14)

        if self.keys_down["LEFT"] and not self.last_keys_down["LEFT"]:
            if self.index > 0:
                self.index -= 1

        if self.keys_down["RIGHT"] and not self.last_keys_down["RIGHT"]:
            if self.index < len(self.keys) - 1:
                self.index += 1

        if self.keys_down["A"] and not self.last_keys_down["A"]:
            if not self.keys[self.index] == "menu":
                self.active = self.games[self.keys[self.index]](self.matrix, self)
            else:
                self.parent.back()

        time.sleep(0.05)

    def get_self_frame(self):
        return self.frame

    def get_frame(self):
        return self.active.get_self_frame()


class Menu(object):
    def __init__(self, matrix):
        self.matrix = matrix

        self.frame = np.zeros((20, 35, 3), np.uint8)

        self.points = {
            "Settings": Settings(self.matrix, self),
            "Games": Games(self.matrix, self),
            "Ambient": Ambient(self.matrix, self)
        }

        self.keys = self.points.keys()
        self.index = 0
        self.active = self

        self.keys_down = self.matrix.get_keys()
        self.last_keys_down = self.keys_down

    def back(self):
        self.active = self

    def self_update(self, keys_down):
        self.last_keys_down = self.keys_down
        self.keys_down = keys_down

        self.frame = np.zeros((20, 35, 3), np.uint8) + theme["background"]
        render_text(self.get_frame(), theme["header"], theme["background"], "1337Table", 0, 0)
        render_text(self.get_frame(), theme["text"], theme["background"], self.keys[self.index], 2, 8)
        a = "<"
        b = ">"
        if self.index == 0:
            a = " "
        if self.index == len(self.keys) - 1:
            b = " "
        render_text(self.frame, (0, 127, 200), (0, 0, 0), "%s      %s" % (a, b), 2, 14)

        if self.keys_down["LEFT"] and not self.last_keys_down["LEFT"]:
            if self.index > 0:
                self.index -= 1

        if self.keys_down["RIGHT"] and not self.last_keys_down["RIGHT"]:
            if self.index < len(self.keys) - 1:
                self.index += 1

        if self.keys_down["A"] and not self.last_keys_down["A"]:
            self.active = self.points[self.keys[self.index]]

        time.sleep(0.05)

    def get_frame(self):
        return self.frame

    def draw(self):
        self.matrix.set_frame(self.active.get_frame())
        # time.sleep(0.05)

    def update(self, keys_down):
        self.active.self_update(keys_down)


def render_text(frame, color, background, text, x, y, font=font_5x3):
    text = text.upper()
    f_w = font["PROP"]["width"]
    f_h = font["PROP"]["height"]

    for char in text:
        if not char in font.keys():
            char = " "
        for y_ in range(0, f_h):
            for x_ in range(0, f_w):
                frame[y + y_, x + x_] = background
                if font[char][y_][x_]:
                    frame[y + y_, x + x_] = color
        x += 4


if __name__ == "__main__":
    import matrix

    matrix = matrix.MatrixSimulator()

    menu = Menu(matrix)

    while 1:
        menu.update(matrix.get_keys())
        menu.draw()
