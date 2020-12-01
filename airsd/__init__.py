"""airsd"""

# Copyright (C) 2019 J.Goutin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from os.path import (
    join as _join,
    isfile as _isfile,
    isdir as _isdir,
    basename as _basename,
)
from secrets import token_hex as _token_hex
from tarfile import open as _tarfile_open
from urllib.parse import urlparse as _urlparse

from airfs import (
    open as _open,
    copy as _copy,
    shareable_url as _shareable_url,
    remove as _remove,
)
from requests import request as _request

from airsd._config import (
    get_host_config as _get_host_config,
    parse_expiry as _parse_expiry,
    configure,
)


__version__ = "1.0.0-alpha.1"
__all__ = ["get", "put", "delete", "configure"]


def get(url, output=".", extract=False):
    """
    Get a file or archive from an URL.

    Args:
        output (str): Output file or directory path.
        url (str): Input URL.
        extract (bool): If True, extract archive.
    """
    response = _request("GET", url, stream=True)
    response.raise_for_status()
    if extract:
        with _tarfile_open(fileobj=response.raw) as archive:
            archive.extractall(output)
    else:
        if not _isfile(output):
            output = _join(output, _basename(_urlparse(url).path))
        with open(output, "wb") as dest:
            for chunk in response.iter_content():
                dest.write(chunk)


def put(sources, host=None, expiry="24h", archive=False, compression=None, name=None):
    """

    Args:
        sources (iterable of str): The files or directory to share.
        archive (bool): If True, create an archive before putting on the share.
            Automatic if "sources" is a directory or multiples files.
        expiry (str or int): The download expiry time. In hours, or with a specific time
            unit by appending: "s" for seconds, "m" for minutes, "h" for hours or "d"
            for days (For instance: "7d" for 7 days, "30m" for 30 minutes).
        compression (str): The compression method to use when archiving.
            Possible values: "gz", "bz2", "xz". Default to value saved in configuration
            or "gz".
        host (str): The remote storage host.
        name (str): Rename the file being put.

    Returns:
        str: The shareable URL to the shared object.
    """
    config = _get_host_config(host)

    expiry = _parse_expiry(expiry)
    max_expiry = config["max_expiry_sec"]
    if max_expiry and expiry > max_expiry:
        raise ValueError(f"Expiry can't be more than {config['max_expiry']}.")

    if archive or len(sources) > 1 or any(_isdir(path) for path in sources):
        compression = compression or config["compression"]
        dst = _set_dst_path(name or f"archive.tar.{compression}", config)
        with _open(dst, "wb") as fileobj:
            with _tarfile_open(fileobj=fileobj, mode=f"w:{compression}") as dst_archive:
                for src in sources:
                    dst_archive.add(src, arcname=_basename(src))

    else:
        dst = _set_dst_path(name or _basename(sources[0]), config)
        _copy(sources[0], dst)

    return _shareable_url(dst, expiry)


def delete(urls):
    """
    Delete a shared file.

    Args:
        urls (iterable of str): Shareable URL of files to delete.
    """
    # TODO: Fix unmounted storage not found because URL starts with https://
    for url in urls:
        url = _urlparse(url)
        _remove(f"{url.scheme}://{url.netloc}{url.path}")


def _set_dst_path(src, config):
    """
    Set the storage destination path.

    Args:
        src (str): Source path of the file to share.
        config (dict): The remote storage host configuration.

    Returns:
        str: Destination path of the file on the storage.
    """
    dst = [config["host"], config["files_directory"]]
    if config["random_prefix"]:
        dst.append(_token_hex())
    dst.append(_basename(src))
    return _join(*dst)
