from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.utils.markdown import hbold, hitalic
from datetime import datetime

from config import ADMIN_GROUP_ID, APK_VERSION, ADMIN_ID

router = Router()


def get_main_keyboard():
    """Создает основную клавиатуру с кнопками"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📞 Qo'llab-quvvatlash",
                callback_data="support"
            ),
            InlineKeyboardButton(
                text=f"📱 Yuklab olish v{APK_VERSION}",
                callback_data="download_apk"
            )
        ]
    ])
    return keyboard


@router.message(CommandStart())
async def start_handler(message: Message):
    """Обработчик команды /start - показывает главное меню"""
    welcome_text = (
        f"👋 {hbold('GeoAgro Support Bot ga xush kelibsiz!')}\n\n"
        f"Kerakli bo'limni tanlang:"
    )
    
    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@router.message(Command("menu"))
async def menu_handler(message: Message):
    """Обработчик команды /menu - показывает главное меню"""
    menu_text = (
        f"📋 {hbold('Asosiy menyu')}\n\n"
        f"Kerakli bo'limni tanlang:"
    )
    
    await message.answer(menu_text, reply_markup=get_main_keyboard())


@router.message(Command("getid"))
async def get_id_handler(message: Message):
    """Обработчик команды /getid - показывает ID чата"""
    chat_id = message.chat.id
    chat_type = message.chat.type
    
    await message.answer(
        f"🆔 <b>Chat haqida ma'lumot:</b>\n\n"
        f"📊 <b>Turi:</b> {chat_type}\n"
        f"🆔 <b>ID:</b> <code>{chat_id}</code>\n\n"
        f"💡 <i>Bot sozlash uchun bu ID ni nusxalang</i>",
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def help_handler(message: Message):
    """Обработчик команды /help"""
    help_text = (
        f"📚 {hbold('Bot ishlatish bo' + chr(39) + 'yicha yordam')}\n\n"
        f"🎫 {hbold('Ariza qanday yaratish:')}\n"
        f"• Bot ga har qanday xabar yuboring\n"
        f"• Muammoingiz yoki savolingizni tasvirlab bering\n"
        f"• Rasmlar va hujjatlarni biriktirish mumkin\n\n"
        f"📊 {hbold('Buyruqlar:')}\n"
        f"• /start - asosiy menyu\n"
        f"• /menu - menyuni qayta ochish\n"
        f"• /help - bu yordam\n\n"
        f"📱 {hbold('Ilova yuklab olish:')}\n"
        f"• /start yoki /menu buyrug'ini yuboring\n"
        f"• " + chr(34) + "Yuklab olish" + chr(34) + " tugmasini bosing\n\n"
        f"⏰ {hbold('Javob vaqti:')}\n"
        f"• Odatda 24 soat ichida javob beramiz\n"
        f"• Favqulodda holatlarda - tezroq\n\n"
        f"❓ {hitalic('Savollar bormi? Xabar yuboring!')}"
    )
    
    await message.answer(help_text)


@router.message(F.document, F.chat.type == "private")
async def handle_document_from_admin(message: Message):
    """Обработчик документов от админа - показывает file_id для APK"""
    
    # Проверяем, что это админ
    if not ADMIN_ID or str(message.from_user.id) != str(ADMIN_ID):
        return  # Не обрабатываем, пройдет в create_ticket_handler
    
    # Получаем информацию о документе
    document = message.document
    file_name = document.file_name
    file_size_mb = document.file_size / (1024 * 1024)
    file_id = document.file_id
    
    response_text = (
        f"📎 {hbold('Hujjat haqida ma' + chr(39) + 'lumot')}\n\n"
        f"📄 {hbold('Fayl nomi:')} {file_name}\n"
        f"📦 {hbold('Hajmi:')} {file_size_mb:.2f} MB\n\n"
        f"🆔 {hbold('File ID:')}\n"
        f"<code>{file_id}</code>\n\n"
        f"💾 {hitalic('Serverdagi .env ga qo' + chr(39) + 'shing:')}\n"
        f"<code>APK_FILE_ID={file_id}</code>\n\n"
        f"🔄 {hitalic('Keyin botni qayta ishga tushiring:')}\n"
        f"<code>systemctl restart agro-bot</code>"
    )
    
    await message.answer(response_text, parse_mode="HTML")
    
    print(f"📋 Admin {message.from_user.id} dan file_id olindi: {file_id}")
    print(f"📄 Fayl: {file_name} ({file_size_mb:.2f} MB)")


@router.message(F.media_group_id)
async def handle_media_group_handler(message: Message, bot):
    """Обработчик медиагрупп (несколько медиафайлов в одном сообщении)"""
    
    # Обрабатываем только сообщения из личных чатов (не из групп)
    if message.chat.type != 'private':
        return
    
    # Игнорируем команды
    if message.text and message.text.startswith('/'):
        return
    
    print(f"🔍 Получена медиагруппа от пользователя {message.from_user.id}")
    
    # Для медиагрупп просто пересылаем все файлы
    user = message.from_user
    user_id = user.id
    user_name = user.full_name or "Неизвестно"
    user_username = user.username or ""
    
    # Формируем информацию о пользователе
    if user_username:
        user_info = f"{user_name} (@{user_username}) ID: {user_id}"
    else:
        user_info = f"{user_name} (ID: {user_id})"
    
    try:
        # Отправляем уведомление о медиагруппе
        group_message = (
            f"🎫 <b>Yangi ariza (Media guruhi)</b>\n\n"
            f"👤 <b>Foydalanuvchi:</b> {user_info}\n"
            f"⏰ <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            f"📎 <b>Media fayllar:</b> Fayllar guruhi\n\n"
            f"💬 <i>Foydalanuvchiga javob berish uchun bu xabarga javob bering</i>"
        )
        
        sent_message = await bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=group_message,
            parse_mode="HTML"
        )
        
        # Пересылаем медиагруппу
        await bot.forward_message(
            chat_id=ADMIN_GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        
        # Отправляем подтверждение пользователю
        await message.answer(
            f"✅ {hbold('Media guruhi yuborildi!')}\n\n"
            f"📎 {hbold('Sizning fayllaringiz:')} Media fayllar guruhi\n\n"
            f"⏳ {hitalic('Biz sizning fayllaringizni oldik va tez orada javob beramiz!')}",
            parse_mode="HTML"
        )
        
    except Exception as e:
        print(f"❌ Ошибка обработки медиагруппы: {e}")
        await message.answer(
            f"⚠️ {hbold('Ошибка при отправке медиагруппы')}\n\n"
            f"❌ Не удалось отправить файлы в группу поддержки.\n"
            f"Попробуйте отправить файлы по одному."
        )


@router.message(F.text | F.photo | F.document | F.video | F.audio | F.voice | F.video_note | F.sticker)
async def create_ticket_handler(message: Message, bot):
    """Обработчик создания заявки от пользователя"""
    
    # Обрабатываем только сообщения из личных чатов (не из групп)
    if message.chat.type != 'private':
        return
    
    # Игнорируем команды (они обрабатываются отдельно)
    if message.text and message.text.startswith('/'):
        return
    user = message.from_user
    user_id = user.id
    user_name = user.full_name or "Неизвестно"
    user_username = user.username or ""
    
    # Формируем текст заявки в зависимости от типа сообщения
    message_text = ""
    
    if message.text:
        message_text = message.text
    elif message.caption:
        message_text = message.caption
    elif message.photo:
        message_text = "📷 Фото"
    elif message.document:
        message_text = f"📄 Документ: {message.document.file_name or 'Без названия'}"
    elif message.video:
        message_text = "🎥 Видео"
    elif message.audio:
        message_text = "🎵 Аудио"
    elif message.voice:
        message_text = "🎤 Голосовое сообщение"
    elif message.video_note:
        message_text = "📹 Видеосообщение"
    elif message.sticker:
        message_text = "😀 Стикер"
    else:
        message_text = "📎 Медиафайл"
    
    # Формируем информацию о пользователе (всегда включаем ID)
    if user_username:
        user_info = f"{user_name} (@{user_username}) ID: {user_id}"
    else:
        user_info = f"{user_name} (ID: {user_id})"
    
    # Отправляем заявку в группу администраторов
    try:
        # Формируем сообщение для группы
        group_message = (
            f"🎫 <b>Yangi ariza</b>\n\n"
            f"👤 <b>Foydalanuvchi:</b> {user_info}\n"
            f"⏰ <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            f"📝 <b>Xabar:</b>\n{message_text}\n\n"
            f"💬 <i>Foydalanuvchiga javob berish uchun bu xabarga javob bering</i>"
        )
        
        print(f"🔍 Отправка в группу ID: {ADMIN_GROUP_ID}")
        
        # Сначала проверим, может ли бот получить информацию о чате
        try:
            chat_info = await bot.get_chat(ADMIN_GROUP_ID)
            print(f"✅ Информация о чате: {chat_info.title} (тип: {chat_info.type})")
        except Exception as chat_error:
            print(f"❌ Не удалось получить информацию о чате: {chat_error}")
            raise chat_error
        
        # Отправляем сообщение в группу
        sent_message = await bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=group_message,
            parse_mode="HTML"
        )
        
        print(f"✅ Сообщение отправлено в группу, ID сообщения: {sent_message.message_id}")
        
        # Если это медиа-сообщение, пересылаем оригинал
        if message.photo or message.document or message.video or message.audio or message.voice or message.video_note or message.sticker:
            print(f"🔍 Пересылаем медиафайл в группу")
            try:
                await bot.forward_message(
                    chat_id=ADMIN_GROUP_ID,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id
                )
                print(f"✅ Медиафайл переслан в группу")
            except Exception as e:
                print(f"❌ Ошибка пересылки медиафайла: {e}")
                # Отправляем текстовое уведомление о медиафайле
                await bot.send_message(
                    chat_id=ADMIN_GROUP_ID,
                    text=f"📎 <b>Медиафайл</b> от пользователя (не удалось переслать)\n"
                         f"👤 Пользователь: {user_info}\n"
                         f"📝 Описание: {message_text}",
                    parse_mode="HTML"
                )
        
        # Отправляем подтверждение пользователю
        confirmation_text = (
            f"✅ {hbold('Ariza yuborildi!')}\n\n"
            f"📝 {hbold('Sizning xabaringiz:')} {message_text[:100]}{'...' if len(message_text) > 100 else ''}\n\n"
            f"⏳ {hitalic('Biz sizning arizangizni oldik va tez orada javob beramiz!')}\n\n"
            f"💡 {hitalic('Qo' + chr(39) + 'llab-quvvatlash xizmatimizdan javob kutib turing')}"
        )
        await message.answer(confirmation_text, parse_mode="HTML")
        
    except Exception as e:
        # Если не удалось отправить в группу, уведомляем пользователя
        print(f"❌ Ошибка отправки в группу: {e}")
        print(f"🔍 ID группы: {ADMIN_GROUP_ID}")
        
        await message.answer(
            f"⚠️ {hbold('Ошибка при отправке заявки')}\n\n"
            f"❌ Не удалось отправить заявку в группу поддержки.\n"
            f"Ошибка: {str(e)[:100]}\n\n"
            f"🔧 Проверьте:\n"
            f"• Правильность ID группы\n"
            f"• Права бота в группе\n"
            f"• Админские права бота"
        )