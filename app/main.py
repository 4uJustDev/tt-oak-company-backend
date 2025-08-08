from fastapi import FastAPI
from app.routers import auth_routes

app = FastAPI(title="Company API")

app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "API is working"}
