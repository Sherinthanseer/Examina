# Generated by Django 4.2.7 on 2024-12-12 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_alter_clock_time_left'),
    ]

    operations = [
        migrations.AddField(
            model_name='descriptiveanswer',
            name='marks_awarded',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
