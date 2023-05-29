from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AuthorRegistrationSerializer, AuthorLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Author
from django.contrib.auth.hashers import check_password
import bcrypt
from django.contrib.auth.hashers import make_password


class RegisterAuthor(APIView):
    """ registering new user """
    def post(self, request, format=None):
        try:
            name = request.data.get("name")
            email = request.data.get("email")
            password = request.data.get("password")
            hashed_password = make_password(password)
            new_user = {
                "name": name,
                "email": email,
                "password": hashed_password
            }
            serializer = AuthorRegistrationSerializer(data=new_user)
            if serializer.is_valid():
                serializer.save()
                return Response("successful", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            msg = "Please provide sufficient data"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        except BaseException:
            msg = "Error"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class LoginAuthor(APIView):
    """user credentials matching"""
    def post(self, request, format=None):
        try:
            email = request.data["email"]
            password = request.data["password"]
            try:
                is_email_present = Author.objects.get(email=email)
                password_match = check_password(password, is_email_present.password)
                if password_match:
                    msg = "successful"
                    return Response(msg, status=status.HTTP_200_OK)
                else:
                    msg = "email and password don't match"
                    return Response(msg, status=status.HTTP_403_FORBIDDEN)
            except Author.DoesNotExist:
                msg = "Author does not exist"
                return Response(msg, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            msg = "Please provide sufficient Data"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        except BaseException:
            msg = "Error"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
