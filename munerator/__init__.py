"""Munerator

Usage:
  munerator <modules> [options] 

Options:
  -v --verbose          Verbose logging.
  -h --help             Show this screen.
  --version             Show version.
  --raw-socket url      ZMQ socket for raw logline [default: tcp://127.0.0.1:9000]
  --events-socket url   ZMQ socket for raw events [default: tcp://127.0.0.1:9001]
  --context-socket url  ZMQ socket for context events [default: tcp://0.0.0.0:9002]
  --old-api url         Url to old api [default: http://quake.ijohan.nl/events]
"""
from docopt import docopt
from rcfile import rcfile
import pkg_resources
import logging

from importlib import import_module

version = pkg_resources.get_distribution("munerator").version


def main():
    args = rcfile(__name__, docopt(__doc__, version=version, options_first=True))

    module_name = args['<modules>']
    module = import_module('munerator.%s' % module_name)

    extra_options = getattr(module, 'mandatory_options')

    print __doc__+extra_options
    args = rcfile(__name__, docopt(__doc__+extra_options, version=version))
    print args
    if args.get('verbose'):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('debug logging enabled')

    module.main(args)
