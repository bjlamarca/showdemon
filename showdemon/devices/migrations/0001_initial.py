# Generated by Django 5.1.5 on 2025-02-01 05:33

import devices.constants
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('interface', models.CharField(blank=True, choices=devices.constants.Interfaces, max_length=10, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('feature_class', models.CharField(choices=devices.constants.FeatureList, max_length=100)),
                ('system', models.CharField(choices=devices.constants.SystemType, max_length=10)),
                ('sort_order', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Device Feature',
            },
        ),
        migrations.CreateModel(
            name='LibraryDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('system', models.CharField(choices=devices.constants.SystemType, max_length=10)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': ('Device Library',),
                'verbose_name_plural': 'Device Library',
            },
        ),
        migrations.CreateModel(
            name='Manufacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('comments', models.TextField(blank=True, null=True, verbose_name='comments')),
            ],
        ),
        migrations.CreateModel(
            name='LibraryChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('channel_type', models.CharField(choices=devices.constants.ChannelType, max_length=100)),
                ('int_min', models.IntegerField(blank=True, null=True)),
                ('int_max', models.IntegerField(blank=True, null=True)),
                ('str_value', models.CharField(blank=True, max_length=1000)),
                ('parameter', models.CharField(blank=True, max_length=1000)),
                ('sort_order', models.IntegerField()),
                ('device_feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.devicefeature')),
            ],
        ),
        migrations.CreateModel(
            name='ChannelParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('allow_fading', models.BooleanField(default=False)),
                ('int_value', models.IntegerField(blank=True, null=True)),
                ('int_min', models.IntegerField(blank=True, null=True)),
                ('int_max', models.IntegerField(blank=True, null=True)),
                ('str_value', models.CharField(blank=True, max_length=5000, null=True)),
                ('library_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.librarychannel')),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_channel', models.IntegerField(blank=True, null=True)),
                ('channel_number', models.IntegerField()),
                ('int_value', models.IntegerField(blank=True, null=True)),
                ('str_value', models.CharField(blank=True, max_length=1000, null=True)),
                ('parameter', models.CharField(blank=True, max_length=1000, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.device')),
                ('library_channel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.librarychannel')),
            ],
        ),
        migrations.AddField(
            model_name='devicefeature',
            name='library_device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.librarydevice'),
        ),
        migrations.AddField(
            model_name='device',
            name='device_library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.librarydevice'),
        ),
        migrations.AddField(
            model_name='librarydevice',
            name='manufacture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='devices.manufacture'),
        ),
    ]
