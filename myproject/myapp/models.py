from django.db import models
from django.contrib.auth.models import User

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=512, blank=True)
    negative_prompt = models.CharField(max_length=512, blank=True)
    width = models.IntegerField()
    height = models.IntegerField()
    seed = models.IntegerField()
    image = models.ImageField(upload_to='generated_images/', null=True, blank=True)
    def __str__(self):
        return f"Request by {self.user.username} with prompt: {self.prompt}"

class Model(models.Model):
    name = models.CharField(max_length=100)
    hash_value = models.CharField(max_length=64)

    def __str__(self):
        return self.name
