import os
import sys

from datetime import datetime

from django import VERSION

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_VERSION = sys.version
DJANGO_VERSION = VERSION
START_TIME = datetime.utcnow()

PROJECT_DATA = (
    {"date":2019, "name": "Poképan Crystal", "category":"Games", "url":"/pokepan-crystal"},
    {"date":2019, "name": "Sisyphus", "category":"Games", "url":"/zzt/sisyphus"},
    {"date":2019, "name": "OwO Who's This?", "category":"Games", "url":"/owo-whos-this"},
    {"date":2019, "name": "The Unknowable Timothy Billings", "category":"Games", "url":"/zzt/timothy-billings"},
    {"date":2018, "name": "Window Fragments", "category":"Games", "url":"/zzt/window-fragments"},
    {"date":2017, "name": "Quickhack", "category":"Games", "url":"/zzt/quickhack"},
    {"date":2016, "name": "Ruins of ZZT", "category":"Games", "url":"/zzt/ruins-of-zzt"},
    {"date":2015, "name": "Pokémon Type Chart Quiz", "category":"Games", "url":"/pokemon-type-chart-quiz"},
    {"date":2015, "name": "Pokémon Size Quiz", "category":"Games", "url":"/pokemon-size-quiz"},
    {"date":2012, "name": "Chimp Or Chump", "category":"Games", "url":"/chimp-or-chump"},
    {"date":2015, "name": "Museum of ZZT", "category":"Websites", "url":"https://museumofzzt.com", "ext":True},
    {"date":2015, "name": "<s>Tabiran Tome</s>", "category":"Websites", "url":"https://tome.talesoftabira.com", "ext":True},
    {"date":2015, "name": "Andalusst Atlas", "category":"Websites", "url":"http://pmdu.pokyfriends.com", "ext":True},
    {"date":2019, "name": "Super Show Screens", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/CDi_Screens", "ext":True},
    {"date":2018, "name": "Pokédex Ebooks - Mastodon", "category":"Twitter/Mastodon Bots", "url":"https://botsin.space/@pokedex_ebooks", "ext":True},
    {"date":2014, "name": "Pokédex Ebooks - Twitter", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/pokedex_ebooks", "ext":True},
    {"date":2015, "name": "Flowey's Advice", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/floweys_advice", "ext":True},
    {"date":2016, "name": "Bun EBooks", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/bun_ebooks", "ext":True},
    {"date":2016, "name": "Worlds of ZZT", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/worldsofzzt", "ext":True},
    {"date":2016, "name": "GDQ is No. 1", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/gdqisno1", "ext":True},
    {"date":2016, "name": "BEMANIbooks", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/bemani_books", "ext":True},
    {"date":2016, "name": "Poké Harem", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/poke_harem", "ext":True},
    {"date":2017, "name": "PMD Everyword", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/pmd_everyword", "ext":True},
    {"date":2018, "name": "Pokémon Art Museum", "category":"Twitter/Mastodon Bots", "url":"https://twitter.com/pkmn_art_museum", "ext":True},
    {"date":2017, "name": "PMD Everyword - Web", "category":"Doodles", "url":"/pmdexplorers"},
    {"date":"", "name": "Train Box Release", "category":"Doodles", "url":"/train-box-release"},
    {"date":"", "name": "Gen4 Wi-Fi", "category":"Doodles", "url":"/wifi", "ext":True},
    {"date":2016, "name": "Gen5 Pokémon Clock", "category":"Doodles", "url":"/clock"},
    {"date":2016, "name": "Maestro Tiles", "category":"Doodles", "url":"/maestro-tiles"},
    {"date":2015, "name": "Pokédex Ebooks - Web", "category":"Doodles", "url":"/pokedex-ebooks"},
    {"date":2019, "name": "Twitter Archive Browser", "category":"Tools", "url":"https://github.com/DrDos0016/tab", "ext":True},
    {"date":2016, "name": "Stitchr", "category":"Tools", "url":"/stitchr", "ext":True},
    {"date":2015, "name": "Blitzkrieg Mario Maker", "category":"Tools", "url":"/bkmario", "ext":True},
    {"date":2013, "name": "Blackout Poetry", "category":"Tools", "url":"/blackout"},
    {"name": "Art Gallery", "category":"Art", "url":"/gallery"},
    {"name": "Sticker Gallery", "category":"Art", "url":"/stickers"},
    {"name": "Latest Blog Post", "category":"Blog", "url":"/blog"},
    {"name": "All Blog Posts", "category":"Blog", "url":"/blog/archive"},
    {"name": "All Blog Tags", "category":"Blog", "url":"/blog/tagged"},
    {"name": "Contact", "category":"Personal", "url":"/contact"},
    {"name": "Support", "category":"Personal", "url":"/support"},
)

print("POKYFRIENDS STARTUP")
print("Start time :", START_TIME)
print("Site Root  :", SITE_ROOT)
print("Python Ver.:", PYTHON_VERSION)
print("Django Ver.:", DJANGO_VERSION)
