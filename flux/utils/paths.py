import urllib3.util
from urllib3.util import Url

def parse_url(path: str) -> Url:
    """
    A cross platform version of `urllib3.utils.parse_url`
 
    `:param` path: the path to extract the scheme from  
    `:returns` a `Url` object.
    """
    path = fr"{path}".lower().replace("file://", "")
    return urllib3.util.parse_url(path)


def is_local_path(path: str) -> bool:
    """
    Determine if the given path is a local path or a remote one

    `:param` path: the path to extract the scheme from.

    `:returns` true if the path is local
    """

    if (path := path.strip()) == '':
        return False

    url = parse_url(path)

    if not url.scheme and not url.host:
        return True
    
    if url.scheme and url.scheme.lower() == "c":
        return True
    
    if url.host and url.host.replace('.', '') == '':
        return True

    return False


