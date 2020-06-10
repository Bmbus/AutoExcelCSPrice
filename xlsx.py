import pandas as pd
from steampy.client import SteamClient
from steampy.utils import GameOptions
import json
import os

with open("config.json") as file:
    config = json.load(file)

steam_client = SteamClient(config["steam_api_token"])
df = pd.read_excel(config["excel_file"])
prices = []
items = []

for i in df["Name"]:
    if not isinstance(i, float) and not i in config["ignore_words"]:
        items.append(i)
        #print(i)
        if len(items) >= 20:
            print("TOO MUCHHH")
        price = steam_client.market.fetch_price(i, GameOptions.CS)
        if price["success"]:
            prices.append(float(price["median_price"].split(" USD")[0].split("$")[1]) * 0.88)
        elif not price["success"]:
            prices.append(0)

df["Steam"] = pd.Series(prices)

try:
    os.remove(f"copy_{config['excel_file']}")
except:
    pass

df.to_excel(f"copy_{config['excel_file']}") 