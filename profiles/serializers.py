from rest_framework import serializers
from .models import Profile

class PublicProfileSerializer(serializers.ModelSerializer):
	username = serializers.SerializerMethodField(read_only=True)
	follower_count = serializers.SerializerMethodField(read_only=True)
	following_count = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Profile
		fields = [
				'id',
				'username',
				'follower_count',
				'following_count'
		]


	def get_username(self, obj):
		return obj.user.username

	def get_following_count(self, obj):
#		print(obj.user.following.count())
		return obj.user.following.count()

	def get_follower_count(self, obj):
#		print(obj.followers.all())
		return obj.followers.count()


class PublicSerializer(serializers.ModelSerializer):
	username = serializers.SerializerMethodField(read_only=True)
	follower_count = serializers.SerializerMethodField(read_only=True)
	following_count = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Profile
		fields = [
				'id',
				'username',
				'follower_count',
				'following_count'
		]


	def get_username(self, obj):
		return obj.user.username

	def get_following_count(self, obj):
		return obj.user.following.values_list('user__username', flat=True)


	def get_follower_count(self, obj):
		return obj.followers.values_list('username', flat=True)
