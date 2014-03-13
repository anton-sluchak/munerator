import zmq
import logging
log = logging.getLogger(__name__)

import time
from subprocess import Popen, PIPE

mandatory_options = """
Usage:
    munerator wrap <cmd>
"""


def wrap(socket, command):
    args = command.split()
    p = Popen(args, stdout=PIPE)

    while p.poll() is None:
        line = p.stdout.readline()

        if line:
            msg = "%s %s" % (time.time(), line.strip())
            log.debug('sending: ' + msg)
            socket.send_string(msg)


def main(args):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect(args['raw-socket'])

    wrap(socket, args['command'])
