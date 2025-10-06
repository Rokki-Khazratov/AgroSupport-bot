from aiogram import Router, F
from aiogram.types import Message, ReplyToMessage
from aiogram.utils.markdown import hbold, hitalic
from datetime import datetime

from models.ticket import Reply, TicketStatus
from utils.formatters import format_reply_for_user

router = Router()


@router.message(F.reply_to_message)
async def handle_admin_reply(message: Message, db, bot):
    """Обработчик ответов администраторов в группе"""
    
    # Проверяем, что это ответ на сообщение в группе
    if not message.chat.id == int(message.bot.config.ADMIN_GROUP_ID):
        return
    
    # Получаем сообщение, на которое отвечают
    replied_message = message.reply_to_message
    
    # Ищем заявку по ID сообщения в группе
    ticket = await db.get_ticket_by_group_message_id(replied_message.message_id)
    
    if not ticket:
        await message.reply(
            f"❌ {hbold('Ошибка')}\n\n"
            f"Не удалось найти заявку для этого сообщения.\n"
            f"Убедитесь, что вы отвечаете на сообщение с заявкой."
        )
        return
    
    # Получаем информацию об администраторе
    admin = message.from_user
    admin_id = admin.id
    admin_name = admin.full_name or "Администратор"
    admin_username = admin.username or ""
    
    # Формируем текст ответа
    reply_text = message.text or "Ответ администратора"
    
    # Создаем ответ в базе данных
    reply = Reply(
        ticket_id=ticket.id,
        admin_id=admin_id,
        admin_name=admin_name,
        admin_username=admin_username,
        reply_text=reply_text
    )
    
    created_reply = await db.create_reply(reply)
    
    # Обновляем статус заявки на "в обработке"
    await db.update_ticket_status(ticket.id, TicketStatus.IN_PROGRESS)
    
    try:
        # Форматируем ответ для пользователя
        user_reply_text = format_reply_for_user(created_reply, ticket.id)
        
        # Отправляем ответ пользователю
        await bot.send_message(
            chat_id=ticket.user_id,
            text=user_reply_text,
            parse_mode="HTML"
        )
        
        # Подтверждаем администратору об отправке
        await message.reply(
            f"✅ {hbold('Ответ отправлен')}\n\n"
            f"👤 Пользователю: {ticket.user_name}\n"
            f"🎫 Заявка: #{ticket.id}\n"
            f"📝 Ответ: {reply_text[:50]}{'...' if len(reply_text) > 50 else ''}"
        )
        
    except Exception as e:
        # Если не удалось отправить пользователю
        await message.reply(
            f"❌ {hbold('Ошибка отправки')}\n\n"
            f"Не удалось отправить ответ пользователю.\n"
            f"Возможно, пользователь заблокировал бота.\n\n"
            f"🎫 Заявка: #{ticket.id}\n"
            f"👤 Пользователь: {ticket.user_name} (ID: {ticket.user_id})"
        )


@router.message(F.text.startswith("/close"))
async def close_ticket_handler(message: Message, db):
    """Обработчик команды закрытия заявки"""
    
    # Проверяем, что это группа администраторов
    if not message.chat.id == int(message.bot.config.ADMIN_GROUP_ID):
        return
    
    # Извлекаем номер заявки из команды
    command_parts = message.text.split()
    if len(command_parts) != 2:
        await message.reply(
            f"❌ {hbold('Неправильный формат команды')}\n\n"
            f"Используйте: /close <номер_заявки>\n"
            f"Пример: /close 123"
        )
        return
    
    try:
        ticket_id = int(command_parts[1])
    except ValueError:
        await message.reply(
            f"❌ {hbold('Неверный номер заявки')}\n\n"
            f"Номер заявки должен быть числом."
        )
        return
    
    # Получаем заявку
    ticket = await db.get_ticket_by_id(ticket_id)
    
    if not ticket:
        await message.reply(
            f"❌ {hbold('Заявка не найдена')}\n\n"
            f"Заявка #{ticket_id} не существует."
        )
        return
    
    # Закрываем заявку
    await db.update_ticket_status(ticket.id, TicketStatus.CLOSED)
    
    await message.reply(
        f"✅ {hbold('Заявка закрыта')}\n\n"
        f"🎫 Заявка #{ticket.id} закрыта\n"
        f"👤 Пользователь: {ticket.user_name}\n"
        f"📝 Сообщение: {ticket.message_text[:100]}{'...' if len(ticket.message_text) > 100 else ''}"
    )


@router.message(F.text.startswith("/stats"))
async def stats_handler(message: Message, db):
    """Обработчик команды статистики заявок"""
    
    # Проверяем, что это группа администраторов
    if not message.chat.id == int(message.bot.config.ADMIN_GROUP_ID):
        return
    
    # Здесь можно добавить получение статистики из базы данных
    # Пока отправляем заглушку
    await message.reply(
        f"📊 {hbold('Статистика заявок')}\n\n"
        f"🔧 Функция в разработке\n"
        f"Скоро здесь будет отображаться статистика по заявкам."
    )
