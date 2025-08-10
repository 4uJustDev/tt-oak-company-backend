# venv
.\venv\Scripts\Activate.ps1

# Running app
run : uvicorn app.main:app --reload

# Alembic
alembic revision --autogenerate -m "comment" 
alembic upgrade head