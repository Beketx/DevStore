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
        return Response("123")

    def post(self, request):
        data = request.data
        user = request.user
        client = Client.objects.get(user=user)
        dev_id = data["developer_id"]
        dev = Developer.objects.get(id=dev_id)
        if not DevClientInContact.objects.filter(client_id=client).exists():
            contact = DevClientInContact.objects.create(client_id=client)
        contact = DevClientInContact.objects.get(client_id=client)
        contact.dev_id.add(dev)

        return Response("one")