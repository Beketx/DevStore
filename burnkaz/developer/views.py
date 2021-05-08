from rest_framework import viewsets, filters, status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, \
                        CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, \
                                            IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from client.models import DevClientInContact
from userauth.models import User, City
from utils.developer_pagination.pagination import DeveloperPagination
from utils.filters import PriceFilter
from . import models
from . import serializers
from django_filters.rest_framework import FilterSet, filters
from rest_framework import filters as searchers

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
    queryset = models.Stacks.objects.all()
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
    queryset = models.Developer.objects.filter(user__role=2)
    filter_backends = [DjangoFilterBackend, searchers.SearchFilter, ]
    filter_class = PriceFilter
    search_fields = ('stacks_id__title', 'user__name', 'education', 'dev_service__id', 'user__city__title', 'about', )
    pagination_class = DeveloperPagination

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
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

"""
REVIEW
"""

class ReviewView(ListModelMixin, RetrieveModelMixin,
             CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = models.Review.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user)

class RatingView(ListModelMixin, RetrieveModelMixin,
             CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.RatingSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = models.Rating.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user)

class FeedbackView(ListModelMixin, RetrieveModelMixin,
             CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.FeedbackSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = models.Feedback.objects.all()
        return queryset.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user)

class FeedbackAPIView(APIView):

    def post(self, request):
        try:
            data = request.data
            dev = models.Developer.objects.get(id=data['developer_id'])
            if dev.user.email == self.request.user.email:
                result = {
                    "status": False,
                    "description": "You cannot review yourself"
                }
                return Response(result, status=status.HTTP_406_NOT_ACCEPTABLE)
            if dev:
                rating = models.Rating.objects.create(communication=data['rating_id']['communication'],
                                               quality=data['rating_id']['quality'],
                                               truth_review=data['rating_id']['truth_review'],
                                               developer_id=dev.id,
                                               user_id=self.request.user)
                review = models.Review.objects.create(text=data['review_id']['text'],
                                               developer_id=dev.id,
                                               user_id=self.request.user)
                feeedback = models.Feedback.objects.create(rating_id=rating,
                                                    review_id=review,
                                                    developer_id=dev,
                                                    user_id=self.request.user)
            result = {
                "status": True,
                "description": "Feedback created"
            }
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e))

    def get(self, request):
        feedbacks = models.Feedback.objects.filter(user_id=self.request.user)
        serializer = serializers.FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def get_extra_actions(cls):
        return []