from operator import length_hint
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator

# Create your models here.

class Tag(models.Model):
    caption=models.CharField(max_length=20) 
    
    def __str__(self):
        return f"{self.caption}"

class Author(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField() #max_length is not required (it's optional)
    
    def full_name (self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name()
    
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    author=models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts") #sets field to null if we delete related author, so we cna use "posts" instead of post_set for inverse querying
    excerpt= models.CharField(max_length=200)
    image= models.ImageField(upload_to="posts", null=True) #allows null values here
    date= models.DateField(auto_now=True) #it records date every time we modify field in the DB
    slug=models.SlugField(unique=True)#unique because I want to use it as an identifier
    content=models.TextField(validators=[MinLengthValidator(10)])
    tags=models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.title #overwrite this so the title of the post shows in the comments admin page instead of "object"
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)
    
class Comment(models.Model):
    user_name = models.CharField(max_length=200) #I want this to use label Your Name in the form
    user_email = models.EmailField() #And this to use label Your Email
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "comments")
    
        

 
       
    
    
