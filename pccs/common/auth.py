import requests
import json

from requests import exceptions


def login(base_url, username, password):
    url = f"{base_url}/login"

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
            print("SSL error occurred. Please turn off VPN and retry")
        except Exception as e:
            print(f"Failed to login: {e}")
    else:
        print("Failed to login. Please ensure PC_ACCESS_KEY and PC_SECRET_KEY environment variables are set")
    return ''


def get_auth_headers(token, content_type=False):
    return {
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    } if not content_type else {
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token,
        'Content-Type': 'application/json'
    }

