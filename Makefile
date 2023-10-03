init:
	@echo "Setting up python environment..."
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "Python environment setup complete."

install:
	@echo "Installing local module..."
	.venv/bin/pip install -e .
	@echo "Local module installed."

test:
	@echo "Running tests..."
	.venv/bin/python -m unittest discover
	@echo "Tests complete."
