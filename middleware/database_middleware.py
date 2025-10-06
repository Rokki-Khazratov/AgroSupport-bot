from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from database import db


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для инициализации базы данных"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Инициализируем базу данных если она еще не инициализирована
        await db.init_db()
        
        # Добавляем экземпляр базы данных в данные
        data["db"] = db
        
        return await handler(event, data)
