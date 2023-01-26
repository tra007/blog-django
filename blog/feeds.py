import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):
    title = 'my blog'
    link = reverse_lazy("blog:post_list")
    description = "new posts of my blog"

    def items(self):
        """method retrieves the objects to be included in the feed"""
        return Post.published.all()[:5]

    def item_title(self, item):
        """return the title"""
        return item.title

    def item_description(self, item):
        """return the description"""
        return truncatechars_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        """return publication"""
        return item.publish
