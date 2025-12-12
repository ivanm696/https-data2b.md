from databases import Database
from sqlalchemy import create_engine
from src.core.config import settings
from src.database.models import metadata

# Асинхронный объект для выполнения запросов
database = Database(settings.DATABASE_URL)

# Синхронный движок для создания таблиц (SQLAlchemy)
engine = create_engine(
    settings.DATABASE_URL,
    # Необходимо для SQLite в асинхронном режиме
    connect_args={"check_same_thread": False} 
)

def create_db_tables():
    """Создает все определенные таблицы в БД, если они не существуют."""
    metadata.create_all(engine)
