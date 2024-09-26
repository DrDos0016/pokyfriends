import glob
import io
import os
import time
import subprocess

from django.shortcuts import render

SITE_ROOT = "/home/drdos/projects/pokyfriends/"

def pokedex_ebooks_web_index(request):
    context = {}
    default_seed = hex(int(time.time()))[2:]

    SITE_PYTHON = os.path.join(SITE_ROOT, "venv", "bin", "python3")

    ambiguity_arg = ""
    starts_with_arg = ""
    if int(request.GET.get("ambiguous", 0)):
        ambiguity_arg = "-a"
    if request.GET.get("starts_with", ""):
        starts_with_arg = "-s " + request.GET.get("starts_with")

    if request.GET.get("seed"):
        seed = request.GET.get("seed")
    else:
        seed = default_seed

    proc_call = [
        SITE_PYTHON,
        os.path.join(SITE_ROOT, "website", "pokedex_ebooks.py"),
        "-l {}".format(request.GET.get("size", 140)),
        "-r {}".format(seed)
    ]

    if starts_with_arg:
        proc_call.append(starts_with_arg)
    if ambiguity_arg:
        proc_call.append(ambiguity_arg)

    proc_resp = subprocess.run(proc_call, capture_output=True, text=True)

    context["markov"] = proc_resp.stdout
    context["error"] = proc_resp.stderr
    context["seed"] = seed
    return render(request, "website/doodle/pokedex-ebooks-web.html", context)

def pokedex_ebooks_web_comics(request):
    context = {}
    return render(request, "website/doodle/pokedex-ebooks-comics.html", context)
