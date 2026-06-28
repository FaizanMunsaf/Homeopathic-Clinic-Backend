from fastapi import FastAPI

from api.health import router as health_router

app = FastAPI(title="Homeopathic Backend", version="0.1.0")
app.include_router(health_router)


@app.get("/")
def read_root():
    return {"message": "Homeopathic Backend API is running"}
