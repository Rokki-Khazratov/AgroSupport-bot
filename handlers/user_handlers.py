from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.utils.markdown import hbold, hitalic
from datetime import datetime

from models.ticket import Ticket, TicketStatus
from utils.formatters import format_ticket_confirmation, format_ticket_status
from config import ADMIN_GROUP_ID

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, db):
    """Обработчик команды /start"""
    welcome_text = (
        f"👋 {hbold('Добро пожаловать в службу поддержки!')}\n\n"
        f"📝 {hitalic('Отправьте любое сообщение, чтобы создать заявку')}\n\n"
        f"🔧 {hbold('Доступные команды:')}\n"
        f"• /help - помощь и инструкции\n"
        f"• /status - статус вашей последней заявки\n\n"
        f"💬 {hitalic('Мы поможем вам решить любые вопросы!')}"
    )
    
    await message.answer(welcome_text)


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
        f"• /help - эта справка\n"
        f"• /status - проверить статус заявки\n\n"
        f"⏰ {hbold('Время ответа:')}\n"
        f"• Обычно мы отвечаем в течение 24 часов\n"
        f"• В экстренных случаях - быстрее\n\n"
        f"❓ {hitalic('Есть вопросы? Отправьте сообщение!')}"
    )
    
    await message.answer(help_text)


@router.message(Command("status"))
async def status_handler(message: Message, db):
    """Обработчик команды /status - показывает статус последней заявки"""
    user_id = message.from_user.id
    
    # Получаем последнюю заявку пользователя
    last_ticket = await db.get_user_last_ticket(user_id)
    
    if not last_ticket:
        await message.answer(
            f"❌ {hbold('Заявки не найдены')}\n\n"
            f"📝 {hitalic('У вас пока нет заявок. Отправьте сообщение, чтобы создать заявку!')}"
        )
        return
    
    # Форматируем и отправляем статус заявки
    status_text = format_ticket_status(last_ticket)
    await message.answer(status_text)


@router.message(F.text | F.photo | F.document | F.video | F.audio | F.voice | F.video_note | F.sticker)
async def create_ticket_handler(message: Message, db, bot):
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
    
    # Создаем заявку в базе данных
    ticket = Ticket(
        user_id=user_id,
        user_name=user_name,
        user_username=user_username,
        message_text=message_text,
        status=TicketStatus.NEW
    )
    
    created_ticket = await db.create_ticket(ticket)
    
    # Отправляем заявку в группу администраторов
    try:
        # Формируем сообщение для группы
        group_message = (
            f"🎫 <b>Заявка #{created_ticket.id}</b>\n\n"
            f"👤 <b>Пользователь:</b> {user_name}"
            f" (@{user_username})" if user_username else f" (ID: {user_id})"
            f"\n⏰ <b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            f"📝 <b>Сообщение:</b>\n{message_text}\n\n"
            f"💬 <i>Ответьте на это сообщение, чтобы ответить пользователю</i>"
        )
        
        # Отправляем сообщение в группу
        sent_message = await bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=group_message,
            parse_mode="HTML"
        )
        
        # Если это медиа-сообщение, пересылаем оригинал
        if not message.text and not message.caption:
            await bot.forward_message(
                chat_id=ADMIN_GROUP_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        
        # Обновляем ID сообщения в группе в базе данных
        await db.update_ticket_group_message_id(created_ticket.id, sent_message.message_id)
        
        # Отправляем подтверждение пользователю
        confirmation_text = format_ticket_confirmation(created_ticket)
        await message.answer(confirmation_text, parse_mode="HTML")
        
    except Exception as e:
        # Если не удалось отправить в группу, уведомляем пользователя
        await message.answer(
            f"⚠️ {hbold('Ошибка при отправке заявки')}\n\n"
            f"❌ Не удалось отправить заявку в группу поддержки.\n"
            f"Попробуйте позже или обратитесь к администратору.\n\n"
            f"🆔 {hitalic('Номер заявки:')} #{created_ticket.id}"
        )
