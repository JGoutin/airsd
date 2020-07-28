#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""Command line interface"""


def _run_command():
    """
    Command line entry point
    """
    from os.path import dirname, realpath
    import sys

    sys.path.insert(0, dirname(dirname(realpath(__file__))))

    from argparse import ArgumentParser
    from argcomplete import autocomplete
    from airsd._config import (
        get_default_host,
        APP_NAME,
        get_config,
        DEFAULTSECT,
        COMPRESSIONS,
    )

    parser = ArgumentParser(
        prog=APP_NAME, description="Simple file sharing in the cloud."
    )
    sub_parsers = parser.add_subparsers(
        dest="parser_action", title="Commands", help="Commands", description=""
    )
    parser.add_argument(
        "--debug", action="store_true", help="If True, show the full error traceback."
    )

    config = get_config()
    default_host = get_default_host()
    description = "Put the file to share on the storage and return a shareable URL."
    action = sub_parsers.add_parser("put", help=description, description=description)
    action.add_argument("sources", nargs="*", help="The files or directory to share.")
    action.add_argument(
        "--archive",
        "-a",
        action="store_true",
        help="Create an archive before putting on the share. Automatic "
        "if SOURCES is a directory or multiples files.",
    )
    action.add_argument(
        "--expiry",
        "-e",
        default="24",
        help="The download expiry time. In hours, or with a "
        'specific time unit by appending: "s" for seconds, '
        '"m" for minutes, "h" for hours or "d" for days '
        '(For instance: "7d" for 7 days, "30m" for 30 minutes). '
        "Must be greater than zero.",
    )
    action.add_argument(
        "--host",
        "-H",
        help="The remote storage host.",
        default=default_host,
        required=default_host is None,
    )
    action.add_argument(
        "--compression",
        "-c",
        help="The compression method to use when archiving.",
        default=config.get(DEFAULTSECT, "compression"),
        choices=COMPRESSIONS,
    )
    action.add_argument("--name", "-n", help="Rename the file being put.")
    action.add_argument(
        "--quiet", "-q", help="Only return download URL as output.", action="store_true"
    )

    description = "Get shared file from an URL."
    action = sub_parsers.add_parser("get", help=description, description=description)
    action.add_argument("url", help="The URL.")
    action.add_argument("--output", "-o", help="Output file or directory.", default=".")
    action.add_argument(
        "--extract", "-e", help="Extract an archived file.", action="store_true"
    )
    action.add_argument(
        "--quiet", "-q", help="Does no show output.", action="store_true"
    )

    description = "Delete a shared file."
    action = sub_parsers.add_parser("delete", help=description, description=description)
    action.add_argument("urls", nargs="*", help="Shareable URL of files to delete.")

    description = "Set a configuration option."
    action = sub_parsers.add_parser(
        "configure", help=description, description=description
    )
    action.add_argument("option", help="Name of option to set.")
    action.add_argument("value", help="Value of option to set.")
    action.add_argument("--host", help="Set option for the specified host.")

    autocomplete(parser)

    args = vars(parser.parse_args())
    parser_action = args.pop("parser_action")
    if not parser_action:
        parser.error("An action is required")

    try:
        import airsd

        url = getattr(airsd, parser_action)(**args)
        if url:
            print(url)

    except KeyboardInterrupt:  # pragma: no cover
        parser.exit(status=1, message="Interrupted by user\n")

    except Exception as exception:
        if args.get("debug"):
            raise
        parser.exit(status=1, message=f"\033[31m{exception}\033[30m\n")


if __name__ == "__main__":
    _run_command()
