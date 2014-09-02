
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *
import os
import uuid
import random

def is_digital(s):
    if s >= "0" and s <= "9":
        return True
    return False


def index(request):
    questions = Question.objects.all()
    question = random.choice(questions)
    return render_to_response('index.html', locals())


def read_data(request):
    # Question.objects.all().delete()
    # Answer.objects.all().delete()
    read_choice("01.txt")
    read_choice("02.txt")
    read_choice("03.txt")
    read_choice("04.txt")
    read_judge("05.txt")
    read_judge("06.txt")
    return HttpResponse("Read Complete!")



def answer(request):
    questions = Question.objects.all()
    question = random.choice(questions)
    return render_to_response('index.html', locals())



def correct(request):
    questions = Question.objects.all()
    question = random.choice(questions)
    return render_to_response('index.html', locals())



def read_choice(fn):
    s = open(fn).read()
    for q in s.split("|||"):

        if q.count("\n") < 2:
            continue

        if not q.count("A"):
            continue

        i = q.find("\n")
        topic = q[:i].strip()
        answers = q[i:].replace("A", "|").replace("B", "|").replace("C", "|").replace("D", "|")
        answers = answers.split("|")

        da = answers[1].strip()
        db = answers[2].strip()
        dc = answers[3].strip()
        dd = answers[4].strip()
        i = dd.find("\n")
        if i > 0:
            dd = dd[:i]

        aa = Answer(label="A", desc=da)
        ab = Answer(label="B", desc=db)
        ac = Answer(label="C", desc=dc)
        ad = Answer(label="D", desc=dd)
        aa.save()
        ab.save()
        ac.save()
        ad.save()

        question = Question(topic=topic.replace("A", " ").replace("B", " ").replace("C", " ").replace("D", " "))
        question.save()
        question.answer.add(aa)
        question.answer.add(ab)
        question.answer.add(ac)
        question.answer.add(ad)

        if topic.count("A"):
            question.correct.add(aa)
        if topic.count("B"):
            question.correct.add(ab)
        if topic.count("C"):
            question.correct.add(ac)
        if topic.count("D"):
            question.correct.add(ad)

        question.save()

        if not question.correct.count():
            question.delete()

        print topic.decode("utf8")

    return "ok"



def read_judge(fn):

    s = open(fn).read()
    for q in s.split("\n"):
        q = q.strip()

        if not q:
            continue

        if is_digital(q[0]) or is_digital(q[1]):
            
            topic = q

            if Answer.objects.filter(label="√"):
                at = Answer.objects.get(label="√")
            else:
                at = Answer(label="√")
                at.save()
                
            if Answer.objects.filter(label="×"):
                af = Answer.objects.get(label="×")
            else:
                af = Answer(label="×")
                af.save()


            question = Question(topic=topic.replace("√", " ").replace("×", " "))
            question.save()
            question.answer.add(at)
            question.answer.add(af)

            if topic.count("√"):
                question.correct.add(at)
            elif topic.count("×"):
                question.correct.add(af)

            question.save()

            print topic.decode("utf8")

    return "ok"




