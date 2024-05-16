from django.db import models

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/')

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    negative_prompt = models.TextField()
    width = models.IntegerField()
    height = models.IntegerField()
    seed = models.IntegerField()
    image = models.ImageField(upload_to='images/')

class Model(models.Model):
    name = models.CharField(max_length=50)
    hash = models.CharField(max_length=100)