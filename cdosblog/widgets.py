from django import forms

from .models import Icon, Tag

class Blog_Icon_Widget(forms.Select):
    template_name = "cdosblog/widgets/post-icon-widget.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["icons"] = Icon.objects.all().order_by("title")
        return context

class Blog_Tags_Widget(forms.CheckboxSelectMultiple):
    use_fieldset = False
    template_name = "cdosblog/widgets/blog-tags-widget.html"
    option_template_name = "cdosblog/widgets/blog-tags-widget-options.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        print("Calling all tags")
        context["tags"] = Tag.objects.all()
        if hasattr(self, "tags_str"):
            context["tags_str"] = self.tags_str
        else:
            context["tags_str"] = ""
        return context
