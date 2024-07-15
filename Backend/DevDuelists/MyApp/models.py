from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard')
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    sample_tc = models.TextField()
    custom_tc = models.TextField()
    hidden_tc = models.TextField()
    accepted = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, default='Medium')
    frequency = models.IntegerField(default=0) 

    def __str__(self):
        return self.name

class Code(models.Model):
    myuser = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    result = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.result}'

class Discussions(models.Model):
    myuser = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.TextField()
    likes = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.discussion}'

