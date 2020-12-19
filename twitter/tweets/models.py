from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

class Tweet(models.Model):
    # Maps to SQL data
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # many users can have many tweets
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    
    # can be used to return customised result in admin panel
    # so that we can see self.content for ex when we search something related to 
    # tweets
    def __str__(self):
        return self.content
    
    class Meta:
        # to return list of data in descending order of the id
        # if not - then asecending
        ordering = ['-id']
    # serialising data here so that can return serialised data
    # to the view rather than formatting in the view    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }