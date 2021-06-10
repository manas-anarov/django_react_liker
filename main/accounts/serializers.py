from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    EmailField,
)
from django.contrib.auth.models import User
from django.conf import settings
import requests

import clearbit

clearbit.key = settings.CLEARBIT_SECRET


class RegisterSerializer(ModelSerializer):
    email = EmailField(label='Email address')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        ]

    extra_kwargs = {"password": {"write_only": True},
                    "id": {"read_only": True},
                    "first_name": {'required': False, 'allow_blank': True},
                    "last_name": {'required': False, 'allow_blank': True},
                    }

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise ValidationError("User with this username already exists")
        return value

    def validate_email(self, value):
        email = value
        email_qs = User.objects.filter(email___iexact=email)
        if email_qs.exists():
            raise ValidationError("Email already registered")

        hunter_secret = settings.HUNTER_SECRET
        hunter_url = 'https://api.hunter.io/v2/email-verifier?email={}&api_key={}'.format(email, hunter_secret)
        hunter_data = requests.get(hunter_url)

        hunter_json = hunter_data.json()
        email_status = hunter_json['data']['status']
        if email_status == 'invalid':
            raise ValidationError(email_status)

        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        final_first_name = ""
        final_last_name = ""

        if len(first_name) > 0:
            final_first_name = first_name
        else:

            clear_data = clearbit.Enrichment.find(email=email, stream=True)
            clear_name = clear_data['person']['name']['givenName']
            if len(clear_name) > 0:
                final_first_name = clear_name

        if len(last_name) > 0:
            final_last_name = last_name
        else:
            clear_data = clearbit.Enrichment.find(email=email, stream=True)
            clear_last_name = clear_data['person']['name']['familyName']
            if len(clear_last_name) > 0:
                final_last_name = clear_last_name

        user_obj = User(
            username=username,
            email=email,
            first_name=final_first_name,
            last_name=final_last_name,
        )
        user_obj.set_password(password)
        user_obj.save()
        return user_obj
