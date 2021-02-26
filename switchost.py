#!/usr/bin/env python

import sys
import argparse
import common
import config


def rewrite_hosts_file(hosts_content: str) -> None:
    try:
        with open(common.get_hosts_path(), 'w') as f:
            f.write(hosts_content)
    except PermissionError:
        common.indent_print('please try `sudo %s`' % sys.argv[0])
        exit(1)


def update(conf: dict, name: str) -> None:
    if conf['type'] == 'local':
        with open(conf['uri']) as f:
            content = f.read()
    else:
        content = common.http_get(conf['uri'])
    if not content:
        common.indent_print('load hosts file error: %s' % conf['uri'])
    rewrite_hosts_file(content)
    common.set_state(name)


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-a', '--all', dest='_all', action='store_true',
                       help='show all hosts names from `config.json`')
    parse.add_argument('-s', '--current', dest='_current',
                       action='store_true', help='show current state')
    parse.add_argument('name', nargs='?', type=str, help='hosts config name')
    args = parse.parse_args()

    if args._current:
        common.indent_print(common.get_state())
        exit(0)

    hosts = config.load(common.config_file_path)
    if args._all:
        for k in hosts.keys():
            common.indent_print(k)
        exit(0)

    conf = hosts.get(args.name)
    if not conf:
        parse.print_help()
        exit(1)

    update(conf, args.name)
