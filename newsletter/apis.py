from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .models import Newsletter
from db import get_session

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post("/subscribe", response_model=Newsletter)
def subscribe_newsletter(
    *, session: Session = Depends(get_session), newsletter: Newsletter
):
    existing_subscription = session.exec(
        select(Newsletter).where(Newsletter.email == newsletter.email)
    ).first()
    if existing_subscription:
        raise HTTPException(status_code=400, detail="Email already subscribed")

    session.add(newsletter)
    session.commit()
    session.refresh(newsletter)
    return newsletter 