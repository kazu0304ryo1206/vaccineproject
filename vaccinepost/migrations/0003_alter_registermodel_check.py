# Generated by Django 3.2.6 on 2022-01-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinepost', '0002_registermodel_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermodel',
            name='check',
            field=models.BooleanField(),
        ),
    ]