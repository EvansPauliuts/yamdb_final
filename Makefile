VENV := .venv
SRC_DIR_TEST := ./tests
BIN := $(VENV)/bin
PYTHON := $(BIN)/python3
SHELL := /bin/bash
FLAKE8 := "$(BIN)/flake8"
AUTOPEP8 := "$(BIN)/autopep8"

REQUIREMENTS:="requirements.txt"

include .env.prod

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv $(VENV) && source $(BIN)/activate
	@echo '************ SUCCESS ACTIVATE VENV ************'

.PHONY: install
install: venv ## Make venv and install requirements
	$(BIN)/pip install --upgrade -r $(REQUIREMENTS)
	@echo '************ SUCCESS REQUIREMENTS ************'

freeze: ## Pin current dependencies
	$(BIN)/pip freeze > $(REQUIREMENTS)
	@echo '************ SUCCESS FREEZE ************'

migrate: ## Make and run migrations
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	@echo '************ SUCCESS MIGRATIONS ************'

.PHONY: test
tests: ## Run tests
	$(PYTHON) manage.py test
	@echo '************ SUCCESS TEST ************'

.PHONY: run
run: ## Run the Django server
	$(PYTHON) manage.py runserver
	@echo '************ SUCCESS RUN DJANGO ************'

.PHONY: test
test: ## Run the Django server
	pytest
	@echo '************ SUCCESS RUN TEST ************'

.PHONY: shell
shell: # run shell
	$(PYTHON) manage.py shell
	@echo '************ SUCCESS SHELL ************'

.PHONY: check
check: ## run flake8
	@$(FLAKE8)
	@echo '************ SUCCESS FLAKE8 ************'

.PHONY: gunicorn_run
gunicorn_run: # run wsgi
	gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
	@echo '************ SUCCESS GUNICORN ************'

.PHONY: test_django
test_django:
	coverage run --source='posts,users' manage.py test -v 2
	@echo '************ SUCCESS TESTING ************'

.PHONY: test_report
test_report:
	coverage report
	@echo '************ SUCCESS TESTING REPORT ************'

# DOCKER

.PHONY: docker_prod
docker_prod: # docker-compose dev run project app
	docker-compose up --build
	@echo '************ SUCCESS DOCKER BUILD ************'

.PHONY: docker_down
docker_down: # docker-compose dev down project
	docker-compose down
	@echo '************ SUCCESS DOCKER BUILD ************'

.PHONY: docker_stop
docker_stop: # docker stop
	docker-compose stop
	@echo '************ SUCCESS DOCKER STOP ************'

.PHONY: docker_status
docker_status: # docker status
	docker-compose ps
	@echo '************ SUCCESS DOCKER STATUS ************'

.PHONY: docker_rm
docker_rm: # docker rm
	docker-compose rm app
	@echo '************ SUCCESS DOCKER REMOVE ************'