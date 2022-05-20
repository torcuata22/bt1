from operator import length_hint
from tkinter import CASCADE
from django.db import models
from django.utils.text import slugify

# Create your models here.

class Tag(models.Model):
    caption=models.CharField(max_length=25) 

class Author(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=300)
    
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    author=models.ForeignKey(Author, on_delete=CASCADE)
    excerpt= models.CharField(max_length=200)
    image_name = models.CharField(max_length=100) #temporary
    date= models.DateField(auto_now=True) #it records date every time we modify field in the DB
    slug=models.SlugField(unique=True)#unique because I want to use it as an identifier
    content=models.TextField()
    tag=models.ManyToManyField(Tag)
    
    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        


       
    
    
