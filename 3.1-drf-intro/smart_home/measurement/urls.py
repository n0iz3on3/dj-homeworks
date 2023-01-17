from django.urls import path

from .views import SensorAPIListView, SensorAPIDetailView, MeasurementAPIListView

urlpatterns = [
    path('v1/sensors/', SensorAPIListView.as_view()),
    path('v1/sensors/<int:pk>/', SensorAPIDetailView.as_view()),
    path('v1/measurements/', MeasurementAPIListView.as_view()),
]