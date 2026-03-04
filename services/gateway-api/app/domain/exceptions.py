class IdempotencyConflict(Exception):
    """Same idempotency key used with different payload."""
    pass
