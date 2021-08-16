from nasawrapper import NeoWs
from pprint import pprint
from datetime import datetime

neows = NeoWs("DEMO_KEY")
print(datetime(year=2020, month=1, day=10))
print(datetime(year=2020, month=1, day=9))
pprint(neows.get_neo_feed({
    "end_date": datetime(year=2021, month=7, day=18),
    "start_date": datetime(year=2021, month=7, day=10)
}))