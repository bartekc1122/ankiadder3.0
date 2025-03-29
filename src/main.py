import os
import logging
from anki_adder import AnkiAdder
from colorlog import ColoredFormatter

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)

log_format = "%(asctime)s - %(name)-20s - %(levelname)-5s - %(message)s"
color_format = "%(log_color)s" + log_format

color_formatter = ColoredFormatter(
    color_format,
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)

file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
file_handler.setFormatter(logging.Formatter(log_format))

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(color_formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler])
log = logging.getLogger(__name__)

log.info("Launching AnkiAdder.")
app = AnkiAdder()
