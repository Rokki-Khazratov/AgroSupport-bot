# 📱 Настройка функции скачивания APK

Это руководство поможет настроить функцию скачивания APK файла через бота.

## 📋 Содержание

1. [Обзор](#обзор)
2. [Метод 1: Через file_id (рекомендуется)](#метод-1-через-file_id-рекомендуется)
3. [Метод 2: Локальный файл](#метод-2-локальный-файл)
4. [Обновление версии APK](#обновление-версии-apk)
5. [Решение проблем](#решение-проблем)

---

## Обзор

Бот поддерживает два метода отправки APK файла пользователям:

1. **file_id (рекомендуется)** - быстрый, не нагружает сервер
2. **Локальный файл** - fallback метод, если file_id недоступен

### Преимущества file_id:

- ✅ Мгновенная отправка (файл уже на серверах Telegram)
- ✅ Не нагружает сервер
- ✅ Работает с файлами любого размера (до 2GB)
- ✅ Не нужно хранить APK в git репозитории

---

## Метод 1: Через file_id (рекомендуется)

### Шаг 1: Подготовка

1. Убедитесь, что в `.env` файле указан ваш `ADMIN_ID`:

```env
ADMIN_ID=your_telegram_user_id
```

Получить свой ID можно:
- Отправив `/start` боту [@userinfobot](https://t.me/userinfobot)
- Или через команду `/getid` в вашем боте

### Шаг 2: Загрузка APK и получение file_id

1. **Откройте личную переписку** с вашим ботом
2. **Отправьте APK файл** боту как документ
3. **Бот автоматически ответит** с информацией о файле и file_id:

```
📎 Hujjat haqida ma'lumot

📄 Fayl nomi: geoagro.apk
📦 Hajmi: 60.25 MB

🆔 File ID:
BQACAgIAAxkBAAIB...

💾 Serverdagi .env ga qo'shing:
APK_FILE_ID=BQACAgIAAxkBAAIB...

🔄 Keyin botni qayta ishga tushiring:
systemctl restart agro-bot
```

4. **Скопируйте file_id** из ответа бота

### Шаг 3: Настройка на сервере

1. Подключитесь к серверу:

```bash
ssh user@your-server.com
```

2. Откройте `.env` файл:

```bash
cd /root/projects/geoagro/support-bot/AgroSupport-bot
nano .env
```

3. Добавьте или обновите строку:

```env
APK_FILE_ID=BQACAgIAAxkBAAIB...  # вставьте ваш file_id
APK_VERSION=2.2.0  # укажите версию
```

4. Сохраните файл (Ctrl+X, затем Y, затем Enter)

5. Перезапустите бота:

```bash
systemctl restart agro-bot
```

6. Проверьте статус:

```bash
systemctl status agro-bot
```

### Шаг 4: Тестирование

1. Откройте бота в Telegram
2. Отправьте `/start`
3. Нажмите кнопку "📱 Yuklab olish v2.2.0"
4. Проверьте, что APK успешно отправляется

✅ **Готово!** Пользователи теперь могут скачивать APK через бота.

---

## Метод 2: Локальный файл

Этот метод используется как fallback, если file_id не указан или недоступен.

### Шаг 1: Загрузка APK на сервер

1. Создайте папку для APK:

```bash
mkdir -p /root/projects/geoagro/support-bot/apk
```

2. Загрузите APK файл на сервер (через scp, ftp или wget):

```bash
# Пример через scp (с локального компьютера)
scp /path/to/geoagro.apk user@server:/root/projects/geoagro/support-bot/apk/

# Или через wget (если файл доступен по ссылке)
cd /root/projects/geoagro/support-bot/apk
wget https://example.com/geoagro.apk
```

3. Переименуйте файл для единообразия:

```bash
cd /root/projects/geoagro/support-bot/apk
mv your-apk-file.apk geoagro.apk
```

### Шаг 2: Настройка `.env`

```env
APK_PATH=/root/projects/geoagro/support-bot/apk/geoagro.apk
APK_VERSION=2.2.0
```

### Шаг 3: Перезапуск бота

```bash
systemctl restart agro-bot
```

### ⚠️ Ограничения локального метода:

- Максимальный размер файла: **50 MB**
- Медленнее, чем file_id
- Нагружает сервер при каждой отправке

Если ваш APK больше 50MB, используйте **Метод 1 (file_id)**.

---

## Обновление версии APK

### Сценарий: Вышла новая версия (например, v2.3.0)

#### Если используете file_id:

1. **Отправьте новый APK боту** (от имени админа)
2. **Скопируйте новый file_id** из ответа бота
3. **Обновите `.env` на сервере**:

```bash
nano .env
```

Измените:

```env
APK_FILE_ID=новый_file_id_здесь
APK_VERSION=2.3.0
```

4. **Перезапустите бота**:

```bash
systemctl restart agro-bot
```

✅ Готово! Пользователи увидят кнопку "📱 Yuklab olish v2.3.0"

#### Если используете локальный файл:

1. **Загрузите новый APK на сервер**:

```bash
scp /path/to/new-geoagro.apk user@server:/root/projects/geoagro/support-bot/apk/geoagro.apk
```

2. **Обновите версию в `.env`**:

```env
APK_VERSION=2.3.0
```

3. **Перезапустите бота**:

```bash
systemctl restart agro-bot
```

---

## Решение проблем

### Проблема: Бот не отправляет APK

#### Проверка 1: Логи бота

```bash
journalctl -u agro-bot -f
```

Ищите ошибки при попытке скачивания.

#### Проверка 2: file_id действителен

File_id может устареть. Попробуйте:

1. Отправить APK боту заново
2. Получить новый file_id
3. Обновить в `.env`

#### Проверка 3: Локальный файл существует

```bash
ls -lh /root/projects/geoagro/support-bot/apk/geoagro.apk
```

Если файл не найден, загрузите его по [Методу 2](#метод-2-локальный-файл).

### Проблема: APK больше 50MB и file_id не работает

**Решение:** Используйте Telegram Desktop для загрузки:

1. Откройте бота в Telegram Desktop (поддерживает файлы до 2GB)
2. Отправьте APK боту
3. Скопируйте file_id из ответа
4. Используйте этот file_id в `.env`

### Проблема: Пользователь не видит кнопку "Yuklab olish"

**Решение:**

1. Проверьте, что `APK_VERSION` указана в `.env`
2. Перезапустите бота: `systemctl restart agro-bot`
3. Попросите пользователя отправить `/start` заново

### Проблема: Кнопка есть, но при нажатии ничего не происходит

**Решение:**

1. Проверьте логи: `journalctl -u agro-bot -f`
2. Убедитесь, что `APK_FILE_ID` или `APK_PATH` правильно настроены
3. Попробуйте отправить APK боту заново для получения нового file_id

---

## 📊 Мониторинг скачиваний

Все скачивания логируются в файл `downloads.log`:

```bash
cat /root/projects/geoagro/support-bot/AgroSupport-bot/downloads.log
```

Формат записи:

```
2025-10-06 08:30:15 | 123456789 | John Doe | @johndoe | v2.2.0
2025-10-06 09:15:42 | 987654321 | Jane Smith | @janesmith | v2.2.0
```

### Статистика скачиваний:

```bash
# Всего скачиваний
wc -l downloads.log

# Скачивания за сегодня
grep "$(date +%Y-%m-%d)" downloads.log | wc -l

# Самая популярная версия
awk -F'|' '{print $5}' downloads.log | sort | uniq -c | sort -rn
```

---

## 🔐 Безопасность

### Рекомендации:

1. **Не добавляйте APK в git** - файл игнорируется через `.gitignore`
2. **Храните file_id в .env** - не коммитьте его в репозиторий
3. **Используйте ADMIN_ID** - только вы сможете получать file_id
4. **Регулярно обновляйте** - следите за безопасностью приложения

---

## 📞 Поддержка

Если возникли вопросы или проблемы:

1. Проверьте [Решение проблем](#решение-проблем)
2. Посмотрите логи: `journalctl -u agro-bot -f`
3. Проверьте конфигурацию: `cat .env`

---

## 🎯 Чек-лист настройки

- [ ] ADMIN_ID указан в `.env`
- [ ] APK отправлен боту от админа
- [ ] file_id получен и добавлен в `.env`
- [ ] APK_VERSION указана в `.env`
- [ ] Бот перезапущен: `systemctl restart agro-bot`
- [ ] Статус проверен: `systemctl status agro-bot`
- [ ] Протестировано: `/start` → кнопка "Yuklab olish" → APK отправлен
- [ ] downloads.log создан и пишется

✅ Все пункты выполнены = Функция работает!

