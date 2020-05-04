# Generated by Django 3.0.5 on 2020-05-04 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_portfolio_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]
