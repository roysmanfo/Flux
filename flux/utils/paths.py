import urllib3.util
from typing import Optional

def get_scheme(path: str) -> Optional[str]:
    """
    Extract and return the scheme of the given path

    `:param` path: the path to extract the scheme from.
    `:returns` the scheme of the path, or None if the path is a local file.
    """
    path = fr"{path}".lower().replace("file://", "")
    return urllib3.util.parse_url(path)

def is_local_path(path: str) -> bool:
    """
    Determine if the given path is a local path or a remote one

    `:param` path: the path to extract the scheme from.
    `:returns` true if the path is local
    """
    return get_scheme(path) is None



