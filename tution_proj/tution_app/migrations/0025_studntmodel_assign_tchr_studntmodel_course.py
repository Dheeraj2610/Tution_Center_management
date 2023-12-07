# Generated by Django 4.2.5 on 2023-11-09 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tution_app', '0024_remove_studntmodel_assign_tchr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studntmodel',
            name='assign_tchr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students_assigned', to='tution_app.teachermodel'),
        ),
        migrations.AddField(
            model_name='studntmodel',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students_assigned', to='tution_app.coursemodel'),
        ),
    ]