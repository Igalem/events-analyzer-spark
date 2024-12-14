import csv
import random
import uuid
from datetime import datetime, timedelta


TOTAL_EVENTS = 500
TOTAL_USERS = 20
EVENTS_LAG_TIMERANGE_SEC = 120
EVENTS_DAY_TIMERANGE = 1

URL_HOST = 'https://myfrontsite.com'

URLS = [
    "/search-products",
    "/display-product/1",
    "/display-product/2",
    "/buy-product",
    "/checkout",
    "/home",
    "/contact",
]

EVENT_TYPES = ["start_session", "in-page", "conversion", "end_session"]

TARGET_PATH = 'csv'


def create_user_list(total_users=TOTAL_USERS):
    users = [random.randint(10000, 99999) for _ in range(total_users)]
    return users


def create_ts_list(total_events=TOTAL_EVENTS, day_timerange=EVENTS_DAY_TIMERANGE, timerange=EVENTS_LAG_TIMERANGE_SEC):
    today = datetime.today() - timedelta(days=day_timerange)
    current_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    event_ts = []
    for _ in range(total_events):
        random_second = random.randint(1, timerange)
        current_date += timedelta(seconds=random_second)
        event_ts.append(current_date)
    return event_ts


def create_events():
    events = []
    user_ids = create_user_list()
    event_ts = create_ts_list()

    for i in range(TOTAL_EVENTS):
        user_id = random.choice(user_ids)
        event_type = random.choices(EVENT_TYPES, weights=[0.1, 0.5, 0.4, 0.1])[0]
        url = f"{URL_HOST}{random.choice(URLS)}"

        events.append({
            "event_id": str(uuid.uuid4()),
            "user_id": user_id,
            "timestamp": event_ts[i].strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "url": url,
        })

    return events


def create_csv_file(filename, events):
    with open(filename, mode="w") as file:
    # with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["event_id", "user_id", "timestamp", "event_type", "url"])
        writer.writeheader()
        writer.writerows(events)


if __name__ == "__main__":
    filename = f"{TARGET_PATH}/events.csv"

    print('Creating events.csv file...')
    try:

        events = create_events()
        create_csv_file(filename, events)
        print(f"successfully created filename: {filename}")
    except Exception as e:
        print(f"Unable to create filename: {filename}")
        print(e)
