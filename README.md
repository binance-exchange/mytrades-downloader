# Binance Mytrades Downlaoder

This is a small app to download Binance spot mytrades history.
It's not recommended for production, but for demostration only.

## Why this app
Users may need to download trades history for review or tax purpose.  This app can be used to download all trades within the time windows.

## How the csv will looks like

|Local Time|symbol|Side|id|orderId|orderListId|price|qty|quoteQty|commission|commissionAsset|
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
2020-03-10 10:32:57|ATOMBNB|BUY|729810|24907600|-1|0.18050000|1.00000000|0.18050000|0.00013538|BNB|

## How to run

### Install the dependencies

```shell
pip install -r requirements.txt
```

### Set the properties

```shell
cp app.properties.example app.properties

# add API key/secret, timezone, timestamp, etc
```

### Run the script

```shell
python main.py

```

## License
MIT
