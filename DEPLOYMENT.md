# 🚀 Production Deployment Guide

Bu qo'llanma bot ni production serverda ishga tushirish uchun.

## 📋 Talablar

- Ubuntu 20.04+ server
- Python 3.8+
- Git
- Systemd (bot ni xizmat sifatida ishga tushirish uchun)

## 🔧 Server sozlash

### 1. Server yangilash
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Python va zarur paketlarni o'rnatish
```bash
sudo apt install python3 python3-pip python3-venv git -y
```

### 3. Bot uchun foydalanuvchi yaratish
```bash
sudo useradd -m -s /bin/bash agro-bot
sudo usermod -aG sudo agro-bot
```

### 4. Foydalanuvchi qatoriga o'tish
```bash
sudo su - agro-bot
```

## 📦 Bot o'rnatish

### 1. Loyihani klonlash
```bash
cd /home/agro-bot
git clone https://github.com/Rokki-Khazratov/AgroSupport-bot.git
cd AgroSupport-bot
```

### 2. Virtual environment yaratish
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Zarur kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Sozlamalar faylini yaratish
```bash
cp env.example .env
nano .env
```

.env faylini to'ldiring:
```env
BOT_TOKEN=your_actual_bot_token
ADMIN_GROUP_ID=your_actual_group_id
ADMIN_ID=your_admin_user_id
LOG_LEVEL=INFO
```

## 🔄 Systemd xizmat yaratish

### 1. Xizmat faylini yaratish
```bash
sudo nano /etc/systemd/system/agro-bot.service
```

### 2. Xizmat konfiguratsiyasi
```ini
[Unit]
Description=AgroSupport Telegram Bot
After=network.target

[Service]
Type=simple
User=agro-bot
WorkingDirectory=/home/agro-bot/AgroSupport-bot
Environment=PATH=/home/agro-bot/AgroSupport-bot/venv/bin
ExecStart=/home/agro-bot/AgroSupport-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Xizmatni yoqish
```bash
sudo systemctl daemon-reload
sudo systemctl enable agro-bot
sudo systemctl start agro-bot
```

### 4. Xizmat holatini tekshirish
```bash
sudo systemctl status agro-bot
```

## 📊 Monitoring va loglar

### 1. Loglarni ko'rish
```bash
sudo journalctl -u agro-bot -f
```

### 2. Xizmat holatini tekshirish
```bash
sudo systemctl status agro-bot
```

### 3. Xizmatni qayta ishga tushirish
```bash
sudo systemctl restart agro-bot
```

### 4. Xizmatni to'xtatish
```bash
sudo systemctl stop agro-bot
```

## 🔧 Bot yangilash

### 1. Yangi versiyani olish
```bash
cd /home/agro-bot/AgroSupport-bot
git pull origin main
```

### 2. Yangi kutubxonalarni o'rnatish
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Bot ni qayta ishga tushirish
```bash
sudo systemctl restart agro-bot
```

## 🛡️ Xavfsizlik

### 1. Firewall sozlash
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow out 443  # HTTPS
sudo ufw allow out 80   # HTTP
```

### 2. Fail2ban o'rnatish
```bash
sudo apt install fail2ban -y
```

### 3. .env fayl huquqlarini cheklash
```bash
chmod 600 /home/agro-bot/AgroSupport-bot/.env
```

## 📈 Performance monitoring

### 1. CPU va RAM ishlatishini kuzatish
```bash
htop
```

### 2. Disk ishlatishini tekshirish
```bash
df -h
```

### 3. Log fayllar hajmini tekshirish
```bash
sudo journalctl --disk-usage
```

## 🔍 Troubleshooting

### Bot ishlamayapti
```bash
# Xizmat holatini tekshiring
sudo systemctl status agro-bot

# Loglarni ko'ring
sudo journalctl -u agro-bot --since "1 hour ago"

# Xizmatni qayta ishga tushiring
sudo systemctl restart agro-bot
```

### Token xatosi
```bash
# .env faylni tekshiring
cat /home/agro-bot/AgroSupport-bot/.env

# Token to'g'ri ekanligini tekshiring
curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"
```

### Guruh ID xatosi
```bash
# Guruh ID ni tekshiring
# Bot guruhda bo'lishi va admin huquqlarga ega bo'lishi kerak
```

## 📞 Qo'llab-quvvatlash

Agar muammolar bo'lsa:
1. Loglarni tekshiring: `sudo journalctl -u agro-bot -f`
2. GitHub da issue yarating
3. Telegram da @username ga yozing

## 🔄 Avtomatik yangilash (ixtiyoriy)

Cron job yaratish:
```bash
crontab -e
```

Qo'shing:
```bash
# Har kuni ertalab 3:00 da yangilash
0 3 * * * cd /home/agro-bot/AgroSupport-bot && git pull && sudo systemctl restart agro-bot
```
