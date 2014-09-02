# -*- coding: utf-8 -*-

from django.db import models


class Answer(models.Model):
    label = models.CharField(max_length=64, blank=True , null=True)
    desc = models.CharField(max_length=255, blank=True , null=True)


class Question(models.Model):
    topic = models.CharField(max_length=255, blank=True , null=True)
    answer = models.ManyToManyField(Answer, related_name="answer_question")
    correct = models.ManyToManyField(Answer, related_name="correct_question")

    @property
    def is_multiple(self):
    	if self.correct.count() > 1:
    		return True
    	return False
