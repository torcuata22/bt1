from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def starting_page(request):
    latest_posts=Post.objects.all().order_by("-date")[:3] #Django doesn't support negtive indexing in this case 
    return render (request, "blog/index.html", {
        "posts": latest_posts
        }) # we added "templates" to settings.py, so Django will look there, we just need to specify blog/index.html

def posts(request):
    all_posts=Post.objects.all().order_by("-date") #this gives us all the posts from the database
    return render(request, "blog/all-posts.html", {
        "all_posts":all_posts
    })

#this one fetches the one post I select
def post_detail(request, slug):
    #identified_post = Post.objects.get(slug=slug)gets a single post, left slug is the slig form db and right slug is argument slug
    identified_post=get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {
        "post":identified_post,
        "post_tags": identified_post.tags.all()
    })