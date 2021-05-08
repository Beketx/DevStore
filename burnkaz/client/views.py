from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from developer.models import Developer
from .models import DevClientInContact, Client

class ClientContactDev(APIView):
    """
    {
    dev_id:123
    }
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        res = {
            'status': True,
            'detail': 'Message to developer send'
        }
        return Response(res, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            user = request.user
            client = Client.objects.get(user=user)
            dev_id = data["developer_id"]
            if Developer.objects.get(id=dev_id):
                dev = Developer.objects.get(id=dev_id)
            if not DevClientInContact.objects.filter(client_id=client).exists():
                contact = DevClientInContact.objects.create(client_id=client)
            contact = DevClientInContact.objects.get(client_id=client)
            contact.dev_id.add(dev)
            res = {
                'status': True,
                'detail': 'Message to developer send'
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            res = {
                'status': False,
                'detail': 'Message to developer not send'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)