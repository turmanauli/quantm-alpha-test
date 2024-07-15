from django.http import HttpResponse
from django.template import loader
import time
import websocket
import json
import datetime
from api.models import ChartData

def save_to_db(symbol, interval, open, high, low, close, volume, time):
    if(symbol and interval and open and high and low and close and volume and time):
        calculated_tf = 1 if interval == '1m' else (5 if interval == '5m' else 60)   
        chart_data = ChartData(
            ticker=symbol,
            open=open,
            high=high,
            low=low,
            close=close,
            volume=volume,
            timeframe=calculated_tf,
            date=time 
            )
        chart_data.save()


def on_open(ws):
    print('websocket connection opened: ', ws)

def on_close(ws, close_status_code, close_msg):
    print('websocket connection closed: ', close_msg)

def on_message(ws, message):
    object = json.loads(message)
    if('k' in object):
        symbol = str(object['k']['s'])
        interval = object['k']['i']
        open = object['k']['o']
        high = object['k']['h']
        low = object['k']['l']
        close = object['k']['c']
        volume = object['k']['v']
        open_time = object['k']['t']
        close_time = object['k']['T']
        try:
            save_to_db(symbol, interval, open, high, low, close, volume, close_time)
        except Exception as e:
            print('error: ', e)
        print('websocket message: ', symbol, interval, open, high, low, close)

def on_error(ws, error):
    print('websocket error: ', error)
    ws.close()

def connect(ticker, interval=1):
    if(ticker):
        interval_str = '1m' if interval is 1 else '5m' if interval is 5 else '1h'
        stream = "wss://stream.binance.com:9443/ws/" + ticker.lower() + "@kline_" + interval_str
        print('subscribing to: ', stream)
        ws = websocket.WebSocketApp(stream, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
        ws.run_forever()


# Create your views here.
def main_view(request):
    t = loader.get_template("index.html")
    e = loader.get_template("error.html")
    ticker =  request.GET.get('ticker')
    interval = int(request.GET.get('interval'))
    if(ticker):
        print('Subscribing to ticker: ', ticker)
        c = {"ticker": ticker}
        if(interval):
            c = {"ticker": ticker, "interval": interval}
            connect(ticker, interval)
        else:
            connect(ticker)
        return HttpResponse(t.render(c, request), content_type="text/html")
    return HttpResponse(e.render({}, request), content_type="text/html")