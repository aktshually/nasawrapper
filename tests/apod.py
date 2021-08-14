from src.main import Apod
from pprint import pprint

apod = Apod("DEMO_KEY")
pprint(apod.get_apod({
    "thumbs": False,
    "count": 2
}))