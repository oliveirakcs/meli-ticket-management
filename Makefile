tests:
	@printf "Running tests app/tests/$(TEST_PATH)...\n\n"
	DOCKER_TEST_PATH=app/tests/$(TEST_PATH) docker compose -p meli-backend-test -f docker-compose.test.yml up --build --abort-on-container-exit || (docker compose -p meli-backend-test down --volumes && exit 1)
	docker compose -p meli-backend-test down --volumes --rmi local

containers:
	docker compose -p meli-backend -f docker-compose.dev.yml up --build -d

up:
	docker compose -p meli-backend -f docker-compose.dev.yml up --abort-on-container-exit -d

restart:
	docker compose -p meli-backend -f docker-compose.dev.yml down
	docker compose -p meli-backend -f docker-compose.dev.yml up --build -d