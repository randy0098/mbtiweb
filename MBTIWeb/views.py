# coding:utf-8
'''
Created on Jun 5, 2014

@author: xiafeng
'''

import uuid

from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from paper.models import Question, Option, User_Paper, User_Answer


def index(request):
    return render_to_response('index.html')


def startExam(request):
    if "paper_id" in request.POST:
        paper_id = request.POST["paper_id"]
        if not paper_id:
            message = "fail"
            return HttpResponse(message)
        else:
            serialNo = 1
            userId = uuid.uuid1()
            userPaper = User_Paper(paper_id=paper_id,user_id=userId,serialno=serialNo)
            userPaper.save()
            message = "success"
            #存入session
            request.session["user_paper_id"] = userPaper.id  
            request.session["paper_id"] = paper_id 
            return HttpResponse(message)
        
def question(request):
    paper_id = request.session["paper_id"]
    if "qno" in request.GET and request.GET["qno"]:
        qno = request.GET["qno"]
        qno = int(qno)+1
    else:
        qno = 0
    
    question = Question.objects.filter(paper_id=paper_id)[int(qno)]
    options = Option.objects.filter(question_id=question.id)
    #显示第一道问题时
    if qno == 0:
        #查询试题总数并存入session
        totalNum = len(Question.objects.all())
        request.session["totalNum"] = totalNum  
        return render_to_response('question.html', locals(), RequestContext(request))
    #显示下一道试题
    else:
        return render_to_response('question_content.html', locals())

    
def saveAnswer(request):
    user_paper_id = request.session["user_paper_id"]
    if "question_id" in request.POST and request.POST["question_id"] and "option_id" in request.POST and request.POST["option_id"]:
        question_id = request.POST["question_id"]
        option_id = request.POST["option_id"]
        userAnswer = User_Answer(user_paper_id=user_paper_id,question_id=question_id,option_id=option_id)
        userAnswer.save()
        message = "success"       
        return HttpResponse(message)    
    


