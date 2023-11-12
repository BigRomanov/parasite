from __future__ import annotations

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

install_requires = (here / 'requirements.txt').read_text(encoding='utf-8').splitlines()

setup(
    install_requires=install_requires,
    package_dir={'': 'lib',
                 'parasite_test': 'test/lib/parasite_test'},
    packages=find_packages('lib') + find_packages('test/lib'),
    entry_points={
        'console_scripts': [
            'parasote=parasite.cli.adhoc:main',
        ],
    },
)