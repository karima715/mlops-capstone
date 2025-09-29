import time
import os

LOG_PATH = "logs/inference.log"
WINDOW_SEC = 300  # last 5 minutes
ERROR_KEYWORD = "ERROR"  # demo: look for "ERROR" lines

def count_recent_events():
    if not os.path.exists(LOG_PATH):
        return 0, 0
    cutoff = time.time() - WINDOW_SEC
    total, errors = 0, 0
    with open(LOG_PATH, "r") as f:
        for line in f:
            # naive parsing: assume log lines are appended with \n
            total += 1
            if ERROR_KEYWORD in line:
                errors += 1
    return total, errors

if __name__ == "__main__":
    print(f"Monitoring {LOG_PATH} every 10s (window={WINDOW_SEC}s)")
    while True:
        total, errs = count_recent_events()
        rate = 0.0 if total == 0 else (errs / total) * 100.0
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} total={total} err={errs} rate={rate:.2f}%")
        # here you could send an email or Slack if rate > threshold
        time.sleep(10)
