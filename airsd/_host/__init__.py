""""""
# TODO

_TIME_UNITS = {
    's': 1,
    'm': 60,
    'h': 3600,
    'd': 86400
}


def get_host(host):
    """"""
    return _HostBase()


class _HostBase:
    """"""

    def get_path(self, path):
        """"""

    def create_url(self, path, expiry):
        """"""

    @staticmethod
    def _parse_expiry(expiry):
        """"""
        try:
            return int(expiry) * 3600
        except ValueError:
            return int(expiry[:-1]) * _TIME_UNITS[expiry[-1].lower()]
