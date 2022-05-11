import json
import re

import requests
from requests import exceptions

from pccs.common import auth


def get_custom_policy_suppressions(base_url, token, verbose=False):
    url = f"{base_url}/bridgecrew/api/v1/suppressions"
    headers = auth.get_auth_headers(token)
    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        res_json = json.loads(response.text)
        # filter out OOTB policies
        bc_id_pattern = re.compile('^BC_')
        custom_suppressions = []
        for s in res_json:
            if not bc_id_pattern.match(s.get('policyId')) and s.get('suppressionType') == 'Policy':
                custom_suppressions.append(s)
        print(json.dumps(custom_suppressions, indent=4))

    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")


def create_custom_policy_suppression(base_url, token, policy_id):
    url = f"{base_url}/bridgecrew/api/v1/suppressions/{policy_id}"
    headers = auth.get_auth_headers(token)
    try:
        response = requests.request("POST", url, headers=headers)
        response.raise_for_status()
        res_json = json.loads(response.text)
        # filter out OOTB policies
        bc_id_pattern = re.compile('^BC_')
        custom_suppressions = []
        for s in res_json:
            if not bc_id_pattern.match(s.get('policyId')) and s.get('suppressionType') == 'Policy':
                custom_suppressions.append(s)
        print(json.dumps(custom_suppressions, indent=4))

    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")