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
    excerpt= models.TextField()
    image_name = models.CharField(max_length=200)
    date= models.DateField(auto_now=False, auto_now_add=False)
    slug=models.SlugField(default="", null=False)
    content=models.TextField()
    tag=models.ManyToManyField(Tag)
    
    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        


       
    
    
