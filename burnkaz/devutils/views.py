from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated,\
                                       IsAuthenticatedOrReadOnly, \
                                       AllowAny

from developer.models import Stacks, Skills
from devutils.serializers import StacksSerializer, SkillsSerializer


class StacksView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = StacksSerializer
    queryset = Stacks.objects.all()
    permission_class = [AllowAny, ]

class SkillsView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = SkillsSerializer
    queryset = Skills.objects.all()
    permission_class = [AllowAny, ]