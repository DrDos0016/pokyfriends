import time

BOOT_TS = int(time.time())

def pokyfriends_global_context(request):
    context = {}
    context["TS"] = BOOT_TS
    return context
