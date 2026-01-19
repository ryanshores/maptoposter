from typing import NamedTuple

class ApiContext(NamedTuple):
    api_key: str
    api_version: str
    base_url: str