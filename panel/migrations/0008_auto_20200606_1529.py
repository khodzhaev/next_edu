# Generated by Django 3.0.7 on 2020-06-06 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0007_auto_20200606_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]