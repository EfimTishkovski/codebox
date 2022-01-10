@echo off
start/b  ""  venv\Scripts\activate
venv\Scripts\pip install -r requirements.txt
echo Done. Closed commandline.
echo launch:  launch.bat.
exit /b


