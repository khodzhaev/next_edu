from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    title = models.CharField(max_length=200, default=0)
    level = models.IntegerField()
    date_pub = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def datepublished(self):
        return self.date_pub.strftime('%d.%m.%Y')

    def get_students_total(self):
        students = self.student_set.all().count()
        return students

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-date_pub',)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ('-date_pub',)


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date_pub = models.DateTimeField(auto_now_add=True)
    video = models.TextField(max_length=200)
    lesson = models.FileField(upload_to='lessons/%Y/%m/%d/')

    def __str__(self):
        return self.title

    def datepublished(self):
        return self.date_pub.strftime('%d.%m.%Y')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('-date_pub',)


class Homework(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='homeworks/%Y/%m/%d/', null=True, blank=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.student.username

    def datepublished(self):
        return self.date_pub.strftime('%d.%m.%Y')

    class Meta:
        verbose_name = 'Домашка'
        verbose_name_plural = 'Домашки'
        ordering = ('-date_pub',)
