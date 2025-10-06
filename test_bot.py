#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы бота без запуска
"""

import asyncio
from database import db
from models.ticket import Ticket, TicketStatus
from utils.formatters import format_ticket_for_group, format_ticket_confirmation


async def test_database():
    """Тестирование работы с базой данных"""
    print("🔧 Инициализация базы данных...")
    await db.init_db()
    print("✅ База данных инициализирована")
    
    # Создаем тестовую заявку
    print("\n📝 Создание тестовой заявки...")
    test_ticket = Ticket(
        user_id=12345,
        user_name="Тестовый Пользователь",
        user_username="test_user",
        message_text="Это тестовая заявка для проверки работы системы",
        status=TicketStatus.NEW
    )
    
    created_ticket = await db.create_ticket(test_ticket)
    print(f"✅ Заявка создана с ID: {created_ticket.id}")
    
    # Тестируем форматирование
    print("\n📄 Тестирование форматирования...")
    formatted_message = format_ticket_for_group(created_ticket)
    print("Сообщение для группы:")
    print(formatted_message)
    
    confirmation_message = format_ticket_confirmation(created_ticket)
    print("\nПодтверждение для пользователя:")
    print(confirmation_message)
    
    # Получаем заявку обратно
    print(f"\n🔍 Получение заявки #{created_ticket.id}...")
    retrieved_ticket = await db.get_ticket_by_id(created_ticket.id)
    if retrieved_ticket:
        print(f"✅ Заявка найдена: {retrieved_ticket.user_name} - {retrieved_ticket.message_text}")
    else:
        print("❌ Заявка не найдена")
    
    print("\n🎉 Тест завершен успешно!")


if __name__ == "__main__":
    asyncio.run(test_database())
