import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Основные настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_GROUP_ID = os.getenv('ADMIN_GROUP_ID')

# Автоматически добавляем минус для ID группы если его нет
if ADMIN_GROUP_ID and not ADMIN_GROUP_ID.startswith('-'):
    ADMIN_GROUP_ID = f"-{ADMIN_GROUP_ID}"

# Проверка обязательных переменных окружения
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения. Создайте .env файл на основе env.example")

if not ADMIN_GROUP_ID:
    raise ValueError("ADMIN_GROUP_ID не найден в переменных окружения. Создайте .env файл на основе env.example")

# Дополнительные настройки
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
