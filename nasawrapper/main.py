import requests
import re
from datetime import datetime, timedelta


class Apod:
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
            a list containing the API response.

        This project is under MIT LICENSE.
    """

    def __init__(self, api_key: str, logging: bool = True):
        self.__api_key = api_key
        self.__allowed_keys = ["date", "start_date", "end_date",
                               "count", "thumbs"]
        self.__date_keys = ["date", "start_date", "end_date"]

    def get_apod(self, options: dict):
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.__api_key}"
        checks = ["end_date" in options.keys(
        ), "start_date" in options.keys(), "date" in options.keys()]

        # verify options and raise errors
        if len([option for option in options.keys() if option in self.__allowed_keys]) == 0:
            raise ValueError(
                """Missing some properties like 'start_date' or 'end_date'.
                Check the documentation for more information.""")

        if len([option for option in options.keys() if option not in self.__allowed_keys]) > 0:
            raise ValueError(
                "Use only properties described in the documentation (https://github.com/End313234/nasawrapper-python#apod).")

        # check values to make sure they are valid and have a specific type
        if checks[0] and not checks[1]:
            raise ValueError("'end_date' can not be used without 'start_date'")

        for key in self.__date_keys:
            if key in options.keys():
                value = options[key]
                if not isinstance(value, datetime):
                    raise TypeError(f"'{key}' must be datetime.datetime")

                if value > datetime.now():
                    raise ValueError(f"'{key}' must be a valid date.")

        for key, value in options.items():
            if key == "count" and not isinstance(value, int):
                raise TypeError(f"'{key}' must be an integer.")

            if key == "thumbs" and not isinstance(value, bool):
                raise TypeError(f"'{key}' must be a boolean.")

            if key == "end_date":
                start_date = options["start_date"]
                if value < datetime(year=1995, month=6, day=16):
                    raise ValueError("'end_date' must be after Jun 16, 1995.")

                if value < options["start_date"]:
                    raise ValueError(f"'{key}' can not be before 'start_date'")

                options["end_date"] = f"{value.year}-{value.month}-{value.day}"
                options["start_date"] = f"{start_date.year}-{start_date.month}-{start_date.day}"

        if "count" in options.keys() and any(checks):
            raise ValueError(
                f"'count' can not be used with 'end_date', 'start_date' or 'date'")

        if "start_date" in options.keys() and checks[2]:
            raise ValueError(f"'start_date' can not be used with 'date'")

        for key, value in options.items():
            url += f"&{key}={value}"

        return requests.get(url).json()


class NeoWs:
    """
        NeoWs()
        Refers to NeoWs (Near Earth Object Web Service) NASA API.
        Acording to https://api.nasa.gov/, this is a RESTful web 
        service for near earth Asteroid information. With NeoWs 
        a user can: search for Asteroids based on their closest 
        approach date to Earth, lookup a specific Asteroid with 
        its NASA JPL small body id, as well as browse the overall 
        data-set.

    :: get_neo_feed()
            Takes on parameter, which is a dict with a 'start_date'
            and 'end_date', only the 'start_date' is required.
            These parameters are validated by type and value (both
            have to be 'datetime.datetime' and 'end_date' limit is 
            7 days from 'start_date').
            If you don't provide a 'end_date', the value provided by default
            will be 7 days from the 'start_date'.
    """

    def __init__(self, api_key):
        self.__api_key = api_key
        self.__allowed_keys = ["start_date", "end_date"]

    def get_neo_feed(self, options: dict):
        url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={self.__api_key}&"

        if len([option for option in options.keys() if option in self.__allowed_keys]) == 0:
            raise ValueError("You have to provide 'start_date'.")

        if len([option for option in options.keys() if option not in self.__allowed_keys]) > 0:
            raise ValueError(
                "Use only values described on the documentation (https://github.com/End313234/nasawrapper-python#documentation)")

        if "end_date" in options.keys() and not "start_date" in options.keys():
            raise ValueError("'end_date' can not be used without 'start_date'.")

        for key, value in options.items():
            if not isinstance(value, datetime):
                raise ValueError(f"{key} must be 'datetime.datetime'")

        if options.get("end_date") == None:
            options["end_date"] = options["start_date"] + timedelta(days=7)
        
        if options["end_date"] > options["start_date"] + timedelta(days=7):
            raise ValueError(f"'end_date' must be before/equal to 7 days from 'start_date'.")

        start_date = options["start_date"]
        end_date = options["end_date"]
        options["start_date"] = f"{start_date.year}-{start_date.month}-{start_date.day}"
        options["end_date"] = f"{end_date.year}-{end_date.month}-{end_date.day}"

        for key, value in options.items():
            url += f"&{key}={value}"

        return requests.get(url).json()