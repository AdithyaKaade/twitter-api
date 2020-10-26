from django.urls import path
from . import views

urlpatterns = [
   
   	path('tweets/',views.tweet_list_view),
   	path('tweets/feed',views.tweet_feed_view),
   	path('tweets/feed/retweet/<int:tweet_id>',views.tweet_feed_retweet_view),   	
   	path('tweets/feed/likes/<int:tweet_id>',views.tweet_feed_likes_view),
    path('tweets/<int:tweet_id>',views.tweet_detail_view),
    path('create-tweet/', views.tweet_create_view),
    path('tweets/<int:tweet_id>/delete', views.tweet_delete_view),
    path('tweets/action',views.tweet_action_view),

    
    
]