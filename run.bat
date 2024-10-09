@echo off

:: Navigate to the directory containing the frontend and run npm start
start cmd /k "npm start"

:: Navigate to the directory containing the backend and activate the virtual environment
cd /d server
call venv\Scripts\activate

:: Run the Python app
python app.py

pause