# API for social networking project for YAMDB service
**YAMDB**  collects user feedback on works in the categories "Books", "Movies", "Music".
The project is a web application and a database, raised in two docker containers.

![example workflow](https://github.com/EvansPauliuts/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### 1. Installing and running on the local machine

2. Clone repository
```shell
  https://github.com/EvansPauliuts/yamdb_final.git
```

3. Create and activate a virtual environment for the project
```shell
  python -m venv venv
  source venv/bin/activate
```

#### 4. Install docker и docker-compose
If you already have docker and docker-compose installed, you can skip this step. If not, the installation instructions are https://docs.docker.com/engine/install/

5. Starting the container
```shell
make docker
```
6. Turning off the container
```shell
make down
```

# Examples of use
#### Creating a Django superuser
```shell
docker-compose run app python manage.py createsuperuser
```

#### View API documentation
```shell
  http://127.0.0.1:1337/redoc/
  http://127.0.0.1:1337/swagger/
```