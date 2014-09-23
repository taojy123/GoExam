# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *
import os
import uuid
import random
import traceback



def index(request):
    question_id = request.REQUEST.get("question_id")
    if question_id:
        question = Question.objects.get(id=question_id)
    else:
        questions = Question.objects.order_by("id")
        if not questions:
            return HttpResponseRedirect("/input/")
        question = questions[0]
    prev_id = question.id - 1
    next_id = question.id + 1
    if not Question.objects.filter(id=prev_id):
        prev_id = ""
    if not Question.objects.filter(id=next_id):
        next_id = ""
    return render_to_response('index.html', locals())



def answer(request):
    question_id = request.REQUEST.get("question_id")
    answer_ids = request.REQUEST.getlist("answer_id")
    question = Question.objects.get(id=question_id)
    answer_ids.sort()

    corrects = question.correct.all()
    correct_ids = list(corrects.values_list("id", flat=True))
    correct_ids = [str(cid) for cid in correct_ids]
    correct_ids.sort()

    if answer_ids == correct_ids:
        next_id = int(question_id) + 1
        if not Question.objects.filter(id=next_id):
            return HttpResponseRedirect("/")
        return HttpResponseRedirect("/?question_id=%d" % next_id)

    wrong = True
    prev_id = question.id - 1
    next_id = question.id + 1
    if not Question.objects.filter(id=prev_id):
        prev_id = ""
    if not Question.objects.filter(id=next_id):
        next_id = ""

    return render_to_response('index.html', locals())



def input_view(request):
    qs_num = Question.objects.all().count()
    return render_to_response('input.html', locals())


def input_file(request):
    print "-----------------------------------"
    f = request.FILES.get("file")
    if f:
        s = f.read()
        s = s.decode("gbk")
        s = s.strip()
        s = s.replace("\r", "")
        while True:
            if "\n\n\n" not in s:
                break
            s = s.replace("\n\n\n", "\n\n")
        qs = s.split("\n\n")
        success_count = 0
        for q in qs:
            q = q.strip()
            if "\n" in q:
                if read_choice(q):
                    success_count += 1
            else:
                if read_judge(q):
                    success_count += 1
        success = True
    qs_num = Question.objects.all().count() 
    return render_to_response('input.html', locals())


def clean(request):
    for q in Question.objects.all():
        print "delete", q.topic
        q.delete()
    return HttpResponseRedirect("/input")



def read_choice(q):
    try:
        if not q.count("A"):
            raise

        i = q.find("\n")
        topic = q[:i].strip()
        answers = q[i:].replace("A", "|").replace("B", "|").replace("C", "|").replace("D", "|").replace("E", "|")
        answers = answers.split("|")

        topic_show = topic.replace("A", " ").replace("B", " ").replace("C", " ").replace("D", " ").replace("E", " ")

        if Question.objects.filter(topic=topic_show):
            print "exist", topic
            return

        question = Question(topic=topic_show)
        question.save()
        question.answer.clear()
        question.correct.clear()

        if len(answers) > 1:
            da = answers[1].strip()
            aa = Answer(label="A", desc=da)
            aa.save()
            question.answer.add(aa)

        if len(answers) > 2:
            db = answers[2].strip()
            ab = Answer(label="B", desc=db)
            ab.save()
            question.answer.add(ab)

        if len(answers) > 3:
            dc = answers[3].strip()
            ac = Answer(label="C", desc=dc)
            ac.save()
            question.answer.add(ac)

        if len(answers) > 4:
            dd = answers[4].strip()
            ad = Answer(label="D", desc=dd)
            ad.save()
            question.answer.add(ad)

        if len(answers) > 5:
            de = answers[5].strip()
            ae = Answer(label="E", desc=de)
            ae.save()
            question.answer.add(ae)


        if topic.count("A"):
            question.correct.add(aa)
        if topic.count("B"):
            question.correct.add(ab)
        if topic.count("C"):
            question.correct.add(ac)
        if topic.count("D"):
            question.correct.add(ad)
        if topic.count("E"):
            question.correct.add(ae)

        question.save()

        print "success", topic

    except:
        print "error", topic
        traceback.print_exc()
        return

    return True



def read_judge(q):

    try:

        topic = q

        if (u"√" not in q) and (u"×" not in q):
            raise

        if Answer.objects.filter(label=u"√"):
            at = Answer.objects.get(label=u"√")
        else:
            at = Answer(label=u"√")
            at.save()
            
        if Answer.objects.filter(label=u"×"):
            af = Answer.objects.get(label=u"×")
        else:
            af = Answer(label=u"×")
            af.save()

        topic_show = topic.replace(u"√", " ").replace(u"×", " ")
        if Question.objects.filter(topic=topic_show):
            print "exist", topic
            return

        question = Question(topic=topic_show)
        question.save()
        question.answer.clear()
        question.correct.clear()
        
        question.answer.add(at)
        question.answer.add(af)

        if topic.count(u"√"):
            question.correct.add(at)
        elif topic.count(u"×"):
            question.correct.add(af)

        question.save()

        print "success", topic

    except:
        print "error", topic
        traceback.print_exc()
        return

    return True




