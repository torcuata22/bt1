from django.shortcuts import render
from datetime import date

posts=[
    {
        "slug":"hike-in-the-mountains",
        "image": "mounatins.jpg",
        "author":"Marilyn",
        "date": date(2022, 5, 17),
        "title":"Mountin Hiking",
        "excerpt": "Nothing beats the view from the top of a mountain"
        
    }
    
]

# Create your views here.
def starting_page(request):
   return render (request, "blog/index.html") # we added "templates" to settings.py, so Django will look there, we just need to specify blog/index.html

def posts(request):
    return render(request, "blog/all-posts.html")

def post_detail(request, slug):
    return render(request, "blog/post-detail.html")