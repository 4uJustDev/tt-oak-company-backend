from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import User, Role
from app.core.security import get_password_hash


def seed():
    db: Session = SessionLocal()

    # Создаем роли
    for role_name in ["admin", "user"]:
        role = db.query(Role).filter_by(name=role_name).first()
        if not role:
            db.add(Role(name=role_name))
    db.commit()

    # Создаем админа, если его нет
    admin = db.query(User).filter_by(email="admin@example.com").first()
    if not admin:
        db.add(
            User(
                email="admin@example.com",
                hashed_password=get_password_hash("Admin123!"),
                role_id=db.query(Role).filter_by(name="admin").first().id,
            )
        )
        db.commit()
    db.close()


if __name__ == "__main__":
    seed()
