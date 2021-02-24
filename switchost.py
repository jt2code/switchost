#!/usr/bin/env python

import sys
import common
import config


def rewrite_hosts_file(hosts_content: str) -> None:
    try:
        with open(common.get_hosts_path(), 'w') as f:
            f.write(hosts_content)
    except PermissionError as e:
        print(e)
        print('    Please try `sudo %s`' % sys.argv[0])
        exit(1)


def update(conf: dict, name: str) -> None:
    if conf['type'] == 'local':
        with open(conf['uri']) as f:
            content = f.read()
    else:
        content = common.http_get(conf['uri'])
    if not content:
        print('load hosts file error:', conf['uri'])
    rewrite_hosts_file(content)
    common.set_state(name)


if __name__ == '__main__':
    host_config_name = None
    if len(sys.argv) > 1:
        host_config_name = sys.argv[1]
        if host_config_name == '--current ':
            print(common.get_state())
            exit(0)

    hosts = config.load(common.config_file_path)
    conf = hosts.get(host_config_name)
    if not conf:
        print('Usage', sys.argv[0], '{ --current | %s }' % ' | '.join(hosts.keys()))
        exit(1)
    update(conf, host_config_name)
