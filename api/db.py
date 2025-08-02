from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from settings import settings

def get_engine() -> Engine:
    pwd = settings.DB_PASSWORD or ""
    uri = (
        f"mysql+pymysql://{settings.DB_USER}:{pwd}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    engine = create_engine(uri, pool_pre_ping=True)
    return engine