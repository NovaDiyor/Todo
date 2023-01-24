from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    status = models.IntegerField(choices=(
        (1, 'admin'),
        (2, 'user')
    ), default=2)
    img = models.ImageField(upload_to='user/', null=True, blank=True)


class Task(models.Model):
    title = models.CharField(max_length=210)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

