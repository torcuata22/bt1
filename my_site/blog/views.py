from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView

# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post #we need to override 2 methods here because home page doens't display ALL of the post, only 3 most recent ones
    ordering = ["-date"] #list of fields I want to use to order the data
    
    def get_queryset(self):
        queryset = super().get_queryset() #default fetches all posts
        data = queryset [:3] #limits number of posts fetched to only 3
        return data
    
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