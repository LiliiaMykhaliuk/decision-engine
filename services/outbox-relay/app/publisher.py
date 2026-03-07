import json


def publish_event(event):

    message = {
        "event_id": str(event.id),
        "event_type": event.event_type,
        "entity_type": event.entity_type,
        "entity_id": str(event.entity_id),
        "payload": event.payload,
    }

    print("Publishing event:", json.dumps(message))
