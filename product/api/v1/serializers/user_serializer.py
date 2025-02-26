from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = ('email',
                  'username',
                  'first_name',
                  'last_name',
                  )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    class Meta:
        model = Subscription
        fields = (
            'student',
            'course',
            'enrolled_at',
        )
