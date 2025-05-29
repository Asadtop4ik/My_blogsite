from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)  # Reduced max_length
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # Reduced max_length
    publish = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager()  # Fixed typo from 'object' to 'objects'
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog_site:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)  # Made optional
    body = models.TextField(max_length=1000)  # Added max_length
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'