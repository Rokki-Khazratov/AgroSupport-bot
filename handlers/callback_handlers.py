import os
import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.markdown import hbold, hitalic

from config import APK_FILE_ID, APK_VERSION, APK_PATH, ADMIN_ID

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery):
    """Обработчик кнопки Support - показать информацию о поддержке"""
    
    await callback.answer()
    
    help_text = (
        f"📚 {hbold('Qo' + chr(39) + 'llab-quvvatlash')}\n\n"
        f"🎫 {hbold('Ariza qanday yaratish:')}\n"
        f"• Bot ga har qanday xabar yuboring\n"
        f"• Muammoingiz yoki savolingizni tasvirlab bering\n"
        f"• Rasmlar va hujjatlarni biriktirish mumkin\n\n"
        f"📊 {hbold('Buyruqlar:')}\n"
        f"• /start - asosiy menyu\n"
        f"• /menu - menyuni qayta ochish\n"
        f"• /help - bu yordam\n\n"
        f"⏰ {hbold('Javob vaqti:')}\n"
        f"• Odatda 24 soat ichida javob beramiz\n"
        f"• Favqulodda holatlarda - tezroq\n\n"
        f"❓ {hitalic('Savollar bormi? Xabar yuboring!')}"
    )
    
    await callback.message.answer(help_text, parse_mode="HTML")
    logger.info(f"👤 Foydalanuvchi {callback.from_user.id} support menyusini ochdi")


@router.callback_query(F.data == "download_apk")
async def download_apk_callback(callback: CallbackQuery, bot):
    """Обработчик кнопки Download APK - отправить APK файл пользователю"""
    
    await callback.answer("📥 Yuklanmoqda...")
    
    user = callback.from_user
    user_id = user.id
    user_name = user.full_name or "Noma'lum"
    user_username = user.username or ""
    
    logger.info(f"📱 Foydalanuvchi {user_id} ({user_name}) APK ni yuklab olmoqda (v{APK_VERSION})")
    
    try:
        # Метод 1: Отправка через file_id (приоритет)
        if APK_FILE_ID:
            logger.info(f"📤 APK yuborilmoqda file_id orqali...")
            await bot.send_document(
                chat_id=user_id,
                document=APK_FILE_ID,
                caption=(
                    f"✅ {hbold('GeoAgro ilovasi')}\n\n"
                    f"📱 {hbold('Versiya:')} {APK_VERSION}\n"
                    f"📦 {hitalic('Ilovani o' + chr(39) + 'rnatish uchun fayl menejerini oching')}\n\n"
                    f"💡 {hitalic('O' + chr(39) + 'rnatishda muammo bo' + chr(39) + 'lsa, /help buyrug' + chr(39) + 'ini yuboring')}"
                ),
                parse_mode="HTML"
            )
            logger.info(f"✅ APK muvaffaqiyatli yuborildi (file_id)")
            
        # Метод 2: Отправка локального файла (fallback)
        elif os.path.exists(APK_PATH):
            logger.info(f"📤 APK yuborilmoqda lokal fayl orqali: {APK_PATH}")
            document = FSInputFile(APK_PATH)
            sent_message = await bot.send_document(
                chat_id=user_id,
                document=document,
                caption=(
                    f"✅ {hbold('GeoAgro ilovasi')}\n\n"
                    f"📱 {hbold('Versiya:')} {APK_VERSION}\n"
                    f"📦 {hitalic('Ilovani o' + chr(39) + 'rnatish uchun fayl menejerini oching')}\n\n"
                    f"💡 {hitalic('O' + chr(39) + 'rnatishda muammo bo' + chr(39) + 'lsa, /help buyrug' + chr(39) + 'ini yuboring')}"
                ),
                parse_mode="HTML"
            )
            
            # Сохраняем file_id для будущего использования
            if sent_message.document:
                new_file_id = sent_message.document.file_id
                logger.info(f"💾 Yangi file_id olindi: {new_file_id}")
                logger.info(f"💡 .env ga qo'shing: APK_FILE_ID={new_file_id}")
            
            logger.info(f"✅ APK muvaffaqiyatli yuborildi (lokal fayl)")
            
        else:
            # Файл не найден
            logger.error(f"❌ APK fayli topilmadi: {APK_PATH}")
            await callback.message.answer(
                f"⚠️ {hbold('Xatolik')}\n\n"
                f"❌ APK fayli hozirda mavjud emas.\n"
                f"Iltimos, administratorga murojaat qiling.\n\n"
                f"📞 Yordam uchun: /help"
            )
            return
        
        # Логируем успешное скачивание
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {user_id} | {user_name} | @{user_username} | v{APK_VERSION}\n"
        with open("downloads.log", "a", encoding="utf-8") as f:
            f.write(log_entry)
        
    except Exception as e:
        logger.error(f"❌ APK yuborishda xatolik: {e}")
        await callback.message.answer(
            f"⚠️ {hbold('Yuborishda xatolik')}\n\n"
            f"❌ Fayl yuborib bo'lmadi. Iltimos, qaytadan urinib ko'ring.\n"
            f"Muammo davom etsa, /help buyrug'ini yuboring.\n\n"
            f"Xatolik: {str(e)[:100]}"
        )


@router.callback_query(F.data == "get_file_id")
async def get_file_id_callback(callback: CallbackQuery):
    """Обработчик для админов - показать инструкцию по получению file_id"""
    
    await callback.answer()
    
    # Проверяем, что это админ
    if ADMIN_ID and str(callback.from_user.id) != str(ADMIN_ID):
        await callback.message.answer("❌ Bu buyruq faqat administratorlar uchun")
        return
    
    instruction_text = (
        f"📋 {hbold('APK file_id ni olish bo' + chr(39) + 'yicha ko' + chr(39) + 'rsatma:')}\n\n"
        f"1️⃣ APK faylni botga yuklang (bu chatda)\n"
        f"2️⃣ Bot sizga file_id ni ko'rsatadi\n"
        f"3️⃣ File_id ni nusxalang\n"
        f"4️⃣ Serverdagi .env faylga qo'shing:\n"
        f"   <code>APK_FILE_ID=olgan_file_id</code>\n"
        f"5️⃣ Botni qayta ishga tushiring:\n"
        f"   <code>systemctl restart agro-bot</code>\n\n"
        f"💡 {hitalic('File_id orqali yuborish tezroq va serverni yuklamaydi!')}"
    )
    
    await callback.message.answer(instruction_text, parse_mode="HTML")

