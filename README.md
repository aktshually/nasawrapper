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
The class responsable for this API is `Apod`, which you have to instantiate with 2 parameters: an api key (you can get it [here](https://api.nasa.gov/)) and a boolean indicating if you want to be warned about some eventually alerts when using the wrapper (defaults to `True`). <br>
Example:
```py
from nasawrapper import Apod

apod = Apod("your-api-key", False)
# in this case, it will not warn you on the console

# setting the second variable to True or not specifying
# it will make the lib warn you in the console
```

This class has only one method which make the request to the API, called `get_apod`.
For using it, you have to provide a single parameter (a dict) with some keys with the information you want to use to make the request. Avaliable keys are:

|  Parameter  |  Function  | Type |
|-------------|------------|------|
|     date    | The date of the APOD image to retrieve (must be in format YYYY-MM-DD) | datetime.datetime |
|  start_date | The start of a date range, when requesting date for a range of dates. Cannot be used with `date` (must be in format YYYY-MM-DD). Also, can not be before Jun 16, 1995.| datetime.datetime |
|  end_date   | The end of the date range, when used with `start_date`. Can not be used without `start_date` and can not be after `start_date` (must be in format YYYY-MM-DD). | datetime.datetime |
| count | 	If this is specified then count randomly chosen images will be returned. Cannot be used with `date` or `start_date` and `end_date`. | int
| thumbs | Return the URL of video thumbnail. If an APOD is not a video, this parameter is ignored. | bool |

You can not provide any other parameters, or an error will be thrown. <br>
Examples:
```py
from nasawrapper import Apod

apod = Apod("your-api-key", False)

# fetching data between two dates
print(apod.get_apod({
    "start_date": "2020-10-10",
    "end_date": "2020-10-11",
    "thumbs": True
}))

# fetch specific number of data
print(apod.get_apod({
    "count": 5
}))
```
