from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.ChartDataListCreate.as_view(), name='chart-data-view')
]