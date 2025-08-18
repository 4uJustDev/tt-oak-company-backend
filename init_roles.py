#!/usr/bin/env python3
"""
Скрипт для инициализации базовых данных (роли и админ пользователь)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scripts.seeds import seed_data
from app.database import SessionLocal


def main():
    """Главная функция для инициализации данных"""
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
