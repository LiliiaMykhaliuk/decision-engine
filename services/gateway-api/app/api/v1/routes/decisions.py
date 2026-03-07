from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.core.services.decision_service import create_or_get_decision

from app.db.session import get_session
from app.api.deps.request_context import get_caller_id, get_idempotency_key

from app.api.v1.schemas.decision import DecisionCreate


router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/decisions", status_code=202)
def post_decision(
    request: DecisionCreate,
    session: Session = Depends(get_session),
    caller_id=Depends(get_caller_id),
    idempotency_key=Depends(get_idempotency_key)
):

    decision_id, status, _created = create_or_get_decision(
        session,
        caller_id=caller_id,
        idempotency_key=idempotency_key,
        personal_number=request.personal_number,
        request_payload=request.model_dump(),
    )
    return {"decision_id": str(decision_id), "status": status}

