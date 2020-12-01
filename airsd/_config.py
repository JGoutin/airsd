"""Configuration file"""

from configparser import ConfigParser, NoOptionError, NoSectionError, DEFAULTSECT
import os
from os import getenv, makedirs
from os.path import join, expandvars, expanduser
import airfs

#: Application name
APP_NAME = __name__.split(".")[0]

# OS dependant configuration directory
if os.name == "nt":
    CONFIG_DIR = join(expandvars("%APPDATA%"), APP_NAME)

elif os.getuid() != 0:
    CONFIG_DIR = join(getenv("XDG_CONFIG_HOME", expanduser("~/.config")), APP_NAME)

else:
    CONFIG_DIR = f"/etc/{APP_NAME}"

#: User configuration file
CONFIG_FILE = join(CONFIG_DIR, "config.cfg")

#: Server side configuration file
HOST_CONFIG_FILE = f".{APP_NAME}.cfg"

#: Default configuration
DEFAULT_CONFIG = dict(
    compression="gz",
    random_prefix=True,
    files_directory="files",
    max_expiry="1d",
    default_host="",
    host="",
)

#: Available compression methods
COMPRESSIONS = ("gz", "bz2", "xz")

#: Expiration time units
_TIME_UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400}

#: Cached configurations
_CACHED_CONFIG = dict()


def parse_expiry(expiry):
    """
    Parse the expiry time.

    Args:
        expiry (str or int): The download expiry time. Must be greater than zero.

    Returns:
        int: Expiry time in seconds.
    """
    try:
        expiry = int(expiry) * 3600
    except ValueError:
        try:
            expiry = int(expiry[:-1]) * _TIME_UNITS[expiry[-1].lower()]
        except (KeyError, ValueError, TypeError):
            raise ValueError(f"Invalid expiration value: {expiry}")
    if expiry <= 0:
        raise ValueError(f"Invalid expiration value: {expiry}")
    return expiry


def get_config():
    """
    Get local configuration.

    Returns:
        configparser.ConfigParser: Configuration.
    """
    try:
        return _CACHED_CONFIG[DEFAULTSECT]
    except KeyError:
        pass
    parser = ConfigParser(defaults=DEFAULT_CONFIG)
    parser.read(CONFIG_FILE)

    _CACHED_CONFIG[DEFAULTSECT] = parser
    return parser


def configure(option, value, host=None):
    """
    Set a configuration option.

    Args:
        option (str): Name of option to set.
        value (str): Value of option to set.
        host (str): The remote storage host.
    """
    value = str(value)

    if host and option in ("host", "default_host"):
        raise ValueError(f'"{option}" can not be set for a specific host.')
    elif option == "compression" and value not in COMPRESSIONS:
        raise ValueError(f'"{option}" value must be in: {", ".join(COMPRESSIONS)}.')
    elif option == "random_prefix" and value.lower() not in ConfigParser.BOOLEAN_STATES:
        raise ValueError(f'"{option}" value must be "True" or "False".')
    elif option == "max_expiry":
        parse_expiry(value)

    section = host or DEFAULTSECT
    parser = get_config()

    try:
        current_value = parser.get(section, option)
    except (NoOptionError, NoSectionError):
        current_value = None
    if current_value == value:
        return

    parser.set(section, option, value)
    makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "wt") as config_file:
        parser.write(config_file)


def get_host_config(host=None):
    """
    Get host configuration from local user configuration and remote host configuration
    files.

    Args:
        host (str): Storage host.

    Returns:
        dict: Host configuration.
    """
    if not host:
        host = get_default_host()
        if not host:
            raise ValueError('"host" must be specified.')
    else:
        configure("host", host)
    try:
        return _CACHED_CONFIG[host]
    except KeyError:
        pass

    parsers = [get_config()]

    try:
        with airfs.open(join(host, HOST_CONFIG_FILE), "rt") as config_file:
            parser = ConfigParser()
            parser.read_file(config_file)
    except (FileNotFoundError, PermissionError):
        pass

    config = DEFAULT_CONFIG.copy()
    for parser in parsers:
        for key in DEFAULT_CONFIG:
            try:
                if key == "random_prefix":
                    value = parser.getboolean(host, key)
                else:
                    value = parser.get(host, key)
            except (NoOptionError, NoSectionError):
                continue
            config[key] = value

    config["host"] = host
    config["max_expiry_sec"] = parse_expiry(config["max_expiry"])

    _CACHED_CONFIG[host] = config
    return config


def get_default_host():
    """
    Get default host from the configuration.

    Returns:
        str or None: host.
    """
    for option in ("default_host", "host"):
        try:
            value = get_config().get(DEFAULTSECT, option)
        except NoOptionError:
            continue
        if value:
            return value
    return None
