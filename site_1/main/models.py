from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "table" ,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Canvas(models.Model):
    #table = models.ForeignKey(Table, on_delete=models.CASCADE)
    txt = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'images',null=True, blank=True)
    show = models.BooleanField()
