class NotFound(Exception):
    """
    Exception that's raised when an item is not found in
    any NASA API
    """
    pass

class InvalidKey(Exception):
    """
    Exception that's raised when the developer provides
    an invalid key
    """
    pass

class InvalidDate(Exception):
    """
    Exception that's raised when the developer provides
    an invalid date
    """
    pass

class InvalidApiKey(Exception):
    """
    Exception that's raised when the developer
    provides an invalid API key
    """
    pass

class RateLimitError(Exception):
    """
    Exception that's raised when the develper
    make too many requests to the API
    """