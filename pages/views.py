from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth

from .models import Clients
from panel.models import Group, Lesson, Student, Homework, Test, TestAnswer, TestStudent, TestItem
import os


########################################################
def index(requests):
    return render(requests, 'pages/index.html', {})


@login_required(login_url='index')
def dashboard(requests):
    lessons = Lesson.objects.filter(group=requests.user.student.group)
    hws = Homework.objects.filter(student=Student.objects.get(user_id=requests.user.id))
    tests = Test.objects.filter(avaible=True, group=Group.objects.get(title=requests.user.student.group))
    context = {
        'lessons': lessons,
        'hws': hws,
        'tests': tests,
    }
    return render(requests, 'pages/dash.html', context)


@login_required(login_url='index')
def dashboard_test(requests, id):
    test = Test.objects.get(id=id, avaible=True, group=Group.objects.get(title=requests.user.student.group))
    try:
        flag = TestStudent.objects.get(test=Test.objects.get(id=id),
                                       student=Student.objects.get(user_id=requests.user.id))
        if flag.avaible == False:
            return redirect('dashboard')
    except:
        pass

    context = {
        'test': test,
    }
    return render(requests, 'pages/dashboard_test.html', context)


def dashboard_answer(requests):
    if requests.method == "POST":
        t = TestItem.objects.filter(test=Test.objects.get(id=requests.POST['test_id']))
        count = 0
        ts = TestStudent.objects.create(
            test=Test.objects.get(id=requests.POST['test_id']),
            student=Student.objects.get(user_id=requests.user.id),
            point='Не проверена',
            avaible=False,
        )
        for i in requests.POST:
            if i == 'csrfmiddlewaretoken':
                continue
            if i == 'test_id':
                continue
            print(requests.POST['{}'.format(i)])
            TestAnswer.objects.create(
                test=Test.objects.get(id=requests.POST['test_id']),
                student=Student.objects.get(user_id=requests.user.id),
                answer=requests.POST['{}'.format(i)],
                question=t[count].title,
                teststudent=TestStudent.objects.get(id=ts.id)
            )
            count += 1

        messages.success(requests, 'Тест отправлен')
        return redirect('dashboard')
    messages.error(requests, 'Тест не отправлен')
    return redirect('dashboard')


@login_required
def upload_hws(request):
    if request.method == "POST" and request.FILES['upload']:
        upload = request.FILES['upload']
        p = Homework.objects.create(
            student=Student.objects.get(user_id=request.user.id),
            group=Group.objects.get(title=request.POST['group']),
            upload=upload
        )
        p.save()
        messages.success(request, 'Успешно отправленно')
        return redirect('dashboard')
    messages.error(request, 'Что то пошло не так, не загрузилась')
    return redirect('dashboard')


@login_required
def delete_self_hws(requests, id):
    hws = Homework.objects.get(
        id=id,
        student=Student.objects.get(user_id=requests.user.id),
    )
    os.system('rm {}'.format(hws.upload.path))
    hws.delete()
    messages.success(requests, 'Успешна удалена')
    return redirect('dashboard')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name'].title()
        number = request.POST['number']
        email = request.POST['email']
        client = Clients(name=name, number=number, email=email)
        client.save()
        messages.success(request, 'Успешно отправлено')
        return render(request, 'pages/index.html', {'anchor': 'check'})
    return redirect('index')


########################################################## Auth
def login(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.last_name == 'Администратор':
                return redirect('panel')
            messages.success(request, 'Добро пожаловать {}'.format(request.user.student.fname))
            return redirect('dashboard')

    return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')


########################################################## 404
def handler404(request):
    return render(request, '404.html', status=404)
