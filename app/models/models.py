from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey, Text, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    # API: "contactId": "16" — у нас это связь ниже через Contact
    name = Column(String(255), nullable=False)
    short_name = Column(String(64), nullable=True, index=True)
    business_entity = Column(String(64), nullable=True)  # e.g. "Partnership"
    contract_no = Column(String(64), nullable=True)
    contract_issue_date = Column(Date, nullable=True)

    # В ТЗ: type — массив строк
    type = Column(ARRAY(String), nullable=False, server_default="{}")  # TEXT[]

    status = Column(String(32), nullable=False, server_default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Связи
    contact = relationship(
        "Contact",
        uselist=False,
        back_populates="company",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    photos = relationship(
        "Photo",
        back_populates="company",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Photo.created_at.desc()",
    )

    __table_args__ = (
        Index("ix_companies_name", "name"),
    )

    def __repr__(self) -> str:
        return f"<Company id={self.id} name={self.name!r}>"


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # в ТЗ у компании один контакт — 1:1
    )
    firstname = Column(String(128), nullable=True)
    lastname  = Column(String(128), nullable=True)
    phone     = Column(String(32),  nullable=True)
    email     = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    company = relationship("Company", back_populates="contact")

    __table_args__ = (
        Index("ix_contacts_email", "email"),
        Index("ix_contacts_phone", "phone"),
    )

    def __repr__(self) -> str:
        return f"<Contact id={self.id} company_id={self.company_id}>"


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    filename  = Column(String(255), nullable=False)  # имя файла на диске
    filepath  = Column(Text, nullable=False)         # публичный URL
    thumbpath = Column(Text, nullable=False)         # публичный URL превью
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    company = relationship("Company", back_populates="photos")

    __table_args__ = (
        UniqueConstraint("company_id", "filename", name="uq_photos_company_file"),
    )

    def __repr__(self) -> str:
        return f"<Photo id={self.id} company_id={self.company_id} filename={self.filename!r}>"
