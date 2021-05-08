from rest_framework import serializers
from developer.models import DeveloperImages


class DevAvatarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperImages
        fields = ('image')