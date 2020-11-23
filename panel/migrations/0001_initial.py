# Generated by Django 3.1.3 on 2020-11-23 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('lang', models.CharField(max_length=255)),
                ('pages', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=0, max_length=200)),
                ('level', models.IntegerField()),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'ordering': ('-date_pub',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=200)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
                'ordering': ('-date_pub',),
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('avaible', models.BooleanField(default=False)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.group')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
                'ordering': ('-date_pub',),
            },
        ),
        migrations.CreateModel(
            name='TestStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.CharField(max_length=255)),
                ('avaible', models.BooleanField(default=True)),
                ('processed', models.BooleanField(default=False)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.test')),
            ],
            options={
                'verbose_name': 'Тест Студент',
                'verbose_name_plural': 'Тесты Студенты',
                'ordering': ('-date_pub',),
            },
        ),
        migrations.CreateModel(
            name='TestItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('count', models.IntegerField()),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.test')),
            ],
            options={
                'verbose_name': 'Тест вопрос',
                'verbose_name_plural': 'Тесты вопросы',
            },
        ),
        migrations.CreateModel(
            name='TestAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.test')),
                ('teststudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.teststudent')),
            ],
            options={
                'verbose_name': 'Тест ответы',
                'verbose_name_plural': 'Тесты ответы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('video', models.TextField(max_length=200)),
                ('lesson', models.FileField(upload_to='lessons/%Y/%m/%d/')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.group')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
                'ordering': ('-date_pub',),
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(blank=True, null=True, upload_to='homeworks/%Y/%m/%d/')),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.student')),
            ],
            options={
                'verbose_name': 'Домашка',
                'verbose_name_plural': 'Домашки',
                'ordering': ('-date_pub',),
            },
        ),
    ]
