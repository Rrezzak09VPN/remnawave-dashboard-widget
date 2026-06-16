@echo off
title Remnawave Dashboard Runner
color 0B
echo ===================================================
echo     Запуск Remnawave Live Dashboard
echo ===================================================
echo.

:: Проверяем, установлен ли Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден в системе!
    echo Пожалуйста, установите Python и добавьте его в PATH (переменные среды).
    echo Скачать можно с официального сайта: https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

:: Проверяем и устанавливаем зависимости
echo [1/3] Проверка библиотек Python...
python -c "import fastapi, httpx, uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo Библиотеки не найдены. Устанавливаю необходимые зависимости...
    python -m pip install fastapi httpx uvicorn
    if %errorlevel% neq 0 (
        echo [ОШИБКА] Не удалось установить библиотеки! Проверьте интернет-соединение.
        pause
        exit /b
    )
) else (
    echo Все библиотеки (fastapi, httpx, uvicorn) уже установлены.
)

:: Автоматически открываем браузер
echo [2/3] Открытие страницы в браузере...
start http://127.0.0.1:8000/

:: Запускаем сервер
echo [3/3] Запуск локального сервера...
echo Для остановки сервера закройте это окно.
echo.
python start_dashboard.py

pause
