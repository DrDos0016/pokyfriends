from django import forms

from .models import Icon

class Blog_Icon_Widget(forms.Select):
    template_name = "cdosblog/widgets/post-icon-widget.html"
