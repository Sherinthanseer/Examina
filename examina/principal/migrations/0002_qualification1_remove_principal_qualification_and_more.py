# Generated by Django 5.1.1 on 2024-09-28 08:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='qualification1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='principal',
            name='qualification',
        ),
        migrations.AddField(
            model_name='principal',
            name='qualificationid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='principal.qualification1'),
        ),
    ]
