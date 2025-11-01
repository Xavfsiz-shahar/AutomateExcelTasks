@echo off
chcp 65001 > nul
echo ========================================
echo  Hisobot tizimi / Система отчётов
echo ========================================
echo.

REM Проверка установки зависимостей
pip show Flask > nul 2>&1
if errorlevel 1 (
    echo Установка зависимостей...
    echo Bog'liqliklarni o'rnatish...
    pip install -r requirements.txt
    echo.
)

echo Запуск приложения...
echo Dasturni ishga tushirish...
echo.
echo ========================================
echo  Откройте / Oching:
echo  http://localhost:5000
echo ========================================
echo.
echo Шаблон / Shablon: static\file\Шаблон.xlsx
echo.
echo Для остановки нажмите Ctrl+C
echo To'xtatish uchun Ctrl+C bosing
echo.

python app.py

pause

