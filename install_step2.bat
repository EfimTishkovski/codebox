@echo off
chcp 65001
echo Активация виртуальной среды
start/b "" venv\Scripts\activate
venv\Scripts\pip install -r requirements.txt
echo Пакеты успешно установлены
echo Готово. Закройте командную строку.
echo Запуск приложения: запустите файл launch.bat
exit /b


