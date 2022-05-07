from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post (models.Model):
    post_body=models.TextField()
    date=models.DateTimeField()
    updated_dat=models.DateTimeField(auto_now=True,null=True)
    likes=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user} wrote post at {self.date}'

    def serialize(self):
        return {
            "id": self.id,
            "post_body": self.post_body,
            "user": self.user.username,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,

        }

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.CharField(max_length=500)
    posts=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user} wrote {self.comments}'
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'



class Follower (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_profile')
    user_follower=models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    user_following=models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True)
    def __str__(self):
        return f'{self.user}:  has {self.user_follower} as follower'

    class Meta:
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'


class Like (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='userLike')
    posts=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='likePost')
    def __str__(self):
        return f'{self.user} like {self.posts}'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
