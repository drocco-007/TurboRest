# -*- coding: utf-8 -*-

from setuptools import setup

packages = ('turborest_example', 'turborest',)

setup(
    name='TurboRest',
    version='1.0',

    paster_plugins=['TurboGears'],
    setup_requires=['PasteScript >= 1.7'],
    install_requires=[
        'TurboGears >= 1.5.1',
    ],
    zip_safe=False,
    packages=packages,
    entry_points="""
        [console_scripts]
        start-tg_resources = tg_resources.command:start
        # See the tg_resources.command.bootstrap function for details
        bootstrap-tg_resources = tg_resources.command:bootstrap

        [turbogears.extensions]
        turborest = turborest.turbogears.rest
    """,
    )
