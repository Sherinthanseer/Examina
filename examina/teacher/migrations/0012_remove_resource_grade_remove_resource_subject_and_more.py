# Generated by Django 5.0.6 on 2024-12-19 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0011_grade_subject_resource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.DeleteModel(
            name='Resource',
        ),
    ]
