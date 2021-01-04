from django.conf import settings
from rest_framework import serializers

from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

# This will help us return the serialized data{key:value} validated content
# using forms we were only able to validate and had to write the serialize fn self
# modelSerializer since we are to serialize tweet model
class TweetCreateSerializer(serializers.ModelSerializer):
    # two types of serializers
    # -> Read only serializer 
    # -> Create only serializer
    # # not this is worng<<->>here we are using read only serializer since wearen't to save any data to model
    likes = serializers.SerializerMethodField(read_only=True)
    # not above line so no get_likes method
    class Meta:
        model = Tweet
        fields = ['id','content','likes']
    def get_likes(self,obj):
        return obj.likes.count()
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("Tweet Length is bigger than 261")
        return value
class TweetSerializer(serializers.ModelSerializer):
    # -> Read only serializer
    likes = serializers.SerializerMethodField(read_only=True)#this help get_likes method return value to be serialized while executing the serializer
    parent = TweetCreateSerializer(read_only = True)# this will assign parent attribute tweet value of the parent which is retweeted i.e tweetCreateSerializer
    # since @property is used while def is_retweet function therefore we can take it as an attribute
    class Meta:
        model = Tweet
        fields = ['id','content','likes','is_retweet','parent']

    def get_likes(self,obj):
        return obj.likes.count()

# just to serialize the json data coming from the client side for action events
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank = True, required = False)
    # Field-level validation
    def validate_action(self, value):
        value = value.strip().lower()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError('Invalid Action')
        return value