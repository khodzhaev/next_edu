from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth

from .models import Clients
from panel.models import Group, Lesson, Student,Homework


########################################################
def index(requests):
    return render(requests, 'pages/index.html', {})


@login_required(login_url='index')
def dashboard(requests):
    lessons = Lesson.objects.filter(group=requests.user.student.group)
    context = {
        'lessons': lessons,
    }
    return render(requests, 'pages/dashboard.html', context)


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
            return redirect('dashboard')

    return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')


########################################################## 404
def handler404(request):
    return render(request, '404.html', status=404)
