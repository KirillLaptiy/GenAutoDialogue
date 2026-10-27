@echo off
chcp 65001 > nul

:: Проверка прав администратора. Если их нет, скрипт перезапустит сам себя с запросом прав.
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_script
) else (
    echo Запрос прав администратора...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_script
:: Переходим в папку, где лежит сам bat-файл
cd /d "%~dp0"

echo [ОК] Права администратора получены.
echo Запуск GTFO
echo ---------------------------------------

:: Запуск вашего python-скрипта
python gtfo.py

pause
