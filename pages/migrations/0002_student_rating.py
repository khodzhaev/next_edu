# Generated by Django 3.0.3 on 2020-02-29 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='rating',
            field=models.CharField(default='5', max_length=200),
        ),
    ]
