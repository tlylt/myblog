#two base forms 1.form 2.ModelForm
from django import forms
from .models import Comment

#1
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # widget attribute changes the default mapping of HTML element
    comments = forms.CharField(required=False,widget=forms.Textarea) 
    
#2
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')


