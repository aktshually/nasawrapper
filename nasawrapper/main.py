import requests
import re
from datetime import datetime


class Apod:

    def __init__(self, api_key: str, logging: bool = True):
        self.__api_key = api_key
        self.__date_format = r"\d{4}-\d{2}-\d{2}"
        self.__allowed_keys = ["date", "start_date", "end_date",
                              "count", "thumbs"]
        self.__logging = logging
        self.__date_keys = ["date", "start_date", "end_date"]

    def get_apod(self, options: dict) -> dict:
        """
        Apod()
        Refers to APOD (Astronomy Picture of the Day) NASA API.
        Find more about this API at
        'https://github.com/nasa/apod-api#astronomy-picture-of-the-day-apod-microservice'

        :: get_apod()
            This function have one parameter which is a dict with some keys
            (you have to provide at least one key that matches with keys on
            'self.__allowed_keys'). Then, the keys are validated by their type
             and values and then, the function returns
            a dict containing the API response or an error message.

            The function can also log some warning on the console.
            Set logging property to False when instantiating the class to
            disable warnings.

        This project is under MIT LICENSE.
        """

        url = f"https://api.nasa.gov/planetary/apod?api_key={self.__api_key}"
        checks = ["end_date" in options.keys(), "start_date" in options.keys(), "date" in options.keys()]
        _format = "%Y-%m-%d"

        # throw warning
        if "thumbs" in options.keys() and self.__logging:
            print("\033[93m[Warning] 'thumbs' returns the URL of video thumbnail. If an APOD is not a video, this parameter is ignored.\033[0m")

        # verify options and raise errors
        if len([option for option in options.keys() if option in self.__allowed_keys]) == 0:
            raise ValueError(
                """Missing some properties like 'start_date' or 'end_date'.
                Check the documentation for more information.""")

        if len([option for option in options.keys() if option not in self.__allowed_keys]) > 0:
            raise ValueError("Use only properties described in the documentation (https://github.com/End313234/nasawrapper-python#documentation).")

        # check values to make sure they are valid and have a specific type
        if checks[0] and not checks[1]:
            raise ValueError("'end_date' can not be used without 'start_date'")

        for key, value in options.items():
            if key in self.__date_keys:
                if not isinstance(value, str):
                    raise TypeError(f"'{key}' must be a string.")

                if re.search(self.__date_format, value) is None:
                    raise ValueError(f"'{key}' must be in YYYY-MM-DD format.")
                
                try:
                    assert not datetime.strptime(value, _format) > datetime.now()
                except (ValueError, AssertionError):
                    raise ValueError(f"'{key}' must be a valid date.")

            if key == "count" and not isinstance(value, int):
                raise TypeError(f"'{key}' must be an integer.")

            if key == "thumbs" and not isinstance(value, bool):
                raise TypeError(f"'{key}' must be a boolean.")

            if key == "end_date" and datetime.strptime(options["start_date"], _format) > datetime.strptime(options["end_date"], _format):
                raise ValueError(f"'{key}' can not be after 'start_date'")

        if "count" in options.keys() and any(checks):
            raise ValueError(f"'count' can not be used with 'end_date', 'start_date' or 'date'")
        
        if "start_date" in options.keys() and checks[2]:
            raise ValueError(f"'start_date' can not be used with 'date'")

        for key, value in options.items():
            url += f"&{key}={value}"

        return requests.get(url).json()