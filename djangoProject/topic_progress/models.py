from django.db import models
from questions.models import Question
from topics.models import Topic


class TopicProgress(models.Model):
    questions_learned = models.ManyToManyField(Question, related_name='questions_learned')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def questions_total(self):
        return Question.objects.filter(topic=self.topic).count()
