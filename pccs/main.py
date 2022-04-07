import argparse
import logging
import sys
import os

from common import auth
from actions import policy_actions

base_url = os.getenv('PC_API_URL', '')
username = os.getenv('PC_ACCESS_KEY')
password = os.getenv('PC_SECRET_KEY')


def run():
    parser = argparse.ArgumentParser('Manage PCCS policies')
    parser.add_argument('--list', '-l', help='List custom policies', required=False, action='store_true')
    parser.add_argument('--publish', '-p', help='Publish policies from file', required=False)
    parser.add_argument('--delete', '-d', help='Delete policy by ID', required=False)
    parser.add_argument('--update', '-u', help='Update policy by ID', required=False)
    parser.add_argument('--verbose', '-v', help='Print verbose response', required=False, action='store_true', default=False)
    args = parser.parse_args()
    if base_url and username and password:
        token = auth.login(base_url, username, password)
    else:
        logging.error("Please set PC_API_URL, PC_ACCESS_KEY and PC_SECRET_KEY environment variables.")
        sys.exit(1)
    if not token:
        sys.exit(1)
    elif args.list:
        policy_actions.get_custom_policies(base_url, token, args.verbose)


if __name__ == '__main__':
    run()
