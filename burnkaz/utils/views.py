import hashlib
import os
import requests
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
import datetime as dt
from datetime import datetime
from rest_framework.response import Response

from developer.models import DeveloperImages
from utils.serializers import DevAvatarsSerializer


class ML(APIView):

    def post(self, request):
        data = request.data


        date = datetime.today().strftime('%Y-%m-%d')
        folder = 'media/' + str(date) + 'ml/'
        myfile = request.FILES['document']
        fileName, fileExtension = os.path.splitext(myfile.name)
        myfile.name = 'passport' + hashlib.md5(fileName.encode('utf-8')).hexdigest() + fileExtension
        url_name = 'media/' + str(date) + '/' + str(myfile.name)
        fs = FileSystemStorage(location=folder)
        fileName = fs.save(myfile.name, myfile)
        payload = {
            'document': url_name
        }
        url = 'http://138.68.184.57:5000/compare-faces/'
        result = requests.post(url, data=payload)
        if result.status_code == 200:
            return Response({"Status": 200})
        else:
            return {"Status": 404}

class MLViewSet(viewsets.ModelViewSet):
    queryset = DeveloperImages.objects.all()
    serializer_class = DevAvatarsSerializer
    parser_classes = (MultiPartParser, )

