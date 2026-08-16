.PHONY: install test lint run-dev run-prod docker-build docker-up clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm
	python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"

test:
	pytest tests/ -v

lint:
	flake8 app/ tests/ --count --max-line-length=127 --statistics

run-dev:
	python run.py

docker-build:
	docker build -t newstrace:latest .

docker-up:
	docker compose up -d

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
