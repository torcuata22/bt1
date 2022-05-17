from django.shortcuts import render

# Create your views here.
def starting_page(request):
   return render (request, "blog/index.html") # we added "templates" to settings.py, so Django will look there, we just need to specify blog/index.html

def posts(request):
    return render(request, "blog/all-posts.html")

def post_detail(request, slug):
    return render(request, "blog/post-detail.html")