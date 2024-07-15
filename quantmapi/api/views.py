from django.shortcuts import render
from rest_framework import generics
from .models import ChartData
from .serializers import ChartDataSerializer

# Create your views here.
class ChartDataListCreate(generics.ListCreateAPIView):
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer