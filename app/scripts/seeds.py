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

        created_roles = {}
        for role_data in roles_data:
            existing_role = crud_role.get_role_by_name(db, role_data["name"])
            if not existing_role:
                role = RoleCreate(**role_data)
                created_role = crud_role.create_role(db, role)
                created_roles[role_data["name"]] = created_role
                print(f"✅ Создана роль: {created_role.name} (ID: {created_role.id})")
            else:
                created_roles[role_data["name"]] = existing_role
                print(
                    f"ℹ️  Роль {existing_role.name} уже существует (ID: {existing_role.id})"
                )

        # Создаем админа, если его нет
        admin_role = created_roles.get("admin")
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
            print(
                f"✅ Создан админ пользователь: admin / admin123 (Role ID: {admin_role.id})"
            )
        else:
            # Обновляем роль существующего админа
            if existing_admin.role_id != admin_role.id:
                existing_admin.role_id = admin_role.id
                db.commit()
                print(f"✅ Обновлена роль админа на admin (Role ID: {admin_role.id})")
            else:
                print("ℹ️  Админ пользователь уже существует с правильной ролью")

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
