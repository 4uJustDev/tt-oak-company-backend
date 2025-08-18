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

TESTETSTTETTESTET32321321321321312

# API
http://tamasaya.chickenkiller.com/api/project1/docs
http://185.255.134.218/api/project1/docs