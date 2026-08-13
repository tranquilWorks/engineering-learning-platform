SHELL := /bin/bash

.PHONY: dev serve validate-courses verify-backend verify build docker

dev:
	npm run dev

serve:
	ELP_WEB_DIST=$${ELP_WEB_DIST:-apps/web/dist} PYTHONPATH=apps/api/src python3 -m uvicorn elp_api.main:app --host 0.0.0.0 --port $${PORT:-8080}

validate-courses:
	PYTHONPATH=apps/api/src python3 scripts/validate_courses.py --execute --deterministic

verify-backend:
	PYTHONPATH=apps/api/src pytest -q apps/api/tests

build:
	npm run build

verify:
	./scripts/verify.sh

docker:
	docker compose up --build
