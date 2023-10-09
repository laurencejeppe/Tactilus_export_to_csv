@ECHO OFF
TITLE Tactilus Pressure Export to CSV
if not exist "venv" (
	ECHO Creating Virtual Environment
	python -m venv venv
	ECHO Activating Virtual Environment
	call "venv/Scripts/activate"
	ECHO Updating pip
	python -m pip install --upgrade pip
	ECHO Installing Packages
	pip install -r requirements.txt
) else (
	ECHO Activating Virtual Environment
)
call "venv/Scripts/activate" 
ECHO Opening Python GUI
python gui.py
deactivate
pause