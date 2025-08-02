import mlflow
import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from db import get_engine
from typing import Dict

app = FastAPI(title="Producto API", version="0.1.0")

#MLFLOW_TRACKING_URI = "http://9000aca66145.ngrok-free.app" # Dirección pública de tu servidor MLflow
MLFLOW_TRACKING_URI = "http://localhost:5000"

# Nombre y stage del modelo registrado
MODEL_NAME = "modelo_real"  # O cambia por "randomforest_model", etc.
MODEL_STAGE = "1"             # O reemplaza por versión, como "1"

# Conectarse al servidor MLflow
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Cargar el modelo desde el Model Registry
model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
model = mlflow.pyfunc.load_model(model_uri)
# ---------- Esquemas (placeholders por ahora) ----------
class VarsRequest(BaseModel):
    CodEspec: int = Field(
        ..., ge=0, le=10,
        description=("0: Sin valor temático, 1: Arte y creatividad, 2: Desarrollo personal, " 
        "3: Entorno familiar, 4: Entorno laboral, 5: Entorno social, 6: Hogar, " 
        "7: Gestión emocional, 8: Cuidado personal, 9: Instituciones, 10: Innovación"),
        examples=[0]
    )
    CodCat: int = Field(
        ..., ge=0, le=4,
        description="0=Fashion, 1=Home Appliance, 2=Electronics, 3=Books, 4=Fitness",
        examples=[0]
    )
    Categoria: str = Field(
        ..., min_length=1,
        description="Nombre de la categoría (ej: 'Fashion', 'Electronics')",
        examples=["Fashion"]
    )
    CodPrecio: int = Field(
        ..., ge=1, le=7,
        description="1:De ₹10 a ₹100, 2:De ₹101 a ₹200, 3:De ₹201 a ₹300, 4:De ₹301 a ₹400, 5:De ₹401 a ₹500",
        examples=[1]
    )
    CodGenero: int = Field(
        ..., ge=0, le=2,
        description="0:Hombre, 1:Mujer, 2:Ambos",
        examples=[0]
    )
    Edad: str = Field(
        ..., min_length=1,
        description=("1. Hasta 25, 2. De 26 a 34, 3. De 35 a 41, 4. De 42 a 48, "
        "5. De 49 a 55, 6. De 56 a 62, 7. Más de 62"),
        examples=["1. Hasta 25"]
    )
    CodMes: int = Field(
        ...,ge=1, le=12,
        description="1:01. Enero, 2:02. Febrero, 3:03. Marzo, 4:04. Abril, 05. Mayo, " +
        "6:06. Junio, 7:07. Julio, 8:08. Agosto, 9:09. Setiembre, 10:10. Octubre, " +
        "11:11. Noviembre, 12:12. Diciembre",
        examples=[1]
    )

class VarsResponse(BaseModel):
    CodEspec: int
    CodCat: int
    Categoria: str
    CodPrecio: int
    CodGenero: int
    Edad: str
    CodMes: int
    varH: float
    varM: float
    EdadPts: int
    MesPts: int

class PredictRequest(BaseModel):
    #Variables predictoras
    varH: float
    varM: float
    EdadPts: int
    CodPrecio: int
    CodCat: int
    CodEspec: int
    MesPts: int

class PredictResponse(BaseModel):
    flag_exito: int

# ---------- Funciones para consultas SQL ----------
def ConsultaAfinidad(categoria: str, codgenero: int) -> tuple[float, float]:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            query = text("SELECT Afin_Hombre, Afin_Mujer FROM DE_RAT_GEN_CAT WHERE Category=:categoria")
            result = conn.execute(query, {"categoria": categoria}).fetchone()

            if result is None:
                raise HTTPException(status_code=404, detail="¡Categoría no encontrada en la base de datos!")

            afinH, afinM = result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando la base de datos: {e}")

    # Lógica del género
    if codgenero == 0:
        varH = afinH
        varM = 0
    elif codgenero == 1:
        varH = 0
        varM = afinM
    elif codgenero == 2:
        varH = afinH
        varM = afinM
    else:
        raise HTTPException(status_code=400, detail="¡Valor inválido para CodGenero!")

    # Respuesta para validación en Streamlit
    return varH, varM

def ConsultaPtsEdad(categoria: str, ran_edad: str) -> float:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            query = text("SELECT puntaje FROM DE_PTS_EDAD_CAT WHERE Category=:categoria AND Ran_edad=:ran_edad")
            result = conn.execute(query, {"categoria": categoria, "ran_edad": ran_edad}).fetchone()

            if result is None:
                raise HTTPException(status_code=404, detail="¡Categoría no encontrada en la base de datos!")

            puntaje = result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando la base de datos: {e}")

    # Respuesta para validación en Streamlit
    return puntaje

def ConsultaPtsMes(categoria: str, mes: int) -> float:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            query = text("SELECT Pts_Lanza FROM DE_PTS_MESL_CAT WHERE Category=:categoria AND Mes_Lanza=:mes")
            result = conn.execute(query, {"categoria": categoria, "mes": mes}).fetchone()

            if result is None:
                raise HTTPException(status_code=404, detail="¡Categoría no encontrada en la base de datos!")

            puntaje = result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando la base de datos: {e}")

    # Respuesta para validación en Streamlit
    return puntaje

def ObtenerVars(data: VarsRequest):
    try:
        varHombre,varMujer = ConsultaAfinidad(data.Categoria,data.CodGenero)
        ptsEdad = ConsultaPtsEdad(data.Categoria,data.Edad)
        ptsMesL = ConsultaPtsMes(data.Categoria,data.CodMes)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando la base de datos: {e}")

    return VarsResponse(
        CodEspec=data.CodEspec,
        CodCat=data.CodCat,
        Categoria=data.Categoria,
        CodPrecio=data.CodPrecio,
        CodGenero=data.CodGenero,
        Edad=data.Edad,
        CodMes=data.CodMes,
        varH=varHombre,
        varM=varMujer,
        EdadPts=ptsEdad,
        MesPts=ptsMesL
    )

# ---------- Endpoints ----------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/vars", response_model=VarsResponse)
def vars(data: VarsRequest):
    return ObtenerVars(data)

@app.post("/predict", response_model=PredictResponse)
def predict(data: VarsRequest):
    # Modelo desde MLflow
    try:
        # Paso 1: Obtener variables finales
        VarsResultado = ObtenerVars(data)

        # Paso 2: Copiar variables
        InputModelo = PredictRequest(
            varH=VarsResultado.varH,
            varM=VarsResultado.varM,
            EdadPts=VarsResultado.EdadPts,
            CodPrecio=VarsResultado.CodPrecio,
            CodCat=VarsResultado.CodCat,
            CodEspec=VarsResultado.CodEspec,
            MesPts=VarsResultado.MesPts
        )

        df = pd.DataFrame([InputModelo.dict()])

        # Renombrar columnas al nombre que usaste al entrenar el modelo
        df.columns = ['Afin_Hombre', 'Afin_Mujer', 'Edad_Pts', 'Val_Ran_Precio',
                      'Category', 'Grupo_Specs', 'MesL_Pts']

        prediction = model.predict(df)
        resultado = int(prediction[0])
        return {
            "flag_exito": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))