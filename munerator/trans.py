import zmq
import logging
log = logging.getLogger(__name__)

import re


translaters = [
    (r'[0-9: ]*InitGame: .*\\mapname\\(?P<mapname>[\w]+).*', 'initgame'),
    (r'[0-9: ]*ShutdownGame:.*', 'shutdowngame'),
    (r'[0-9: ]*say: (?P<playername>[^:]+): (?P<text>.+)', 'say'),
    (r'[0-9: ]*ClientUserinfoChanged: (?P<client_id>\d+) n\\(?P<player_name>[\w\s]+).*id\\(?P<guid>[\w]+)',
     'clientuserinfochanged'),
    (r'[0-9]+: client:(?P<client_id>\d+) health:(?P<health>\d+).*', 'hit'),
    (r'[0-9: ]*Kill: [^:]+: (?P<killer>[\w\s]+) killed (?P<killed>[\w\s]+) by (?P<mod>[\w]+)', 'kill'),
    (r'[0-9: ]*ClientDisconnect: (?P<client_id>\d+)', 'clientdisconnect'),
    (r'[0-9: ]*ClientConnect: (?P<client_id>\d+)', 'clientconnect'),
    (r'[0-9: ]*ClientBegin: (?P<client_id>\d+)', 'clientbegin'),
    (r'[0-9: ]*PlayerScore: (?P<client_id>\d+) (?P<score>[\d\-]):.*', 'playerscore'),
]

regexes = [(re.compile(r), k) for r, k in translaters]


def translate(line, regexes):
    data = {}

    for regex, kind in regexes:
        m = regex.match(line)
        if m:
            yield kind, m.groupdict()


def eventstream(in_socket, out_socket):
    while True:
        msg = in_socket.recv_string()
        ts, line = msg.split(' ', 1)

        if not line:
            continue

        log.debug('translating: ' + line)

        for kind, data in translate(line, regexes):
            data['timestamp'] = ts
            data['kind'] = kind
            out_socket.send_json(data)


def main(args):
    context = zmq.Context()
    in_socket = context.socket(zmq.PULL)
    in_socket.bind(args['raw-socket'])

    out_socket = context.socket(zmq.PUSH)
    out_socket.connect(args['events-socket'])

    eventstream(in_socket, out_socket)
