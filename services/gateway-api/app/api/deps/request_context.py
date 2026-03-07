from fastapi import Header

def get_caller_id(x_caller_id: str = Header(..., alias="X-Caller-Id")) -> str:
    return x_caller_id


def get_idempotency_key(idempotency_key: str = Header(..., alias="Idempotency-Key")) -> str:
    return idempotency_key
