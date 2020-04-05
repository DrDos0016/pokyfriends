from django.shortcuts import render


def generic(request, page="index.html", slug=None):
    data = {
        "title": "Let's Be Pokyfriends",
    }

    if slug:
        page = "info/" + slug + ".html"

    return render(request, "pokyfriends_web/" + page, data)
