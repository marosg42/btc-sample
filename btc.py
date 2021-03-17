import requests
import yaml
from yaml.parser import ParserError


def get_data(crypto="BTC", fiat="EUR"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={crypto}{fiat}"
    response = requests.get(url)
    if not response.ok:
        result = f"Cannot get {crypto}{fiat} rate"
    else:
        rate = float(response.json()["price"])
        if fiat == "EUR":
            actual = rate * my_crypto[crypto]["volume"]
            difference = actual - my_crypto[crypto]["paid"]
        else:
            actual = 0
            difference = 0
        result = f"{crypto}{fiat}\t{rate:10.2f}\t{actual:10.2f} {fiat}\t diff {difference:+10.2f}"
    return result


try:
    my_crypto = yaml.load(open("data.yaml"), Loader=yaml.FullLoader)
except IOError as e:
    print(e)
    exit(1)
except ParserError as e:
    print("Error parsing yaml file")
    print(e)
    exit(2)

print(get_data(fiat="USDT"))
for crypto in my_crypto:
    print(get_data(crypto=crypto))
