# Generated by Django 4.2.5 on 2023-11-06 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tution_app', '0016_assignment_assignmentsubmission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='student',
        ),
        migrations.DeleteModel(
            name='Assignment',
        ),
        migrations.DeleteModel(
            name='AssignmentSubmission',
        ),
    ]
