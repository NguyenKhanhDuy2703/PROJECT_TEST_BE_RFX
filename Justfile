set shell := ["powershell.exe", "-c"]

install :
    @echo "Building the project..."
    # Add your build commands here
    pip install -r requirements.txt
build :
    @echo "Building the Docker image..."
    docker build -t fastapi-app .
up : 
    @echo "Starting database and redis services  using Docker..."
    docker-compose -f docker-compose.yml up -d
down :
    @echo "Stopping database and redis services using Docker..."
    docker-compose -f docker-compose.yml down
reset-db :
    @echo "Resetting the database..."
    docker-compose -f docker-compose.yml down -v
make-migrate Name:
    @echo "Creating a new migration script named "{{Name}}"..."
    python -m alembic revision --autogenerate -m "{{Name}}"
migrate :
    @echo "Applying database migrations..."
    python -m alembic upgrade head

run : 
    @echo "Running the FastAPI application..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
test :
    @echo "Running tests..."
    pytest -v