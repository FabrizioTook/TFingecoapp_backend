from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from firebase_config import firebase_init

router = APIRouter()
db = firebase_init()

# Modelo de datos financieros
class FinanceInput(BaseModel):
    id: Optional[str]
    userId: str
    precio_venta: float
    cuota_inicial: float
    fecha_emision: date
    numero_anios: int
    tasa_interes: float
    tasa_descuento: float
    periodo_tasa: str

# Crear un nuevo registro
@router.post("/american", response_model=FinanceInput)
async def crear_registro(finance_data: FinanceInput):
    try:
        data = finance_data.dict()
        data.pop("id", None)
        doc_ref = db.collection("american").add(data)
        doc_snapshot = doc_ref[1].get()
        document_id = doc_snapshot.id
        return FinanceInput(id=document_id, **doc_snapshot.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear: {e}")

# Obtener registros por filtros opcionales: userId, id o ambos
@router.get("/american", response_model=List[FinanceInput])
async def listar_registros(userId: Optional[str] = Query(None), registro_id: Optional[str] = Query(None)):
    try:
        coleccion = db.collection("american")

        if registro_id:
            doc = coleccion.document(registro_id).get()
            if not doc.exists:
                raise HTTPException(status_code=404, detail="Registro no encontrado")
            data = doc.to_dict()
            # Si se pide también filtrar por userId
            if userId and data.get("userId") != userId:
                return []
            return [FinanceInput(id=doc.id, **data)]

        if userId:
            docs = coleccion.where("userId", "==", userId).stream()
        else:
            docs = coleccion.stream()

        return [FinanceInput(id=doc.id, **doc.to_dict()) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener registros: {e}")

# Actualizar un registro
@router.put("/american/{registro_id}", response_model=FinanceInput)
async def actualizar_registro(registro_id: str, datos_actualizados: FinanceInput):
    try:
        doc_ref = db.collection("american").document(registro_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        data = datos_actualizados.dict()
        data["id"] = registro_id
        doc_ref.set(data)
        return FinanceInput(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {e}")

# Eliminar un registro
@router.delete("/american/{registro_id}", response_model=dict)
async def eliminar_registro(registro_id: str):
    try:
        doc_ref = db.collection("american").document(registro_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        doc_ref.delete()
        return {"mensaje": "Registro eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {e}")
