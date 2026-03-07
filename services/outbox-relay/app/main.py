import time
from app.relay import process_outbox_batch

POLL_INTERVAL = 2  # seconds

def main():
    while True:
        process_outbox_batch()
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
