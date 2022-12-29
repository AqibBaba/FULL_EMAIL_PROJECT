from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("register/",RegisterView.as_view()),
    path("login/",LoginView.as_view()),
    path("emailsend/",EmailSend.as_view()),
    path("newpassword/",NewPassword.as_view()),
    path("forgotpassword/",ForgotPassword.as_view()),
    path("forgetpasswordforuser/<int:id>/<str:token>",ForgetPasswordForUser.as_view()),
    path("allUsers/",AllUsersView.as_view()),
    path("delete/<int:id>/",DeleteView.as_view()),
    path("update/<int:id>/",UpdateUserView.as_view()),
]