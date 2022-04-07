import ssl

import requests
import json
import os
import logging

from requests import exceptions


def login():
    url = "https://api0.prismacloud.io/login"
    username = os.getenv('PC_ACCESS_KEY')
    password = os.getenv('PC_SECRET_KEY')

    if username and password:
        payload = json.dumps({
            "username": username,
            "password": password
        })
        headers = {
            'accept': 'application/json; charset=UTF-8',
            'content-type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            res_json = json.loads(response.text)
            response.raise_for_status()
            return res_json.get('token', '')
        except exceptions.SSLError:
            logging.error("SSL error occurred. Please turn off VPN and retry")
        except Exception:
            logging.error("Failed to login. ", exc_info=True)
    else:
        logging.error("Failed to login. Please ensure PC_ACCESS_KEY and PC_SECRET_KEY environment variables are set")
    return ''

