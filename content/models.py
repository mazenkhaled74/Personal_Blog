from django.db import models
from auth_manager.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name="posts", blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    comments = models.ManyToManyField(Comment, related_name="posts", blank=True)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
