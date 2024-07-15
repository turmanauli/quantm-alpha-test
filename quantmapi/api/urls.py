from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.ChartDataListCreate.as_view(), name='chart-data-view'),
    path('api/<int:pk>', views.ChartDataRetrieveUpdateDestroy.as_view(), name='chart-data-update'),
    path('api/<str:ticker>', views.ChartDataListTicker.as_view(), name='ticker-data-view'),
    path('api/<str:ticker>/<int:timeframe>', views.ChartDataListTickerTimeframe.as_view(), name='ticker-data-tf-view'),
    path('api/<str:ticker>/<int:timeframe>/<str:indicator>', views.ChartDataListTickerIndicator.as_view(), name='ticker-data-tf-view'),
]