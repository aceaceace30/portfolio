# Generated by Django 3.0.5 on 2020-05-04 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_auto_20200505_0117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='slug',
        ),
    ]