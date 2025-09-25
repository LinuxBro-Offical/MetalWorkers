import sys
from pathlib import Path

# Add the project root to sys.path to ensure modules can be imported
# Assuming this script is run from the project root (metalworkers-api)
project_root = Path(__file__).resolve().parents[1] # Go up two levels to reach metalworkers-api
sys.path.insert(0, str(project_root))

from sqlmodel import Session, create_engine, select, SQLModel
from accounts.models import Service
from settings.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def add_services():
    create_db_and_tables()

    services_to_add = [
        Service(name="Aluminum Roofing"),
        Service(name="Car Porch"),
        Service(name="Grills"),
        Service(name="Compound Wall Gates"),
    ]

    with Session(engine) as session:
        for service in services_to_add:
            existing_service = session.exec(
                select(Service).where(Service.name == service.name)
            ).first()
            if not existing_service:
                session.add(service)
                print(f"Added service: {service.name}")
            else:
                print(f"Service already exists: {service.name}")
        session.commit()

if __name__ == "__main__":
    add_services() 