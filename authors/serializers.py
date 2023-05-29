from .models import Author
from rest_framework import serializers


class AuthorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "email", "password"]
    

class AuthorLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author 
        fields = ["email", "password"]