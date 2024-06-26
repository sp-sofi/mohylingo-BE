# Generated by Django 5.0.4 on 2024-04-18 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField()),
                ('questions_learned', models.ManyToManyField(related_name='questions_learned', to='questions.question')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='topics.topic')),
            ],
        ),
    ]
