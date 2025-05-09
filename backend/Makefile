LIBS_DIR?=libs
TESTS_DIR?="tests libs/shared/tests"
project?=auth-server
platform?=linux/amd64

.PHONY: help # Generate list of targets with descriptions
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/ - \1 - \2/'

#--------------------------------------- LOAD ENV VARS ---------------------------------
.PHONY: load-env # Load environment variables
load-env:
	@echo "Loading environment variables..."
	@echo "Loading .env file..."
	@export $(cat .env | xargs) > /dev/null 2>&1
	@echo "Environment variables loaded."
	@echo "Done."

#--------------------------------------- DB -----------------------------------
.PHONY: db-create # Creates DB
db-create:
	./scripts/create_db.sh

.PHONY: db-update # Updates DB
db-update:
	@echo "Updating DB..."
	@python manage.py makemigrations
	@python manage.py migrate

.PHONY: db-base-seeds # Adds base seeds
db-base-seeds:
	@python manage.py loaddata 000_user

.PHONY: db-dev-seeds # Adds dev seeds
db-dev-seeds:

.PHONY: db-update # Updates DB
db-update: db-create
	@python manage.py migrate
	@make db-base-seeds

#--------------------------------------- DOCKER -----------------------------------

.PHONY: make-requirements # Generates requirements.txt file from poetry
make-requirements:
	@poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: start-local # Starts local docker image
start-local:
	@docker compose -p $(project) up -d

.PHONY: stop-local # Stops local docker image
stop-local:
	@docker compose -p $(project) down

.PHONY: build-image # Builds docker image - parameters: platform (default: linux/amd64)
build-image: clean
	@DOCKER_DEFAULT_PLATFORM=$(platform) docker compose -f docker-compose.yml -f docker-compose.prod.yml build
	@echo "Image built with platform: $(platform)"

.PHONY: exec-prod # Executes command in prod
exec-prod:
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml run api bash

.PHONY: run-prod # Runs docker image
run-prod:
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

.PHONY: stop-prod # Stops docker image
destroy-prod:
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml down

.PHONY: prod-logs # Shows docker logs
prod-logs:
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f api

.PHONY: ecr-login # Login to AWS ECR - parameters: registry, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
ecr-login:
	@docker run --rm --platform=$(platform) -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) -e AWS_REGION=$(AWS_REGION) amazon/aws-cli ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(registry)
	@echo "Logged in to ECR registry $(registry) using platform: $(platform)."

.PHONY: prod-push # Pushes docker image to AWS ECR - parameters: image_name, tag, registry, AWS_REGION and platform (default: linux/amd64)
prod-push: ecr-login
	@echo "Registering image $(image_name):$(tag) to $(registry) using platform: $(platform)"
	@docker tag datacare_api:local $(registry)/$(image_name):$(tag)
	@docker tag datacare_api:local $(registry)/$(image_name):latest
	@docker push $(registry)/$(image_name):$(tag)
	@echo "Successfully pushed $(image_name):$(tag) to $(registry)"
	@docker push $(registry)/$(image_name):latest
	@echo "Successfully pushed $(image_name):latest to $(registry)"
	@echo "Done."

#------------------------------------- DEV ENV -----------------------------------
.PHONY: install-git-hooks # Install the git hooks
install-git-hooks:
	@poetry run pre-commit install

.PHONY: safey # Check for security vulnerabilities
safety:
	poetry export --without-hashes --without-urls | safety check --stdin

.PHONY: lint # Run the linters
lint:
	@isort .
	@black .
	@flake8 .

.PHONY: check-lint # Run the linters
check-lint:
	bandit -c pyproject.toml -r -f custom ${LIBS_DIR}
	isort -c ${LIBS_DIR}
	black --check ${LIBS_DIR}
	flake8 ${LIBS_DIR}
	pytest --dead-fixtures
	mypy ${LIBS_DIR}

#--------------------------------------- TESTS -----------------------------------
.PHONY: tests # Run all tests
tests:
	@pytest -v

.PHONY: tests-all # Run all tests
time-tests:
	@/usr/bin/time -f "%E" -o /dev/tty make tests >/dev/null 2>/dev/null

.PHONY: tests-all # Run all tests with coverage
coverage:
	@pytest --cov-config=pyproject.toml --cov=. --cov-report=term-missing --cov-report=xml

.PHONY: tests-all # Generates coverage report
coverage-html:
	@pytest --cov-config=pyproject.toml --cov=. --cov-report=term-missing --cov-report=html

#------------------------------- UTILS -----------------------------------
.PHONY: clean # Clean all the temporary files
clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f .coverage.NB-SBDEV*
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log
	@rm -f .env.bkp*
