from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic
from datetime import datetime

from config import ADMIN_GROUP_ID

router = Router()


@router.message(F.reply_to_message)
async def handle_admin_reply(message: Message, bot):
    """Обработчик ответов администраторов в группе"""
    
    # Проверяем, что это ответ на сообщение в группе
    if not message.chat.id == int(ADMIN_GROUP_ID):
        return
    
    # Получаем сообщение, на которое отвечают
    replied_message = message.reply_to_message
    
    # Проверяем, что это сообщение с заявкой (содержит "Новая заявка")
    if not replied_message.text or "Новая заявка" not in replied_message.text:
        await message.reply(
            f"❌ {hbold('Ошибка')}\n\n"
            f"Ответьте на сообщение с заявкой для отправки ответа пользователю."
        )
        return
    
    # Извлекаем информацию о пользователе из сообщения заявки
    try:
        # Парсим текст сообщения для получения user_id
        lines = replied_message.text.split('\n')
        user_info_line = None
        for line in lines:
            if "Пользователь:" in line:
                user_info_line = line
                break
        
        if not user_info_line:
            await message.reply("❌ Не удалось найти информацию о пользователе в заявке")
            return
        
        # Извлекаем user_id из строки вида "ID: 12345" или "@username"
        user_id = None
        if "ID:" in user_info_line:
            # Ищем ID в формате "ID: 12345"
            import re
            id_match = re.search(r'ID:\s*(\d+)', user_info_line)
            if id_match:
                user_id = int(id_match.group(1))
        elif "@" in user_info_line:
            # Если есть username, нужно будет получить user_id по-другому
            # Пока просто пропускаем такие случаи
            pass
        
        if not user_id:
            await message.reply("❌ Не удалось определить ID пользователя")
            return
        
        # Получаем информацию об администраторе
        admin = message.from_user
        admin_name = admin.full_name or "Администратор"
        admin_username = admin.username or ""
        
        # Формируем текст ответа
        reply_text = message.text or "Ответ администратора"
        
        # Формируем информацию об админе
        admin_info = f"@{admin_username}" if admin_username else f"ID: {admin.id}"
        if admin_name:
            admin_info = f"{admin_name} ({admin_info})"
        
        try:
            # Формируем ответ для пользователя
            user_reply_text = (
                f"✅ {hbold('Ответ от поддержки')}\n\n"
                f"👨‍💼 {hbold('Администратор:')} {admin_info}\n"
                f"⏰ {hbold('Время:')} {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                f"💬 {hbold('Ответ:')}\n{reply_text}"
            )
            
            # Отправляем ответ пользователю
            await bot.send_message(
                chat_id=user_id,
                text=user_reply_text,
                parse_mode="HTML"
            )
            
            # Подтверждаем администратору об отправке
            await message.reply(
                f"✅ {hbold('Ответ отправлен')}\n\n"
                f"👤 Пользователю ID: {user_id}\n"
                f"📝 Ответ: {reply_text[:50]}{'...' if len(reply_text) > 50 else ''}"
            )
            
        except Exception as e:
            # Если не удалось отправить пользователю
            await message.reply(
                f"❌ {hbold('Ошибка отправки')}\n\n"
                f"Не удалось отправить ответ пользователю.\n"
                f"Возможно, пользователь заблокировал бота.\n\n"
                f"👤 Пользователь ID: {user_id}"
            )
    
    except Exception as e:
        await message.reply(
            f"❌ {hbold('Ошибка обработки')}\n\n"
            f"Произошла ошибка при обработке ответа: {str(e)}"
        )