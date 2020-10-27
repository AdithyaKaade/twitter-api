# twitter-api

Here we have the backend of a twitter like program, where a user can view their feed(timeline) containing all tweets in the past 24hrs by the user and the people they follow. 
A user can like or retweet tweets on their feed.
A user can see who has liked or tweeted a particular tweet, given that the user follows that specific person.
A user can view all the people who follow a particular user and which user that specific user is following. 

<h2>In the sqlite database I've stored the following details:<h2>

<h3>Users are:</h3>
<br>adithya
<br>jim
<br>tom
<br>jerry

<h3>Following relationship : (eg. A -> B,C. Here it means 'A' is following 'B' and 'C')</h3>

<br>adithya: jim, tom, jerry
<br>jim: tom, jerry
<br>tom: jerry, adithya
<br>jerry: adithya, jim

<h3>Details about tweets:</h3>

Each user has posted 1 tweet.
<br>Each user likes and rewteets all the tweets on their feed, except for their own tweet.


['GET'] URLs:

'/tweets/' - to view all the tweets in the database.
'/tweets/<int:tweet_id>' - to view a specific tweet in the database.
'/profile/<str:username>' - to view the details of a user. It contains the people followed by the user and the people who are following the user.
*have to be logged in to view the following:
'/tweets/feed' - to view the feed/timeline of a specific user.
'/tweets/feed/likes/<int:tweet_id> - to view the users who have liked a specific tweet.
'/tweets/feed/retweet/<int:tweet_id> - to view the users who have retweeted a specific tweet.

['POST'] URLs:

*have to be logged in to perfom this action
'/tweets/create-tweet' - creates a new tweet with the given content.
'/tweets/action' - the action can be like, unlike or retweet. We need to provide the tweet_id, action and content. If the action is like or unlike we don't have to provide the content.
'/profile/<str:username>' - the action can be either follow or unfollow depending on what the user logged in wants to perform.


['DELETE'] URL:

'/tweets/<int:tweet_id>/delete' - to delete a specific tweet in the database.
