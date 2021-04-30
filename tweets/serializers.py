from rest_framework import serializers
from django.conf import settings
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweet")
        return value

class TweetCreateSerializer(serializers.ModelSerializer):
    # user = PublicProfileSerializer(source='user.profile', read_only=True) # serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['content', 'likes']
    def get_likes(self, obj):
        return obj.likes.count()
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value
    def get_user(self, obj):
        return obj.user.id

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    # 这里的SerializerMethodField对应下面的 def get_likes
    class Meta:
        model = Tweet
        fields = [
            'user',
            'content',
            'likes',
            'is_retweet',
            'parent',
            'timestamp'
        ]
    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value