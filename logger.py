import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class ColoredFormatter(logging.Formatter):
    """Форматтер с цветными логами для консоли"""

    # ANSI цвета
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[31m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        # Добавляем цвет к уровню логирования
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname[:3]}{self.RESET}"
        return super().format(record)


def setup_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Избегаем дублирования handlers при повторном вызове
    if logger.handlers:
        return logger

    # Формат логов
    log_format = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    date_format = "%d.%m.%Y %H:%M:%S"

    # В зависимости от окружения, где мы запускаем бота, будем выводить логи в файл или в консоль
    match os.getenv("ENV", "local"):
        case "prod" | "dev":
            # Создаем директорию logs если её нет
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)

            # Создаем имя файла с датой и временем запуска
            start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = logs_dir / f"{start_time}.log"

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_formatter = logging.Formatter(log_format, datefmt=date_format)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        case _:
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = ColoredFormatter(log_format, datefmt=date_format)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

    return logger
