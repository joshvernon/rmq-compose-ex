#!/usr/bin/env python
#
# rabbitconsume.py
#
# Adapted from here:
# https://pika.readthedocs.io/en/0.10.0/examples/blocking_consume.html

import ssl
import subprocess

import pika

from secrets import COMPOSE_CERT, Q_CONN

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def on_message(channel, method_frame, header_frame, body):
    print('##### Start message: {0} #####'.format(method_frame.delivery_tag))
    print(body)
    print('##### End message #####')
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

certfile = COMPOSE_CERT

ssl_opts = urlencode(
    {'ssl_options': {'ca_certs': certfile, 'cert_reqs': ssl.CERT_REQUIRED}})
full_url = Q_CONN + ssl_opts
parameters = pika.URLParameters(full_url)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_consume(on_message, 'fred')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
