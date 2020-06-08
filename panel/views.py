from django.shortcuts import render, redirect, HttpResponse, Http404
from .models import Group, Student, Homework, Lesson
from pages.models import Clients
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings


def lastname_admin_check(user):
    return user.last_name == 'Администратор'


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def panel(request):
    context = {
    }
    return render(request, 'panel/panel.html', context)


##########################################################################
# Groups
##########################################################################
def groups(requests):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(requests, 'panel/groups.html', context)


def groups_add(requests):
    if requests.method == 'POST':
        Group.objects.create(
            title=requests.POST['title'],
            level=requests.POST['level'],
        )
        messages.success(requests, 'Группа успешна создана')
        return redirect('groups')
    messages.error(requests, 'Группа не создана')
    return redirect('groups')


def groups_edit(requests, id):
    if requests.method == 'POST':
        g = Group.objects.get(id=id)
        g.title = requests.POST['title']
        g.level = requests.POST['level']
        g.completed = requests.POST['completed']
        g.save()
        messages.success(requests, 'Группа успешна изменена')
        return redirect('groups')
    messages.error(requests, 'Группа не изменена')
    return redirect('groups')


def groups_delete(requests, id):
    if requests.method == 'POST':
        g = Group.objects.get(id=id)
        g.delete()
        messages.success(requests, 'Группа успешна удалена')
        return redirect('groups')
    messages.error(requests, 'Группа не удалена')
    return redirect('groups')


##########################################################################
# Students
##########################################################################
def students(requests):
    students = Student.objects.all()
    groups = Group.objects.all()
    context = {
        'students': students,
        'groups': groups,
    }
    return render(requests, 'panel/students.html', context)


def students_add(requests):
    if requests.method == 'POST':
        u = User.objects.create_user(
            username=requests.POST['username'],
            password=requests.POST['password'],
        )
        s = Student.objects.get(user=User.objects.get(id=u.id))
        s.group = Group.objects.get(title=requests.POST['group'])
        s.fname = requests.POST['first_name']
        s.rating = 100
        s.save()
        messages.success(requests, 'Студент создан')
        return redirect('students')
    messages.error(requests, 'Студент не создан')
    return redirect('students')


def students_edit(requests, id):
    if requests.method == 'POST':
        u = User.objects.get(id=id)
        s = Student.objects.get(user=u)
        s.fname = requests.POST['first_name']
        s.rating = requests.POST['rating']
        s.group = Group.objects.get(title=requests.POST['group'])
        u.username = requests.POST['username']
        hasher = PBKDF2PasswordHasher()
        u.password = hasher.encode(password=requests.POST['password'],
                                   salt='salt',
                                   iterations=50000)
        s.save()
        u.save()
        messages.success(requests, 'Студент успешно изменен')
        return redirect('students')
    messages.error(requests, 'Студент не изменен')
    return redirect('students')


def students_delete(requests, id):
    if requests.method == 'POST':
        u = User.objects.get(id=id)
        u.delete()
        messages.success(requests, 'Студент удален')
        return redirect('students')
    messages.error(requests, 'Студент не удален')
    return redirect('students')


##########################################################################
# Lessons
##########################################################################
def lessons(requests):
    lessons = Lesson.objects.all()
    groups = Group.objects.all()
    context = {
        'lessons': lessons,
        'groups': groups,
    }
    return render(requests, 'panel/lessons.html', context)


def lessons_add(requests):
    if requests.method == 'POST' and requests.FILES['file']:
        Lesson.objects.create(
            title=requests.POST['title'],
            group=Group.objects.get(title=requests.POST['group']),
            video=requests.POST['video'],
            lesson=requests.FILES['file'],
        )
        messages.success(requests, 'Урок создан')
        return redirect('lessons')
    messages.error(requests, 'Урок не создан')
    return redirect('lessons')


def lessons_delete(requests, id):
    if requests.method == 'POST':
        l = Lesson.objects.get(id=id)
        os.system('rm {}'.format(l.lesson.path))
        l.delete()
        messages.success(requests, 'Урок удален')
        return redirect('lessons')
    messages.error(requests, 'Урок не удален')
    return redirect('lessons')


##########################################################################
# Clients
##########################################################################
def clients(requests):
    clients = Clients.objects.all()
    context = {
        'clients': clients,
    }
    return render(requests, 'panel/clients.html', context)


def clients_complete(requests, id):
    c = Clients.objects.get(id=id)
    if c.processed == True:
        c.processed = False
    elif c.processed == False:
        c.processed = True
    c.save()
    return redirect('clients')


##########################################################################
# HWs
##########################################################################
def hws(requests):
    hws = Homework.objects.all()
    context = {
        'hws': hws,
    }
    return render(requests, 'panel/hws.html', context)


def hws_delete(requests, id):
    if requests.method == 'POST':
        h = Homework.objects.get(id=id)
        os.system('rm {}'.format(h.upload.path))
        h.delete()
        messages.success(requests, 'Домашнее задание удалено')
        return redirect('hws')
    messages.error(requests, 'Домашнее задание не удалено')
    return redirect('hws')

def hws_complete(requests, id):
    h = Homework.objects.get(id=id)
    if h.processed == True:
        h.processed = False
    elif h.processed == False:
        h.processed = True
    h.save()
    return redirect('hws')

##########################################################################
# Download function
##########################################################################


def download(requests, id):
    file_lesson = Lesson.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_lesson.lesson.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def download_hws(requests, id):
    file_lesson = Homework.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_lesson.upload.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
