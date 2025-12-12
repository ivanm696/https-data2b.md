#!/bin/bash

echo "🚀 Запуск узла data2b-fastapi..."

# --reload включает автоматическую перезагрузку при изменении кода (удобно для разработки)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
