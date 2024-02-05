import logging
import logging.config
import json
import subprocess
with open('logging_config.json', 'r') as config_file:
    config = json.load(config_file)

logging.config.dictConfig(config)

# Пример использования
logger = logging.getLogger(__name__)


def adb_server_start():
    try:
        subprocess.run('adb start-server')
        logger.debug("Запуск сервера")
    except subprocess.CalledProcessError as error:
        logger.error(f"Ошибка команды \"adb start-server\". Код ошибки : {error}")

def adb_server_kill():
    try:
        subprocess.run('adb kill-server')
        logger.debug("Остановка сервера")
    except subprocess.CalledProcessError as error:
        logger.error(f"Ошибка команды \"adb kill-server\". Код ошибки : {error}")

def adb_server_restart():
    adb_server_start()
    adb_server_kill()

logger.debug("This is a debug message")
