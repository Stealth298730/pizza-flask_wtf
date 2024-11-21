import requests


response = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11")
exchenge_json = response.json()

usd_exchenge = [exchenge_dict for exchenge_dict in exchenge_json if exchenge_dict.get("ccy") == "USD"][0]

print(usd_exchenge.get("buy"))