from django.db import models
from django.conf import settings
from django.db.models import Q
# Create your models here.

User = settings.AUTH_USER_MODEL

class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True)
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-time")

class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Tweet(models.Model):
	#id = models.AutoField(primary_key=true)
	# if a user deletes his account, all his tweets are deleted
	# foreignkey is used because we want one user to be able to post multiple tweets
	# parent is null for an original tweet, for retweets parents aren't null
	parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='tweets') 
	likes = models.ManyToManyField(User, related_name='tweet_user', blank=True)
	content = models.TextField()
	time = models.DateTimeField('content', auto_now=True)
	objects = TweetManager()

	class Meta:
		ordering = ['-id']

	@property
	def is_retweet(self):
		return self.parent != None