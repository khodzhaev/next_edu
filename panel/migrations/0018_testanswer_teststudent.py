# Generated by Django 3.0.7 on 2020-06-15 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0017_remove_testanswer_teststudent'),
    ]

    operations = [
        migrations.AddField(
            model_name='testanswer',
            name='teststudent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='panel.TestStudent'),
            preserve_default=False,
        ),
    ]
