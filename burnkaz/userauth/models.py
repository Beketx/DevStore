from django.contrib.auth.models import BaseUserManager
import jwt

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function
     which we will use
    to create `User` objects.
    """


    def _create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a `User` with an email, username and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
    """
    Defines our custom user class.
    Username, email and password are required.
    """
    username = models.CharField(max_length=3, null=True,
                                blank=True, default="one")
    name = models.CharField(max_length=254, null=True, blank=True)
    surname = models.CharField(max_length=254, null=True, blank=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{11,13}$',
                                message="Phone number must be entered in the form of +7(708)791-22-65.")
    phone = models.CharField(max_length=20, unique=True,
                             null=True, blank=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False,
        null=True
    )
    birth_date = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    password = models.CharField(max_length=140, default='ADminadmin123',
                                null=True)
    iin = models.CharField(unique=True, max_length=9, null=True)
    city = models.ForeignKey(to="City", on_delete=models.CASCADE, null=True)
    MALE = 1
    FEMALE = 2
    UNDEFINED = 3
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNDEFINED, 'Undefined'),
    )
    gender = models.IntegerField(choices=GENDER, null=True, blank=True)
    CLIENT = 1
    DEVELOPER = 2
    ROLE = (
        (CLIENT, 'Client'),
        (DEVELOPER, 'Developer')
    )
    role = models.IntegerField(choices=ROLE, null=True, blank=True)


    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_joined = models.BooleanField(default=True)

    # The `USERNAME_FIELD` property tells us
    # which field we will use to log in.
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ()

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        if self.email:
            return self.email
        elif self.phone:
            return self.phone
        elif self.name:
            return self.name
        elif self.username:
            return self.username

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.email

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.email

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the form of +919999999999.")
    phone = models.CharField(validators=[phone_regex], max_length=17,
                             null=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        blank=False,
        null=True
    )
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of opt_sent')
    validated = models.BooleanField(default=False,
                                    help_text='if it is true, that means user have validate opt correctly in seconds')
    key_token = models.CharField(max_length=150, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible.
         `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this
         user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class City(models.Model):
    title = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title