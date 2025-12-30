import ccxt
import pandas as pd
import requests
import time
import os

SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
SMA_FAST = 5
SMA_SLOW = 20

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

exchange = ccxt.binance()

def send_discord(msg):
    requests.post(DISCORD_WEBHOOK, json={"content": msg})

def bot():
    last_signal = ''
    while True:
        try:
            candles = exchange.fetch_ohlcv(SYMBOL, TIMEFRAME)
            df = pd.DataFrame(candles, columns=[
                'time','open','high','low','close','volume'
            ])

            df['fast'] = df['close'].rolling(SMA_FAST).mean()
            df['slow'] = df['close'].rolling(SMA_SLOW).mean()

            last = df.iloc[-1]
            prev = df.iloc[-2]

            signal = ''

            if prev['fast'] < prev['slow'] and last['fast'] > last['slow']:
                signal = '📈 COMPRA'
            elif prev['fast'] > prev['slow'] and last['fast'] < last['slow']:
                signal = '📉 VENDA'

            if signal and signal != last_signal:
                send_discord(f"{signal} | {SYMBOL} | Preço: {last['close']}")
                last_signal = signal

            time.sleep(60)

        except Exception as e:
            send_discord(f"❌ Erro: {e}")
            time.sleep(60)

if __name__ == "__main__":
    send_discord("🤖 Bot iniciado com sucesso")
    bot()
