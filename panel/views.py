from django.shortcuts import render, redirect, HttpResponse, Http404
from .models import Group, Student, Homework, Lesson, Test, TestStudent, TestItem
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
    return redirect('groups')


##########################################################################
# Groups
##########################################################################
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def groups(requests):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    return render(requests, 'panel/groups.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
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


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
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


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
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
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def students(requests):
    students = Student.objects.all()
    groups = Group.objects.all()
    context = {
        'students': students,
        'groups': groups,
    }
    return render(requests, 'panel/students.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def students_add(requests):
    if requests.method == 'POST':
        u = User.objects.create_user(
            username=requests.POST['username'],
            password=requests.POST['password'],
        )
        group = requests.POST['group']
        s = Student.objects.get(user_id=User.objects.get(id=u.id))
        s.group = Group.objects.get(title=group)
        s.fname = requests.POST['first_name']
        s.rating = 100
        s.save()
        messages.success(requests, 'Студент создан')
        return redirect('students')
    messages.error(requests, 'Студент не создан')
    return redirect('students')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
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


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def students_delete(requests):
    if requests.method == 'POST':
        u = User.objects.get(username=requests.POST['login'])
        u.delete()
        messages.success(requests, 'Студент удален')
        return redirect('students')
    messages.error(requests, 'Студент не удален')
    return redirect('students')


##########################################################################
# Lessons
##########################################################################
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def lessons(requests):
    lessons = Lesson.objects.all()
    groups = Group.objects.all()
    context = {
        'lessons': lessons,
        'groups': groups,
    }
    return render(requests, 'panel/lessons.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
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


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
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
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def clients(requests):
    clients = Clients.objects.all()
    context = {
        'clients': clients,
    }
    return render(requests, 'panel/clients.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
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
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def hws(requests):
    hws = Homework.objects.all()
    context = {
        'hws': hws,
    }
    return render(requests, 'panel/hws.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def hws_delete(requests, id):
    if requests.method == 'POST':
        h = Homework.objects.get(id=id)
        os.system('rm {}'.format(h.upload.path))
        h.delete()
        messages.success(requests, 'Домашнее задание удалено')
        return redirect('hws')
    messages.error(requests, 'Домашнее задание не удалено')
    return redirect('hws')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def hws_complete(requests, id):
    h = Homework.objects.get(id=id)
    if h.processed == True:
        h.processed = False
    elif h.processed == False:
        h.processed = True
    h.save()
    return redirect('hws')


##########################################################################
# Test
##########################################################################
@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test(requests):
    tests = Test.objects.all()
    groups = Group.objects.all()
    context = {
        'tests': tests,
        'groups': groups
    }
    return render(requests, 'panel/test.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_add(requests):
    if requests.method == 'POST':
        Test.objects.create(
            title=requests.POST['title'],
            group=Group.objects.get(title=requests.POST['group'])
        )
        messages.success(requests, 'Тест создан')
        return redirect('test')
    messages.error(requests, 'Тест не создан')
    return redirect('test')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_edit(requests, id):
    if requests.method == 'POST':
        t = Test.objects.get(id=id)
        t.title = requests.POST['title']
        t.group = Group.objects.get(title=requests.POST['group'])
        if 'avaible' in requests.POST:
            t.avaible = True
        else:
            t.avaible = False
        t.save()
        messages.success(requests, 'Тест изменен')
        return redirect('test')
    messages.error(requests, 'Тест не изменен')
    return redirect('test')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_delete(requests, id):
    if requests.method == 'POST':
        t = Test.objects.get(id=id)
        t.delete()
        messages.success(requests, 'Тест удален')
        return redirect('test')
    messages.error(requests, 'Тест не удален')
    return redirect('test')


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_detail(requests, id):
    test = Test.objects.get(id=id)
    context = {
        'test': test,
    }
    return render(requests, 'panel/test_detail.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_add_queston(requests):
    if requests.method == 'POST':
        ti = TestItem.objects.filter(test=Test.objects.get(id=requests.POST['test_id']))

        page = requests.POST['test_id']
        c = ti.count()
        TestItem.objects.create(
            title=requests.POST['title'],
            test=Test.objects.get(id=requests.POST['test_id']),
            count=(c + 1),
        )
        messages.success(requests, 'Создан вопрос')
        return redirect('/admin/test_detail/{}/'.format(page))
    messages.error(requests, 'Вопрос не создана')
    return redirect('/admin/test_detail/{}/'.format(page))


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_question_delete(requests, id):
    if requests.method == 'POST':
        page = requests.POST['test_id']
        t = TestItem.objects.get(id=id)
        t.delete()
        messages.success(requests, 'Удален вопрос')
        return redirect('/admin/test_detail/{}/'.format(page))
    messages.error(requests, 'Не удален вопрос')
    return redirect('/admin/test_detail/{}/'.format(page))


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_result(requests):
    tests = Test.objects.all()
    context = {
        'tests': tests
    }
    return render(requests, 'panel/test_result.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_result_student(requests, id):
    test = TestStudent.objects.get(id=id)
    context = {
        'test': test
    }
    return render(requests, 'panel/test_result_student.html', context)


@login_required(login_url='index')
@user_passes_test(lastname_admin_check)
def test_result_processed(requests, id):
    test = TestStudent.objects.get(id=id)
    if requests.method == 'POST':
        test.point = requests.POST['point']
        test.processed = requests.POST['processed']
        test.save()
        messages.success(requests, 'Тест студента изменена')
        return redirect('test_result')
    messages.error(requests, 'Тест студента не изменена')
    return redirect('test_result')


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
