from datetime import datetime, timedelta
from typing import Dict, List, Type, TypedDict, Any
import requests
import aiohttp

from .errors import *

class EstimatedDiameterDetails(TypedDict):
    """
    Equals to 'estimated_diameter_max'
    and 'estimated_diameter_min' on
    API response
    """
    estimated_diameter_max: float
    estimated_diameter_min: float

class EstimatedDiameter(TypedDict):
    """
    Equals to 'estimated_diameter' on
    API response
    """
    kilometers: EstimatedDiameterDetails
    meters: EstimatedDiameterDetails
    miles: EstimatedDiameterDetails
    feet: EstimatedDiameterDetails

class RelativeVelocity(TypedDict):
    """
    Equals to 'relative_velocity' on
    API response
    """
    kilometers_per_second: str
    kilometers_per_hour: str
    miles_per_hour: str

class MissDistance(TypedDict):
    """
    Equals to 'miss_distance' on
    API response
    """
    astronomical: str
    lunar: str
    kilometers: str
    miles: str

class CloseApproachData(TypedDict):
    """
    Equals to 'close_approach_data' on
    API response
    """
    close_approach_date: str
    close_approach_date_full: str
    epoch_date_close_approach: int
    epoch_date_close_approach: int
    relative_velocity: RelativeVelocity
    miss_distance: MissDistance
    orbiting_body: str

class Asteroid(TypedDict):
    """
    Equals to an asteroid on API
    response
    """
    links: Dict[str, str]
    id: str
    neo_reference_id: str
    name: str
    nasa_jpl_url: str
    absolute_magnitude_h: float
    estimated_diameter: EstimatedDiameter
    is_potentially_hazardous_asteroid: bool
    close_approach_data: List[CloseApproachData]
    is_sentry_object: bool


class Links(TypedDict, total=False):
    """
    Equals to 'links'
    """
    next: str
    prev: str
    self: str

class NeoWsFeedResponse(TypedDict):
    """
    Equals to /feed response
    """
    links: Links
    element_count: int
    near_earth_objects: Dict[str, List[Asteroid]]

class OrbitClass(TypedDict):
    """
    Equals to 'orbit_class' in
    OrbitralData
    """
    orbit_class_type: str
    orbit_class_description: str
    orbit_class_range: str

class OrbitralData(TypedDict):
    """
    Equals to 'orbitral_data' in
    /browse asteroid response
    """
    oribt_id: str
    orbit_determination_date: str
    first_observation_date: str
    last_observation_date: str
    data_arc_in_days: int
    observations_used: int
    orbit_uncertainty: str
    minimum_orbit_intersection: str
    jupiter_tisserand_invariant: str
    epoch_osculation: str
    eccentricity: str
    semi_major_axis: str
    inclination: str
    ascending_node_longitude: str
    orbital_period: str
    perihelion_distance: str
    perihelion_argument: str
    aphelion_distance: str
    perihelion_time: str
    mean_anomaly: str
    mean_motion: str
    equinox: str
    oribt_class: OrbitClass

class NeoWsBrowseAsteroid(Asteroid, TypedDict):
    """
    Equals to an asteroid in /browse
    """
    orbitral_data: OrbitralData

class Page(TypedDict):
    """
    Refers to 'page' in /browse
    API response
    """
    size: int
    total_elements: int
    total_page: int
    number: int

class NeoWsBrowseResponse(TypedDict):
    links: Links
    page: Page
    near_earth_objects: List[NeoWsBrowseAsteroid]

class Validator:
    """
    Will be called to validate the options provided
    by the developer
    """
    @classmethod
    def validate(cls, options: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, str]:
        # checking keys
        if "start_date" not in options.keys() and not "end_date" in options.keys():
            raise InvalidKey("You have to provide a 'start_date' or 'end_date'")

        # checking types
        for key in allowed_keys:
            if key in options.keys() and not isinstance(key, datetime):
                value = options[key]
                if not isinstance(value, datetime):
                    raise TypeError(f"'{key}' must be 'datetime.datetime', got '{value.__class__.__name__}'")
        
        # checking if dates are valid
        if options["end_date"] - timedelta(days=7) < datetime(1900, 1, 1):
            raise InvalidDate("'start_date' has a default value of 7 days before 'end_date', however, this value is before than Jan 1, 1. Please, set a 'start_date' or make 'end_date' be after Jan 8, 1900")
        elif options.get("start_date") and options["start_date"] < datetime(1900, 1, 1) or options["end_date"] < datetime(1900, 1, 1):
            raise InvalidDate("'start_date' and/or 'end_date' must be after Jan 1, 1900")

        # creating a start_date in case it doesnt exist
        if "end_date" in options.keys() and not "start_date" in options.keys():
            options["start_date"] = options["end_date"] - timedelta(days=7)

        # continue checking dates
        if options["start_date"] > options["end_date"]:
            raise InvalidDate("'start_date' can not be after 'end_date'")
        elif options["start_date"] + timedelta(days=7) < options["end_date"]:
            raise InvalidDate("'start_date' can is limited to 7 days before 'end_date' or minus")

        # stringify dates
        if options.get("end_date"):
            options["end_date"] = options["end_date"].strftime("%Y-%m-%d")
        options["start_date"] = options["start_date"].strftime("%Y-%m-%d")

        return options

class SyncNeoWs:
    """
    This class uses asynchronous programming
    syntax to make requests to the NeoWs
    web service and returns the API response.

    Descriptions of the methods are from
    the `NASA API Portal <https://api.nasa.gov/>`_.
    """
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._allowed_keys = ["start_date", "end_date"]

    @property
    def api_key(self):
        """
        Returns the API key.
        """
        return self._api_key

    @property
    def allowed_keys(self):
        """
        Returns the allowed keys in list format.
        """
        return self._allowed_keys

    def get_neo_feed(self, options: Dict[str, Any]) -> NeoWsFeedResponse:
        """
        Retrieve a list of Asteroids based on
        their closest approach date to Earth.
        Here's a list of the allowed keys:
        
        **Allowed Keys**

            ========== ========================== ============================================
            Key        Type                       Function
            ========== ========================== ============================================
            start_date :class:`datetime.datetime` Sets a starting date for the asteroid search
            end_date   :class:`datetime.datetime` Sets a ending date for the asteroid search
            ========== ========================== ============================================

        **Example**

            .. code-block:: python3

                from nasawrapper import SyncNeoWs
                from datetime import datetime

                neows = SyncNeoWs("DEMO_KEY")
                result = neows.get_neo_feed({
                    "start_date": datetime(2010, 2, 3),
                    "end_date": datetime(2010, 2, 4)
                })
        """

        url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={self._api_key}"
        options = Validator.validate(options, self._allowed_keys)

        # building url
        for key, value in options.items():
            url += f"&{key}={value}"

        # making request
        request = requests.get(url)
        if request.status_code == 429:
            raise RateLimitError("You are being rate limited")
        elif request.status_code == 403:
            raise InvalidApiKey(f"'{self._api_key}' is not a valid API key")

        return request.json()

    def get_today_neo_feed(self) -> NeoWsFeedResponse:
        """
        Retrieve a list of Asteroids based on
        today's date in the current UTC.

        **Example**

            .. code-block:: python3

                from nasawrapper import SyncNeoWs

                neows = SyncNeoWs("DEMO_KEY")
                result = neows.get_today_neo_feed()
                print(result)
        """
        start_date = end_date = datetime.now()
        options = {
            "start_date": start_date,
            "end_date": end_date
        }

        return self.get_neo_feed(options)

    def get_neo_lookup(self, asteroid_id: int) -> Asteroid:
        """
        Lookup a specific Asteroid based on its
        NASA JPL small body (SPK-ID) ID. Find more
        about this at
        https://ssd.jpl.nasa.gov/tools/sbdb_query.html
        to get the overall data-set of asteroids and their ids.

        **Example**

            .. code-block:: python3

                from nasawrapper import SyncNeoWs

                neows = SyncNeoWs("DEMO_KEY")
                result = neows.get_neo_lookup(3542519)
                print(results)
        """
        if not isinstance(asteroid_id, int):
            raise TypeError(f"'asteroid_id' must be 'int', got {asteroid_id.__class__.__name__}")

        url = f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={self._api_key}"
        

        # making request
        request = requests.get(url)
        if request.status_code == 404:
            raise NotFound(f"Asteroid of id '{asteroid_id}' could not be found")
        elif request.status_code == 429:
            raise RateLimitError("You are being rate limited")
        elif request.status_code == 403:
            raise InvalidApiKey(f"'{self._api_key}' is not a valid API key")

        return request.json()

    def get_neo_browse(self) -> NeoWsBrowseResponse:
        """
        Browse the overall Asteroid data-set.

        **Example**

            .. code-block:: python3

                from nasawrapper import SyncNeoWs

                neows = SyncNeoWs("DEMO_KEY")
                result = neows.get_neo_browse() # this may take some time, 
                                                # since the API's searching for all asteroids
                print(result)
        """
        url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={self._api_key}"

        # making request
        request = requests.get(url)
        if request.status_code == 429:
            raise RateLimitError("You are being rate limited")
        elif request.status_code == 403:
            raise InvalidApiKey(f"'{self._api_key}' is not a valid API key")

        return request.json()

class AsyncNeoWs:
    """
    This class uses asynchronous syntax to 
    make requests to the NeoWs web service
    and returns the API response.

    Descriptions of the methods are from
    the `NASA API Portal <https://api.nasa.gov/>`_.
    """
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._allowed_keys = ["start_date", "end_date"]

    @property
    def api_key(self):
        """
        Returns the API key.
        """
        return self._api_key

    @property
    def allowed_keys(self):
        """
        Returns the allowed keys in list format.
        """
        return self._allowed_keys

    async def get_neo_feed(self, options: Dict[str, Any]) -> NeoWsFeedResponse:
        """
        |coro|
        
        Same this as
        :py:class:`SyncNeoWs.get_neo_feed <nasawrapper.neows.SyncNeoWs.get_neo_feed>`,
        but with asynchronous syntax.

        **Example**

            .. code-block:: python3

                from nasawrapper import AsyncNeoWs
                from datetime import datetime
                import asyncio

                async def main():
                    neows = AsyncNeoWs("DEMO_KEY")
                    result = await neows.get_neo_feed({
                        "start_date": datetime(2010, 2, 3),
                        "end_date": datetime(2010, 2, 4)
                    })
                    print(result)

                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
        """
        url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={self._api_key}"
        options = Validator.validate(options, self._allowed_keys)

        # building url
        for key, value in options.items():
            url += f"&{key}={value}"

        # making request
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                if request.status == 429:
                    raise RateLimitError("You are being rate limited")
                elif request.status == 403:
                    raise InvalidApiKey(f"'{self._api_key}' is not a valid API key")

                request = await request.json()

        return request

    async def get_today_neo_feed(self) -> NeoWsFeedResponse:
        """
        |coro|
        
        Same this as
        :py:class:`SyncNeoWs.get_today_neo_feed <nasawrapper.neows.SyncNeoWs.get_today_neo_feed>`,
        but with asynchronous syntax.

        **Example**

            .. code-block:: python3

                from nasawrapper import AsyncNeoWs
                from datetime import datetime
                import asyncio

                async def main():
                    neows = AsyncNeoWs("DEMO_KEY")
                    result = await neows.get_today_neo_feed()
                    print(result)

                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
        """
        start_date = end_date = datetime.now()
        options = {
            "start_date": start_date,
            "end_date": end_date
        }
        return await self.get_neo_feed(options)

    async def get_neo_lookup(self, asteroid_id: int) -> Asteroid:
        """
        |coro|
        
        Lookup a specific asteroid based on its
        NASA JPL small body (SPK-ID) ID. Find more
        about this at
        `https://ssd.jpl.nasa.gov/tools/sbdb_query.html <https://ssd.jpl.nasa.gov/tools/sbdb_query.html>`_
        or simply use
        :py:class:`AsyncNeoWs.get_neo_browse <nasawrapper.neows.AsyncNeoWs.get_neo_browse>`
        to get the overall data-set of asteroids and their ids.

        **Example**

            .. code-block:: python3

                from nasawrapper import AsyncNeoWs
                from datetime import datetime
                import asyncio

                async def main():
                    neows = AsyncNeoWs("DEMO_KEY")
                    result = await neows.get_neo_lookup(3542519)
                    print(result)

                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
        """
        if not isinstance(asteroid_id, int):
            raise TypeError(f"'asteroid_id' must be 'int', got {asteroid_id.__class__.__name__}")

        url = f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={self._api_key}"
        
        # making request
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                if request.status == 429:
                    raise RateLimitError("You are being rate limited")
                elif request.status == 403:
                    raise InvalidApiKey(f"'{self._api_key}' is not a valid API key")
                elif request.status == 404:
                    raise NotFound(f"Asteroid of id '{asteroid_id}' could not be found")

                request = await request.json()

        return request

    async def get_neo_browse(self) -> NeoWsBrowseResponse:
        """
        |coro|
        
        Browse the overall asteroid data-set.

        **Example**

            .. code-block:: python3

                from nasawrapper import AsyncNeoWs
                from datetime import datetime
                import asyncio

                async def main():
                    neows = AsyncNeoWs("DEMO_KEY")
                    result = await neows.get_neo_browse()
                    print(result)

                loop = asyncio.get_event_loop()
                loop.run_until_complete(main())
        """
        url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={self._api_key}"

        # making request
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                if request.status == 429:
                    raise RateLimitError("You are being rate limited")
                elif request.status == 403:
                    raise InvalidApiKey(f"'{self._api_key}' is not a valid API key")

                request = await request.json()

        return request

class NeoWsQueryBuilder:
    """
    Retrieve a list of Asteroids based on
    their closest approach date to Earth,
    just like
    :py:class:`SyncNeoWs.get_neo_feed <nasawrapper.neows.SyncNeoWs.get_neo_feed>`,
    except by the fact that you are the person who will build the query.

    **Example**

        .. code-block:: python3

            from nasawrapper import NeoWsQueryBuilder
            from datetime import datetime

            builder = NeoWsQueryBuilder("DEMO_KEY")
            result = builder.set_start_date(datetime(2020, 2, 3)).set_end_date(datetime(2020, 2, 4)).get_feed()
            print(result)
    """
    def __init__(self, api_key: str, options = {}) -> None:
        self._api_key = api_key
        self._options = options

    @property
    def api_key(self):
        """
        Returns the API key.
        """
        return self._api_key

    @property
    def options(self):
        """
        Returns the options in dict format.
        """
        return self._api_key

    def set_start_date(self, start_date: datetime):
        """
        Set 'start_date' field to the options.
        """
        if not isinstance(start_date, datetime):
            raise TypeError(f"'start_date' must be 'datetime.datetime', got {start_date.__class.__name__}")

        self._options["start_date"] = start_date   
        return NeoWsQueryBuilder(self._api_key, self._options)     

    def set_end_date(self, end_date: datetime):
        """
        Set 'end_date' field to the options.
        """
        if not isinstance(end_date, datetime):
            raise TypeError(f"'end_date' must be 'datetime.datetime', got {end_date.__class.__name__}")

        self._options["end_date"] = end_date 
        return NeoWsQueryBuilder(self._api_key, self._options)

    def get_feed(self):
        """
        Make the request with the provided
        information.
        """
        options = Validator.validate(self._options, ["start_date", "end_date"])
        
        url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={self._api_key}"

        # building url
        for key, value in options.items():
            url += f"&{key}={value}"

        # making request
        request = requests.get(url)
        if request.status_code == 429:
            raise RateLimitError("You are being rate limited")
        elif request.status_code == 403:
            raise InvalidApiKey(f"'{self._api_key}' is not a valid API key")

        return request.json()