import json

from collections import namedtuple
from datetime import datetime, timedelta

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import time

from .settings import ORG_DATA_PATH

#@login_required
def cdosorganize(request):
    context = {"title": "CDosOrganize"}
    STATE_IGNORE = -1
    STATE_TODO = 0
    STATE_DONE = 1
    STATE_PARTIAL = 2

    KIND_DAILY = 0
    KIND_MONDAY = 1
    KIND_TUESDAY = 2
    KIND_WEDNESDAY = 3
    KIND_THURSDAY = 4
    KIND_FRIDAY = 5
    KIND_SATURDAY = 6
    KIND_SUNDAY = 7
    KIND_MWF = 8
    KIND_ONEOFF = 9
    KIND_102030 = 10

    #10/20/30
    #QoZZT Queue
    #Proj Upd8
    #M: Steam Sched/Post Friday VOD/
    #W:Post Sunday VOD
    #:SAT Discord Poll for stream next

    if request.method == "POST":
        with open(ORG_DATA_PATH, "w") as fh:
            fh.write(request.POST.get("stickers"))
        return HttpResponse("OK")

    today = datetime.now()
    context["today"] = today
    last_visit = request.session.get("last_visit", today)
    print("Last visit is now", last_visit)
    if today > last_visit:
        print("Yo it's a new day")

    Sticker = namedtuple("Sticker", "icon, state, title, timestamp", defaults=["?", STATE_TODO, "UNDEFINED", ""])
    stickers = []


    raw = json.load(open(ORG_DATA_PATH))
    for s in raw:
        print(s)
        stickers.append(Sticker(icon=s["icon"], state=s["state"], title=s["title"], timestamp=s["timestamp"]))

    """
    stickers = [
        Sticker(icon="🏃‍➡️", state=STATE_TODO, title="Ring Fit", timestamp=""),
        Sticker(icon="🍴", state=STATE_TODO, title="Dishes", timestamp=""),
        Sticker(icon="🏛️", state=STATE_TODO, title="Museum Dev", timestamp=""),
        Sticker(icon="🔎", state=STATE_TODO, title="Closer Look", timestamp=""),
        Sticker(icon="🧠", state=STATE_TODO, title="Enrichment", timestamp=""),
        Sticker(icon="🚽", state=STATE_TODO, title="Clean Bathroom", timestamp=""),
        Sticker(icon="🍞", state=STATE_TODO, title="Clean Kitchen", timestamp=""),
        Sticker(icon="🧦", state=STATE_TODO, title="Laundry", timestamp=""),
        Sticker(icon="☕", state=STATE_TODO, title="Coffee", timestamp=""),
        Sticker(icon="🍄", state=STATE_TODO, title="Metamucil", timestamp=""),
        Sticker(icon="📺", state=STATE_TODO, title="Post VOD"),
        Sticker(icon="📊", state=STATE_TODO, title="CL Poll"),
        Sticker(icon="📊", state=STATE_TODO, title="Stream Poll"),
        Sticker(icon="📒", state=STATE_TODO, title="Proj Update"),
        Sticker(icon="0️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="1️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="2️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="3️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="4️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="5️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="6️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="7️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="8️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="9️⃣", state=STATE_TODO, title="Custom"),
        Sticker(icon="🫐", state=STATE_TODO, title="Custom"),
        Sticker(icon="🫐", state=STATE_TODO, title="Custom"),
        Sticker(icon="🫐", state=STATE_TODO, title="Custom"),
    ]"""


    """🍎🍏🍐🍑🍒🍓🫐"""

    context["stickers"] = stickers
    return render(request, "website/cdosorganize.html", context)
