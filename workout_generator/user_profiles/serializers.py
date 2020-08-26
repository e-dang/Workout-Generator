from rest_framework import serializers
from user_profiles.models import UserProfile
from users.serializers import UserSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    following = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)
    following_requests = serializers.StringRelatedField(many=True)
    follower_requests = serializers.StringRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'gender', 'weight', 'height', 'bmi', 'visibility',
                  'following', 'followers', 'following_requests', 'follower_requests')
