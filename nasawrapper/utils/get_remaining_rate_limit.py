import requests

def get_remaining_rate_limit(api_key: str) -> int:
    """
    Returns your remaining rate limit by
    making a request to
    :ref:`Apod <extensions/apod:Apod>` and
    getting the header ``X-RateLimit-Remaining``,
    that's returned on every API response.

    For example, if you are using an
    API key different from ``DEMO_KEY``,
    you have a default hourly rate
    limit of 1.000 requests, acording
    to the `Portal <https://api.nasa.gov/>`_.
    So, if you make 2 requests, your
    remaining rate limit will be equal to
    998.

    **Example**
        
        .. code-block:: python3

            from nasawrapper.utils import get_remaining_rate_limit

            remaining = get_remaining_rate_limit("DEMO_KEY")
            print(reamining)
    """
    headers = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}").headers
    return int(headers["X-RateLimit-Remaining"])