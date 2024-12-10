import logging
from os import path
from datetime import datetime


log_file_path = path.abspath(f'logs/{datetime.now().strftime("%Y-%m-%d")}.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file_path
)
