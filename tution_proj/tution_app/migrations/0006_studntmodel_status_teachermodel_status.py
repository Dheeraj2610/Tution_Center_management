# Generated by Django 4.2.5 on 2023-11-03 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tution_app', '0005_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='studntmodel',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teachermodel',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
