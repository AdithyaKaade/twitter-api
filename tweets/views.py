from django.shortcuts import render
from django.conf import settings
import requests
from django.db.models import Q
from datetime import datetime, timezone, timedelta
from django.http import HttpResponse ,Http404, JsonResponse
# Create your views here.
import random
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Tweet
from .forms import TweetForm
from .serializers import (
						TweetSerializer,	
						TweetActionSeralizer,
						TweetCreateSerializer,
						TweetSerializerLikes)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
	qs = Tweet.objects.filter(id = tweet_id)
	if not qs.exists():
		return Response({}, status=404)
	obj = qs.first()
	tweets_list = TweetSerializer(obj)
	return Response(tweets_list.data)

@api_view(['DELETE'])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
	qs = Tweet.objects.filter(id = tweet_id)
	if not qs.exists():
		return Response({}, status=404)
	qs = qs.filter(user=request.user)
	if not qs.exists():
		return Response({"Message": "You cannot delete this tweet"})
	obj = qs.first()
	obj.delete()
	return Response({"Message": "Tweet removed"}, status=200)

@api_view(['POST'])
def tweet_action_view(request, *args, **kwargs):
	"""
	action: like, unlike and retweet

	"""
	serializer = TweetActionSeralizer(data=request.data)
	if serializer.is_valid(raise_exception=True):
		data = serializer.validated_data
		tweet_id = data.get("id")
		action = data.get("action")
		content = data.get("content")
		qs = Tweet.objects.filter(id = tweet_id)
		if not qs.exists():
			return Response({}, status=404)
		obj = qs.first()
		if action == 'like':
			obj.likes.add(request.user)
			serializer = TweetSerializer(obj)
			return Response(serializer.data, status=200)
		elif action == 'unlike':
			obj.likes.remove(request.user)
			serializer = TweetSerializer(obj)
			return Response(serializer.data, status=200)
		elif action == 'retweet':
			new_tweet = Tweet.objects.create(user=request.user, parent=obj, content=content)
			serializer = TweetSerializer(new_tweet)
			return Response(serializer.data, status=201)
			pass
	return Response({}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request, *args, **kwargs):
	time_threshold = datetime.now(timezone.utc) - timedelta(hours=24)
	user = request.user
	qs = Tweet.objects.feed(user).filter(time__gte=time_threshold)
	tweets_list = TweetSerializer(qs, many=True)
	return Response(tweets_list.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweet_feed_likes_view(request, tweet_id, *args, **kwargs):

	time_threshold = datetime.now(timezone.utc) - timedelta(hours=24)
	user = request.user
	user_data = requests.get('http://127.0.0.1:8000/profile/'+str(user))
	following = set(user_data.json()['following_count'])
	following.add(str(user))
	qs = Tweet.objects.feed(user).filter(
            Q(time__gte=time_threshold) &
            Q(id=tweet_id))
	tweets_list = TweetSerializerLikes(qs, many=True)
	if(len(tweets_list.data) == 0):
		return Response({"message": "Not Authorised"})
	show_likes = {'usernames':[]}
#	print(following, tweets_list.data[0]['likes'])
	for like in tweets_list.data[0]['likes']:
		if like in following:
			show_likes['usernames'].append(like)
	return Response(show_likes)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
	qs = Tweet.objects.all()
	username = request.GET.get('username')
	if username != None:
		qs = qs.by_username(username)
	tweets_list = TweetSerializer(qs, many=True)
	return Response(tweets_list.data)

@api_view(['GET'])
def tweet_feed_retweet_view(request, tweet_id, *args, **kwargs):
	user = request.user
	user_data = requests.get('http://127.0.0.1:8000/profile/'+str(user))
	following = set(user_data.json()['following_count'])
	following.add(str(user))
	qs = Tweet.objects.all().filter(
							#Q( ) |
							Q(parent__id=tweet_id))
	username = request.GET.get('username')

	if username != None:
		qs = qs.by_username(username)
	tweets_list = TweetSerializer(qs, many=True)
	if(len(tweets_list.data) == 0):
		return Response({"message": "Not Authorised/No retweets"})

	show_retweets = []
	final_retweets = {'viewable_username':[], 'Total_count': qs.count()}
#	print(tweets_list.data[0]['parent'])
	for retweet in tweets_list.data:
		#print(retweet)
		show_retweets.append(retweet['user']['username']) 

	for retweet in show_retweets:
		if retweet in following:
			final_retweets['viewable_username'].append(retweet)
	return Response(final_retweets)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
	serializer = TweetCreateSerializer(data=request.data)
	if serializer.is_valid(raise_exception=True):
		serializer.save(user=request.user)
		return Response(serializer.data, status = 201)
	return Response({}, status=400)
