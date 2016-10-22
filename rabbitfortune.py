#!/usr/bin/env python
#
# rabbitfortune.py
#
# Adapted from here:
# https://github.com/compose-ex/rabbitmqconns/blob/master/python/RabbitMQConnectorSSL.py

import ssl
import subprocess

import pika

from secrets import COMPOSE_CERT, Q_CONN

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

certfile = COMPOSE_CERT

ssl_opts = urlencode(
    {'ssl_options': {'ca_certs': certfile, 'cert_reqs': ssl.CERT_REQUIRED}})
full_url = Q_CONN + ssl_opts
parameters = pika.URLParameters(full_url)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Run the fortune-mod program to get a random message text
# to publish.
p = subprocess.Popen('fortune', stdout=subprocess.PIPE, universal_newlines=True)
message, _ = p.communicate()
my_routing_key='tributes'
exchange_name='postal'

channel.exchange_declare(exchange=exchange_name,
                         type='direct',
                         durable=True)


channel.basic_publish(exchange=exchange_name,
                      routing_key=my_routing_key,
                      body=message)

channel.close()
connection.close()
