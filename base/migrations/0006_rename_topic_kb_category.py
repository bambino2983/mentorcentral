# Generated by Django 3.2.6 on 2022-06-16 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20220615_1843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kb',
            old_name='topic',
            new_name='category',
        ),
    ]