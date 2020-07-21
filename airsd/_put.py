"""Put command"""
from os.path import isdir, basename
import tarfile
import airfs

from airsd._host import get_host


def put(*sources, archive=False, expiry="24h", host=None, name=None):
    """

    Args:
        *sources (str): The files or directory to share.
        archive (bool): If True, create an archive before putting on the share.
            Automatic if "sources" is a directory or multiples files.
        expiry (str or int): The download expiry time. In hours, or with a specific time
            unit by appending: "s" for seconds, "m" for minutes, "h" for hours or "d"
            for days (For instance: "7d" for 7 days, "30m" for 30 minutes).
        host (str): The remote storage host.
        name (str): Rename the file being put.

    Returns:
        str: The shareable URL to the shared object.
    """

    host_obj = get_host(host)

    # Put archive
    if archive or len(sources) > 1 or any(isdir(path) for path in sources):
        dest = host_obj.get_path(name or 'archive.tar.gz')
        with airfs.open(dest, 'wb') as fileobj:
            with tarfile.open(fileobj=fileobj, mode='w:gz') as archive:
                for source in sources:
                    # TODO: arcname
                    archive.add(source, arcname=None)

    # Put file
    else:
        dest = host_obj.get_path(name or basename(sources[0]))
        airfs.copy(sources[0], dest)

    # Get temporary URL
    return host_obj.create_url(dest, expiry)
