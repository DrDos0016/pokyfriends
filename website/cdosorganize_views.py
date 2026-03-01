from collections import namedtuple
from datetime import datetime, timedelta

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import time

#@login_required
def cdosorganize(request):
    context = {}
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

    today = datetime.now()
    context["today"] = today
    last_visit = request.session.get("last_visit", today)
    print("Last visit is now", last_visit)
    if today > last_visit:
        print("Yo it's a new day")
    Sticker = namedtuple("Sticker", "icon, state, title, kind", defaults=["?", STATE_TODO, "UNDEFINED", KIND_DAILY])
    stickers = [
        Sticker(icon="🏃‍➡️", state=STATE_TODO, title="Ring Fit", kind=KIND_DAILY),
        Sticker(icon="🍴", state=STATE_TODO, title="Dishes", kind=KIND_DAILY),
        Sticker(icon="🏛️", state=STATE_TODO, title="Museum Dev", kind=KIND_DAILY),
        Sticker(icon="🔎", state=STATE_TODO, title="Closer Look", kind=KIND_DAILY),
        Sticker(icon="🧠", state=STATE_TODO, title="Enrichment", kind=KIND_DAILY),
        Sticker(icon="🚽", state=STATE_TODO, title="Clean Bathroom", kind=KIND_DAILY),
        Sticker(icon="🍞", state=STATE_TODO, title="Clean Kitchen", kind=KIND_DAILY),
        Sticker(icon="🧦", state=STATE_TODO, title="Laundry", kind=KIND_SATURDAY),
        Sticker(icon="☕", state=STATE_TODO, title="Coffee", kind=KIND_DAILY),
        Sticker(icon="🍄", state=STATE_TODO, title="Metamucil", kind=KIND_DAILY),
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
    ]

    """🍎🍏🍐🍑🍒🍓🫐"""

    context["stickers"] = stickers
    return render(request, "website/cdosorganize.html", context)
