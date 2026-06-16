@echo off
chcp 65001 >nul
title Remnawave Dashboard Runner
color 0B

echo ===================================================
echo     Запуск Remnawave Live Dashboard
echo ===================================================
echo.

:: Проверяем, установлен ли Python
python --version >nul 2>&1
if errorlevel 1 goto NO_PYTHON

:: Проверяем библиотеки
echo [1/3] Проверка библиотек Python...
python -c "import fastapi, httpx, uvicorn" >nul 2>&1
if errorlevel 1 goto INSTALL_DEPS

echo Все библиотеки уже установлены.
goto START_BROWSER

:INSTALL_DEPS
echo Библиотеки не найдены. Устанавливаю зависимости (fastapi, httpx, uvicorn)...
python -m pip install fastapi httpx uvicorn
if errorlevel 1 goto DEPS_ERROR
goto START_BROWSER

:START_BROWSER
echo [2/3] Открытие страницы в браузере...
start http://127.0.0.1:8000/

echo [3/3] Запуск сервера...
python start_dashboard.py
goto END

:NO_PYTHON
echo [ОШИБКА] Python не установлен или не добавлен в PATH!
echo Пожалуйста, скачайте и установите Python (отметьте галочку "Add Python to PATH" при установке).
echo Официальный сайт: https://www.python.org/downloads/
echo.
pause
exit

:DEPS_ERROR
echo [ОШИБКА] Не удалось установить библиотеки! Проверьте интернет-соединение.
echo.
pause
exit

:END
pause
