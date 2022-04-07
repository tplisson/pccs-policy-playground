import json
import sys
import requests
import yaml

from requests import exceptions
from pathlib import Path


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
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")


def get_custom_policy_by_id(base_url, token, policy_id, verbose=False):
    url = f"{base_url}/bridgecrew/api/v1/policies/{policy_id}"
    headers = {
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    }
    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        res_json = json.loads(response.text)
        print(json.dumps(res_json, indent=4))
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")


def create_custom_policy(base_url, token, file_path, verbose=False):
    path = Path(file_path).resolve()
    try:
        with open(path, "r") as stream:
            try:
                policy_data = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)
                sys.exit(1)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    url = f"{base_url}/bridgecrew/api/v1/policies"
    headers = {
        'Accept': 'application/json; charset=UTF-8',
        'Content-Type': 'application/json',
        'x-redlock-auth': token
    }
    if policy_data["metadata"]["id"]:
        print(f"Note: Found unnecessary attribute \"id: {policy_data['metadata']['id']}\" in policy. Ignoring it for "
              f"publishing.")
        policy_data["metadata"].pop("id", None)
    payload = {"code": policy_data}
    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        res_json = json.loads(response.text)
        print(json.dumps(res_json, indent=4))
        response.raise_for_status()
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred while publishing policy: {e}")
        sys.exit(1)


def delete_custom_policy_by_id(base_url, token, policy_id, verbose=False):
    url = f"{base_url}/bridgecrew/api/v1/policies/{policy_id}"
    headers = {
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    }
    try:
        response = requests.request("DELETE", url, headers=headers)
        response.raise_for_status()
        res_json = json.loads(response.text)
        print(json.dumps(res_json, indent=4))
    except exceptions.SSLError:
        print("SSL error occurred. Please disable VPN and try again.")
    except Exception as e:
        print(f"Error occurred while listing policies: {e}")
