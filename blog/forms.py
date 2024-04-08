from django import forms

from blog.models import Blog
from users.forms import FormStyleMixin


class BlogForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ('slug',)
