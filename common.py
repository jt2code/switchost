import os
import sys
import urllib.request


base_path = os.path.abspath(os.path.dirname(__file__))
state_file_path = os.path.join(base_path, 'run.state')
config_file_path = os.path.join(base_path, 'config.json')


def get_hosts_path() -> str:
    if sys.platform == 'linux' or sys.platform == 'darwin':
        return '/etc/hosts'
    elif sys.platform == 'win32':
        return 'C:\\Windows\\System32\\drivers\\etc\\hosts'
    raise Exception('Not support platform: %s' % sys.platform)


def http_get(url: str) -> str:
    with urllib.request.urlopen(url) as req:
        return req.read().decode()


def get_state() -> str:
    if os.path.isfile(state_file_path):
        with open(state_file_path) as f:
            return f.read().strip()
    return ''


def set_state(state: str) -> None:
    with open(state_file_path, 'w') as f:
        f.write(state.strip())


def indent_print(s, **kwargs):
    print(' ', s, **kwargs)
