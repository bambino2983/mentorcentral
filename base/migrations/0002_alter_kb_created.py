# Generated by Django 3.2.6 on 2022-06-12 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kb',
            name='created',
            field=models.CharField(max_length=100),
        ),
    ]
