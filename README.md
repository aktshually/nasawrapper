## Warnings
This library is not ready yet, please report bugs at issues tab.
**This library does not have any directly relationship to NASA, this is just a wrapper for make requests to their APIs easier**

## Instalation
You can install this package by pip using the following command:
```
pip install nasawrapper
```

## Updating package
```
pip install --upgrade nasawrapper
```

## Documentation

### APOD
This API has the following description in their website: "Each day a different image or photograph of our fascinating universe is featured, along with a brief explanation written by a professional astronomer.". <br>
The class responsable for this API is `Apod`, which you have to instantiate with 2 parameters: an api key (you can get it [here](https://api.nasa.gov/)) and a boolean indicating if you want to be warned about some eventually alerts when using the wrapper (defaults to `True`).
Example:
```py
from nasawrapper import Apod;

apod = Apod("your-api-key", False);
# in this case, it will not warn you on the console
```

This class has only one method which make the request to the API.