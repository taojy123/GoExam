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
import re
import datetime
import time



def index(request):
    userid = request.REQUEST.get("userid", "")
    username = request.REQUEST.get("username", "")
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
            if "\n\n" not in s:
                break
            s = s.replace("\n\n", "\n")

        qs = re.split(r"\n\d+?\.", s)
        print len(qs)

        success_count = 0
        for q in qs:
            if read_choice(q):
                success_count += 1
        success = True
    qs_num = Question.objects.all().count() 
    return render_to_response('input.html', locals())


def clean(request):
    for q in Question.objects.all():
        print "delete", q.topic
        q.delete()
    return HttpResponseRedirect("/input")




def create(request):
    # for exam in Exam.objects.filter(userid="99999_99999"):
    #     if (exam.single_count + exam.multiple_count) != exam.qa.count():
    #         exam.delete()
    exam_num = Exam.objects.filter(userid="99999_99999").count()
    return render_to_response('create.html', locals())


def create_exam(request):
    now = datetime.datetime.now()

    num = int(request.REQUEST.get("num", 1))

    for i in range(num):
        try:
            config = open("config.ini").read().strip().split("\n")
            single_count = int(config[0])
            multiple_count = int(config[1])

            exam = Exam()
            exam.userid = "99999_99999"
            exam.username = ""
            exam.single_count = single_count
            exam.multiple_count = multiple_count
            exam.begin_time = now
            exam.save()
            exam.qa.clear()

            single_list = []
            multiple_list = []

            for question in Question.objects.all():
                if question.correct.count():
                    if question.is_multiple:
                        multiple_list.append(question)
                    else:
                        single_list.append(question)
            if single_count:
                single_list = random.sample(single_list, single_count)
            else:
                single_list = []
            if multiple_count:
                multiple_list = random.sample(multiple_list, multiple_count)
            else:
                multiple_list = []
            n = 0
            for question in single_list + multiple_list:
                n += 1
                print n
                qa = QA()
                qa.num = n
                qa.question = question
                qa.save()
                qa.answer.clear()
                exam.qa.add(qa)
            exam.save()
            time.sleep(1)
        except Exception, e:
            try:
                exam.delete()
            except:
                pass
            print "recreate"

    return HttpResponseRedirect("/create")



def del_exam(request):
    Exam.objects.filter(userid="99999_99999").delete()
    return HttpResponseRedirect("/create")






def read_choice(q):
    try:
        q = q.strip()
        lines = q.split("\n")
        topic = lines[0]

        corrects = lines[1].replace("Answer", "").strip()

        question = Question(topic=topic)
        question.save()
        question.answer.clear()
        question.correct.clear()

        for answer in lines[2:]:
            label, desc = answer.split(".", 1)
            a = Answer(label=label, desc=desc)
            a.save()
            question.answer.add(a)
            if label in corrects:
                question.correct.add(a)

        question.save()

        print "success", topic

    except:
        print "error", topic
        traceback.print_exc()
        return

    return True





def begin(request):
    
    while True:
        try:
            now = datetime.datetime.now()

            userid = request.REQUEST.get("userid")
            username = request.REQUEST.get("username")
            submit = request.REQUEST.get("submit")
            
            config = open("config.ini").read().strip().split("\n")
            single_count = int(config[0])
            multiple_count = int(config[1])

            if Exam.objects.filter(userid=userid).count():
                if submit == u"开始考试":
                    Exam.objects.filter(userid=userid).delete()
                else:
                    exam = Exam.objects.get(userid=userid)
                    return HttpResponseRedirect("/question/?exam_id=%s" % exam.id)

            if Exam.objects.filter(userid="99999_99999").count():
                exam = Exam.objects.filter(userid="99999_99999")[0]
                exam.userid = userid
                exam.username = username
                exam.begin_time = now
                exam.save()
                return HttpResponseRedirect("/question/?exam_id=%s" % exam.id)

            exam = Exam()
            exam.userid = userid
            exam.username = username
            exam.single_count = single_count
            exam.multiple_count = multiple_count
            exam.begin_time = now
            exam.save()
            exam.qa.clear()

            single_list = []
            multiple_list = []

            for question in Question.objects.all():
                if question.correct.count():
                    if question.is_multiple:
                        multiple_list.append(question)
                    else:
                        single_list.append(question)

            if single_count:
                single_list = random.sample(single_list, single_count)
            else:
                single_list = []
            if multiple_count:
                multiple_list = random.sample(multiple_list, multiple_count)
            else:
                multiple_list = []
                
            n = 0

            for question in single_list + multiple_list:
                n += 1
                print n
                qa = QA()
                qa.num = n
                qa.question = question
                qa.save()
                qa.answer.clear()
                exam.qa.add(qa)
            exam.save()
            time.sleep(1)
            break
        except Exception, e:
            try:
                exam.delete()
            except:
                pass
            print "retry"
            print e
    return HttpResponseRedirect("/question/?exam_id=%s" % exam.id)



def question(request):
    n = 0
    while True:
        try:
            now = datetime.datetime.now()
            today = now

            exam_id = request.REQUEST.get("exam_id")
            question_num = request.REQUEST.get("question_num", 1)
            answer_ids = request.REQUEST.getlist("answer_id")

            exam = Exam.objects.get(id=exam_id)
            question_num = int(question_num)
            if question_num > exam.question_count or question_num < 1:
                question_num = 1
            qa = exam.qa.get(num=question_num)
            question = qa.question

            remain_seconds = 1850 - ( (now - exam.begin_time).seconds + (now - exam.begin_time).days * 3600 *24 )
            break
        except:
            time.sleep(500)
            n += 1
            if n > 10:
                return HttpResponseRedirect("/")
    return render_to_response('question.html', locals())



def add_answer(request):

    while True:
        try:
            exam_id = request.REQUEST.get("exam_id")
            question_num = request.REQUEST.get("question_num", 1)
            answer_id = request.REQUEST.get("answer_id")

            answer = Answer.objects.get(id=answer_id)
            exam = Exam.objects.get(id=exam_id)
            question_num = int(question_num)
            qa = exam.qa.get(num=question_num)
            if qa.question.is_multiple:
                if answer in qa.answer.all():
                    qa.answer.remove(answer)
                else:
                    qa.answer.add(answer)
            else:
                qa.answer.clear()
                qa.answer.add(answer)
            break
        except:
            pass
    return HttpResponseRedirect("/question/?exam_id=%s&question_num=%s" % (exam_id, question_num))


def del_answer(request):

    while True:
        try:
            exam_id = request.REQUEST.get("exam_id")
            question_num = request.REQUEST.get("question_num", 1)
            answer_id = request.REQUEST.get("answer_id")

            answer = Answer.objects.get(id=answer_id)
            exam = Exam.objects.get(id=exam_id)
            question_num = int(question_num)
            qa = exam.qa.get(num=question_num)
            if qa.question.is_multiple:
                qa.answer.remove(answer)
            break
        except:
            pass
    return HttpResponseRedirect("/question/?exam_id=%s&question_num=%s" % (exam_id, question_num))




def finish(request):

    while True:
        try:
            exam_id = request.REQUEST.get("exam_id")
            exam = Exam.objects.get(id=exam_id)
            score = 0
            for qa in exam.qa.all():
                if qa.is_right:
                    if qa.question.is_multiple:
                        score += 2
                    else:
                        score += 1
            exam.score = score
            exam.is_end = True
            exam.save()
            break
        except:
            pass
    return HttpResponseRedirect("/question/?exam_id=%s" % exam.id)



