import time
from datetime import datetime
from django.conf import settings

from random import choice

BOOT_TS = int(time.time())

def pokyfriends_global_context(request):
    context = {}
    context["TS"] = BOOT_TS
    context["DEBUG"] = settings.DEBUG
    #TODO glob these on server boot
    bgs = [
        "cs-arthur.png",
        "cs-night.png",
        "kdc-1.png",
        "kdc-2.png",
        "kdc-3.png",
        "bb-1.png",
        "sor2-1.png",
    ]
    if not request.GET.get("bg"):
        day_count = datetime.now().strftime("%j")
        idx = int(day_count) % len(bgs)
    else:
        try:
            idx = int(request.GET.get("bg"))
        except ValueError:
            idx = 0
        if idx >= len(bgs):
            idx = 1
    bg = bgs[idx]
    context["bg_url"] = "/static/global/bg/" + bg
    return context
