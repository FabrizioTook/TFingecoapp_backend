from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from firebase_config import firebase_init, firebase_auth

router = APIRouter()
db = firebase_init()
auth = firebase_auth()

# Modelo de usuario
class UserModel(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    password: Optional[str] = Field(None, exclude=True)

class LoginModel(BaseModel):
    email: str
    password: str

# Registro de usuario
@router.post("/register", response_model=dict)
async def register(user: UserModel):
    try:
        if db.collection("users").where(filter=("email", "==", user.email)).limit(1).get():
            raise HTTPException(status_code=400, detail="Ya existe un usuario con este email.")

        user_record = auth.create_user_with_email_and_password(
            email=user.email,
            password=user.password
        )
        user_id = user_record.get("localId")

        user_data = {
            "id": user_id,
            "name": user.name,
            "email": user.email
        }
        db.collection("users").document(user_id).set(user_data)

        return user_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar el usuario: {e}")

# Inicio de sesión
@router.post("/login", response_model=dict)
async def login(user: LoginModel):
    try:
        auth_data = auth.sign_in_with_email_and_password(user.email, user.password)
        user_id = auth_data.get("localId")

        if not user_id:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        doc = db.collection("users").document(user_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        return doc.to_dict()

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al iniciar sesión: {e}")