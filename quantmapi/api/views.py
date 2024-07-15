from urllib import request, response
from django.shortcuts import render
from rest_framework import generics
from .models import ChartData
from .serializers import ChartDataSerializer
from rest_framework.response import Response

# Create your views here.
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
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer

    def get_queryset(self):
        ticker = self.kwargs['ticker']
        return ChartData.objects.filter(ticker=ticker)

    def get(self, request, ticker):
        queryset = self.get_queryset()
        serializer = ChartDataSerializer(queryset, many=True)
        return Response(serializer.data)


# list entries by ticker and timeframe
class ChartDataListTickerTimeframe(generics.ListAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer
    
    def get_queryset(self):
        ticker = self.kwargs['ticker']
        timeframe = self.kwargs['timeframe']
        return ChartData.objects.filter(ticker=ticker, timeframe=timeframe)

    def get(self, request, ticker, timeframe):
        queryset = self.get_queryset()
        serializer = ChartDataSerializer(queryset, many=True)
        return Response(serializer.data)