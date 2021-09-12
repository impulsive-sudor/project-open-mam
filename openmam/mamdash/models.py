from django.core.files.storage import FileSystemStorage
from django.db import models
import re

fs = FileSystemStorage(location='/media/videos')

class Loginmanager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = "Your first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Your last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Must be at least 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email addresss!")

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=255)
    admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Loginmanager()

class Video(models.Model):
    title = models.CharField(max_length=255)
    # not sure how file path works vs file field
    file = models.FilePathField(path="/videos", match="*.mp4", recursive=True)
    file2 = models.FileField(storage=fs, default="none")
    filepath = models.FileField(default="none")
    details = models.TextField(default="some text")
    restricted = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, related_name='uploaded_video', on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favvideos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
