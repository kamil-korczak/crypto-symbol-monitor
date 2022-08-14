import decimal
import json
import websocket


BINANCE_URI = 'wss://stream.binance.com:9443'


class BinancePriceMonitor:

    def __init__(self, symbol, user_price):
        self.symbol = symbol
        self.user_price = user_price


    def on_open(self, ws):
        print("Opened connection")


    def on_message(self, ws, raw_data):
        data = json.loads(raw_data)
        price = data.get('p')
        self.process_price(price)


    def on_error(self, ws, error):
        print(error)


    def on_close(self, ws, close_status_code, close_msg):
        print("### Closed connection ###")


    def process_price(self, price):
        price = decimal.Decimal(price)

        if price > self.user_price:
            print(f'Price of {self.symbol.upper()}: {price}')


    def run(self):
        print(f"Starting monitoring price of {self.symbol.upper()} symbol...")

        uri = f"{BINANCE_URI}/ws/{self.symbol}@trade"
        ws = websocket.WebSocketApp(uri, 
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        ws.run_forever()



