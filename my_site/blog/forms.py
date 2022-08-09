from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"] #fields I don't want to include
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email", 
            "text": "Your Comment"
        }
        
        #fields = [""] create list of fields I want to include, post field not included, becuase users should not see it