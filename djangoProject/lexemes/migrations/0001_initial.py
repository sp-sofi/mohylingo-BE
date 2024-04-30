# Generated by Django 5.0.4 on 2024-04-14 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('levels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lexeme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField()),
                ('translation', models.CharField()),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels.level')),
            ],
        ),
    ]