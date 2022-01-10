@ echo off
chcp 65001
rem Создание виртуальной среды
start/b "" python -m venv venv 
echo Виртуальна среда успешно создана.
echo Готово.Закройте командную строку. Запустите install_step2.bat
pause & exit