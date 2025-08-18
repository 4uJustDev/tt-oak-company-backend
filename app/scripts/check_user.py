#!/usr/bin/env python3
"""
Скрипт для проверки пользователей в базе данных
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.auth import verify_password


def check_users():
    """Проверка пользователей в базе данных"""
    db = SessionLocal()
    try:
        # Проверяем роли
        print("=== РОЛИ ===")
        roles = db.query(Role).all()
        for role in roles:
            print(f"ID: {role.id}, Name: {role.name}, Description: {role.description}")

        print("\n=== ПОЛЬЗОВАТЕЛИ ===")
        users = db.query(User).all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Role ID: {user.role_id}")
            if user.role:
                print(f"  Role: {user.role.name}")

        # Проверяем конкретно админа
        print("\n=== ПРОВЕРКА АДМИНА ===")
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print(f"Админ найден: {admin.username}")
            print(f"Role ID: {admin.role_id}")
            if admin.role:
                print(f"Role Name: {admin.role.name}")

            # Проверяем пароль
            is_valid = verify_password("admin123", admin.password_hash)
            print(f"Пароль 'admin123' валиден: {is_valid}")
        else:
            print("Админ не найден!")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    check_users()
