start-windows:
	bash -c "python -m venv venv"
	bash -c "source venv/Scripts/activate"
	bash -c "python -m pip install --upgrade pip"
	bash -c "cd game && python main.py"

start-linux:
	bash -c "python3 -m venv venv"
	bash -c "source venv/bin/activate"
	bash -c "python3 -m pip install --upgrade pip"
	bash -c "cd game && python main.py"

start:
	bash -c "cd game && python main.py"