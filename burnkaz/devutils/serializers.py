from rest_framework import serializers
from developer.models import *

class StackTitleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, read_only=True)

class SkillTitleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, read_only=True)



class StacksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stacks
        fields = ['id', 'title']

    # def to_representation(self, instance):
    #     return instance.title

class SkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ['id', 'title']
    # def to_representation(self, instance):
    #     return instance.title