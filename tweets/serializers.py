from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import  Tweet

TWEET_ACTION_OPTIONS = ['like', 'unike', 'retweet']

class TweetCreateSerializer(serializers.ModelSerializer):
	user = PublicProfileSerializer(source='user.profile', read_only=True) #serializers.SerializerMethodField(read_only=True)
	likes = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model=Tweet
		fields='__all__'
	def get_likes(self, obj):
		return obj.likes.count()


class TweetSerializer(serializers.ModelSerializer):
	user = PublicProfileSerializer(source='user.profile', read_only=True)
	likes = serializers.SerializerMethodField(read_only=True)
	parent = TweetCreateSerializer(read_only=True)
	class Meta:
		model=Tweet
		fields='__all__'
	def get_likes(self, obj):
		return obj.likes.count()


class TweetSerializerLikes(serializers.ModelSerializer):
	user = PublicProfileSerializer(source='user.profile', read_only=True)
	likes = serializers.SerializerMethodField(read_only=True)
	parent = TweetCreateSerializer(read_only=True)
	class Meta:
		model=Tweet
		fields='__all__'
	def get_likes(self, obj):
#		print(obj.user)
#		print(type(obj))
#		print(user_likes, user)
#		users_who_like = obj.likes.values_list('username', flat=True)
#		user_followers = user.profile.followers.values_list('username', flat=True)
#		print(users_who_like, user_followers)
		return obj.likes.values_list('username', flat=True)



class TweetActionSeralizer(serializers.Serializer):
	id = serializers.IntegerField()
	action = serializers.CharField()
	content = serializers.CharField(allow_blank=True, required=False)

	def validate_actions(self, value):
		value = value.lower().strip()
		if not value in TWEET_ACTION_OPTIONS:
			raise serializers.ValidationError("This is not a valid action for tweets")
		return value