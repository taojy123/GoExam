# -*- coding: utf-8 -*-

from django.db import models
import datetime

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
        else:
            return False

    @property
    def score(self):
        if self.is_multiple:
            return 2
        else:
            return 1



class QA(models.Model):
    num = models.IntegerField()
    question = models.ForeignKey(Question)
    answer = models.ManyToManyField(Answer)

    @property
    def is_right(self):
        qaas = [a.label for a in self.answer.all()]
        qucs = [a.label for a in self.question.correct.all()]
        qaas.sort()
        qucs.sort()
        # print qaas, qucs
        if qaas == qucs:
            return True
        else:
            return False



class Exam(models.Model):
    userid = models.CharField(max_length=255, blank=True , null=True)
    username = models.CharField(max_length=255, blank=True , null=True)
    single_count = models.IntegerField(default=0)
    multiple_count = models.IntegerField(default=0)
    qa = models.ManyToManyField(QA)
    begin_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    is_end = models.BooleanField(default=False)


    @property
    def question_count(self):
        return self.single_count + self.multiple_count



