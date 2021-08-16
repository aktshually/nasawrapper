from nasawrapper import NeoWs
from pprint import pprint
from datetime import datetime

neows = NeoWs("DEMO_KEY")
pprint(neows.get_neo_feed({
    "start_date": datetime(year=2021, month=7, day=10)
}))