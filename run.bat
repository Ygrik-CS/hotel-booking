@echo off
REM Создание виртуального окружения (если ещё нет)
IF NOT EXIST venv (
    python -m venv venv
)

REM Активация окружения
call venv\Scripts\activate

REM Установка зависимостей
pip install -r requirements.txt

REM Запуск сервера FastAPI
uvicorn app.main:app --reload
