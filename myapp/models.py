from django.db import models

from django.contrib.auth.models import User


class TimeStamp(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields you want to store for the user

    def __repr__(self):
        return f'{self.user}'

class Image(TimeStamp):
    image = models.ImageField(upload_to='images/')

    def __repr__(self):
        return f'{self.image}'

class Post(TimeStamp):
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    images = models.ManyToManyField(Image, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)    

    def __repr__(self):
        return f'{self.title}'
