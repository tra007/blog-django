from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post


# Create your views here.

def post_list(request):
    """ return all post published in html page """
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, post, year, month, day):
    """ return item with id get """
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("page not found")
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, "blog/post/detail.html", {"post": post})
