from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null=True)
    title = models.CharField(max_length=300)
    desciption = models.TextField()
    due_date = models.DateTimeField()
    priority = models.IntegerField(default=1)
    completed = models.BooleanField(default=False) # by default it is set to  False
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank= True, null=True)
    

    

