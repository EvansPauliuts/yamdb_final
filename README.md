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

#### 2. Install docker и docker-compose
If you already have docker and docker-compose installed, you can skip this step. If not, the installation instructions are https://docs.docker.com/engine/install/

5. Starting the container
```shell
make docker_prod
```
6. Turning off the container
```shell
make docker_down
```

# Examples of use

#### Install Django migrate
```shell
docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate
```

#### Install static project
```shell
docker-compose exec app python manage.py collectstatic
```

#### Creating a Django superuser
```shell
docker-compose exec app python manage.py createsuperuser
```

#### Example of initialization of start data
```shell
docker exec <id_container_app> python manage.py dumpdata > fixtures.json
```

#### View API documentation
```shell
  http://62.84.114.33/swagger/
```