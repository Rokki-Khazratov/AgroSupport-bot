from datetime import datetime
from typing import Optional
from models.ticket import Ticket, Reply


def format_ticket_for_group(ticket: Ticket) -> str:
    """Форматирование заявки для отправки в группу администраторов"""
    user_info = f"@{ticket.user_username}" if ticket.user_username else f"ID: {ticket.user_id}"
    
    if ticket.user_name:
        user_info = f"{ticket.user_name} ({user_info})"
    
    if ticket.created_at:
        if isinstance(ticket.created_at, str):
            created_time = ticket.created_at
        else:
            created_time = ticket.created_at.strftime("%d.%m.%Y %H:%M")
    else:
        created_time = "Неизвестно"
    
    return (
        f"🎫 <b>Заявка #{ticket.id}</b>\n\n"
        f"👤 <b>Пользователь:</b> {user_info}\n"
        f"⏰ <b>Время:</b> {created_time}\n"
        f"📝 <b>Сообщение:</b>\n{ticket.message_text}\n\n"
        f"💬 <i>Ответьте на это сообщение, чтобы ответить пользователю</i>"
    )


def format_reply_for_user(reply: Reply, ticket_id: int) -> str:
    """Форматирование ответа администратора для отправки пользователю"""
    admin_info = f"@{reply.admin_username}" if reply.admin_username else f"ID: {reply.admin_id}"
    
    if reply.admin_name:
        admin_info = f"{reply.admin_name} ({admin_info})"
    
    if reply.created_at:
        if isinstance(reply.created_at, str):
            created_time = reply.created_at
        else:
            created_time = reply.created_at.strftime("%d.%m.%Y %H:%M")
    else:
        created_time = "Неизвестно"
    
    return (
        f"✅ <b>Ответ от поддержки</b>\n\n"
        f"👨‍💼 <b>Администратор:</b> {admin_info}\n"
        f"⏰ <b>Время:</b> {created_time}\n"
        f"🎫 <b>Заявка:</b> #{ticket_id}\n\n"
        f"💬 <b>Ответ:</b>\n{reply.reply_text}"
    )


def format_ticket_confirmation(ticket: Ticket) -> str:
    """Форматирование подтверждения создания заявки для пользователя"""
    return (
        f"✅ <b>Заявка создана!</b>\n\n"
        f"🎫 <b>Номер заявки:</b> #{ticket.id}\n"
        f"📝 <b>Ваше сообщение:</b> {ticket.message_text[:100]}{'...' if len(ticket.message_text) > 100 else ''}\n\n"
        f"⏳ <i>Мы получили вашу заявку и скоро ответим!</i>\n\n"
        f"💡 <i>Используйте /status для проверки статуса вашей заявки</i>"
    )


def format_ticket_status(ticket: Ticket) -> str:
    """Форматирование статуса заявки для пользователя"""
    status_emoji = {
        "new": "🆕",
        "in_progress": "🔄", 
        "closed": "✅"
    }
    
    status_text = {
        "new": "Новая",
        "in_progress": "В обработке",
        "closed": "Закрыта"
    }
    
    if ticket.created_at:
        if isinstance(ticket.created_at, str):
            created_time = ticket.created_at
        else:
            created_time = ticket.created_at.strftime("%d.%m.%Y %H:%M")
    else:
        created_time = "Неизвестно"
    
    if ticket.updated_at:
        if isinstance(ticket.updated_at, str):
            updated_time = ticket.updated_at
        else:
            updated_time = ticket.updated_at.strftime("%d.%m.%Y %H:%M")
    else:
        updated_time = "Не обновлялась"
    
    return (
        f"🎫 <b>Заявка #{ticket.id}</b>\n\n"
        f"📝 <b>Сообщение:</b> {ticket.message_text[:100]}{'...' if len(ticket.message_text) > 100 else ''}\n"
        f"{status_emoji.get(ticket.status.value, '❓')} <b>Статус:</b> {status_text.get(ticket.status.value, 'Неизвестно')}\n"
        f"📅 <b>Создана:</b> {created_time}\n"
        f"🔄 <b>Обновлена:</b> {updated_time}"
    )


def truncate_text(text: str, max_length: int = 100) -> str:
    """Обрезание текста до указанной длины"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
