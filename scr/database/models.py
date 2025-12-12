from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, MetaData, Table

# --- Pydantic-модели (для проверки данных) ---

class CompanyDataIn(BaseModel):
    """Модель для входящих данных (тело POST-запроса)."""
    name: str
    reg_number: str

class CompanyDataOut(CompanyDataIn):
    """Модель для данных, возвращаемых из БД (включает ID)."""
    id: int


# --- SQLAlchemy-модели (для структуры БД) ---

metadata = MetaData()

companies = Table(
    "companies",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    # Уникальный индекс гарантирует, что reg_number не будет повторяться
    Column("reg_number", String, unique=True, index=True), 
)
