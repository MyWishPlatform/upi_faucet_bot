import datetime

from cache import get_timeout


def readable_timeout(id: int, address: str):
    id_sec, address_sec = get_timeout(id, address)
    output = datetime.timedelta(seconds=id_sec) if id_sec > 0 else datetime.timedelta(seconds=address_sec)
    return output
