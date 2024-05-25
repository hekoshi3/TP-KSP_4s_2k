from django.db import models
from django.contrib.auth.models import User

class Model(models.Model):
    name = models.CharField(max_length=100)
    hash_value = models.CharField(max_length=64)
    sampler_name = models.CharField(max_length=100, default='Euler_a')
    sampler_steps = models.IntegerField()
    cfg_scale = models.IntegerField()

    def __str__(self):
        return self.name

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=512, blank=True)
    negative_prompt = models.CharField(max_length=512, blank=True)
    width = models.IntegerField()
    height = models.IntegerField()
    seed = models.IntegerField()
    image = models.ImageField(upload_to='generated_images/', null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self):
        return f"Request by {self.user.username} with prompt: {self.prompt}"

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favourite by {self.user.username} for request: {self.request.id}"
