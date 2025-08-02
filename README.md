# 🚀 Modelo de Éxito de Productos en E-commerce

## 📋 Descripción del Proyecto

**Proyecto Interfaz Inteligente de Soporte a Decisiones de Marketing en E-commerce mediante Aprendizaje Automático**

Este proyecto implementa un sistema de inteligencia artificial que predice el éxito de productos en plataformas de e-commerce. Utiliza machine learning para evaluar si un producto será exitoso basándose en características como categoría, precio, público objetivo, especificaciones y mes de lanzamiento.

## 🏗️ Arquitectura del Sistema

El proyecto está compuesto por los siguientes componentes:

- **Frontend**: Aplicación Streamlit para interfaz de usuario
- **Backend**: API FastAPI para procesamiento de datos
- **Base de Datos**: MySQL para almacenamiento de datos históricos
- **MLflow**: Gestión de modelos de machine learning
- **Modelo ML**: Random Forest para predicción de éxito

## 📁 Estructura del Proyecto

```
modelo-exito/
├── api/                          # Backend API
│   ├── app.py                    # Aplicación Streamlit
│   ├── main.py                   # API FastAPI
│   ├── db.py                     # Configuración de base de datos
│   ├── settings.py               # Configuraciones
│   └── test_app.py              # Tests de la aplicación
├── Artefactos/                   # Datos y scripts
│   └── MySQL/
│       ├── 1. Tablas/           # Archivos CSV de datos
│       └── 2. Script/           # Scripts SQL
├── pryMLflow/                    # Entrenamiento de modelos
│   ├── entrenar.py              # Script de entrenamiento
│   └── dataset.csv              # Dataset de entrenamiento
├── requirements.txt              # Dependencias Python
└── test_conexion.py             # Test de conexión a BD
```

## 🛠️ Requisitos Previos

### Software Necesario
- **Python 3.8+**
- **MySQL 8.0+**
- **Git**

### Dependencias del Sistema
```bash
# Windows
# Instalar MySQL desde: https://dev.mysql.com/downloads/installer/

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install mysql-server python3-pip git

# macOS
brew install mysql python3 git
```

## 🚀 Instalación y Configuración

### Paso 1: Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd modelo-exito
```

### Paso 2: Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos MySQL

#### 4.1. Crear Base de Datos
```sql
CREATE DATABASE bd_amazon_ecom;
USE bd_amazon_ecom;
```

#### 4.2. Importar Datos
```bash
# Importar archivos CSV desde Artefactos/MySQL/1. Tablas/
mysql -u root -p bd_amazon_ecom < "Artefactos/MySQL/1. Tablas/DE_RAT_GEN_CAT.csv"
mysql -u root -p bd_amazon_ecom < "Artefactos/MySQL/1. Tablas/DE_PTS_EDAD_CAT.csv"
mysql -u root -p bd_amazon_ecom < "Artefactos/MySQL/1. Tablas/DE_PTS_MESL_CAT.csv"
mysql -u root -p bd_amazon_ecom < "Artefactos/MySQL/1. Tablas/DE_SPECS.csv"
mysql -u root -p bd_amazon_ecom < "Artefactos/MySQL/1. Tablas/T_PROD_VARS.csv"
```

#### 4.3. Ejecutar Script de Tratamiento
```bash
mysql -u root -p bd_amazon_ecom < "Artefactos/MySQL/2. Script/1. Tratamiento de datos.sql"
```

### Paso 5: Configurar Variables de Entorno

Crear archivo `.env` en la carpeta `api/`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=bd_amazon_ecom
```

### Paso 6: Configurar MLflow

#### 6.1. Iniciar Servidor MLflow
```bash
# Terminal 1
mlflow server --host 0.0.0.0 --port 5000
```

#### 6.2. Entrenar Modelo
```bash
# Terminal 2
cd pryMLflow
python entrenar.py
```

## 🚀 Despliegue y Ejecución

### Paso 1: Iniciar API Backend
```bash
# Terminal 1
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Paso 2: Iniciar Aplicación Frontend
```bash
# Terminal 2
cd api
streamlit run app.py --server.port 8501
```

### Paso 3: Verificar Conexiones
```bash
# Test de conexión a MySQL
python test_conexion.py

# Test de API
curl http://localhost:8000/health
```

## 📊 Uso del Sistema

### Interfaz de Usuario
1. **Acceder a la aplicación**: http://localhost:8501
2. **Completar formulario** con características del producto:
   - Especificaciones del producto
   - Categoría (Fashion, Electronics, Books, etc.)
   - Rango de precio
   - Género del público objetivo
   - Rango de edad
   - Mes de lanzamiento
3. **Evaluar éxito**: Hacer clic en "Evaluar éxito del producto"

### API Endpoints

#### Health Check
```bash
GET http://localhost:8000/health
```

#### Predicción de Éxito
```bash
POST http://localhost:8000/predict
Content-Type: application/json

{
  "CodEspec": 1,
  "CodCat": 0,
  "Categoria": "Fashion",
  "CodPrecio": 2,
  "CodGenero": 1,
  "Edad": "2. De 26 a 34",
  "CodMes": 6
}
```

## 🔧 Configuración Avanzada

### Variables de Entorno Adicionales
```env
# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000
MODEL_NAME=modelo_real
MODEL_STAGE=1

# API
API_HOST=0.0.0.0
API_PORT=8000

# Streamlit
STREAMLIT_SERVER_PORT=8501
```

### Configuración de Base de Datos
```python
# api/settings.py
class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str
    DB_NAME: str = "bd_amazon_ecom"
```

## 🧪 Testing

### Test de Conexión a Base de Datos
```bash
python test_conexion.py
```

### Test de API
```bash
# Test de health check
curl http://localhost:8000/health

# Test de predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"CodEspec":1,"CodCat":0,"Categoria":"Fashion","CodPrecio":2,"CodGenero":1,"Edad":"2. De 26 a 34","CodMes":6}'
```

## 📈 Monitoreo y Logs

### MLflow Tracking
- **URL**: http://localhost:5000
- **Funcionalidades**: Seguimiento de experimentos, versionado de modelos, métricas

### Logs de Aplicación
```bash
# Logs de FastAPI
uvicorn main:app --log-level debug

# Logs de Streamlit
streamlit run app.py --logger.level debug
```

## 🔍 Troubleshooting

### Problemas Comunes

#### 1. Error de Conexión a MySQL
```bash
# Verificar servicio MySQL
sudo systemctl status mysql

# Verificar credenciales
mysql -u root -p
```

#### 2. Error de Puerto Ocupado
```bash
# Verificar puertos en uso
netstat -tulpn | grep :8000
netstat -tulpn | grep :8501

# Cambiar puertos si es necesario
uvicorn main:app --port 8001
streamlit run app.py --server.port 8502
```

#### 3. Error de Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

#### 4. Error de MLflow
```bash
# Verificar servidor MLflow
curl http://localhost:5000

# Reiniciar servidor
mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db
```

## 📚 Documentación Adicional

### Archivos Importantes
- `Artefactos/MySQL/2. Script/1. Tratamiento de datos.sql`: Scripts de procesamiento de datos
- `Artefactos/Notebook/ML_G3.ipynb`: Notebook de análisis y modelado

### Estructura de Datos
- **DE_RAT_GEN_CAT**: Ratios de género por categoría
- **DE_PTS_EDAD_CAT**: Puntajes por edad y categoría
- **DE_PTS_MESL_CAT**: Puntajes por mes de lanzamiento
- **DE_SPECS**: Especificaciones de productos
- **T_PROD_VARS**: Variables finales del modelo

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto:
- Contactar al equipo de desarrollo sanCloud al correo (sancloud@gmail.com)

---

**Nota**: Asegúrate de tener todas las dependencias instaladas y la base de datos configurada correctamente antes de ejecutar el sistema. 
