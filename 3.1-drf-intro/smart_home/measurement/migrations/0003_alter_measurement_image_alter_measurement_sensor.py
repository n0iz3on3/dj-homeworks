# Generated by Django 4.1.5 on 2023-01-17 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0002_rename_sensor_id_measurement_sensor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='measurement/measurements', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='sensor',
            field=models.ForeignKey(db_column='sensor', on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='measurement.sensor'),
        ),
    ]