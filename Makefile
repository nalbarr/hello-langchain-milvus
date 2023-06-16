help:
	@echo make install-milvus
	@echo make run-milvus
	@echo ""
	@echo make install
	@echo make run

install-milvus:
	wget https://github.com/milvus-io/milvus/releases/download/v2.2.10/milvus-standalone-docker-compose.yml -O docker-compose.yml

run-milvus:
	sudo docker-compose up -d

install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade -r requirements.txt --use-pep517

run:
	python main.py

clean:
	rm -fr ./venv
	rm -fr ./volumes

