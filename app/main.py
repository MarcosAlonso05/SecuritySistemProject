from fastapi import FastAPI
from app.routers import sensors

app = FastAPI(title="Security System")

app.include_router(sensors.router)

@app.get("/")
async def home():
    return {"message": "Servidor FastAPI funcionando correctamente"}
