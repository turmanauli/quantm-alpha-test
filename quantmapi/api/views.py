from django.shortcuts import render
from rest_framework import generics
from .models import ChartData
from .serializers import ChartDataSerializer

# Create your views here.
class ChartDataListCreate(generics.ListCreateAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer


class ChartDataListCreate(generics.ListCreateAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer
    lookup_field = 'ticker'

class ChartDataListCreate(generics.ListCreateAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer
    lookup_fields = ['ticker', 'timeframe']


class ChartDataRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer
    lookup_field = 'pk'