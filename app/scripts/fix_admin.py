#!/usr/bin/env python3
"""
Скрипт для исправления админа пользователя
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.auth import hash_password


def fix_admin():
    """Исправление админа пользователя"""
    db = SessionLocal()
    try:
        # Находим роль admin
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            print("❌ Роль admin не найдена!")
            return

        print(f"✅ Найдена роль admin (ID: {admin_role.id})")

        # Находим пользователя admin
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("❌ Пользователь admin не найден!")
            return

        print(f"✅ Найден пользователь admin (текущий Role ID: {admin_user.role_id})")

        # Исправляем роль
        if admin_user.role_id != admin_role.id:
            admin_user.role_id = admin_role.id
            print(
                f"✅ Исправлена роль админа с {admin_user.role_id} на {admin_role.id}"
            )
        else:
            print("ℹ️  Роль админа уже правильная")

        # Пересоздаем пароль
        admin_user.password_hash = hash_password("admin123")
        print("✅ Пароль админа обновлен на 'admin123'")

        db.commit()
        print("🎉 Админ исправлен успешно!")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_admin()
