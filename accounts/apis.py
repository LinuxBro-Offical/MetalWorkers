from typing import List
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from .router import router
from .models import Lead, Service
from db import get_session


@router.get("/profile")
async def get_profile():
    return {"user": {"id": 1, "name": "Jane Doe"}}


@router.post("/login")
async def login():
    return {"message": "Logged in"}


@router.post("/leads/", response_model=Lead)
def create_lead(*, session: Session = Depends(get_session), lead: Lead):
    session.add(lead)
    session.commit()
    session.refresh(lead)
    return lead


@router.get("/leads/", response_model=List[Lead])
def get_all_leads(*, session: Session = Depends(get_session)):
    leads = session.exec(select(Lead)).all()
    return leads


@router.post("/services/", response_model=Service)
def create_service(*, session: Session = Depends(get_session), service: Service):
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


@router.get("/services/", response_model=List[Service])
def get_all_services(*, session: Session = Depends(get_session)):
    services = session.exec(select(Service)).all()
    return services 