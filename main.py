from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from src.core.config import settings
from src.database.connection import database, create_db_tables
from src.api.endpoints import router as api_router

# --- 1. Инициализация FastAPI приложения ---

app = FastAPI(
    title="Data2b-FastAPI Node",
    description="Узел для сбора и постоянного хранения данных о компаниях.",
    version="1.0.0"
)

# --- 2. Настройка CORS ---
# Здесь мы используем список разрешенных доменов из config.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Обработчики событий (Startup/Shutdown) ---

@app.on_event("startup")
async def startup_event():
    """Выполняется при запуске приложения."""
    create_db_tables()  # Создаем таблицы (если их нет)
    await database.connect() # Подключаемся к БД
    print(f"✅ Успешное подключение к БД: {settings.DATABASE_FILE}")

@app.on_event("shutdown")
async def shutdown_event():
    """Выполняется при завершении работы приложения."""
    await database.disconnect() # Отключаемся от БД
    print("❌ База данных отключена.")

# --- 4. Подключение роутеров ---

# Все наши API-ручки будут доступны по префиксу /api/v1
app.include_router(api_router, prefix="/api/v1")
