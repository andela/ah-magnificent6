from rest_framework import serializers

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birth_date', 'bio', 'avatar', 'city', 'country', 'phone', 'website', 'created_at', 'updated_at']
