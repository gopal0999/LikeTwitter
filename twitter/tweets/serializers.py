from django.conf import settings
from rest_framework import serializers

from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

# This will help us return the serialized data{key:value} validated content
# using forms we were only able to validate and had to write the serialize fn self
# modelSerializer since we are to serialize tweet model
class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("Tweet Length is bigger than 261")
        return value