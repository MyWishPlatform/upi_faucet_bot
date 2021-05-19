import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def store(id: int, address: str):
    r.set(id, address, ex=86400)
    r.set(address, id, ex=86400)


def check_timeout(id: int, address: str) -> bool:
    return True if r.exists(id) or r.exists(address) else False


def get_timeout(id: int, address: str):
    id_timeout = r.ttl(id)
    address_timeout = r.ttl(address)
    return id_timeout, address_timeout
