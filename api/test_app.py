import requests

datos = {
    "CodEspec": 1,
    "CodCat": 1,
    "Categoria": "Fashion",  # reemplaza por uno que exista en tu BD
    "CodPrecio": 2,
    "CodGenero": 2,
    "Edad":"1. Hasta 25",
    "CodMes": 7
}

try:
    r = requests.post("http://localhost:8000/score", json=datos)
    print("STATUS:", r.status_code)
    print("RESPUESTA:", r.json())
except Exception as e:
    print("Error de conexión:", e)