from django.shortcuts import render, redirect, get_object_or_404
from forum.models import Question, Answer
from forum.forms import QuestionForm, AnswerForm
from django.db.models import Q
from collections import OrderedDict
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'forum/home.html')

def latest(request):
    questions = Question.objects.all().order_by('-createDate')
    for question in questions:
        if question.likes.filter(id=request.user.id).exists():
            question.is_liked = True
        else:
            question.is_liked = False
    return render(request, 'forum/latest.html', {"questions": questions})

@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'forum/create.html', {'form': QuestionForm()})
    else:
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('latest')
        else:
            error = "Something went wrong. Try again."
            return render(request, 'forum/create.html', {'form': QuestionForm(), 'error':error})

@login_required
def show_detail(request):
    questions = Question.objects.filter(user=request.user)
    return render(request, 'forum/show_detail.html', {'questions': questions})

@login_required
def myDetail(request, questionId):
    question = get_object_or_404(Question, pk=questionId, user=request.user)
    if request.method == "GET":
        form = QuestionForm(instance=question)
        return render(request, 'forum/myDetail.html', {'form': form, 'question': question})
    else:
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            return redirect('show_detail')
        else:
            error = "Something went wrong."
            return render(request, 'forum/myDetail.html', {'form':form, 'error':error, 'question':question})

@login_required
def delete(request, questionId):
    if request.method=="POST":
        question = get_object_or_404(Question, pk=questionId, user=request.user)
        question.delete()
        return redirect('show_detail')

def detail(request, questionId):
    question = get_object_or_404(Question, pk=questionId)
    if question.likes.filter(id = request.user.id).exists():
        question.is_liked = True
    else:
        question.is_liked = False
    answers = question.answers.all()
    for answer in answers:
        if answer.likes.filter(id = request.user.id).exists():
            answer.is_liked = True
        else:
            answer.is_liked = False
    return render(request,'forum/detail.html', {'question': question, 'answers': answers})

def displaySport(request, sportKey):
    questions = Question.objects.filter(category=sportKey)
    return render(request, 'forum/displaySport.html', {'questions': questions})

def search(request):
    keyWords = request.POST.get('search').split(' ')
    for keyWord in keyWords:
        querySet = Question.objects.filter(Q(title__icontains=keyWord) | Q(desc__icontains=keyWord))
        try:
            questions = questions | querySet
        except:
            questions = querySet
    questions.order_by("-createDate")
    noDuplicates = list(OrderedDict.fromkeys(questions))
    return render(request, 'forum/latest.html', {'questions': noDuplicates})

@login_required
def createAnswer(request, questionId):
    question = get_object_or_404(Question, pk=questionId)
    if request.method == "GET":
        return render(request, 'forum/create_answer.html', {'form': AnswerForm(), 'question': question})
    else:
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('latest')
        else:
            error = "Something went wrong. Try again."
            return render(request, 'forum/create_answer.html', {'form': AnswerForm(), 'error':error})

@login_required
def edit_answer(request, answerId):
    answer = get_object_or_404(Answer, pk=answerId, user=request.user)
    if request.method == "GET":
        form = AnswerForm(instance=answer)
        return render(request, 'forum/edit_answer.html', {'form': form, 'answer': answer})
    else:
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('show_detail')
        else:
            error = "Something went wrong."
            return render(request, 'forum/edit_answer.html', {'form':form, 'error':error, 'answer':answer})

@login_required
def like(request, questionId):
    question = get_object_or_404(Question, pk=questionId)
    if question.likes.filter(id=request.user.id).exists():
        question.likes.remove(request.user)
    else:
        question.likes.add(request.user)
    return redirect('latest')

def answerLike(request, answerId):
    answer = get_object_or_404(Answer, pk=answerId)
    if answer.likes.filter(id = request.user.id).exists():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return redirect('latest')

def likeAjax(request):
    questionId = request.POST['questionID']
    question = get_object_or_404(Question, pk=questionId)
    if question.likes.filter(id=request.user.id).exists():
        question.likes.remove(request.user)
    else:
        question.likes.add(request.user)
    return redirect('latest')

