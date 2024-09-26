import json

import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokyfriends.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402

from cdosgallery.models import *

def main():
    with open("pokydb.json") as fh:
        raw = fh.read()

    data = json.loads(raw)

    print("DO NOT RUN WITHOUT PREP WORK")
    return False

    for d in data:
        if d.get("model") == "gallery.character":
            continue
            print(d)
            c = Character(name=d["fields"]["name"], slug=d["fields"]["slug"], species=d["fields"]["species"])
            c.save()

        #continue

        if d.get("model") == "gallery.artist":
            continue
            print(d)
            a = Artist(name=d["fields"]["name"], gallery=d["fields"]["gallery"])
            a.save()

        #continue

        if d.get("model") == "gallery.image":
            continue
            print(d)
            i = Image(filename=d["fields"]["filename"], description=d["fields"]["description"])
            i.save()

        #continue

        if d.get("model") == "gallery.exhibit":
            print(d)
            sfw_value = "Clean" if d["fields"]["sfw"] else "Explicit"
            #OLD: title, slug, description, date, sfw, sources (textfield), visibility (int), artist=FK, images=M2M, characters=M2M
            e = Exhibit(
                title=d["fields"]["title"],
                description=d["fields"]["description"],
                date=d["fields"]["date"],
                rating=sfw_value,
                visibility="Visible",
            )
            e.save()

            # Add sources (\r\n)
            if d["fields"]["sources"]:
                old_sources = d["fields"]["sources"].split("\r\n")
                for src in old_sources:
                    s = Source(url=src)
                    s.save()
                    e.sources.add(s)

            # Add character assoc
            if d["fields"]["characters"]:
                for foo in d["fields"]["characters"]:
                    e.characters.add(foo)

            # Add artist assoc
            if d["fields"]["artist"]:
                e.artist_id = (d["fields"]["artist"])
                e.save()

            # Add image assoc
            if d["fields"]["images"]:
                for foo in d["fields"]["images"]:
                    e.images.add(foo)
    return True


if __name__ == '__main__':
    main()
