from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, BasePermission


def generate_auth_code():
    """Generate a random code """
    import random
    code_list = [str(random.randint(0, 9)) for i in range(6)]
    code = "".join(code_list)
    return int(code)


def sendMail(subject, message, to):
    from django.core.mail import send_mail
    from django.conf import settings

    return send_mail(
        subject,
        str(message),
        settings.EMAIL_HOST_USER,
        [to],
        fail_silently=False
    )
