import datetime

from django import forms
from .models import Exhibit, Artist, Character

class Gallery_Upload_Form(forms.Form):
    use_required_attribute = False
    attrs = {"method": "POST"}

    title = forms.CharField(max_length=255)
    description = forms.CharField()
    rating = forms.ChoiceField(choices=Exhibit.RATING_CHOICES)
    visibility = forms.ChoiceField(choices=Exhibit.VISIBILITY_CHOICES)
    date = forms.DateField(initial=datetime.date.today)
    artist = forms.ModelChoiceField(queryset=Artist.objects.all())
    character = forms.ModelMultipleChoiceField(queryset=Character.objects.all())
    media = forms.FileField()
    source = forms.CharField(max_length=255, help_text="URL of source", required=False)
    source_site = forms.CharField(max_length=100, help_text="Autopopulated from URL when recognized (FA/Tumblr/DA...)", required=False)

    def process(self, root_dir, subdir):
        upload = self.cleaned_data.get("upload")
        destination_name = (self.cleaned_data["alt_name"] or upload.name)
        ext = destination_name.split(".")[-1].upper()
        print("EXT", ext)
        print(self.IMAGE_EXTENSIONS)
        print("DEST", self.cleaned_data["destination"])
        if (ext in self.IMAGE_EXTENSIONS and self.cleaned_data["destination"] == "auto") or (self.cleaned_data["destination"] == "image"):
            today = datetime.now()
            destination_full_path = os.path.join(self.PATH_FOR_IMAGES, str(today.year), destination_name)
        else:
            destination_full_path = os.path.join(root_dir, subdir, destination_name)

        if not self.cleaned_data["allow_overwrite"] and os.path.isfile(destination_full_path):
            self.add_error(None, "File `{}` already exists!".format(destination_full_path))
            return False

        with open(destination_full_path, 'wb+') as fh:
            for chunk in upload.chunks():
                fh.write(chunk)
            print("WROTE", destination_full_path)

        return True
