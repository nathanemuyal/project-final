@echo off

:: Navigate to the directory containing the frontend and run npm start
start cmd /k "npm start"

:: Navigate to the directory containing the backend (Python server)
cd /d server

:: Check if virtual environment exists
if not exist "venv\Scripts\activate" (
    echo Creating a new virtual environment...
    python -m venv venv
    echo Installing dependencies from requirements.txt...`
    pip install -r requirements.txt
) else (
    echo Virtual environment already exists.
)

:: Activate the virtual environment
echo Activating Python virtual environment...
call venv\Scripts\activate


:: Run the Python app
echo Starting app.py...
python app.py

:: Keep the command window open
pause