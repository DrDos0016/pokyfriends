from django import forms
from .models import Exhibit

class Gallery_Upload_Form(forms.ModelForm):
    class Meta:
        model = Exhibit
        fields = ["media", "title", "description", "rating", "visibility", "date", "artist", "characters"]

    use_required_attribute = False
    attrs = {"method": "POST"}

    media = forms.CharField(max_length=10)
    source = forms.CharField(max_length=255, help_text="URL of source")
    source_site = forms.CharField(max_length=100, help_text="Autopopulated from URL when recognized (FA/Tumblr/DA...)")

    def clean_background(self):
        if self.cleaned_data["background"] == "transparent" and not self.fields["background"].widget.allow_transparent:
            self.add_error("background", "Invalid color selected.")
        return self.cleaned_data["background"]
