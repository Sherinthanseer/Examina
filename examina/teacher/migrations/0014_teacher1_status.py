# Generated by Django 5.0.7 on 2025-01-11 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0013_grade_subject_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher1',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
