#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# coding=utf-8
"""Command line interface"""


def _run_command():
    """
    Command line entry point
    """
    from argparse import ArgumentParser
    from argcomplete import autocomplete

    # Parser: "airsd"
    parser = ArgumentParser(
        prog='airsd', description='Simple file sharing in the cloud.')
    sub_parsers = parser.add_subparsers(
        dest='parser_action', title='Commands',
        help='Commands', description=''
        )
    parser.add_argument('--debug',  action='store_true',
                        help='If True, show the full error traceback.')

    # Parser: "airsd put"
    description = 'Put the file to share on the storage and return a shareable URL.'
    action = sub_parsers.add_parser('put', help=description, description=description)
    action.add_argument('sources', nargs='*', help='The files or directory to share.')
    action.add_argument('--archive', '-a', action='store_true',
                        help='Create an archive before putting on the share. Automatic '
                             'if SOURCES is a directory or multiples files.')
    action.add_argument('--expiry', '-e', default="24",
                        help='The download expiry time. In hours, or with a '
                             'specific time unit by appending: "s" for seconds, '
                             '"m" for minutes, "h" for hours or "d" for days '
                             '(For instance: "7d" for 7 days, "30m" for 30 minutes).')
    action.add_argument('--host', '-h', help='The remote storage host.')
    action.add_argument('--name', '-n', help='Rename the file being put.')
    action.add_argument('--quiet', '-q', help='Only return download URL as output.',
                        action='store_true')

    # Parser: "airsd get"
    description = 'Get shared file from an URL.'
    action = sub_parsers.add_parser('get', help=description, description=description)
    action.add_argument('url', help='The URL.')
    action.add_argument('--output', '-o', help='Output file or directory.', default=".")
    action.add_argument('--extract', '-e', help='Extract an archived file.',
                        action='store_true')
    action.add_argument('--quiet', '-q', help='Does no show output.',
                        action='store_true')

    # Parser: "airsd delete"
    # TODO
    # description = 'Delete a shared file.'
    # action = sub_parsers.add_parser('get', help=description, description=description)

    # Enable autocompletion
    autocomplete(parser)

    # Get arguments and call function
    args = vars(parser.parse_args())
    parser_action = args.pop('parser_action')
    if not parser_action:
        parser.error('An action is required')

    try:
        from os.path import dirname, realpath
        import sys
        sys.path.insert(0, dirname(dirname(realpath(__file__))))

        import airsd
        url = getattr(airsd, parser_action)(**args)
        if url:
            print(url)

    except KeyboardInterrupt:  # pragma: no cover
        parser.exit(status=1, message="Interrupted by user\n")

    except Exception as exception:
        if args.get('debug'):
            raise
        parser.exit(status=1, message=f'\033[31m{exception}\033[30m\n')


if __name__ == '__main__':
    _run_command()
