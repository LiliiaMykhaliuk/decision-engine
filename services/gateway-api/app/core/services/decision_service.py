from typing import Any

from sqlalchemy.orm import Session



def create_or_get_decision(
    session: Session,
    *,
    caller_id: str,
    idempotency_key: str,
    personal_number: str,
    request_payload: dict[str, Any],
):
    # TODO: Implement db insert and get logic
    return 1, "test", False
