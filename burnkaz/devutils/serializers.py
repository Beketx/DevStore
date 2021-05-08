from rest_framework import serializers
from developer.models import *
from userauth.serializers import CitiesSerializer


class StackTitleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, read_only=True)

class SkillTitleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, read_only=True)



class StacksSerializer(CitiesSerializer):

    class Meta(CitiesSerializer.Meta):
        model = Stacks
        fields = CitiesSerializer.Meta.fields

    # def to_representation(self, instance):
    #     return instance.title

class SkillsSerializer(CitiesSerializer):

    class Meta(CitiesSerializer.Meta):
        model = Skills
        fields = CitiesSerializer.Meta.fields
    # def to_representation(self, instance):
    #     return instance.title