from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=20, verbose_name='Датчик')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата установки')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, db_column='sensor', related_name='measurements')
    temperature = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Температура')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата измерения температуры')
    image = models.ImageField(null=True, upload_to='measurement/measurements', blank=True, verbose_name='Изображение')