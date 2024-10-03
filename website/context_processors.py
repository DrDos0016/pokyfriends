import time
from django.conf import settings

BOOT_TS = int(time.time())

def pokyfriends_global_context(request):
    context = {}
    context["TS"] = BOOT_TS
    context["DEBUG"] = settings.DEBUG
    return context
