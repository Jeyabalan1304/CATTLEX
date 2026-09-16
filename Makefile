.PHONY: install train seed test demo run-backend run-frontend docker-up docker-down

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

train:
	python ml/scripts/train_models.py

seed:
	python scripts/seed_database.py

test:
	python -m pytest backend/tests/ -v

demo:
	python scripts/run_demo.py

run-backend:
	cd backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

run-frontend:
	cd frontend && npm run dev

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
