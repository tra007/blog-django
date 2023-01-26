from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm


# Create your views here.

def post_list(request, tag_slug=None):
    """ return all post published in html page """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, post, year, month, day):
    """ return item with id get """
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # list similar post
    post_tags_ids = post.tags.values_list("id", flat=True)  # list of id tags for this post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)  # filter post by list of id
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by('-same_tags', '-publish')[
                    :4]  # annotate by tags and ordered

    return render(request, "blog/post/detail.html",
                  {"post": post, "comments": comments, "form": form, 'similar_posts': similar_posts})


def post_share(request, post_id):
    """send post to someone"""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.changed_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n {cd['name']} \'s comments: {cd['comments']}"
            send_mail(subject, message, "your_account@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    result = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            # result = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)) \
            #     .filter(rank__gte=0.3).order_by("-rank")
            result = Post.published.annotate(similarity=TrigramSimilarity('title', query), ) \
                .filter(similarity__gt=0.1).order_by("-similarity")
    return render(request, "blog/post/search.html", {"form": form, "query": query, "results": result})
