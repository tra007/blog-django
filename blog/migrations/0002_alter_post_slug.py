# Generated by Django 4.1.5 on 2023-01-03 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.CharField(max_length=250, unique_for_date='publish'),
        ),
    ]
