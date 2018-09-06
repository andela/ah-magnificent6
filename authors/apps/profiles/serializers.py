from rest_framework import serializers

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birth_date', 'bio', 'gender', 'avatar', 'city', 'country', 'phone', 'website', 'following', 'created_at', 'updated_at']
