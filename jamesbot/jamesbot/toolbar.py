from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from .bot_class import Bot

style = Style.from_dict({
    # 'rprompt': 'bg:#ff0066 #ffffff',

    "bottom-toolbar.text": "#000000 bg:#ff00ff",
    "completion-menu.completion.current": "bg:#00aaaa #000000",
    "completion-menu.completion": "bg:#008888 #ffffff"
})


def rprompt():
    return """Total Contacts: 0 
              Total Notes: 0"""


def bottom_toolbar():
    Ccounter = len(Bot().notes)
    Bcounter = len(Bot().book)
    if Ccounter is not None:
        return f"Total Contacts:{Bcounter}  Total Notes:{Ccounter} "


