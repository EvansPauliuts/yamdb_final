from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import EMAIL_USER
from users.models import User


def send_password(password, email):
    text_mail = f'ваш confirmation code: {password}'
    send_mail('code', text_mail, EMAIL_USER, [email])


def authenticate(email=None, password=None):
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
        else:
            return None
    except User.DoesNotExist:
        return None


def create_username(delta=0):
    delta += 1
    count_user = User.objects.all().first()
    user_name_id = count_user.id + delta
    username = f'user{user_name_id}'
    if User.objects.filter(username=username).exists():
        return create_username(delta)
    return username


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
            ),
        ]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
            ),
        ]
    )

    class Meta:
        fields = [
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        ]
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = ['email', 'username']

    def create(self, validated_data):
        password = get_random_string(
            length=50,
            allowed_chars='abcdefghijklmnopqrstuvwxyz'
                          'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )
        send_password(password, self.validated_data['email'])
        if User.objects.filter(email=self.validated_data['email']).exists():
            instance = User.objects.get(email=self.validated_data['email'])
            instance.set_password(password)
            instance.save()
            return instance
        instance = self.Meta.model(**validated_data)
        instance.username = self.validated_data.get('username')
        if instance.username is None:
            instance.username = create_username()
        instance.email = self.validated_data['email']
        instance.set_password(password)
        instance.save()
        return instance


class RegistrationTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('confirmation_code')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "confirmation_code".'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
