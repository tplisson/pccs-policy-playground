import json
import logging

import requests
from requests import exceptions


def get_custom_policies(base_url, token, verbose=False):
    url = f"{base_url}/bridgecrew/api/v1/policies/table/data"
    headers = {
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    }
    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        res_json = json.loads(response.text)
        if verbose:
            # remove accountsData key
            for p in res_json.get("data"):
                p.pop("accountsData")
            print(json.dumps(res_json.get("data"), indent=4))
        else:
            print(f'Found {len(res_json.get("data"))} custom policies\n')
            print("Policy ID: Title")
            for p in res_json.get("data"):
                print(f'{p.get("id")}: {p.get("title")}')
    except exceptions.SSLError:
        logging.error("SSL error occurred. Please disable VPN and try again.")
    except Exception:
        logging.error("Error occurred while listing policies", exc_info=True)
