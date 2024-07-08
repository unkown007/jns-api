from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, BasePermission
from .serializers import (
    UserSerializer,
    UserAddSerializer,
    AuthTokenSerializer,
    GroupSerializer
)
from .models import User, Code


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


class UserView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        serializer = UserAddSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.groups.add(Group.objects.get(name="AUTHOR"))
            user.save()
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        if request.GET.get('role'):
            group = Group.objects.filter(name=request.GET.get('role'))

            users = User.objects.filter(groups__in=group)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ObtainTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data

        # Perform additional processing if needed

        # Construct the response data
        response_data = {
            'token': user_data['token'],
            'user': user_data['user'].id,
            'email': user_data['email'],
            'username': user_data['username'],
            'groups': GroupSerializer(user_data['user'].groups, many=True).data
        }

        return Response(response_data)


class AuthCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        email = data.get('email', None)
        if email is None:
            return Response({'message': 'email field is required'}, status=status.HTTP_400_BAD_REQUEST)

        code = generate_auth_code()
        subject = "Código de confirmação |  Jornadas Nacionais de Saúde 2024"
        message = f'{code}'
        if data.get('name', ''):
            message = (f"Prezado(a) {data.get('name', '')},\n\nObrigado por efectuar o registo na"
                       f" plataforma de submissão de resumos para as Jornadas Nacionais de Saúde 2024. Insira o código"
                       f" abaixo para validar o seu registo:\n{code}")
        else:
            user = User.objects.filter(email=email).first()
            if user is not None:
                name = f"{user.first_user_name} {user.last_user_name}"
                message = (f"Prezado(a) {name},\n\nObrigado por efectuar o registo na"
                           f" plataforma de submissão de resumos para as Jornadas Nacionais de Saúde 2024. Insira o código"
                           f" abaixo para validar a sua recuperação de senha:\n{code}")
        try:
            if sendMail(subject, message, email) == 1:
                aux = Code.objects.filter(email=email).first()
                if aux is not None:
                    aux.code = code
                    aux.save()
                else:
                    obj = Code(email=email, code=code)
                    obj.save()
        except Exception as e:
            pass
        return Response(status=status.HTTP_200_OK)


class AuthCodeValidateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        email = data.get('email', None)
        code = data.get('code', None)

        aux = Code.objects.filter(email=email, code=code).first()
        if aux is not None:
            aux.delete()
            return Response({'status': 'email validated'}, status=status.HTTP_200_OK)

        return Response({'status': 'email not validated'}, status=status.HTTP_400_BAD_REQUEST)


class AuthUserEmailView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        email = data.get('email', None)
        if email is None:
            return Response({"msg": "Email not specified"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"msg": "Email validated"}, status=status.HTTP_200_OK)
