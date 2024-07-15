from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.ChartDataListCreate.as_view(), name='chart-data-view'),
    path('api/<int:pk>', views.ChartDataRetrieveUpdateDestroy.as_view(), name='chart-data-update')
]