# Generated by Django 5.1.5 on 2025-02-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_channelparameter_color_librarychannel_hide'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicefeature',
            name='hide',
            field=models.BooleanField(default=False),
        ),
    ]
