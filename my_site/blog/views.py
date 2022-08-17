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
    
        def is_stored_post(self,request, post_id):
            stored_posts=request.session.get("stored_posts")
            if stored_posts is not None:
                is_saved_for_later= post_id in stored_posts
            else:
                is_saved_for_later= False
            return is_saved_for_later
            
                  
        def get(self,request, slug):
            post = Post.objects.get(slug = slug) #slug is the id here
            context = {
                "post":post,
                "post_tags": post.tags.all(),
                "comment_form": CommentForm(),  #object generated after info goes in the form (comment_form is the empty form to be filled)   
                "comments": post.comments.all().order_by("-id"), #fetches all comments associated to this comment
                "saved_for_later": self.is_stored_post(request, post.id)
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
                "comments": post.comments.all().order_by("-id"), #do it here, to, in case of failed validation
                "saved_for_later": self.is_stored_post(request, post.id)
            }
            return render (request, "blog/post-detail.html", context)
        
class ReadLaterView(View):
    #add GET method so we can use this view for the stored-posts template
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context={}
        if stored_posts is None or len(stored_posts)==0: #in case list is empty
            context["posts"] = []
            context["has_posts"]=False
        else: #if list is not empty we need to reach out to DB using post model (already imported)
           posts = Post.objects.filter(id__in=stored_posts) 
           context["posts"]=posts
           context["has_posts"]=True 
           
        return render(request, "blog/stored-posts.html", context)
        
    def post(self, request):
        stored_posts = request.session.get("stored_posts") #will return none if there are no saved posts
        
        if stored_posts is None:
            stored_posts=[]
        post_id=int(request.POST["post_id"]) #I don't want to add the whole post, just the id,so create this variable
        #Before appending post, make sure it wasn't already appended, so add if check:
        if post_id not in stored_posts:
             stored_posts.append(post_id)
             request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"]=stored_posts
        return HttpResponseRedirect("/")
        

    
