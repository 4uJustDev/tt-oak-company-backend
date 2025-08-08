from fastapi import FastAPI

app = FastAPI(title="Company API")

@app.get("/health")
def health():
    return {"status": "ok"}
