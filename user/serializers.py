from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from .models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_user_name',
            'last_user_name',
            'gender',
            'nationality',
            'province',
            'district',
            'city',
            'profession',
            'provenance',
            'contact',
            'birthday',
            'password',
            'groups',
            'active',
            'date_joined',
            'last_login'
        ]

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserAddSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_user_name',
            'last_user_name',
            'gender',
            'nationality',
            'province',
            'district',
            'city',
            'profession',
            'provenance',
            'contact',
            'birthday',
            'password',
            'active',
            'date_joined',
            'last_login'
        ]

    def create(self, validated_data):
        user = super(UserAddSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])

        groups = validated_data.pop('groups', [])
        for group in groups:
            group = Group.objects.get(id=group)
            user.groups.add(group)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        from rest_framework.authtoken.models import Token
        username = attrs.get('username')
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            data = {
                'user': user,
                'email': user.email,
                'username': f'{user.first_user_name} {user.last_user_name}',
                'token': Token.objects.get_or_create(user=user)[0].key
            }
            return data
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authentication')


class UserLightSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_user_name = serializers.CharField(read_only=True)
    last_user_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_user_name',
            'last_user_name',
        ]
