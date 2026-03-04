.PHONY: help test lint format clean install demo

help:
	@echo "ASCII Unicode Exploit Kit - Available commands:"
	@echo "  make test     - Run test suite"
	@echo "  make lint     - Run linting checks"
	@echo "  make format   - Format code with black"
	@echo "  make clean    - Clean build artifacts"
	@echo "  make install  - Install package locally"
	@echo "  make demo     - Run interactive demo"

test:
	python tests/test_suite.py

lint:
	flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics

format:
	black src/ tests/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

install:
	pip install -e .

demo:
	python demo.py

# Development setup
dev-setup:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black
