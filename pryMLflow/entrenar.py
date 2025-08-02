import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import os

mlflow.set_tracking_uri("http://localhost:5000")

# Asegúrate que esta ruta tenga tu dataset real
df = pd.read_csv("dataset.csv")

# Ejemplo de columnas, ajusta a las tuyas
X = df[['Afin_Hombre', 'Afin_Mujer', 'Edad_Pts','Val_Ran_Precio','Category', 'Grupo_Specs','MesL_Pts']]
y = df["Flag_Exito6"]

# División
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

with mlflow.start_run():
    modelo = RandomForestClassifier()
    modelo.fit(X_train, y_train)

    mlflow.sklearn.log_model(modelo, artifact_path="modelo_real", registered_model_name="modelo_real")
    print("✅ Modelo entrenado y registrado correctamente")