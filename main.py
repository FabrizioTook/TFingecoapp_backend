from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.authentication import router as auth_router
from routes.american import router as american_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas de autenticación bajo el prefijo /auth
app.include_router(auth_router, prefix="/api")
app.include_router(american_router, prefix="/api")
