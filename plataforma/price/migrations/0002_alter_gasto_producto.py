# Generated by Django 4.2 on 2024-04-14 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasto',
            name='producto',
            field=models.CharField(max_length=100),
        ),
    ]
