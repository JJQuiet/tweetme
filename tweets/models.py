from django.db import models
import random
from django.conf import settings

User = settings.AUTH_USER_MODEL # django 内置对象

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Tweet(models.Model):
    # user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) #  many users can many tweets
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 用来
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def is_retweet(self):
        return self.parent != None
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes":  random.randint(0, 200)
        }
    
    def __str__(self):
        return self.content

