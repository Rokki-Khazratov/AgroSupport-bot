from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class TicketStatus(Enum):
    """Статусы заявок"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


@dataclass
class Ticket:
    """Модель заявки"""
    id: Optional[int] = None
    user_id: int = 0
    user_name: str = ""
    user_username: str = ""
    message_text: str = ""
    message_id_in_group: Optional[int] = None
    status: TicketStatus = TicketStatus.NEW
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Преобразование в словарь для сохранения в БД"""
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_username': self.user_username,
            'message_text': self.message_text,
            'message_id_in_group': self.message_id_in_group,
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Ticket':
        """Создание объекта из словаря БД"""
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id', 0),
            user_name=data.get('user_name', ''),
            user_username=data.get('user_username', ''),
            message_text=data.get('message_text', ''),
            message_id_in_group=data.get('message_id_in_group'),
            status=TicketStatus(data.get('status', 'new')),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )


@dataclass
class Reply:
    """Модель ответа администратора"""
    id: Optional[int] = None
    ticket_id: int = 0
    admin_id: int = 0
    admin_name: str = ""
    admin_username: str = ""
    reply_text: str = ""
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Преобразование в словарь для сохранения в БД"""
        return {
            'ticket_id': self.ticket_id,
            'admin_id': self.admin_id,
            'admin_name': self.admin_name,
            'admin_username': self.admin_username,
            'reply_text': self.reply_text,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Reply':
        """Создание объекта из словаря БД"""
        return cls(
            id=data.get('id'),
            ticket_id=data.get('ticket_id', 0),
            admin_id=data.get('admin_id', 0),
            admin_name=data.get('admin_name', ''),
            admin_username=data.get('admin_username', ''),
            reply_text=data.get('reply_text', ''),
            created_at=data.get('created_at')
        )
