from django.forms import ModelForm, CheckboxInput
from .models import Post
from .widgets import Blog_Icon_Widget

class Post_Form(ModelForm):
    use_required_attribute = False

    class Meta:
        model = Post
        fields= [
            "title", "icon", "css", "content", "privacy", "schema", "password", "warnings",
            "summary",
            "current_mood", "current_music",
            "tags", "account", "django_add_ons",
        ]

        widgets = {
            "icon": Blog_Icon_Widget(),
        }
