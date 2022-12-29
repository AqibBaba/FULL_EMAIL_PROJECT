from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from rest_framework.generics import GenericAPIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from . import sendmail

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response("2 emails cant be same",status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save()
        return Response("User successfully registerd",status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
        
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        password = request.data.get('password')
        user= User.objects.filter(email=email,is_active=True).first()
        if not user:
            return Response({"status": "success", "data": "user not found"}, status=status.HTTP_200_OK)
        if(check_password(password,user.password)):
            if user is not None:
                login(request, user)
                # token_obj = Token.objects.get_or_create(user=user);'''works without underscore but gives bool value at the end of token'''
                token_obj, _ = Token.objects.get_or_create(user=user)
                return Response({'token':str(token_obj),'payload':"successfully log in",'status':200})
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AllUsersView(GenericAPIView):
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    user_id = openapi.Parameter(
        'user_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config,user_id])
    def get(self,request):
        token = request.GET.get('token')
        user_id = request.GET.get('user_id')
        token_check=Token.objects.filter(key=token,user_id=user_id).first()
        if token_check is not None:

            user=User.objects.filter(is_active=True)
            users=UserSerializer2(user,many=True)
            
            return Response(users.data,status=status.HTTP_200_OK)
        return Response("User is not authenticated",status=status.HTTP_401_UNAUTHORIZED)

class DeleteView(GenericAPIView):
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    user_id = openapi.Parameter(
        'user_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config,user_id])
    def delete(self,request,id):
        token = request.GET.get('token')
        user_id = request.GET.get('user_id')
        check=Token.objects.filter(key=token,user_id=user_id).first()
        if check is not None:
            user=User.objects.filter(id=id,is_active=True).first()
            if user is not None:
                user.is_active=False
                user.save()
                return Response("deleted successfully",status=status.HTTP_200_OK)
            return Response("User already deleted",status=status.HTTP_410_GONE)
        return Response("wrong credentials",status=status.HTTP_406_NOT_ACCEPTABLE)



class EmailSend(GenericAPIView):
    serializer_class = EmailVerificationSerializer2   

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    user_id = openapi.Parameter(
        'user_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config,user_id])
    def post(self,request):
        token = request.GET.get('token')
        user_id = request.GET.get('user_id')
        
        token_check=Token.objects.filter(key=token,user_id=user_id).first()
        if token_check is not None:
            # sender=request.data.get('sender')
            receiver=request.data.get('receiver')
            receiver_obj=Receiver.objects.filter(received_emails=receiver).first()
            if receiver_obj is None:
                abc=Receiver()
                abc.received_emails=receiver
                abc.save()

            id=Receiver.objects.filter(received_emails=receiver).first()

            compose=request.data.get('compose')
            subject=request.data.get('subject')
        
            email_saved=Emails()
            # email_saved.sender=sender
            email_saved.receiver=id
            email_saved.compose=compose
            email_saved.subject=subject
            email_saved.save()
            # sendmail.full_mail(html=compose,to_emails=[receiver],from_email=sender)
            sendmail.full_mail(html=compose,subject=subject,to_emails=[receiver])
            return Response("email sended successfully",status=status.HTTP_200_OK)
        return Response("access granted",status=status.HTTP_200_OK)
   
class NewPassword(GenericAPIView):
    serializer_class = NewPasswordSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    user_id = openapi.Parameter(
        'user_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config,user_id])
    def post(self,request):
        token = request.GET.get('token')
        user_id = request.GET.get('user_id')

        check=Token.objects.filter(key=token,user_id=user_id).first()
        if check is None:
            return Response("does not exist",status=status.HTTP_401_UNAUTHORIZED)
        
        user=User.objects.filter(id=user_id).first()
        user.password=make_password(request.data.get('password'))
        user.save()
        return Response("password successfully changed",status=status.HTTP_202_ACCEPTED)

class ForgotPassword(GenericAPIView):
    serializer_class=ForgotPassword

    def post(self,request):
        # mail=request.data.get('forgot_password_email')
        mail=request.data.get('email')
        user=User.objects.filter(email=mail).first()
        token=Token.objects.filter(user_id=user.id).first()
        sendmail.send_mail(html='hello',to_emails=[mail],from_email='akibbaba9@gmail.com',user_id=user.id,token=token)
        return Response("Email Sended!",status=status.HTTP_206_PARTIAL_CONTENT)

class ForgetPasswordForUser(GenericAPIView):
    serializer_class=ForgetPasswordForUser

    def get(self,request,id,token):
        token=Token.objects.filter(user_id=id,key=token).first()
        if token is None:
            return Response("not found",status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"id":str(token.user_id)},status=status.HTTP_201_CREATED,headers={
            'token':str(token.key)
        })

class UpdateUserView(GenericAPIView):
    serializer_class=UpdateUserSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    user_id = openapi.Parameter(
        'user_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config,user_id])
    def put(self,request,id):
        token = request.GET.get('token')
        user_id = request.GET.get('user_id')

        check=Token.objects.filter(key=token,user_id=user_id).first()
        if check is None:
            return Response("does not exist",status=status.HTTP_401_UNAUTHORIZED)
        user=User.objects.filter(id=id,is_active=True).first()
        if user is None:
            return Response("User is already deleted",status=status.HTTP_404_NOT_FOUND)
        user.username=request.data.get('username')
        # user.password=make_password(request.data.get('password'))
        # user.email=request.data.get('email')
        user.save()
        return Response("successfully Updated",status=status.HTTP_202_ACCEPTED)
