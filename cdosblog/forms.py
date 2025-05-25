from django import forms
from django.forms import ModelForm, CheckboxInput
from .models import Post, Tag, Icon
from .widgets import Blog_Icon_Widget, Blog_Tags_Widget

class Post_Form(ModelForm):
    use_required_attribute = False
    tags_str = forms.CharField(widget=Blog_Tags_Widget, label="Tags")

    class Meta:
        model = Post
        fields= [
            "account",
            "title", "content", "current_mood", "current_music", "icon", "summary", "tags_str", "warnings",
            "privacy", "password", "schema", "css", "django_add_ons",
        ]

        widgets = {
            "icon": Blog_Icon_Widget(),
        }

        help_texts = {
            "css" : "&lt;style&gt; tags optional.",
            "warnings": "If set, post is wrapped in a &lt;details&gt; tag. Value set will be displayed as entered in the &lt;summary&gt;",
        }

    def clean_tags_str(self):
        print(self.cleaned_data.get("tags_str"))
        return self.cleaned_data.get("tags_str")

class Update_Post_Form(Post_Form):
    tags_str = forms.CharField(widget=Blog_Tags_Widget, label="Tags")

    class Meta:
        model = Post
        fields= [
            "account",
            "title", "content",
            "revision_date", "revision_details",
            "current_mood", "current_music", "icon", "summary", "tags_str", "warnings",
            "privacy", "password", "schema", "css", "django_add_ons",
        ]

        widgets = {
            "icon": Blog_Icon_Widget(),
        }
