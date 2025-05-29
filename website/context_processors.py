import time
from django.conf import settings

from random import choice

BOOT_TS = int(time.time())

def pokyfriends_global_context(request):
    context = {}
    context["TS"] = BOOT_TS
    context["DEBUG"] = settings.DEBUG
    #TODO glob these on server boot
    bg = choice([
        "cs-arthur.png",
        "cs-night.png",
        "kdc-1.png",
        "kdc-2.png",
        "kdc-3.png",
    ])
    context["bg_url"] = "/static/global/bg/" + bg
    return context
