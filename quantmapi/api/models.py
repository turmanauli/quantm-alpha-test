from django.db import models

# Create your models here.
class ChartData(models.Model):
    ticker = models.CharField(max_length=100)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    rsi = models.FloatField(null=True)
    macd = models.FloatField(null=True)
    timeframe = models.IntegerField()
    date = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker
