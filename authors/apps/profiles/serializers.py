from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='get_username')

    class Meta:
        model = Profile
        fields = [
            'username', 'first_name', 'last_name', 'birth_date', 'bio',
            'avatar', 'city', 'country', 'phone', 'website', 'created_at',
            'updated_at', 'app_notification_enabled'
        ]
