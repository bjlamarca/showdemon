# Generated by Django 5.1.5 on 2025-01-30 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_alter_channelparameter_int_max_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelparameter',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.librarychannel'),
        ),
        migrations.AlterField(
            model_name='librarychannel',
            name='device_feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.devicefeature'),
        ),
    ]
