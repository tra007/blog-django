from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"  # how frequently the content on the page changes it can be : always, daily , yearly and etc
    priority = 0.9  # is the importance of the pages to the other pages on your site. The value can be anywhere from 0.0 to 1.0

    def items(self):
        """returns a list of all of the model objects we want to be listed in the Django sitemap."""
        return Post.published.all()

    def lastmod(self, obj):
        """returns the last time the model object was modified"""
        return obj.updated  # returns the last time the object was modified.

# if haven't the get absolute url we should use location method
