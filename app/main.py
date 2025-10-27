from fastapi import FastAPI
from app.routers import sensors
from app.routers import auth

app = FastAPI(title="Security System")

app.include_router(sensors.router)
app.include_router(auth.router)

@app.get("/")
async def home():
    return {"message": "Servidor FastAPI funcionando correctamente"}
