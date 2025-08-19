## Установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd tt-oak-company-backend
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте переменные окружения:**

5. **Настройте базу данных:**
```bash
# Создайте базу данных PostgreSQL
createdb company_api

# Примените миграции
alembic upgrade head
```

6. **Запустите приложение:**
```bash
uvicorn app.main:app --reload
```

## Полезные команды

# venv
.\venv\Scripts\Activate.ps1

# Running app
run : uvicorn app.main:app --reload

# Alembic
alembic revision --autogenerate -m "comment" 
alembic upgrade head

# Docker 
docker compose down      
docker compose up -d --build  

## API
http://tamasaya.chickenkiller.com/api/project1/docs
http://185.255.134.218/api/project1/docs

## Стэк
- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **PostgreSQL** - реляционная база данных
- **Alembic** - миграции базы данных
- **JWT** - аутентификация
- **Pydantic** - валидация данных
- **bcrypt** - хеширование паролей