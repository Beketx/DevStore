from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, \
                                            IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from client.models import DevClientInContact
from userauth.models import User, City
from utils.developer_pagination.pagination import DeveloperPagination
from .models import Skills, Stacks, Developer, DeveloperService,\
                    Rating, Review, ImageTab
from . import serializers
#birth_date = birth_date.strftime("%d.%m.%Y") if birth_date else None

logger = logging.getLogger(__name__)

class DeveloperProfilesByStacks(RetrieveModelMixin,
                        ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = serializers.StackDeveloperSerializer
    permission_classes = [AllowAny, ]
    serializer_action_classes = {
        'list': serializers.StackDeveloperSerializer,
        'retrieve': serializers.FullInfoDeveloperSerializer,
    }
    queryset = Stacks.objects.all()
    pagination_class = DeveloperPagination

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

class DeveloperProfiles(RetrieveModelMixin,
                        ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = serializers.DevelopersSerializer
    permission_classes = [AllowAny, ]
    serializer_action_classes = {
        'list': serializers.DevelopersSerializer,
        'retrieve': serializers.FullInfoDeveloperSerializer
    }
    queryset = Developer.objects.filter(user__role=2)
    pagination_class = DeveloperPagination

    # def get_queryset(self):
    #     devs =

    def get_serializer_class(self):
        try:
            return self.serialzier_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

class DeveloperContacts(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = DevClientInContact.objects.all()
    def list(self, request):
        queryset = DevClientInContact.objects.filter(dev_id__user=self.request.user)
        serializer_class = serializers.DeveloperContactsSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = DevClientInContact.objects.get(id=pk)
        serializer_class = serializers.DeveloperContactsSerializer(queryset, many=False)
        return Response(serializer_class.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = serializers.DeveloperContactsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

