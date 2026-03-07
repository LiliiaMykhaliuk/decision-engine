from datetime import datetime, timezone
from sqlalchemy import select
from app.db.session import SessionLocal
from decision_db.models import OutboxEvent
from app.publisher import publish_event


BATCH_SIZE = 50


def process_outbox_batch():

    with SessionLocal() as session:

        events = session.execute(
            select(OutboxEvent)
            .where(OutboxEvent.published_at.is_(None))
            .order_by(OutboxEvent.created_at)
            .limit(BATCH_SIZE)
            .with_for_update(skip_locked=True)
        ).scalars().all()

        for event in events:

            try:
                publish_event(event)

                event.published_at = datetime.now(timezone.utc)

            except Exception as e:

                event.publish_attempts += 1
                event.last_error = str(e)

        session.commit()

