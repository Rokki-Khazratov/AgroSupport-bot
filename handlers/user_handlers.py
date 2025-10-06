from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.utils.markdown import hbold, hitalic
from datetime import datetime

from config import ADMIN_GROUP_ID

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        f"👋 {hbold('Добро пожаловать в службу поддержки!')}\n\n"
        f"📝 {hitalic('Отправьте любое сообщение, чтобы создать заявку')}\n\n"
        f"🔧 {hbold('Доступные команды:')}\n"
        f"• /help - помощь и инструкции\n\n"
        f"💬 {hitalic('Мы поможем вам решить любые вопросы!')}"
    )
    
    await message.answer(welcome_text)


@router.message(Command("getid"))
async def get_id_handler(message: Message):
    """Обработчик команды /getid - показывает ID чата"""
    chat_id = message.chat.id
    chat_type = message.chat.type
    
    await message.answer(
        f"🆔 <b>Информация о чате:</b>\n\n"
        f"📊 <b>Тип:</b> {chat_type}\n"
        f"🆔 <b>ID:</b> <code>{chat_id}</code>\n\n"
        f"💡 <i>Скопируйте этот ID для настройки бота</i>",
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def help_handler(message: Message):
    """Обработчик команды /help"""
    help_text = (
        f"📚 {hbold('Помощь по использованию бота')}\n\n"
        f"🎫 {hbold('Как создать заявку:')}\n"
        f"• Просто отправьте любое сообщение боту\n"
        f"• Опишите вашу проблему или вопрос\n"
        f"• Можно прикреплять фото и документы\n\n"
        f"📊 {hbold('Команды:')}\n"
        f"• /start - начать работу с ботом\n"
        f"• /help - эта справка\n\n"
        f"⏰ {hbold('Время ответа:')}\n"
        f"• Обычно мы отвечаем в течение 24 часов\n"
        f"• В экстренных случаях - быстрее\n\n"
        f"❓ {hitalic('Есть вопросы? Отправьте сообщение!')}"
    )
    
    await message.answer(help_text)


@router.message(F.text | F.photo | F.document | F.video | F.audio | F.voice | F.video_note | F.sticker)
async def create_ticket_handler(message: Message, bot):
    """Обработчик создания заявки от пользователя"""
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
    
    # Формируем информацию о пользователе
    user_info = f"@{user_username}" if user_username else f"ID: {user_id}"
    if user_name:
        user_info = f"{user_name} ({user_info})"
    
    # Отправляем заявку в группу администраторов
    try:
        # Формируем сообщение для группы
        group_message = (
            f"🎫 <b>Новая заявка</b>\n\n"
            f"👤 <b>Пользователь:</b> {user_info}\n"
            f"⏰ <b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            f"📝 <b>Сообщение:</b>\n{message_text}\n\n"
            f"💬 <i>Ответьте на это сообщение, чтобы ответить пользователю</i>"
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
        if not message.text and not message.caption:
            await bot.forward_message(
                chat_id=ADMIN_GROUP_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        
        # Отправляем подтверждение пользователю
        confirmation_text = (
            f"✅ {hbold('Заявка отправлена!')}\n\n"
            f"📝 {hbold('Ваше сообщение:')} {message_text[:100]}{'...' if len(message_text) > 100 else ''}\n\n"
            f"⏳ {hitalic('Мы получили вашу заявку и скоро ответим!')}\n\n"
            f"💡 {hitalic('Ожидайте ответ от нашей службы поддержки')}"
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