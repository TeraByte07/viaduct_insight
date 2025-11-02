from fastapi import FastAPI
from app.routes import auth
from app.routes import analysis
app = FastAPI(title="Viaduct Backend")

# Register router
app.include_router(auth.router)
app.include_router(analysis.router)

@app.get("/")
def root():
    return {"message": "Welcome to Viaduct API"}
