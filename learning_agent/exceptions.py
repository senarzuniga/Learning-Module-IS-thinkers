
class MissingApiKeyError(Exception):
    """Raised when the API key is missing."""
    pass


class InvalidApiKeyError(Exception):
    """Raised when the API key is invalid."""
    pass
