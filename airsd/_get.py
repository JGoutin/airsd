"""Get command"""
from os.path import join, isfile, basename
from urllib.parse import urlparse
import tarfile

import requests


def get(url, output=".", extract=False):
    """
    Get a file or archive from an URL.

    Args:
        output (str): Output file or directory path.
        url (str): Input URL.
        extract (bool): If True, extract archive.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    if extract:
        with tarfile.open(fileobj=response.raw) as archive:
            archive.extractall(output)
    else:
        if not isfile(output):
            output = join(output, basename(urlparse(url).path))
        with open(output, 'wb') as dest:
            for chunk in response.iter_content():
                dest.write(chunk)
