#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python Future imports
from __future__ import unicode_literals, absolute_import, print_function

# Python System imports
import requests
import json
import argparse

# Third-party imports
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def root():
    """
    Home handler
    """

    return "OK"


@app.route('/new_event', methods=['POST'])
def new_event():
    """
    PivotalTracker event handler, handles POST events from a
    Pivotal Tracker Project
    """

    if request.json is None:
        print('Invalid Content-Type')
        return 'Content-Type must be application/json and the request body\
                must contain valid JSON', 400

    try:
        primary_ressource = request.json.get('primary_resources')[0]
        message = request.json.get('message')
        message += " - [{}]({})".format(
            primary_ressource.get('name'),
            primary_ressource.get('url')
        )
        if message is not None:
            post_text(message)
    except Exception:
        import traceback
        traceback.print_exc()

    return 'OK'


def post_text(text):
    """
    Mattermost POST method, posts text to the Mattermost incoming webhook URL
    """

    data = {}
    data['text'] = text.strip()
    if app.config['USERNAME']:
        data['username'] = app.config['USERNAME']
    if app.config['ICON_URL']:
        data['icon_url'] = app.config['ICON_URL']
    if app.config['CHANNEL']:
        data['channel'] = app.config['CHANNEL']

    headers = {'Content-Type': 'application/json'}
    resp = requests.post(
        app.config['MATTERMOST_WEBHOOK_URL'],
        headers=headers,
        data=json.dumps(data)
    )

    if resp.status_code is not requests.codes.ok:
        print(
            'Encountered error posting to Mattermost URL {}, status={},\
            response_body={}'.format(
                app.config['MATTERMOST_WEBHOOK_URL'],
                resp.status_code,
                resp.json())
        )


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'MATTERMOST_WEBHOOK_URL',
        help='The Mattermost webhook URL you created'
    )

    server_options = parser.add_argument_group("Server")
    server_options.add_argument('-p', '--port', type=int, default=5000)
    server_options.add_argument('--host', default='0.0.0.0')

    parser.add_argument(
        '-u',
        '--username',
        dest='USERNAME',
        default='Pivotal Tracker'
    )

    # Leave this blank to post to the default channel of your webhook
    parser.add_argument(
        '--channel',
        dest='CHANNEL',
        default='')

    parser.add_argument(
        '--icon',
        dest='ICON_URL',
        default='https://www.pivotaltracker.com/favicon.ico'
    )

    options = vars(parser.parse_args(args=args))

    host, port = options.pop("host"), options.pop("port")

    return host, port, options


def main():
    host, port, options = parse_args()
    app.config.update(options)

    app.run(host=host, port=port)


if __name__ == "__main__":

    main()
