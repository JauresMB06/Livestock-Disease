
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Livestock Disease Surveillance Network")

@app.get("/")
def root():
    return {"message": "LDSN API is running"}

app.include_router(router, prefix="/api")


