# DSpot backend test

## Getting the project

Clone the repository

```bash
git clone git@github.com:reinier-millo/dspot-backend.git
cd dspot-backend
```

## Installing dependencies

You can install dependencies using a virtual environment or directly on your machine. To set up a virtual environment:

```bash
python3 -m venv _python
source ./_python/bin/activate
```

To deactivate the virtual environment, use:

```bash
deactivate
```

If you're using a virtual environment, ensure it's activated when running the service.

Install the required dependencies with:

```bash
pip3 install -r requirements-dev.txt
```

For production dependencies only, use `requirements.txt`. Once done, you’re ready to configure and run the service.


## Setting Up the Service

To run the service, you need to configure environment variables. These can be set as system variables or by using a `.env` file (refer to `.env.example`).

Mandatory environment variables don’t have default values, and the service won't run without them. Required variables are marked with **\***.

### General Variables

- `ENVIRONMENT`: The environment where the service runs (`development` or `production`). In development, Swagger API docs will be available at `/docs` and `/redoc`.

### Setting Up the Database

The service uses PostgreSQL. You can install PostgreSQL from:

- [Microsoft Windows](https://www.postgresql.org/download/windows/)
- [MaxOS](https://postgresapp.com/)
- [GNU/Linux](https://www.postgresql.org/download/linux/)
- [Docker Image](https://hub.docker.com/_/postgres)

To configure the database connection, define the following environment variables:

- `* PG_HOST`: Database server hostname or IP address.
- `* PG_PORT`: Database port.
- `* PG_USER`: Database user.
- `* PG_PASSWORD`: Database password.
- `* PG_DB`: Database name.

Database configuration is essential for running the service. The next section explains how to initialize the database schema.

## Running the Service

After setting the environment variables, you can run the service. On first run, you'll need to create the database and apply the data model.

Create the database using the `psql` tool or a UI tool. To create it via `psql`, use:

```bash
psql -h <PG_HOST> -p <PG_PORT> -U <PG_USER> -d <PG_PASSWORD> -c "CREATE DATABASE <PG_DB>"
```

Replace `<PG_HOST>`, `<PG_PORT>`, `<PG_USER>`, `<PG_PASSWORD>` and `<PG_DB>` with your actual values.

To initialize the database schema, run Alembic migrations:

```bash
alembic upgrade head
```

### Run Locally

To run the service locally:

```bash
uvicorn app.main:app --reload
```

By default, the service listens on all interfaces on port **8000**. To change the host or port use:


```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

You can also run the service as a Python script:

```bash
PYTHONPATH=. python3 app/main.py
```

### Running with Docker

To run the service using Docker, build the image:

```bash
docker build -t dspot-backend .
```

If a `.env` file is present before building, it will be included in the image. Otherwise, pass environment variables when running the container.

Run the container:

```bash
docker run -d -p 8000:8000 dspot-backend
```

### Generating Sample Data

To generate random sample data, run:

```bash
PYTHONPATH=. python3 scripts/gen_profiles.py
```

This creates 100 profiles and 150 friend relationships. You can modify the number of profiles and relationships:

```bash
PYTHONPATH=. python3 scripts/gen_profiles.py --total_profiles 200 --total_friends 250
```

## Linting

To run linting with `pylint`, use the `./lint.sh` script, which will activate the virtual environment and run `pylint`:

```bash
./lint.sh
```

## Testing

The project uses `pytest` for testing. To run all tests:

```bash
PYTHONPATH=. pytest -v
```

To run a specific test file, add the relative file path:

```bash
PYTHONPATH=. pytest -v <path_to_test_file>
```

To run tests with coverage:

```bash
PYTHONPATH=. pytest -v --cov=app --cov-report=term
```
