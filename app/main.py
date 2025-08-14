from fastapi import FastAPI
from app.routers import auth
from app.routers import company


app = FastAPI(root_path="/api/project1", title="Company API")

app.include_router(auth.router)
app.include_router(company.router)

@app.get("/")
def root():
    return {"message": "API is working"}
