import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Основные настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_GROUP_ID = os.getenv('ADMIN_GROUP_ID')

# Автоматически форматируем ID группы для Telegram
if ADMIN_GROUP_ID:
    # Убираем минус если есть
    clean_id = ADMIN_GROUP_ID.lstrip('-')
    
    # Проверяем длину ID
    if len(clean_id) == 10:  # Обычная группа
        ADMIN_GROUP_ID = f"-{clean_id}"
    elif len(clean_id) == 13:  # Супергруппа
        ADMIN_GROUP_ID = f"-100{clean_id}"
    else:
        # Если уже правильно отформатирован, оставляем как есть
        pass

# Проверка обязательных переменных окружения
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения. Создайте .env файл на основе env.example")

if not ADMIN_GROUP_ID:
    raise ValueError("ADMIN_GROUP_ID не найден в переменных окружения. Создайте .env файл на основе env.example")

# Дополнительные настройки
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Выводим финальный ID группы для отладки
print(f"🔧 Сконфигурированный ADMIN_GROUP_ID: {ADMIN_GROUP_ID}")
