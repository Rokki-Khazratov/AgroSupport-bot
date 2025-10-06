import aiosqlite
import asyncio
from datetime import datetime
from typing import Optional, List
from models.ticket import Ticket, Reply, TicketStatus


class Database:
    """Класс для работы с базой данных SQLite"""
    
    def __init__(self, db_path: str = "support_bot.db"):
        self.db_path = db_path
    
    async def init_db(self):
        """Инициализация базы данных и создание таблиц"""
        async with aiosqlite.connect(self.db_path) as db:
            # Таблица заявок
            await db.execute('''
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    user_name TEXT NOT NULL,
                    user_username TEXT DEFAULT '',
                    message_text TEXT NOT NULL,
                    message_id_in_group INTEGER,
                    status TEXT DEFAULT 'new',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица ответов
            await db.execute('''
                CREATE TABLE IF NOT EXISTS replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id INTEGER NOT NULL,
                    admin_id INTEGER NOT NULL,
                    admin_name TEXT NOT NULL,
                    admin_username TEXT DEFAULT '',
                    reply_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticket_id) REFERENCES tickets (id)
                )
            ''')
            
            # Индексы для оптимизации
            await db.execute('CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON tickets(user_id)')
            await db.execute('CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status)')
            await db.execute('CREATE INDEX IF NOT EXISTS idx_replies_ticket_id ON replies(ticket_id)')
            
            await db.commit()
    
    async def create_ticket(self, ticket: Ticket) -> Ticket:
        """Создание новой заявки"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO tickets (user_id, user_name, user_username, message_text, message_id_in_group, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                ticket.user_id,
                ticket.user_name,
                ticket.user_username,
                ticket.message_text,
                ticket.message_id_in_group,
                ticket.status.value
            ))
            
            ticket_id = cursor.lastrowid
            await db.commit()
            
            # Получаем созданную заявку
            return await self.get_ticket_by_id(ticket_id)
    
    async def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """Получение заявки по ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
            row = await cursor.fetchone()
            
            if row:
                return Ticket.from_dict(dict(zip([desc[0] for desc in cursor.description], row)))
            return None
    
    async def get_ticket_by_group_message_id(self, message_id: int) -> Optional[Ticket]:
        """Получение заявки по ID сообщения в группе"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM tickets WHERE message_id_in_group = ?', (message_id,))
            row = await cursor.fetchone()
            
            if row:
                return Ticket.from_dict(dict(zip([desc[0] for desc in cursor.description], row)))
            return None
    
    async def update_ticket_status(self, ticket_id: int, status: TicketStatus):
        """Обновление статуса заявки"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE tickets 
                SET status = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (status.value, ticket_id))
            await db.commit()
    
    async def update_ticket_group_message_id(self, ticket_id: int, message_id: int):
        """Обновление ID сообщения в группе для заявки"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE tickets 
                SET message_id_in_group = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (message_id, ticket_id))
            await db.commit()
    
    async def create_reply(self, reply: Reply) -> Reply:
        """Создание ответа администратора"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO replies (ticket_id, admin_id, admin_name, admin_username, reply_text)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                reply.ticket_id,
                reply.admin_id,
                reply.admin_name,
                reply.admin_username,
                reply.reply_text
            ))
            
            reply_id = cursor.lastrowid
            await db.commit()
            
            # Получаем созданный ответ
            return await self.get_reply_by_id(reply_id)
    
    async def get_reply_by_id(self, reply_id: int) -> Optional[Reply]:
        """Получение ответа по ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM replies WHERE id = ?', (reply_id,))
            row = await cursor.fetchone()
            
            if row:
                return Reply.from_dict(dict(zip([desc[0] for desc in cursor.description], row)))
            return None
    
    async def get_replies_by_ticket_id(self, ticket_id: int) -> List[Reply]:
        """Получение всех ответов по заявке"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM replies WHERE ticket_id = ? ORDER BY created_at', (ticket_id,))
            rows = await cursor.fetchall()
            
            return [Reply.from_dict(dict(zip([desc[0] for desc in cursor.description], row))) for row in rows]
    
    async def get_user_tickets(self, user_id: int, limit: int = 10) -> List[Ticket]:
        """Получение заявок пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                SELECT * FROM tickets 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            rows = await cursor.fetchall()
            
            return [Ticket.from_dict(dict(zip([desc[0] for desc in cursor.description], row))) for row in rows]
    
    async def get_user_last_ticket(self, user_id: int) -> Optional[Ticket]:
        """Получение последней заявки пользователя"""
        tickets = await self.get_user_tickets(user_id, 1)
        return tickets[0] if tickets else None


# Глобальный экземпляр базы данных
db = Database()
