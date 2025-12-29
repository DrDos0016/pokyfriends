import os

from datetime import datetime
from django import forms
from django.template.defaultfilters import slugify

class CDosUpload_Upload_Form(forms.Form):
    DESTINATION_CHOICES = (("auto", "Automatic"), ("current", "Current Directory"), ("image", "Image Directory"))
    POST_PROCESSING_CHOICES =(("optipng", "Optimize PNG"), ("slugify", "Slugify"))
    IMAGE_EXTENSIONS = ["JPG", "JPEG", "GIF", "PNG", "WEBP", "BMP"]
    PATH_FOR_IMAGES = "/home/drdos/projects/pokyfriends/i.pokyfriends/"

    use_required_attribute = False
    attrs = {"method": "POST"}

    upload = forms.FileField()
    alt_name = forms.CharField(required=False, max_length=255, help_text="Rename file on upload. Include file extension.")
    destination = forms.ChoiceField(required=False, choices=DESTINATION_CHOICES, help_text="Auto uses extension to determine if image or not.")
    post_processing = forms.MultipleChoiceField(required=False, choices=POST_PROCESSING_CHOICES, help_text="Hover options for more info.")
    allow_overwrite = forms.BooleanField(required=False, label="Overwrite existing files", initial=True)

    def process(self, root_dir, subdir):
        upload = self.cleaned_data.get("upload")
        destination_name = (self.cleaned_data["alt_name"] or upload.name)

        if "slugify" in self.cleaned_data["post_processing"]:
            (head, tail) = os.path.splitext(destination_name)
            destination_name = slugify(head) + tail

        ext = destination_name.split(".")[-1].upper()
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
            if "optipng" in self.cleaned_data["post_processing"]:
                status = os.system("optipng -o7 -strip=all -fix -nc -quiet " + destination_full_path)

        return True
