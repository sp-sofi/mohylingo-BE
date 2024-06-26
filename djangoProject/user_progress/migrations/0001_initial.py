# Generated by Django 5.0.4 on 2024-04-19 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('levels', '0001_initial'),
        ('lexemes', '0001_initial'),
        ('topic_progress', '0002_remove_topicprogress_text'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_in_row', models.IntegerField(default=0)),
                ('chat_id', models.IntegerField(blank=True, null=True)),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels.level')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='topics.topic')),
                ('topic_progresses', models.ManyToManyField(related_name='topic_progresses', to='topic_progress.topicprogress')),
                ('words_learned', models.ManyToManyField(related_name='words_learned', to='lexemes.lexeme')),
            ],
        ),
    ]
