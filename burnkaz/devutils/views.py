from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated,\
                                       IsAuthenticatedOrReadOnly, \
                                       AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from developer import serializers
from developer.models import Stacks, Skills, Developer, Favorites
from developer.serializers import DevelopersSerializer, FavoritesSerializer
from devutils.serializers import StacksSerializer, SkillsSerializer
from userauth.models import User


class StacksView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = StacksSerializer
    queryset = Stacks.objects.all()
    permission_class = [AllowAny, ]

class SkillsView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = SkillsSerializer
    queryset = Skills.objects.all()
    permission_class = [AllowAny, ]

class AddFavorite(APIView):
    """
    {
    dev_id:123
    }
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            users = request.user
            # client = User.objects.get(user=users)
            favs = Favorites.objects.filter(user=users)
            print(favs)
            data = []
            # for fav in favs:
            # devs = Developer.objects.all()
            # zevs = Favorites.objects.filter(user=users)
            
            serializer = FavoritesSerializer(favs, many=True)
            # data.append(serializer.data)
            res = {
                'status': True,
                'results': data
            }
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            res = {
                'status': False,
                'detail': str(e)
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
            # res = {
            #     'status': False,
            #     'detail': 'Get Favorite not added'
            # }
            # return Response(res, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        try:
            data = request.data
            users = request.user
            dev_id = data["developer_id"]
            dev = Developer.objects.get(id=dev_id)
            print(1)
            if not Favorites.objects.filter(developer=dev).exists():
                contact = Favorites.objects.create(developer=dev, favorite_bool=True, user=users)
            res = {
                'status': True,
                'detail': 'Favorite added'
            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            res = {
                'status': False,
                'detail': str(e)
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)

class MyFavorites(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Favorites.objects.all()
    def list(self, request):
        queryset = Favorites.objects.filter(user=self.request.user)
        serializer_class = serializers.DevelopersSerializer(queryset, many=True)
        return Response(serializer_class.data)