import requests
import aiohttp
from typing import Dict, Union, Optional, Any, List, TypedDict
from datetime import datetime

from .errors import InvalidKey, InvalidDate, InvalidApiKey, RateLimitError

class ApodResponse(TypedDict):
    copyright: Optional[str]
    date: str
    explanation: str
    hd_url: Optional[str]
    media_type: str
    service_version: str
    title: str
    url: str

class Validator:
    """
    Will be called to validate the options provided
    by the developer
    """
    @classmethod
    def validate(
        cls,
        options: Dict[str, Any],
        allowed_keys: Dict[str, type],
        date_related_keys: List[str]
    ) -> Dict[str, Union[str, int, bool, datetime]]:
        """
        Function to validate the options acording to
        the API requisites
        """

        # creating checks for date related keys
        checks = [key in options for key in date_related_keys]

        # checking if the developer didn't provide any values
        if not any([key in options for key in allowed_keys]):
            raise ValueError("Missing properties like 'start_date' or 'end_date'.")

        # checking for 'end_date' and 'start_date'
        # 'start_date' can be used without 'end_date'
        # so ill not check this
        if checks[2] and not checks[1]:
            raise InvalidKey("'end_date' can not be used without 'start_date'")
        
        # checking if 'date' is being used with
        # 'start_date' or 'end_date'
        elif checks[0] and checks[2]:
            raise InvalidKey("'date' can not be used with 'end_date'")

        # interating over date keys to check their
        # types
        for key, value in allowed_keys.items():
            if options.get(key) and not isinstance(options[key], value):
                raise TypeError(f"'{key}' must be '{value.__name__}', got '{options[key].__class__.__name__}'")

        # validating dates
        for key in date_related_keys:
            if options.get(key):
                value = options[key]
                if value > datetime.now():
                    raise InvalidDate(f"'{key}' must be a valid date")

        # validating 'end_date' and 'start_date'
        if "end_date" in options.keys():
            if options["end_date"] < datetime(year=1995, month=6, day=16):
                raise InvalidDate("'end_date' must be after Jun 16, 1995.")

            elif options["end_date"] < options["start_date"]:
                raise InvalidDate(f"'end_date' can not be before 'start_date'")

            options["end_date"] = options["end_date"].strftime("%Y-%m-%d")
        
        if "start_date" in options.keys():
            options["start_date"] = options["start_date"].strftime("%Y-%m-%d")

        # checking 'count' and 'date' keys
        if "count" in options.keys() and any(checks):
            raise InvalidKey("'count' can not be used with 'end_date', 'start_date' or 'date'")

        if checks[0] in options.keys() and "start_date" in options.keys():
            raise InvalidKey("'start_date' can not be used with 'date'")

        return options
        

class SyncApod:
    """
    This class uses synchronous programming
    syntax to make requests to the
    ``APOD`` API and returns the API response.

    **Parameters**

        **api_key** (str) - The API key.
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.allowed_keys = {
            "date": datetime,
            "start_date": datetime,
            "end_date": datetime,
            "count": int,
            "thumbs": bool
        }
        self.date_related_keys = list(filter(lambda item: "date" in item, self.allowed_keys.keys()))
        self.base_url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}"

    def get_apod(self, options: Dict[str, Union[str, int, bool, datetime]]) -> Union[ApodResponse, List[ApodResponse]]:
        """
        Validate the provided options by checking their types
        and values. Here's a list of the allowed keys and an 
        example of how to call the method correctly:

        **Allowed Keys**

            ========== ============================= ==========================================================================================================
            Key        Type                          Function
            ========== ============================= ==========================================================================================================
            date       :py:class:`datetime.datetime` Search for a specific date. Can not be used with 'start_date'.
            start_date :py:class:`datetime.datetime` The start of a date range.
            end_date   :py:class:`datetime.datetime` The end of a date range. Can not be used without 'start_date' and can not be before Jun 16, 1995.
            count      :py:class:`int`               If specified, returns ``count`` randomly images. Can not be used with 'date', 'start_date' or 'end_date'.
            thumbs     :py:class:`bool`              If the APOD is a video, return the URL of the video. Default is ``False``.
            ========== ============================= ==========================================================================================================

        **Examples**

            **Getting asteroids from a range**

                .. code-block:: python3

                    from nasawrapper import SyncApod
                    from datetime import datetime, timedelta

                    apod = SyncApod("DEMO_KEY")
                    result = apod.get_apod({
                        "start_date": datetime.now() - timedelta(days=1),
                        "end_date": datetime.now(),
                        "thumbs": True
                    })

                    print(result)
            
            **Getting asteroids from specific date**
            
                .. code-block:: python3

                    from nasawrapper import SyncApod
                    from datetime import datetime, timedelta

                    apod = SyncApod("DEMO_KEY")
                    result = apod.get_apod({
                        "date": datetime(year=2010, month=3, day=2)
                    })

                    print(result)
        """
        options = Validator.validate(options, self.allowed_keys, self.date_related_keys)

        # building query
        for key, value in options.items():
            self.base_url += f"&{key}={value}"

        # making request
        request = requests.get(self.base_url)
        if request.status_code == 429:
            raise RateLimitError("You are being rate limited")
        elif request.status_code == 403:
            raise InvalidApiKey(f"'{self.api_key}' is not a valid API key")

        return request.json()

    def get_random(self) -> ApodResponse:
        """
        Returns a random picture of APOD API.
        You can manually do this by typing:

        .. code-block:: python3

            from nasawrapper import SyncApod

            apod = SyncApod("DEMO_KEY")
            result = apod.get_apod({
                "count": 1
            })
            print(result) # random picture

        But it's not recommended, since there's
        a specific method for this.
        """
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}&count=1"

        # making request
        request = requests.get(url)
        if request.status_code == 429:
            raise RateLimitError("You are being rate limited")
        elif request.status_code == 403:
            raise InvalidApiKey(f"'{self.api_key}' is not a valid API key")

        return request.json()

    def get_today_apod(self) -> ApodResponse:
        """
        Returns today's APOD. You can also
        clone this method manually by typing:

        .. code-block:: python3

            from nasawrapper import SyncApod
            from datetime import datetime

            apod = SyncApod("DEMO_KEY")
            result = apod.get_apod({
                "date": datetime.now()
            })
            print(result)

        But, for the same reasons as
        :py:class:`SyncApod.get_random <nasawrapper.apod.SyncApod.get_random>`,
        it's not recommended
        to do that.
        """
        now = datetime.now().strftime("%Y-%m-%d")
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}&date={now}"
        
        # making request
        request = requests.get(url)
        if request.status_code == 429:
            raise RateLimitError("You are being rate limited")
        elif request.status_code == 403:
            raise InvalidApiKey(f"'{self.api_key}' is not a valid API key")

        return request.json()

        

        
class AsyncApod:
    """
    This class uses asynchronous programming
    syntax to make requests to the APOD API
    and returns the API response.

    **Parameters**
        
        **api_key** (str) - The API key.
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.allowed_keys = {
            "date": datetime,
            "start_date": datetime,
            "end_date": datetime,
            "count": int,
            "thumbs": bool
        }
        self.date_related_keys = list(filter(lambda item: "date" in item, self.allowed_keys))
        self.base_url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}"

    async def get_apod(self, options: Dict[str, Union[str, int, bool, datetime]]) -> Union[ApodResponse, List[ApodResponse]]:
        """
        |coro|

        Same thing as
        :py:class:`SyncApod.get_apod <nasawrapper.apod.SyncApod.get_apod>`,
        but with asynchronous syntax.

        **Example**

            .. code-block:: python3

                from nasawrapper import AsyncApod
                from datetime import datetime
                import asyncio

                async def main():
                    apod = AsyncApod("DEMO_KEY")
                    result = await apod.get_apod({
                        "date": datetime(2010, 2, 3)
                    })
                    print(result)

                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
        """
        options = Validator.validate(options, self.allowed_keys, self.date_related_keys)

        # building url
        for key, value in options.items():
            self.base_url += f"&{key}={value}"

        # making request
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url) as response:
                if response.status == 429:
                    raise RateLimitError("You are being rate limited")
                elif response.status == 403:
                    raise InvalidApiKey(f"'{self.api_key}' is not a valid API key")
                    
                response = await response.json()

        return response

    async def get_random(self) -> ApodResponse:
        """
        |coro|

        Same thing as
        :py:class:`SyncApod.get_random <nasawrapper.apod.SyncApod.get_random>`
        but with asynchronous syntax.

        **Example**

            .. code-block:: python3

                from nasawrapper import AsyncApod
                import asyncio

                async def main():
                    apod = AsyncApod("DEMO_KEY")
                    result = await apod.get_random()
                    print(result)

                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
        """
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}&count=1"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 429:
                    raise RateLimitError("You are being rate limited")
                elif response.status == 403:
                    raise InvalidApiKey(f"'{self.api_key}' is not a valid API key")
                    
                response = await response.json()

        return response[0]

    async def get_today_apod(self) -> ApodResponse:
        """
        |coro|

        Same this as
        :py:class:`SyncApod.get_today_apod <nasawrapper.apod.SyncApod.get_today_apod>`
        but with asynchronous syntax.

        **Example**

            .. code-block:: python3

                from nasawrapper import AsyncApod
                import asyncio

                async def main():
                    apod = AsyncApod("DEMO_KEY")
                    result = await apod.get_today_apod()
                    print(result)

                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
        """
        now = datetime.now().strftime("%Y-%m-%d")
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}&date={now}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 429:
                    raise RateLimitError("You are being rate limited")
                elif response.status == 403:
                    raise InvalidApiKey(f"'{self.api_key}' is not a valid API key")

                response = await response.json()

        return response

class ApodQueryBuilder:
    """
    If you want to build a query
    using methods, this wrapper
    provides exactly what you want.

    This class will build a query with
    the information provided by the methods.

    **Examples**

        **Getting 2 random pictures**

            .. code-block:: python3

                from nasawrapper import ApodQueryBuilder

                builder = ApodQueryBuilder("DEMO_KEY")
                result = builder.set_count(2).get_apod()
                print(result)

        **Getting picture from specific date**

            .. code-block:: python3

                from nasawrapper import ApodQueryBuilder
                from datetime import datetime

                builder = ApodQueryBuilder("DEMO_KEY")
                result = builder.set_date(datetime(2010, 2, 3))
                print(result)
    """
    def __init__(self, api_key: str, options = {}):
        self.api_key = api_key
        self.options = options

    def set_date(self, date: datetime):
        """
        Add 'date' field to the options
        """
        if not isinstance(date, datetime):
            raise TypeError(f"'date' must be an 'datetime.datetime', got '{date.__class__.__name__}'")

        # checks whenever 'date' appears with
        # 'start_date' or 'count'
        if self.options.get("start_date"):
            raise InvalidKey("'date' can not be used with 'start_date'")    
        elif self.options.get("count"):
            raise InvalidKey("'date' can not be used with 'count'")

        self.options["date"] = date.strftime("%Y-%m-%d")

        return ApodQueryBuilder(self.api_key, self.options)

    def set_start_date(self, start_date: datetime):
        """
        Add 'start_date' field to the options
        """
        if not isinstance(start_date, datetime):
            raise TypeError(f"'start_date' must be an 'datetime.datetime', got '{start_date.__class__.__name__}'")

        if start_date < datetime(year=1995, month=6, day=16):
            raise InvalidDate("'end_date' must be after Jun 16, 1995.")

        return ApodQueryBuilder(self.api_key, self.options)

    def set_end_date(self, end_date: datetime):
        """
        Add 'end_date' field to the options
        """

        if not isinstance(end_date, datetime):
            raise TypeError(f"'end_date' must be an 'datetime.datetime', got '{end_date.__class__.__name__}'")

        return ApodQueryBuilder(self.api_key, self.options)

    def set_count(self, count: int):
        """
        Add 'count' field to the options
        """
        if not isinstance(count, int):
            raise TypeError(f"'count' must be 'int', got '{count.__class__.__name__}'")
        
        # checking whenever 'count' is being
        # used with 'date', 'start_date', 'end_date'
        checks = ["date" in self.options.keys(), "start_date" in self.options.keys(), "end_date" in self.options.keys()]
        if any(checks):
            raise InvalidKey("'count' can not be used with 'date', 'start_date' or 'end_date'")

        self.options["count"] = count
        return ApodQueryBuilder(self.api_key, self.options)

    def set_thumbs(self, thumbs: bool):
        """
        Add 'thumbs' field to the options.
        """
        if not isinstance(thumbs, bool):
            raise TypeError(f"'thumbs' must be 'bool', got '{thumbs.__class__.__name__}'")

        self.options["thumbs"] = thumbs
        return ApodQueryBuilder(self.api_key, self.options)

    def get_apod(self) -> Union[ApodResponse, List[ApodResponse]]:
        """
        Make the request with the provided
        information.
        """
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}"

        options = Validator.validate(
            self.options,
            {
            "date": datetime,
            "start_date": datetime,
            "end_date": datetime,
            "count": int,
            "thumbs": bool
            },
            ["date", "start_date", "end_date"]
        )

        # building query
        for key, value in options.items():
            url += f"&{key}={value}"

        # making request
        request = requests.get(url)
        if request.status_code == 429:
            raise RateLimitError("You are being rate limited")
        elif request.status_code == 403:
            raise InvalidApiKey(f"'{self.api_key}' is not a valid API key")

        return request.json()