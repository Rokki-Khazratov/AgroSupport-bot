import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Основные настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_GROUP_ID = os.getenv('ADMIN_GROUP_ID')

# Автоматически форматируем ID группы для Telegram
if ADMIN_GROUP_ID:
    print(f"🔍 Исходный ID: {ADMIN_GROUP_ID}")
    
    # Если ID уже начинается с минуса, оставляем как есть
    if ADMIN_GROUP_ID.startswith('-'):
        print(f"✅ ID уже правильно отформатирован")
    else:
        # Добавляем минус для обычных групп
        ADMIN_GROUP_ID = f"-{ADMIN_GROUP_ID}"
        print(f"✅ Добавлен минус для обычной группы: {ADMIN_GROUP_ID}")
    
    # Дополнительная проверка - если группа была обновлена до супергруппы
    print(f"⚠️  Если группа была обновлена до супергруппы, используйте команду /getid в группе для получения нового ID")

# Проверка обязательных переменных окружения
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN muhit o'zgaruvchilarida topilmadi. env.example asosida .env fayl yarating")

if not ADMIN_GROUP_ID:
    raise ValueError("ADMIN_GROUP_ID muhit o'zgaruvchilarida topilmadi. env.example asosida .env fayl yarating")

# Дополнительные настройки
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# APK настройки
APK_FILE_ID = os.getenv('APK_FILE_ID')  # file_id из Telegram (приоритетный метод)
APK_VERSION = os.getenv('APK_VERSION', '2.2.0')  # Версия APK
APK_PATH = os.getenv('APK_PATH', '/root/projects/geoagro/support-bot/apk/geoagro.apk')  # Путь к локальному файлу (fallback)
ADMIN_ID = os.getenv('ADMIN_ID')  # ID главного администратора для получения file_id

# Выводим финальный ID группы для отладки
print(f"🔧 Сконфигурированный ADMIN_GROUP_ID: {ADMIN_GROUP_ID}")
print(f"📱 APK версия: {APK_VERSION}")
