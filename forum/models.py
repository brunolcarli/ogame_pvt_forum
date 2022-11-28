from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    avatar = models.BinaryField(null=True)
    bio = models.TextField()


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posted_by')
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey('forum.Thread', on_delete=models.CASCADE)


class Thread(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    content = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='thread_creator')
    open_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    closing_date = models.DateTimeField(null=True)
    closed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_user', null=True)
    section = models.ForeignKey('forum.Section', on_delete=models.CASCADE)
    last_post_datetime = models.DateTimeField(null=True)


class Section(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False)
