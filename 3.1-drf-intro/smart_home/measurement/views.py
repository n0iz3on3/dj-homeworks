from rest_framework import generics
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import Sensor, Measurement
from .serializers import SensorDetailSerializer, MeasurementSerializer, SensorSerializer


class SensorAPIListView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementAPIListView(generics.ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request, *args, **kwargs):
        is_sensor = request.data.get('sensor', None)
        is_temperature = request.data.get('temperature', None)
        if is_sensor and is_temperature:
            try:
                sensor = Sensor.objects.get(id=is_sensor)
                image = request.data.get('image', None)
                data = Measurement.objects.create(sensor=sensor, temperature=is_temperature, image=image)
                data_to_upload = {
                    'sensor': data.sensor.id,
                    'temperature': data.temperature,
                    'created_at': data.created_at,
                }
                return Response(data_to_upload)
            except ObjectDoesNotExist:
                return Response({'ERROR': 'sensor does not exist'})
        return Response({'ERROR': 'does not receive "sensor" or "temperature"'})


class SensorAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer