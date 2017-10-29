from clock import Clock
from GameOfLife import GameOfLife
from dots import Dots
from telegram_ambient import Telegram

apps = {
    "Clock": Clock,
    "GOL": GameOfLife,
    "Tele": Telegram,
    "Dots": Dots
}

standby_apps = [
    Clock,
    GameOfLife,
    Dots
]
