import json


def _load_config(filepath: str) -> dict:
    data = {}
    with open(filepath) as f:
        data = json.loads(f.read())
    return data


def _get_hosts(config: dict) -> dict:
    hosts = config.get('hosts')
    if not hosts:
        raise Exception('load config fialed')

    data = {}
    for hconfig in hosts:
        if not isinstance(hconfig, dict):
            raise Exception('load config fialed')
        name = hconfig.get('name')
        _type = hconfig.get('type')
        uri = hconfig.get('uri')
        if not name or not _type or not uri:
            raise Exception('load config fialed')
        data[name] = hconfig

    return data


def load(filepath: str, need_check: bool = True) -> dict:
    data = _load_config(filepath)
    return _get_hosts(data) if need_check else data
