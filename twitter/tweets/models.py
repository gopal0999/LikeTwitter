from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

# this is just to keep the details of a like and fetch it when we need it

class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    # Maps to SQL data
    # id = models.AutoField(primary_key=True)
    # now null = True to allow in database
    # and on_delete = models.SET_NULL so when parent is deleted then we se null to the parent field of child tweets(retweets)
    parent = models.ForeignKey("self",null = True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # one user can have many tweets
    likes = models.ManyToManyField(User,related_name='tweet_user',blank=True , through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # can be used to return customised result in admin panel
    # so that we can see self.content for ex when we search something related to 
    # tweets
    # def __str__(self):
    #     return self.id
    
    class Meta:
        # to return list of data in descending order of the id
        # if not - then asecending
        ordering = ['-id']
    # serialising data here so that can return serialised data
    # to the view rather than formatting in the view    
    @property
    def is_retweet(self):
        return self.parent != None
        
    def serialize(self):
        '''
        We can remove this as we already have defined correspoding serializers
        '''
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }