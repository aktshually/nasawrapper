from nasawrapper import Apod
from pprint import pprint

apod = Apod("DEMO_KEY")
pprint(apod.get_apod({
    "start_date": "2015-10-05",
    "end_date": "2015-10-06"
}))
