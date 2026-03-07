from __future__ import annotations

from typing import Any, Tuple

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.domain.exceptions import IdempotencyConflict
from decision_db.models import Decision, DecisionTransition, OutboxEvent


def create_or_get_decision(
    session: Session,
    *,
    caller_id: str,
    idempotency_key: str,
    personal_number: str,
    request_payload: dict[str, Any],
) -> Tuple[Any, str, bool]:
    """
    Returns: (
    - decision_id
    - status
    - created: True if a new decision row was inserted. False if this was an idempotent replay
    """

    stmt = (
        insert(Decision)
        .values(
            caller_id=caller_id,
            idempotency_key=idempotency_key,
            personal_number=personal_number,
            status="RECEIVED",
            request_payload=request_payload,
        )
        .on_conflict_do_nothing(index_elements=["caller_id", "idempotency_key"])
        .returning(Decision.id, Decision.status)
    )

    row = session.execute(stmt).first()

    if row is not None:
        decision_id, status = row

        # Insert Transition
        session.add(
            DecisionTransition(
                decision_id=decision_id,
                from_status=None,
                to_status=status,
            )
        )

        # Insert OutBoxEvent
        session.add(
            OutboxEvent(
                entity_type="decision",
                entity_id=decision_id,
                event_type="DecisionReceived",
                payload={
                    "decision_id": str(decision_id),
                    "caller_id": caller_id,
                    "personal_number": personal_number,
                    "request": request_payload,
                },
            )
        )

        return decision_id, status, True

    # Decision already exists: fetch and validate idempotency consistency
    existing = session.execute(
        select(Decision).where(
            Decision.caller_id == caller_id,
            Decision.idempotency_key == idempotency_key,
        )
    ).scalar_one()

    if existing.personal_number != personal_number or existing.request_payload != request_payload:
        raise IdempotencyConflict()

    return existing.id, existing.status, False
