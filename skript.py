import time
import logging
import requests
import os
import json

API_KEY = ""

timestr = time.strftime("%Y%m%d-%H%M%S")
logging.basicConfig(
    filename=f'{__file__.replace(".py", "")}.log',
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)


def download_data(name, timestamp_from, timestamp_to):
    logging.info(f"File {name} does not exist, downloading data.")
    headers = {"X-CoinAPI-Key": API_KEY}
    period = "period_id=5MIN"
    time_start = f"time_start={timestamp_from}"
    time_end = f"time_end={timestamp_to}"
    limit = "limit=10000"
    url = f"https://rest.coinapi.io/v1/ohlcv/BTC/EUR/history?{period}&{time_start}&{time_end}&{limit}"
    response = requests.get(url, headers=headers)
    if not response.ok:
        print(response.content.decode())
        exit(1)
    with open(name, "w") as f:
        json.dump(response.json(), f)


def get_filename(from_time, to_time):
    timestamp_from = f"{from_time.split()[0]}T{from_time.split()[1]}:00"
    timestamp_to = f"{to_time.split()[0]}T{to_time.split()[1]}:00"
    name = f"{timestamp_from}-{timestamp_to}.json"
    if os.path.exists(name):
        return name
    download_data(name, timestamp_from, timestamp_to)
    return name


def get_rates(from_time, to_time):
    filename = get_filename(from_time, to_time)
    with open(filename, "r") as f:
        for record in json.load(f):
            yield record["price_close"]


for rate in get_rates(from_time="2021-03-18 18:45", to_time="2021-03-26 18:45"):
    print(rate)

