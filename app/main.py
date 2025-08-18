from fastapi import FastAPI, HTTPException
from app.routers import auth
from app.routers import company


app = FastAPI(root_path="/api/project1", title="Company API")

app.include_router(auth.router)
app.include_router(company.router)


@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {"message": "Company API is working", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health():
    """Эндпоинт для проверки здоровья приложения"""
    return {"status": "healthy"}


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exc):
    """Глобальный обработчик HTTP исключений"""
    return {"error": exc.detail, "status_code": exc.status_code}
