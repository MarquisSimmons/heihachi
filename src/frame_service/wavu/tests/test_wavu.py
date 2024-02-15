import os

from frame_service import Wavu
from framedb import CharacterName

STATIC_BASE = os.path.join(os.path.dirname(__file__), "static")


def test_wavu_creation() -> None:
    wavu = Wavu()
    assert wavu.name == "Wavu Wiki"
    assert wavu.icon == "https://wavu.wiki/android-chrome-192x192.png"


def test_get_frame_data() -> None:
    wavu = Wavu()
    char = wavu.get_frame_data(CharacterName.AZUCENA)
    assert char.name.value.title() == "Azucena"
    assert char.portrait == "https://i.imgur.com/fjMRO7I.png"
