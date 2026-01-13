set shell := ["powershell.exe", "-c"]

install :
    @echo "Building the project..."
    # Add your build commands here
    pip install -r requirements.txt
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
