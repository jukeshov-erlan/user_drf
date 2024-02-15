from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordCompleteSerializer
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer())
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # is_valid метод который проверяет данные
        serializer.save()
        return Response('Аккаунт успешно создан', status=201)


class ActivationView(APIView):
    @swagger_auto_schema(request_body=ActivationSerializer())
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response('Аккаунт успешно активирован', status=200)
        

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

# class SomeView(APIView):
#     # permission_classes = [IsAuthenticated]
#     def get(self, request):
#         return Response('helloooooooo')


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        print(dir(request))
        Token.objects.filter(user=user).delete()

        return Response('Вы успешно вышли из своего аккаунта')
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно изменен', status=200)



class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_verification_email()
        return Response('Сообщение для восстановления отправлено на почту', status=200)
    

class ForgotPasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer())
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно изменен', status=200)