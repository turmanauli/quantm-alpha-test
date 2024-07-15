from urllib import request, response
from django.shortcuts import render
from rest_framework import generics
from .models import ChartData
from .serializers import ChartDataSerializer
from rest_framework.response import Response


# calculate the simple difference between the current price and the previous price
def calculate_difference(current_price, previous_price):
    return current_price - previous_price

# calculate the absolute value above zero
def calculate_positive_change(diff):
    if diff > 0:
        return diff
    return 0

# calculate the absolute value below zero
def calculate_negative_change(diff):
    if diff < 0:
        return diff * -1
    return 0

'''
price_data = [
    {'close': 4, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 5, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 6, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 6, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 7, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 4, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 6, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 8, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 9, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 10, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 9, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 11, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 9, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 13, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 14, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 12, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 11, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 10, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 12, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 13, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 14, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 15, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 16, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 14, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 12, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 10, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 7, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    {'close': 8, 'positive_changes': 0.0, 'negative_changes': 0.0, 'average_gain': 0.0, 'average_loss': 0.0, 'rsi': 0.0},
    ]
'''


# populate RSI indicator values
def calculate_rsi(price_data, rsi_period = 14):
    
    for i in range(len(price_data)):
        current_difference = 0.0
        if i > 0:
            previous_close = price_data[i-1]['close']
            current_close = price_data[i]['close']
            current_difference = calculate_difference(current_close, previous_close)
        price_data[i]['positive_changes'] = calculate_positive_change(current_difference)
        price_data[i]['negative_changes'] = calculate_negative_change(current_difference)

        if i == max(1, rsi_period):
            gain_sum = 0.0
            loss_sum = 0.0

            for x in reversed(range(max(1, rsi_period))):
                gain_sum += price_data[x]['positive_changes']
                loss_sum += price_data[x]['negative_changes']

            price_data[i]['average_gain'] = gain_sum / max(1, rsi_period)
            price_data[i]['average_loss'] = loss_sum / max(1, rsi_period)


        elif i > max(1, rsi_period):
            price_data[i]['average_gain'] = (price_data[i-1]['average_gain'] * (rsi_period - 1) + price_data[i]['positive_changes']) / max(1, rsi_period)
            price_data[i]['average_loss'] = (price_data[i-1]['average_loss'] * (rsi_period - 1) + price_data[i]['negative_changes']) / max(1, rsi_period)
            price_data[i]['rsi'] = 100 if price_data[i]['average_loss'] == 0 else (0 if price_data[i]['average_gain'] == 0 else (100 - (100 / (1 + price_data[i]['average_gain'] / price_data[i]['average_loss'])))) 

    return price_data    

        


def calculate_macd():
    print('calculating_macd')


class ChartDataListCreate(generics.ListCreateAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer

# display and modify/delete entry by entry id
class ChartDataRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer
    lookup_field = 'pk'


# list entries by ticker
class ChartDataListTicker(generics.GenericAPIView):

    def get_queryset(self):
        ticker = self.kwargs['ticker']
        return ChartData.objects.filter(ticker=ticker)

    def get(self, request, ticker):
        queryset = self.get_queryset()
        serializer = ChartDataSerializer(queryset, many=True)
        return Response(serializer.data)


# list entries by ticker and timeframe
class ChartDataListTickerTimeframe(generics.ListAPIView):
    
    def get_queryset(self):
        ticker = self.kwargs['ticker']
        timeframe = self.kwargs['timeframe']
        return ChartData.objects.filter(ticker=ticker, timeframe=timeframe)

    def get(self, request, ticker, timeframe):
        queryset = self.get_queryset()
        serializer = ChartDataSerializer(queryset, many=True)
        filtered_data = serializer.data
        
        rsi_added_data = calculate_rsi(filtered_data)
    
        return Response(rsi_added_data)