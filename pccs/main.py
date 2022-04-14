import argparse
import sys
import os

from common import auth
from actions import policy_actions


def run():
    parser = argparse.ArgumentParser('Manage PCCS policies')
    parser.add_argument('--auth', help='String with credentials and API endpoint - '
                                       '"https://api.prismacloud.io::<your-access-key>::<your-secret-key>"', required=False)
    parser.add_argument('--list', '-l', help='List custom policies', required=False, action='store_true')
    parser.add_argument('--publish', '-p', help='Publish policy from file', required=False)
    parser.add_argument('--delete', '-d', help='Delete policy by ID', required=False)
    parser.add_argument('--update', '-u', help='Update policy by ID from file', required=False)
    parser.add_argument('--verbose', '-v', help='Print verbose response', required=False, action='store_true', default=False)
    parser.add_argument('--policy-id', '-id', help='Get policy by ID', required=False)
    parser.add_argument('--get-suppressions', '-g', help='List suppressions', required=False, action='store_true')
    parser.add_argument('--suppress', '-s', help='Add a suppression by Policy ID', required=False)
    parser.add_argument('--remove', '-r', help='Remove a suppression by Policy ID', required=False)
    args = parser.parse_args()

    base_url = os.getenv('PRISMA_API_URL', '')
    username = os.getenv('PC_ACCESS_KEY', '')
    password = os.getenv('PC_SECRET_KEY', '')

    if args.auth:
        base_url, username, password = [i for i in args.auth.split("::")]
    if base_url and username and password:
        token = auth.login(base_url, username, password)
    else:
        print("Please set PRISMA_API_URL, PC_ACCESS_KEY and PC_SECRET_KEY environment variables or use the --auth "
                      "argument")
        sys.exit(1)
    if not token:
        sys.exit(1)

    if args.list:
        policy_actions.get_custom_policies(base_url, token, args.verbose)

    if args.policy_id:
        if args.update:
            policy_actions.update_custom_policy_by_id(base_url, token, args.policy_id, args.update)
        if args.suppress:
            policy_actions.suppress_custom_policy_by_id(base_url, token, args.policy_id, args.suppress)
        else:
            policy_actions.get_custom_policy_by_id(base_url, token, args.policy_id, args.verbose)

    if args.publish:
        policy_actions.create_custom_policy(base_url, token, file_path=args.publish)

    if args.delete:
        policy_actions.delete_custom_policy_by_id(base_url, token, args.delete)

    if args.get_suppressions:
        policy_actions.get_suppressions(base_url, token, args.verbose)

    if args.suppress:
        policy_actions.suppress_custom_policy_by_id(base_url, token,  args.policy_id, args.suppress)
        # policy_actions.suppress_custom_policy_by_id(base_url, token,  args.policy_id, args.suppress_id, args.suppress)

    # if args.comment:
    #     policy_actions.suppress_custom_policy_by_id(base_url, token, args.policy_id, args.comment, args.suppress)

    # if args.remove:
    #     policy_actions.remove_suppression_by_policy_id(base_url, token,  args.policy_id, args.suppress)

if __name__ == '__main__':
    run()
