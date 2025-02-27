from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard')
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    sample_tc = models.TextField()
    sample_op = models.TextField()
    hidden_input = models.TextField(default='xD')   
    expected_output = models.TextField()   
    accepted = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, default='Medium')
    frequency = models.IntegerField(default=0) 

    def __str__(self):
        return self.name

class Code(models.Model):
    myuser = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    result = models.TextField() 

    def __str__(self):
        return f'{self.result}'

class Topic(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length = 200)
    desc = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(User, related_name = 'participants', blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.body[0 : 50]