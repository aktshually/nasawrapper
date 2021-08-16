from nasawrapper import Apod
from pprint import pprint
from datetime import datetime

apod = Apod("DEMO_KEY")
print(datetime(year=2021, month=7, day=10))
pprint(apod.get_apod({
    "start_date": datetime(year=2021, month=7, day=10),
    "end_date": datetime(year=2021, month=7, day=18)
}))
