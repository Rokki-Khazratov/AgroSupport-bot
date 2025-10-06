# AgroSupport Bot

Telegram бот для приема заявок от пользователей с автоматической пересылкой в группу администраторов и системой ответов.

## 🎯 Функциональность

### Для пользователей:
- 📝 Создание заявок любым сообщением
- ✅ Подтверждение получения заявки
- 📊 Проверка статуса заявки
- 💬 Получение ответов от администраторов

### Для администраторов:
- 📨 Получение всех заявок в группе
- 💬 Ответ через reply на сообщение заявки
- 🔄 Автоматическая пересылка ответа пользователю
- 📊 Управление статусами заявок

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Rokki-Khazratov/AgroSupport-bot.git
cd AgroSupport-bot
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка конфигурации
```bash
cp env.example .env
```

Отредактируйте файл `.env`:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_GROUP_ID=your_admin_group_id_here
DATABASE_URL=sqlite:///support_bot.db
```

### 4. Получение токена бота
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env`

### 5. Настройка группы администраторов
1. Создайте группу в Telegram
2. Добавьте бота в группу как администратора
3. Получите ID группы (можно через [@userinfobot](https://t.me/userinfobot))
4. Добавьте ID группы в `.env`

### 6. Запуск бота
```bash
python main.py
```

## 📁 Структура проекта

```
agro-support-leads/
├── main.py                    # Основной файл бота
├── config.py                  # Конфигурация
├── database.py                # Работа с БД
├── handlers/
│   ├── user_handlers.py       # Обработчики для пользователей
│   └── admin_handlers.py      # Обработчики для админов
├── middleware/
│   └── database_middleware.py # Middleware для БД
├── models/
│   └── ticket.py              # Модель заявки
├── utils/
│   └── formatters.py          # Форматирование сообщений
├── requirements.txt
├── .env
└── README.md
```

## 🗄️ База данных

Бот использует SQLite базу данных с двумя основными таблицами:

- **tickets** - заявки пользователей
- **replies** - ответы администраторов

## 💻 Команды

### Для пользователей:
- `/start` - приветствие и инструкции
- `/help` - справка по использованию
- `/status` - статус последней заявки
- Любое сообщение - создание заявки

### Для администраторов (в группе):
- Reply на сообщение заявки - ответ пользователю
- `/close <номер_заявки>` - закрыть заявку
- `/stats` - статистика заявок

## 🔧 Разработка

### Установка для разработки
```bash
git clone https://github.com/Rokki-Khazratov/AgroSupport-bot.git
cd AgroSupport-bot
pip install -r requirements.txt
cp env.example .env
# Настройте .env файл
python main.py
```

### Логирование
Логи сохраняются в файл `bot.log` и выводятся в консоль.

## 📝 Лицензия

MIT License

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📞 Поддержка

Если у вас есть вопросы или проблемы, создайте issue в GitHub репозитории.
