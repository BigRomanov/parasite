# Copyright: (c) 2023, Alex Romanov 
# Apache2 License (see COPYING or https://www.apache.org/licenses/LICENSE-2.0.txt)
from __future__ import annotations

import argparse
import importlib
import os
import sys

from importlib.metadata import distribution


def _short_name(name):
    return name.removeprefix('parasite-').replace('parasite', 'adhoc')


def main():
    dist = distribution('paraside-core')
    ep_map = {_short_name(ep.name): ep for ep in dist.entry_points if ep.group == 'console_scripts'}

    parser = argparse.ArgumentParser(prog='python -m parasite', add_help=False)
    parser.add_argument('entry_point', choices=list(ep_map) + ['test'])
    args, extra = parser.parse_known_args()

    if args.entry_point == 'test':
        parasite_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        source_root = os.path.join(parasite_root, 'test', 'lib')

        if os.path.exists(os.path.join(source_root, 'parasite_test', '_internal', '__init__.py')):
            # running from source, use that version of parasite-test instead of any version that may already be installed
            sys.path.insert(0, source_root)

        module = importlib.import_module('parasite_test._util.target.cli.parasite_test_cli_stub')
        main = module.main
    else:
        main = ep_map[args.entry_point].load()

    main([args.entry_point] + extra)


if __name__ == '__main__':
    main()
