# Generated by Django 4.2.3 on 2023-07-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]