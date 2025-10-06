# AgroSupport Bot - Qo'llab-quvvatlash boti

Foydalanuvchilardan arizalarni qabul qilish va administratorlar guruhiga avtomatik yuborish uchun oddiy Telegram bot.

## 🎯 Funksiyalar

### Foydalanuvchilar uchun:
- 📝 Har qanday xabar orqali ariza yaratish
- ✅ Ariza qabul qilinganini tasdiqlash
- 💬 Administratorlardan javob olish
- 📎 Rasm, hujjat va boshqa media fayllar yuborish

### Administratorlar uchun:
- 📨 Barcha arizalarni guruhda olish
- 💬 Ariza xabariga javob berish orqali foydalanuvchiga javob yuborish
- 🔄 Javobni avtomatik foydalanuvchiga yuborish
- 📎 Media fayllar bilan javob berish

## 🚀 O'rnatish va ishga tushirish

### 1. Loyihani klonlash
```bash
git clone https://github.com/Rokki-Khazratov/AgroSupport-bot.git
cd AgroSupport-bot
```

### 2. Zarur kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Sozlashni tayyorlash
```bash
cp env.example .env
```

.env faylini tahrirlang:
```env
BOT_TOKEN=sizning_bot_token_ingiz
ADMIN_GROUP_ID=sizning_admin_guruhi_id_si
ADMIN_ID=admin_user_id
LOG_LEVEL=INFO
```

### 4. Bot token olish
1. Telegram da [@BotFather](https://t.me/BotFather) ni toping
2. `/newbot` buyrug'ini yuboring
3. Ko'rsatmalar bo'yicha bot yarating
4. Olingan tokenni .env ga qo'shing

### 5. Administratorlar guruhini sozlash
1. Telegram da guruh yarating
2. Bot ni guruhga administrator sifatida qo'shing
3. Guruh ID sini oling ([@userinfobot](https://t.me/userinfobot) orqali)
4. ID ni .env ga qo'shing

### 6. Bot ni ishga tushirish
```bash
python main.py
```

## 📁 Loyiha tuzilishi

```
agro-support-leads/
├── main.py                    # Bot asosiy fayli
├── config.py                  # Sozlamalar
├── handlers/
│   ├── user_handlers.py       # Foydalanuvchilar uchun ishlovchilar
│   └── admin_handlers.py      # Administratorlar uchun ishlovchilar
├── requirements.txt
├── .env
└── README.md
```

## 💻 Buyruqlar

### Foydalanuvchilar uchun:
- `/start` - salom va ko'rsatmalar
- `/help` - ishlatish bo'yicha yordam
- Har qanday xabar - ariza yaratish

### Administratorlar uchun (guruhda):
- Ariza xabariga javob berish - foydalanuvchiga javob yuborish

## 🔧 Qanday ishlaydi

1. **Foydalanuvchi xabar yuboradi** → Bot uni administratorlar guruhiga yuboradi
2. **Administrator javob beradi** → Bot avtomatik javobni foydalanuvchiga yuboradi
3. **Ma'lumotlar bazasi yo'q** → Barcha ma'lumotlar xabarlar orqali uzatiladi

## ✨ Xususiyatlar

- 🚀 **Maksimal oddiy** - ma'lumotlar bazasi va murakkab mantiq yo'q
- ⚡ **Tez ishga tushirish** - minimal bog'liqliklar
- 🔄 **Avtomatik yuborish** - javoblar foydalanuvchilarga darhol yetib boradi
- 📱 **Media qo'llab-quvvatlash** - rasm, hujjat, ovoz yuborish mumkin
- 🛡️ **Xavfsizlik** - faqat sozlangan guruhda ishlaydi

## 📝 Litsenziya

MIT License

## 🤝 Loyihaga hissa qo'shish

1. Loyihani fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Branch ga push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching