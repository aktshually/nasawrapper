## Warnings

This library is an **alpha release** yet, maybe there are some bugs, please report them to [issues page](https://github.com/End313234/nasawrapper-python/issues). <br>

## Credits

Every API used in this library is avaliable on [NASA API portal](https://api.nasa.gov/). This is just a simple wrapper to fetch their APIs and this library **does not** have any relationship to NASA, every issue/suggestion should be reported on the [issues page](https://github.com/End313234/nasawrapper-python/issues). <br>
The documentation provided on this readme has inspiration on the documentation provided on the [NASA API portal](https://api.nasa.gov/) about their APIs.

## Instalation

You can install this package by [PIP](https://pip.pypa.io/en/stable/) using the following command:

```
pip install nasawrapper
```

## Updating package

Updating package using [PIP](https://pip.pypa.io/en/stable/):

```
pip install --upgrade nasawrapper
```

## Documentation

### APOD

This API has the following description in their website: "Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.". <br>
The class responsable for this API is `Apod`, which you have to instantiate with an api key (learn how to get [here](https://github.com/End313234/nasawrapper-python#where-can-i-get-an-api-key)). <br>
Example:

```py
from nasawrapper import Apod

apod = Apod("your-api-key")
```

This class has only one method which make the request to the API, called `get_apod`.
For using it, you have to provide a single parameter (a dict) with some keys with the information you want to use to make the request. Avaliable keys are:

| Parameter  | Function                                                                                                                                 | Type              |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| date       | The date of the APOD image to retrieve                                                                                                   | datetime.datetime |
| start_date | The start of a date range, when requesting date for a range of dates. Cannot be used with `date` . Also, can not be before Jun 16, 1995. | datetime.datetime |
| end_date   | The end of the date range, when used with `start_date`. Can not be used without `start_date` and can not be after `start_date`.          | datetime.datetime |
| count      | If this is specified then count randomly chosen images will be returned. Cannot be used with `date` or `start_date` and `end_date`.      | int               |
| thumbs     | Return the URL of video thumbnail. If an APOD is not a video, this parameter is ignored.                                                 | bool              |

You can not provide any other parameters, or an error will be thrown. <br>
Examples:

```py
from nasawrapper import Apod
from datetime import datetime

apod = Apod("your-api-key")

# fetching data between two dates
print(apod.get_apod({
    "start_date": datetime(year=2020, month=10, day=10),
    "end_date": datetime(year=2020, month=10, day=11),
    "thumbs": True
}))

# fetching specific number of data
print(apod.get_apod({
    "count": 5
}))

# fetching data from specific date
print(apod.get_apod({
    "date": datetime(year=2020, month=10, day=12)
}))
```

### NeoWs

The [NASA API portal](https://api.nasa.gov/) describes this API as "a RESTful web service for near earth Asteroid information. With NeoWs a user can: search for Asteroids based on their closest approach date to Earth, lookup a specific Asteroid with its NASA JPL small body id, as well as browse the overall data-set.".

The class responsable for this API is `NeoWs`, which you also must instantiate with an API key (learn how to get it [here](https://github.com/End313234/nasawrapper-python#where-can-i-get-an-api-key)).
Examples:

```py
from nasawrapper import NeoWs

neows = NeoWs("your-api-key")
```

#### Neo - Feed

This endpoint, acording to the [NASA API portal](https://api.nasa.gov/) returns a list of asteroids based on their closest approach date to Earth.

The class responsable for this API has a method called `get_neo_feed`. To use it correctly, you should provide a dict with, at least, a 'start_date' to make the request. The avaliable keys are:
| Parameter | Function | Type |
|-------------|----------|------|
| start_date | Starting date for asteroid search | datetime.datetime |
| end_date | Ending date for asteroid search. The limit is 7 days from the 'start_date' and it is set to 7 days from 'start_date' by default. | datetime.datetime |

Examples:
```py
from nasawrapper import NeoWs
from datetime import datetime

neows = NeoWs("your-api-key")

# fetching from a start_date 
print(neows.get_neo_feed({
    "start_date": datetime(year=2020, month=1, day=10)
}))

# specifying the end_date
print(neows.get_neo_feed({
    "start_date": datetime(year=2020, month=1, day=10),
    "end_date": datetime(year=2020, month=1, day=11)
}))
```

#### Neo - Lookup
- TODO

#### Neo - Browse
- TODO

## Where can I get an API key
To get an API key, access the [NASA API portal](https://api.nasa.gov/) and click on "Generate API key". Then, provide your `First Name`, `Last Name`, `Email` and, if you would like to, an `Application URL` (this parameter is optional).

After clicking on "Signup", you should receive an email on the email address provided with your API key. Then you are ready to use your API key acording to the rate limit (hourlt limit for API keys is 1000 requests).

You can also use a `DEMO_KEY` instead a real API key, however, it has more restricted limits (30 requests per IP address per hour and 50 requests per IP address per day).

## Why you shouldu use this wrapper
- More readable code;
- No long URLs;
- You have absolutely sure about the output: if the code runs without any errors, the output will be the API response about what you want.