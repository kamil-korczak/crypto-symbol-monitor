import decimal
import json
import websocket
import time


BINANCE_URI = 'wss://stream.binance.com:9443'
RECONNECT_TIME = 60*60*23  # in seconds


class BinancePriceMonitor:

    def __init__(self, symbol, user_price):
        self.timer = None
        self.re_run = False
        self.run_forever_flag = True

        self.symbol = symbol
        self.user_price = user_price

    def on_open(self, ws):
        self.timer = time.time()
        print("Opened connection")

    def on_message(self, ws, raw_data):
        data = json.loads(raw_data)
        price = data.get('p')

        self.process_price(price)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### Closed connection ###")
        # Because on_close was triggered, we know the opcode = 8
        if close_status_code or close_msg:
            print("on_close args:")
            print("close status code: " + str(close_status_code))
            print("close message: " + str(close_msg))

    def on_ping(self, ws, message):
        if int(time.time() - self.timer) > RECONNECT_TIME:
            print(f'Reconnect time {RECONNECT_TIME}s passed.')
            print('In a moment websocket is going to reconnect...')
            self.re_run = True
            ws.close(status=websocket.STATUS_NORMAL)

    def on_pong(self, ws, message):
        pass

    def process_price(self, price):
        price = decimal.Decimal(price)

        if price > self.user_price:
            print(f'Price of {self.symbol.upper()}: {price}')

    def run(self):

        print(f"Starting monitoring price of {self.symbol.upper()} symbol...")

        while self.run_forever_flag or self.re_run:

            if self.re_run:
                self.re_run = False

            uri = f"{BINANCE_URI}/ws/{self.symbol}@trade"
            ws = websocket.WebSocketApp(uri,
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close,
                                        on_ping=self.on_ping,
                                        on_pong=self.on_pong
                                        )

            self.run_forever_flag = ws.run_forever()
