# Generated by Django 5.0.4 on 2024-04-18 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('levels', '0001_initial'),
        ('lexemes', '0001_initial'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField()),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lexemes.lexeme')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels.level')),
                ('options', models.ManyToManyField(related_name='questions', to='lexemes.lexeme')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='topics.topic')),
            ],
        ),
    ]