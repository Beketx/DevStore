import datetime
import hashlib
import os
import random

import datetime as dt
from django.core.files.storage import FileSystemStorage

from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from client.models import Client
from developer.models import *
from burnkaz.celery.tasks import send_email_task
from .serializers import CitiesSerializer
from .models import *
from .serializers import LoginSerializer, OTPSerializer
from .serializers import RegistrationSerializer
import logging
from developer import serializers

logger = logging.getLogger(__name__)

class RegistrationStepOne(APIView):
    """
    Registers a new user.
    """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """

        try:
            data = request.data
            keys = request.META['HTTP_AUTHORIZATION']
            keys = keys.split()
            print(keys[1])
            objOpt = PhoneOTP.objects.get(key_token=keys[1])
            if objOpt.email:
                user = User.objects.get(email=objOpt.email)
            #     user.phone = data['phone']
            # elif objOpt.phone:
            #     user = User.objects.get(phone=objOpt.phone)
            #     user.email = data['email']
            user.name = data['name']
            user.surname = data['surname']
            if User.objects.filter(iin=data['iin']).exists():
                res = {
                    'status': False,
                    'detail': "This IIN is already registered"
                }
                return Response(res, status=status.HTTP_403_FORBIDDEN)
            if len(data['iin']) % 9 != 0:
                res = {
                'status': False,
                'detail': 'IIN must be 9 digits'
                }
                return Response(res, status=status.HTTP_304_NOT_MODIFIED)
            user.iin = data['iin']
            user.role = data['role']
            user.save()
            if data['role'] == 2:
                developer = Developer.objects.create(user=user)
            if data['role'] == 1:
                client = Client.objects.create(user=user)
            res = {
                "status": True,
                "detail": "Registration passed successfully",
                "user-id": user.id
            }

            return Response(
                res,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            res = {
                "status": False,
                "detail": str(e)
            }
            return Response(
                res,
                status=status.HTTP_403_FORBIDDEN
            )

class RegistrationStepTwo(APIView):
    """
    Registers a new user.
    """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """

        try:
            data = request.data
            keys = request.META['HTTP_AUTHORIZATION']
            keys = keys.split()
            objOpt = PhoneOTP.objects.get(key_token=keys[1])
            if objOpt.email:
                user = User.objects.get(email=objOpt.email)
                user.phone = data['phone']
            elif objOpt.phone:
                user = User.objects.get(phone=objOpt.phone)
                user.email = data['email']
            if User.objects.filter(phone=data['phone']).exists():
                res = {
                    'status': False,
                    'detail': "This Phone is already registered"
                }
                return Response(res, status=status.HTTP_403_FORBIDDEN)
            user.phone = data['phone']
            user.gender = data['gender']
            user.is_joined = True
            user.birth_date = data['birth_date']
            city = City.objects.get(id=data['city'])
            user.city = city
            user.role = data['role']
            user.save()
            res = {
                "status": True,
                "detail": "Registration passed successfully",
                "user-id": user.id
            }
            return Response(
                res,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            res = {
                "status": False,
                "detail": str(e)
            }
            return Response(
                res,
                status=status.HTTP_403_FORBIDDEN
            )

class RegistrationStepThree(APIView):
    """
    Registers a new user.
    """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """

        try:
            data = request.data
            keys = request.META['HTTP_AUTHORIZATION']
            keys = keys.split()
            objOpt = PhoneOTP.objects.get(key_token=keys[1])
            if objOpt.email:
                user = User.objects.get(email=objOpt.email)
            #     user.phone = data['phone']
            # elif objOpt.phone:
            #     user = User.objects.get(phone=objOpt.phone)
            #     user.email = data['email']
            user.work_place = data['work_place']
            user.role = data['role']
            user.save()
            if data['role'] == 2:
                if Developer.objects.filter(user=user).exists():
                    developer = Developer.objects.filter(user=user).update(education=data['education'],
                                                                           about=data['about'],
                                                                           work_experience=data['work_experience'])

                developer = Developer.objects.get(user=user)
            list_skills = data['skills']
            for skill_id in list_skills:
                developer.skills_id.add(Skills.objects.get(id=skill_id))
            list_stacks = data['stacks']
            for stack_id in list_stacks:
                developer.stacks_id.add(Stacks.objects.get(id=stack_id))
            res = {
                "status": True,
                "detail": "Registration passed successfully",
                "user-id": user.id
            }
            return Response(
                res,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            res = {
                "status": False,
                "detail": str(e)
            }
            return Response(
                res,
                status=status.HTTP_403_FORBIDDEN
            )

class RegistrationStepFour(APIView):
    """
    Registers a new user.
    """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """

        try:
            data = request.data
            keys = request.META['HTTP_AUTHORIZATION']
            keys = keys.split()
            objOpt = PhoneOTP.objects.get(key_token=keys[1])
            if objOpt.email:
                user = User.objects.get(email=objOpt.email)
            #     user.phone = data['phone']
            # elif objOpt.phone:
            #     user = User.objects.get(phone=objOpt.phone)
            #     user.email = data['email']
            user.role = data['role']
            user.save()
            if data['role'] == 2:
                dev_service = DeveloperService.objects.create(service_title=data['service_title'],
                                                              service_description=data['service_description'],
                                                              price=data['price'],
                                                              price_fix=data['price_fix'])
                Developer.objects.filter(user=user).update(dev_service=dev_service)
            res = {
                "status": True,
                "detail": "Registration passed successfully",
                "user-id": user.id
            }
            return Response(
                res,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            res = {
                "status": False,
                "detail": str(e)
            }
            return Response(
                res,
                status=status.HTTP_403_FORBIDDEN
            )

class RegistrationStepFive(APIView):
    """
    Registers a new user.
    """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """

        try:
            logging.info('Some message')
            logging.error('In try')
            data = request.data
            keys = request.META['HTTP_AUTHORIZATION']
            keys = keys.split()
            objOpt = PhoneOTP.objects.get(key_token=keys[1])
            if objOpt.email:
                logging.error('In objopt')
                user = User.objects.get(email=objOpt.email)
            #     user.phone = data['phone']
            # elif objOpt.phone:
            #     user = User.objects.get(phone=objOpt.phone)
            #     user.email = data['email']
            user.role = data['role']
            user.save()
            developer = Developer.objects.get(user=user)
            """
            Image Front
            """
            date = datetime.today().strftime('%Y-%m-%d')
            folder = 'media/' + str(date) + '/front_photo/'
            myfile = request.FILES['front_photo']
            fileName, fileExtension = os.path.splitext(myfile.name)
            myfile.name = 'front_photo' + hashlib.md5(fileName.encode('utf-8')).hexdigest() + fileExtension
            url_name = 'media/' + str(date) + '/front_photo/' + str(myfile.name)
            fs = FileSystemStorage(location=folder)
            file_name = fs.save(myfile.name, myfile)
            file_url = fs.url(file_name)
            timenow = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            check_date = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            images = ImageTab()
            images.developer = developer
            image_type = ImageType.objects.get(type_id=1)
            images.image_type = image_type
            images.image_url = url_name
            images.save()
            logging.error('first message saved')

            """
            Image avatar
            """
            date = datetime.today().strftime('%Y-%m-%d')
            folder = 'media/' + str(date) + '/avatar/'
            myfile = request.FILES['avatar']
            fileName, fileExtension = os.path.splitext(myfile.name)
            myfile.name = 'avatar' + hashlib.md5(fileName.encode('utf-8')).hexdigest() + fileExtension
            url_name = 'media/' + str(date) + '/avatar/' + str(myfile.name)
            fs = FileSystemStorage(location=folder)
            file_name = fs.save(myfile.name, myfile)
            file_url = fs.url(file_name)
            timenow = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            check_date = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            images = ImageTab()
            images.developer = developer
            image_type = ImageType.objects.get(type_id=2)
            images.image_type = image_type
            images.image_url = url_name
            images.save()
            logging.error('second message saved')

            """
            Image passport
            """
            date = datetime.today().strftime('%Y-%m-%d')
            folder = 'media/' + str(date) + '/passport/'
            myfile = request.FILES['passport']
            fileName, fileExtension = os.path.splitext(myfile.name)
            myfile.name = 'passport' + hashlib.md5(fileName.encode('utf-8')).hexdigest() + fileExtension
            url_name = 'media/' + str(date) + '/passport/' + str(myfile.name)
            fs = FileSystemStorage(location=folder)
            file_name = fs.save(myfile.name, myfile)
            file_url = fs.url(file_name)
            timenow = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            check_date = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            images = ImageTab()
            images.developer = developer
            image_type = ImageType.objects.get(type_id=3)
            images.image_type = image_type
            images.image_url = url_name
            images.save()
            logging.error('third message saved')
            res = {
                "status": True,
                "detail": "Registration passed successfully",
                "user-id": user.id
            }
            return Response(
                res,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logging.error('in except')
            res = {
                "status": False,
                "detail": e
            }
            return Response(
                res,
                status=status.HTTP_403_FORBIDDEN
            )

class GetProfile(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.FullInfoDeveloperSerializer


    def list(self, request):
        try:
            devs = Developer.objects.get(user=self.request.user)
            serializer_class = serializers.FullInfoDeveloperSerializer(devs, many=False)
            return Response(serializer_class.data)
        except:
            serializer_class = serializers.UserSerializer(self.request.user, many=False)
            return Response({
                "id": self.request.user.id,
                "user": serializer_class.data
            })

class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ValidatePhoneSendOTP(APIView):
    # permission_classes = (permissions.AllowAny,)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        # phone_number = request.data.get('phone',)
        if email:
            email = str(email)
            # user = User.objects.filter(phone__iexact=phone)
            # if user.exists():
            key = send_otp(email)
            try:
                user = User.objects.get(email=email)
                if key:
                    PhoneOTP.objects.create(
                        # name = name,
                        email=email,
                        otp=key,
                        user_id=user.id
                    )
                    logging.info('Some message')
                    send_email_task.delay(email_to=email)
                    # link = f'API-urls'
                    # requests.get(link)
                    return Response({
                        'status': True,
                        'detail': 'OTP sent successfully.',
                        'key': key
                    })
            except:
                send_email_task.delay(email_to=email)
                user = User.objects.create(email=email, is_joined=False)
                if key:
                    PhoneOTP.objects.create(
                        # name = name,
                        email=email,
                        otp=key,
                        user_id=user.id
                    )
                    # link = f'API-urls'
                    # requests.get(link)
                    logging.info('Some message')
                    return Response({
                        'status': True,
                        'detail': 'OTP sent successfully.',
                        'key': key
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Sending OTP error.'
                })

        else:
            logging.info('Some message')
            return Response({
                'status': False,
                'detail': 'Phone number is not given in post request.'
            })


def send_otp(email):
    if email:
        key = random.randint(999, 9999)
        print(key)
        return key
    else:
        return False


class ValidateOTP(APIView):
    # permission_classes = (permissions.AllowAny,)
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', False)
        otp_sent = request.data.get('otp', False)
        count = 0

        if email and otp_sent:
            old = PhoneOTP.objects.filter(email__iexact=email)
            if old.exists():
                old = old.last()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    if old.key_token == None:
                        old.validated = True
                        user_id = old.user_id
                        user = User.objects.get(id=user_id)
                        token = user.token

                        if user.is_joined == True:
                            logging.info('Some message')
                            res = {
                                "status": True,
                                "registered": True,
                                "token": token
                            }
                        else:
                            logging.info('Some message')
                            res = {
                                "status": True,
                                "registered": False,
                                "token": token
                            }
                        old.key_token = token
                        old.save()
                    else:
                        logging.info('Some message')
                        logging.error('Some message')
                        res = {
                            "status": False,
                            "registered": None,
                            "details": "User already exists"
                        }
                    # user = serializer.is_valid(raise_exception=True)
                    # serializer = self.serializer_class(data=request.data)
                    # serializer.is_valid(raise_exception=True)

                    return Response(res, status=status.HTTP_200_OK)
                # elif str(otp_sent) != str(otp):
                #     if count > 5:
                #         return Response({
                #             'status': False,
                #             'detail': 'Sending otp error. Limit Exceeded. Please contact customer support.'
                #         })
                #     count = count + 1

                elif str(otp_sent) == None:
                    logging.info('Some message')
                    logging.error('Some message')
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect.'
                    })
                return Response({
                    'status': False,
                    'detail': 'Something gone wrong'
                })
            else:
                logging.info('Some message')
                logging.error('Some message')
                return Response({
                    'status': False,
                    'detail': 'First proceed via sending otp request.'
                })
        else:
            logging.info('Some message')
            logging.error('Some message')
            return Response({
                'status': False,
                'detail': 'Please provide both phone and otp for validations'
            })

class CitiesView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CitiesSerializer
    queryset = City.objects.all()
    permission_class = [AllowAny, ]