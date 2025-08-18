from app.database import SessionLocal
from app.models.user import User, Role  # твои модели
from sqlalchemy.orm import Session


def seed_data(db: Session):
    # Создадим роли, если их нет
    for role_name in ["admin", "user"]:
        if not db.query(Role).filter_by(name=role_name).first():
            db.add(Role(name=role_name))

    db.commit()

    # Создадим админа, если его нет
    if not db.query(User).filter_by(email="admin@example.com").first():
        admin_role = db.query(Role).filter_by(name="admin").first()
        user = User(
            email="admin@example.com",
            hashed_password="hashedpassword",  # ⚡ лучше захешировать bcrypt
            role_id=admin_role.id,
        )
        db.add(user)
        db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    seed_data(db)
    db.close()
    print("✅ Seeding complete")
