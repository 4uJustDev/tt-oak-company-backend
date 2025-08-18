#!/usr/bin/env python3
"""
Скрипт для инициализации базовых данных (роли и админ пользователь)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.auth import hash_password
from app.crud import role as crud_role
from app.schemas.role import RoleCreate


def seed_data(db: Session):
    """Инициализация базовых данных"""
    try:
        # Создаем роли, если их нет
        roles_data = [
            {"name": "admin", "description": "Администратор с полными правами доступа"},
            {
                "name": "user",
                "description": "Обычный пользователь с ограниченными правами",
            },
            {"name": "manager", "description": "Менеджер с расширенными правами"},
        ]

        for role_data in roles_data:
            existing_role = crud_role.get_role_by_name(db, role_data["name"])
            if not existing_role:
                role = RoleCreate(**role_data)
                created_role = crud_role.create_role(db, role)
                print(f"✅ Создана роль: {created_role.name}")
            else:
                print(f"ℹ️  Роль {existing_role.name} уже существует")

        # Создаем админа, если его нет
        admin_role = crud_role.get_role_by_name(db, "admin")
        if not admin_role:
            print("❌ Роль admin не найдена, создание админа пропущено")
            return

        existing_admin = db.query(User).filter(User.username == "admin").first()
        if not existing_admin:
            admin_user = User(
                username="admin",
                password_hash=hash_password(
                    "admin123"
                ),  # Измените пароль на более безопасный
                role_id=admin_role.id,
            )
            db.add(admin_user)
            db.commit()
            print("✅ Создан админ пользователь: admin / admin123")
        else:
            print("ℹ️  Админ пользователь уже существует")

        print("🎉 Инициализация данных завершена успешно!")

    except Exception as e:
        print(f"❌ Ошибка при инициализации данных: {e}")
        db.rollback()
        raise


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
