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

        helpt_ext = {"css" : "<style> tags are auto added if missing"}

class Update_Post_Form(Post_Form):

    class Meta:
        model = Post
        fields= [
            "title", "icon", "css", "content", "privacy", "schema", "password", "warnings",
            "summary",
            "current_mood", "current_music",
            "tags", "account", "django_add_ons",
            "revision_date", "revision_details",
        ]

        widgets = {
            "icon": Blog_Icon_Widget(),
        }

        helpt_ext = {"css" : "<style> tags are auto added if missing"}
