from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class PublishedManager(models.Manager):
    """ custom manager for post """

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """ post model for blog """

    class Status(models.TextChoices):
        """ choices filed for status of post """
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
            # this is improve performance for queries filtering or ordering results by this field.
            # This option allows you to define database indexes for your model
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        """ absolute url for post model """
        return reverse("blog:post_detail", args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])
