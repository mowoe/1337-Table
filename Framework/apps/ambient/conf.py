from Framework.apps.ambient.clock import Clock
from Framework.apps.ambient.GameOfLife import GameOfLife
from Framework.apps.ambient.dots import Dots
from Framework.apps.ambient.telegram_ambient import Telegram

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
