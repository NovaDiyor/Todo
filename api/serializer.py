from rest_framework import serializers
from .models import *


class TaskOne(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UserVisible(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'img']
