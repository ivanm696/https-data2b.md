from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert
from src.database.connection import database, companies
from src.database.models import CompanyDataIn, CompanyDataOut

# Создаем роутер, который будет подключен к главному приложению
router = APIRouter()

@router.get("/", summary="Проверка активности узла")
def read_root():
    """Возвращает статус активности узла."""
    return {"message": "Узел data2b-fastapi активен и подключен к БД."}

@router.post("/collect_data", summary="Сбор новых данных о фирме", response_model=CompanyDataOut)
async def collect_data(data: CompanyDataIn):
    """
    Принимает данные о новой фирме и сохраняет их в базе данных.
    """
    query = insert(companies).values(name=data.name, reg_number=data.reg_number)
    
    try:
        last_record_id = await database.execute(query)
        
        return {
            "id": last_record_id, 
            "name": data.name, 
            "reg_number": data.reg_number
        }
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
        raise HTTPException(
            status_code=400, 
            detail=f"Не удалось добавить фирму. Возможно, номер {data.reg_number} уже существует или ошибка БД."
        )

@router.get("/data", summary="Показать все собранные данные", response_model=List[CompanyDataOut])
async def get_collected_data():
    """Возвращает список всех собранных данных о фирмах из БД."""
    query = select(companies)
    results = await database.fetch_all(query)
    
    return [CompanyDataOut(**dict(result)) for result in results]
