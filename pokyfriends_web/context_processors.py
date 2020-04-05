from pokyfriends.settings import DEBUG
from pokyfriends_web.common import *
from datetime import datetime

def pokyfriends_global(request):
    use_debug = True if (DEBUG or request.GET.get("DEBUG")) else False
    data = {"debug": use_debug}

    # Server info
    data["HOST"] = request.get_host()
    if data["HOST"] in ["pokyfriends.com"]:
        data["ENV"] = "PROD"
    else:
        data["ENV"] = "DEV"

    data["PROTOCOL"] = "https" if request.is_secure() else "http"
    data["DOMAIN"] = data["PROTOCOL"] + "://" + data["HOST"]

    # Server date/time
    data["datetime"] = datetime.utcnow()

    # Projects
    data["projects"] = PROJECT_DATA
    return data
