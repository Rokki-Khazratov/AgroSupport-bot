from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic
from datetime import datetime
import re

from config import ADMIN_GROUP_ID

router = Router()


@router.message(F.reply_to_message)
async def handle_admin_reply(message: Message, bot):
    """Обработчик ответов администраторов в группе"""
    
    print(f"🔍 Получено сообщение с reply в чате {message.chat.id}")
    print(f"🔍 ADMIN_GROUP_ID: {ADMIN_GROUP_ID}")
    print(f"🔍 Сравнение: {message.chat.id} == {int(ADMIN_GROUP_ID)}")
    
    # Проверяем, что это ответ на сообщение в группе
    if not message.chat.id == int(ADMIN_GROUP_ID):
        print(f"❌ Сообщение не из админской группы, пропускаем")
        return
    
    print(f"✅ Сообщение из админской группы, обрабатываем reply")
    
    # Получаем сообщение, на которое отвечают
    replied_message = message.reply_to_message
    
    print(f"🔍 Текст сообщения, на которое отвечают: {replied_message.text[:100] if replied_message.text else 'Нет текста'}...")
    
    # Проверяем, что это сообщение с заявкой (содержит "Yangi ariza")
    if not replied_message.text or "Yangi ariza" not in replied_message.text:
        print(f"❌ Сообщение не содержит 'Yangi ariza', пропускаем")
        await message.reply(
            f"❌ {hbold('Xatolik')}\n\n"
            f"Foydalanuvchiga javob yuborish uchun ariza xabariga javob bering."
        )
        return
    
    print(f"✅ Найдено сообщение с заявкой, извлекаем информацию о пользователе")
    
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
            await message.reply("❌ Arizada foydalanuvchi haqida ma'lumot topilmadi")
            return
        
        # Извлекаем user_id из строки вида "ID: 12345"
        user_id = None
        if "ID:" in user_info_line:
            # Ищем ID в формате "ID: 12345"
            id_match = re.search(r'ID:\s*(\d+)', user_info_line)
            if id_match:
                user_id = int(id_match.group(1))
                print(f"🔍 Найден user_id: {user_id}")
        
        if not user_id:
            print(f"❌ Не удалось найти user_id в строке: {user_info_line}")
            await message.reply("❌ Arizadan foydalanuvchi ID sini aniqlash mumkin emas")
            return
        
        # Получаем информацию об администраторе
        admin = message.from_user
        admin_name = admin.full_name or "Administrator"
        admin_username = admin.username or ""
        
        # Формируем текст ответа
        reply_text = message.text or "Administrator javobi"
        
        # Формируем информацию об админе
        admin_info = f"@{admin_username}" if admin_username else f"ID: {admin.id}"
        if admin_name:
            admin_info = f"{admin_name} ({admin_info})"
        
        try:
            # Формируем ответ для пользователя
            user_reply_text = (
                f"✅ {hbold('Qo\'llab-quvvatlashdan javob')}\n\n"
                f"👨‍💼 {hbold('Administrator:')} {admin_info}\n"
                f"⏰ {hbold('Vaqt:')} {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                f"💬 {hbold('Javob:')}\n{reply_text}"
            )
            
            print(f"🔍 Отправка ответа пользователю ID: {user_id}")
            print(f"📝 Текст ответа: {reply_text[:50]}...")
            
            # Отправляем ответ пользователю
            await bot.send_message(
                chat_id=user_id,
                text=user_reply_text,
                parse_mode="HTML"
            )
            
            print(f"✅ Ответ успешно отправлен пользователю ID: {user_id}")
            
            # Если ответ содержит медиафайл, пересылаем его пользователю
            if message.photo or message.document or message.video or message.audio or message.voice or message.video_note or message.sticker:
                print(f"🔍 Пересылаем медиафайл пользователю")
                try:
                    await bot.forward_message(
                        chat_id=user_id,
                        from_chat_id=message.chat.id,
                        message_id=message.message_id
                    )
                    print(f"✅ Медиафайл переслан пользователю")
                except Exception as e:
                    print(f"❌ Ошибка пересылки медиафайла пользователю: {e}")
            
            # Подтверждаем администратору об отправке
            await message.reply(
                f"✅ {hbold('Javob yuborildi')}\n\n"
                f"👤 Foydalanuvchi ID: {user_id}\n"
                f"📝 Javob: {reply_text[:50]}{'...' if len(reply_text) > 50 else ''}"
            )
            
        except Exception as e:
            # Если не удалось отправить пользователю
            await message.reply(
                f"❌ {hbold('Yuborish xatoligi')}\n\n"
                f"Foydalanuvchiga javob yuborish mumkin emas.\n"
                f"Ehtimol, foydalanuvchi bot ni bloklagan.\n\n"
                f"👤 Foydalanuvchi ID: {user_id}\n"
                f"❌ Xatolik: {str(e)[:100]}"
            )
    
    except Exception as e:
        await message.reply(
            f"❌ {hbold('Qayta ishlash xatoligi')}\n\n"
            f"Javobni qayta ishlashda xatolik yuz berdi: {str(e)[:100]}"
        )