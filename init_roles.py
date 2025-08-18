#!/usr/bin/env python3
"""
Скрипт для инициализации базовых ролей в системе
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import role as crud_role
from app.schemas.role import RoleCreate


def init_roles():
    """Инициализация базовых ролей"""
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже роли
        existing_roles = crud_role.get_roles(db)
        if existing_roles:
            print("Роли уже существуют:")
            for role in existing_roles:
                print(f"  - {role.name}: {role.description}")
            return

        # Создаем базовые роли
        roles_data = [
            {"name": "admin", "description": "Администратор с полными правами доступа"},
            {
                "name": "user",
                "description": "Обычный пользователь с ограниченными правами",
            },
            {"name": "manager", "description": "Менеджер с расширенными правами"},
        ]

        for role_data in roles_data:
            role = RoleCreate(**role_data)
            created_role = crud_role.create_role(db, role)
            print(f"Создана роль: {created_role.name} - {created_role.description}")

        print("Инициализация ролей завершена успешно!")

    except Exception as e:
        print(f"Ошибка при инициализации ролей: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_roles()
