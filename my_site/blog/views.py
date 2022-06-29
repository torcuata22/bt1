from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView

# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post #we need to override 2 methods here because home page doens't display ALL of the post, only 3 most recent ones
    ordering = ["-date"] #list of fields I want to use to order the data (-date = date in descending order)
    context_object_name = "posts" #Django uses Object List by default, so I need to change that to this because my template displays "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset() #default fetches all posts
        data = queryset [:3] #limits number of posts fetched to only 3
        return data
    
class AllPostsViews(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"
    
class SinglePostView(DetailView):
        template_name = "blog/post-detail.html"
        model = Post 
        
        def get_context_data(self, **kwargs):
             context = super().get_context_data(**kwargs)
             context["post_tags"] = self.object.tags.all() #access all tags for the post and expose it through our context
             return context
        

    
