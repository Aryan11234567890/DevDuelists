from django.contrib import admin
# from . import models
from .models import User, Discussions, Problem, Code

# Register your models here.
# admin.site.register(User)
admin.site.register(Discussions)
admin.site.register(Problem)
admin.site.register(Code)
