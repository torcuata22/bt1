from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm

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
    
class SinglePostView(View):        
        def get(self,request, slug):
            post = Post.objects.get(slug = slug) #slug is the id here
            context = {
                "post":post,
                "post_tags": post.tags.all(),
                "comment_form": CommentForm(),  #object generated after info goes in the form (comment_form is the empty form to be filled)   
                "comments": post.comments.all().order_by("-id") #fetches all comments associated to this comment
            }
            return render (request, "blog/post-detail.html", context)
            
        def post(self, request, slug):
            comment_form = CommentForm(request.POST)
            post = Post.objects.get(slug=slug)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse("post-detail-page", args=[slug])) #slug is already part of url, functions as id
           
            #this is what happens if the form is invalid
            context={
                "post":post,
                "post_tags": post.tags.all(),
                "comment_form": comment_form,
                "comments": post.comments.all().order_by("-id") #do it here, to, in case of failed validation
            }
            return render (request, "blog/post-detail.html", context)
        

    
