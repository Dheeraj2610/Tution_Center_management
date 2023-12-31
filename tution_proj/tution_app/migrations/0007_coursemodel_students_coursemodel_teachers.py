# Generated by Django 4.2.5 on 2023-11-04 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tution_app', '0006_studntmodel_status_teachermodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemodel',
            name='students',
            field=models.ManyToManyField(blank=True, to='tution_app.studntmodel'),
        ),
        migrations.AddField(
            model_name='coursemodel',
            name='teachers',
            field=models.ManyToManyField(blank=True, to='tution_app.teachermodel'),
        ),
    ]
