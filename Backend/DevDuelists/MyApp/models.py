from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    ph_number = models.CharField(max_length = 10, blank = True, null = True)
    no_submit = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.user.username

class Problem(models.Model):
    name = models.CharField(max_length = 100)
    desc = models.TextField()
    sample_tc = models.TextField()
    custom_tc = models.TextField()
    hidden_tc = models.TextField()
    accepted = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.name

class Code(models.Model):
    myuser = models.ForeignKey(User, on_delete = models.CASCADE)
    code = models.TextField()
    result = models.CharField(max_length = 50)
    
    def __str__(self):
        return f'{self.result}'
    
class Discussions(models.Model):
    myuser = models.ForeignKey(User, on_delete = models.CASCADE)
    discussion = models.TextField()
    likes = models.IntegerField(default = 0)
    replies = models.IntegerField(default = 0)
    
    def __str__(self):
        return f'{self.discussion}'