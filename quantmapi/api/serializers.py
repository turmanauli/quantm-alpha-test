from rest_framework import serializers
from .models import ChartData


class ChartDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartData
        fields = ['id', 'ticker', 'open', 'high', 'low', 'close', 'volume', 'rsi', 'macd', 'timeframe', 'date']


class ChartIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartData
        fields = ['id', 'ticker', 'close', 'rsi', 'macd', 'timeframe', 'date']
