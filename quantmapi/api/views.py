from urllib import request, response
from django.shortcuts import render
from rest_framework import generics
from .models import ChartData
from .serializers import ChartDataSerializer
from rest_framework.response import Response
import pandas as pd
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

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


# populate and return price data with RSI values
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

        

# populate and return price data with MACD values
def calculate_macd(price_data, fast_ema = 12, slow_ema = 26, remove_extra_columns = True, return_raw = False):
    df = pd.DataFrame(price_data)
    df['ema_'+str(fast_ema)] = df['close'].ewm(span=fast_ema, adjust=False).mean()
    df['ema_'+str(slow_ema)] = df['close'].ewm(span=slow_ema, adjust=False).mean()
    df['macd'] = df['ema_'+str(fast_ema)] - df['ema_'+str(slow_ema)]
    df = df.fillna(0.0)
    if return_raw:
        return df
    if remove_extra_columns:
        df = df.drop(['ema_'+str(fast_ema), 'ema_'+str(slow_ema), 'positive_changes', 'negative_changes', 'average_gain', 'average_loss'], axis=1)
    return df.to_dict('records')



# authenticated users only
class ChartDataListCreate(generics.ListCreateAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer
    permission_classes = [IsAuthenticated]

# display and modify/delete entry by entry id, authenticated users only
class ChartDataRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


# list entries by ticker, authenticated users only
class ChartDataListTicker(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ticker = self.kwargs['ticker']
        return ChartData.objects.filter(ticker=ticker)

    def get(self, request, ticker):
        queryset = self.get_queryset()
        serializer = ChartDataSerializer(queryset, many=True)
        return Response(serializer.data)


# list entries by ticker and timeframe, 5 minute delay for non-authenticated users
class ChartDataListTickerTimeframe(generics.ListAPIView):
    
    def get_queryset(self):
        ticker = self.kwargs['ticker']
        timeframe = self.kwargs['timeframe']
        return ChartData.objects.filter(ticker=ticker, timeframe=timeframe)

    def get(self, request, ticker, timeframe):
        if self.request.user.is_authenticated:
            queryset = self.get_queryset()
            serializer = ChartDataSerializer(queryset, many=True)
            filtered_data = serializer.data
            
            rsi_added_data = calculate_rsi(filtered_data)
            rsi_macd_added_data = calculate_macd(rsi_added_data)
            return Response(rsi_macd_added_data)
        else:
            cache_store = ticker + '_' + str(timeframe) + '_rsi_macd_added_data'
            if cache_store in cache:
                return Response(cache.get(cache_store))
            else:
                queryset = self.get_queryset()
                serializer = ChartDataSerializer(queryset, many=True)
                filtered_data = serializer.data
                
                rsi_added_data = calculate_rsi(filtered_data)
                rsi_macd_added_data = calculate_macd(rsi_added_data)
                cache.set(cache_store, rsi_macd_added_data, timeout=300)
                return Response(rsi_macd_added_data)
    

# list Indicator Values by ticker and timeframe
class ChartDataListTickerIndicator(generics.ListAPIView):
    
    def get_queryset(self):
        ticker = self.kwargs['ticker']
        timeframe = self.kwargs['timeframe']
        return ChartData.objects.filter(ticker=ticker, timeframe=timeframe)

    def get(self, request, ticker, timeframe, indicator):
        if self.request.user.is_authenticated:
            queryset = self.get_queryset()
            serializer = ChartDataSerializer(queryset, many=True)
            if indicator.lower() == 'rsi':
                rsi_added_data = calculate_rsi(serializer.data)
                df = pd.DataFrame(rsi_added_data)
                df = df.fillna(0.0)
                df = df.drop([
                    'positive_changes', 
                    'negative_changes', 
                    'average_gain', 
                    'average_loss',
                    'open',
                    'high',
                    'low',
                    'close',
                    'volume',
                    'macd',
                    ], axis=1)
                return Response(df.to_dict('records'))       
            elif indicator.lower() == 'macd':
                macd_added_data = calculate_macd(serializer.data, 12, 26, False, True)
                df = macd_added_data.drop([
                    'open',
                    'high',
                    'low',
                    'close',
                    'volume',
                    'rsi',
                    'ema_'+str(12), 
                    'ema_'+str(26),
                    ], axis=1)
                return Response(df.to_dict('records'))
        else:
            if indicator.lower() == 'rsi':
                cache_store = ticker + '_' + str(timeframe) + '_rsi_data'
                if cache_store in cache:
                    return Response(cache.get(cache_store))
                else:
                    queryset = self.get_queryset()
                    serializer = ChartDataSerializer(queryset, many=True)
                    rsi_added_data = calculate_rsi(serializer.data)
                    df = pd.DataFrame(rsi_added_data)
                    df = df.fillna(0.0)
                    df = df.drop([
                        'positive_changes', 
                        'negative_changes', 
                        'average_gain', 
                        'average_loss',
                        'open',
                        'high',
                        'low',
                        'close',
                        'volume',
                        'macd',
                        ], axis=1)
                    final_data = df.to_dict('records')
                    cache.set(cache_store, final_data, timeout=300)
                    return Response(final_data)
            
            elif indicator.lower() == 'macd':
                cache_store = ticker + '_' + str(timeframe) + '_macd_data'
                if cache_store in cache:
                    return Response(cache.get(cache_store))
                else:
                    queryset = self.get_queryset()
                    serializer = ChartDataSerializer(queryset, many=True)
                    macd_added_data = calculate_macd(serializer.data, 12, 26, False, True)
                    df = macd_added_data.drop([
                        'open',
                        'high',
                        'low',
                        'close',
                        'volume',
                        'rsi',
                        'ema_'+str(12), 
                        'ema_'+str(26),
                        ], axis=1)
                    final_data = df.to_dict('records')
                    cache.set(cache_store, final_data, timeout=300)
                    return Response(final_data)
            