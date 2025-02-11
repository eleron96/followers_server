# Имя образа и контейнера
IMAGE_NAME=linkedin_project
CONTAINER_NAME=linkedin_project_container

# Переменные для развертывания
SERVER_USER=root
SERVER_IP=194.35.119.49

ARCHIVE=linkedin_project_files.tar.gz
REMOTE_DIR=/root
DOCKER_IMAGE=linkedin_project:latest

# Загрузка переменных из .env
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: build stop run update deploy_all package copy deploy clean deploy-script

# Локальная сборка Docker-образа
build:
	docker build -t $(IMAGE_NAME) .

# Локальная остановка и удаление контейнера
stop:
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true

# Локальный запуск нового контейнера (добавили --shm-size=2g)
run: stop build
	docker run -d --name $(CONTAINER_NAME) \
		--shm-size=2g \
		-v /var/lib/followers_data:/var/lib/followers_data \
		-p $(APP_PORT):$(APP_PORT) \
		--env-file .env \
		$(IMAGE_NAME)


# Локальное обновление (перезапуск контейнера)
update: run

# Полное развертывание на удаленном сервере
deploy_all: package copy deploy

# Упаковка проекта в архив
package:
	@echo "Packaging files..."
	tar czvf $(ARCHIVE) Dockerfile pyproject.toml poetry.lock src \
		tests chromedriver Makefile README.md cookies.json \
		linkedin_token_cache.json

# Копирование архива и переменных окружения на удаленный сервер
copy:
	@echo "Copying archive and .env to remote server..."
	scp $(ARCHIVE) $(SERVER_USER)@$(SERVER_IP):$(REMOTE_DIR)/
	scp .env $(SERVER_USER)@$(SERVER_IP):$(REMOTE_DIR)/

# Развертывание на удаленном сервере
deploy: deploy-script
	@echo "Deploying on remote server..."
	ssh $(SERVER_USER)@$(SERVER_IP) 'bash -s' < deploy.sh

# Создание скрипта развертывания на удаленном сервере (добавили --shm-size=2g)
deploy-script:
	@echo "Creating deploy script..."
	@echo 'cd $(REMOTE_DIR)' > deploy.sh
	@echo 'tar xzvf $(ARCHIVE)' >> deploy.sh
	@echo 'docker build -t $(DOCKER_IMAGE) .' >> deploy.sh
	@echo 'docker stop $(CONTAINER_NAME) || true' >> deploy.sh
	@echo 'docker rm $(CONTAINER_NAME) || true' >> deploy.sh
	@echo 'docker run --name $(CONTAINER_NAME) -d --restart always --shm-size=2g \
		-v /var/lib/followers_data:/var/lib/followers_data \
		-p $(APP_PORT):$(APP_PORT) --env-file .env $(DOCKER_IMAGE)' >> deploy.sh

# Очистка временных файлов локально
clean:
	@echo "Cleaning up..."
	rm -f $(ARCHIVE) deploy.sh
