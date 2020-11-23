from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    email = models.CharField(max_length=200)
    date_pub = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('-date_pub',)


class Start(models.Model):
    title = models.CharField(max_length=200)
