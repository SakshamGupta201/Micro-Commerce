# Generated by Django 4.1.13 on 2024-10-07 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='handle',
            field=models.SlugField(blank=True, max_length=120, unique=True),
        ),
    ]