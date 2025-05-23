# Generated by Django 4.2.7 on 2024-12-11 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_alter_exam_duration_examattempt'),
        ('student', '0007_clock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clock',
            name='title',
        ),
        migrations.AddField(
            model_name='clock',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='teacher.exam'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clock',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
            preserve_default=False,
        ),
    ]
