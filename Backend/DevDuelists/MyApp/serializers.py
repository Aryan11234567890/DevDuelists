# serializers.py
from rest_framework import serializers
from .models import Problem, Code, Discussions

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'

class DiscussionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussions
        fields = '__all__'
