"""
Core code for managing the EESSI infrastructure
:author: Terje Kvernes (University of Oslo)
"""

import argparse
import os
import sys

from eessi.infrastructure import Infrastructure
from eessi.tools import ARCHITECTURES, NODE_TYPES
from eessi.tools import destroy_infrastructure

# TODO:
# Create throw-away ssh keys?

def required_environment_keys_are_set(keys):
    """
    Check that the given environment keys are set.
    """
    missing_keys = []
    for key in keys:
        if not key in os.environ:
            missing_keys.append(key)

    if missing_keys:
        sys.stderr.write("ERROR: The following environment variables must be set:\n ")
        sys.stderr.write(", ".join(missing_keys))
        sys.stderr.write("\n\n")
        return False

    return True

def main():
    mode = 'test'
    parser = argparse.ArgumentParser(description='Create EESSI infrastructure.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--architectures', dest='architectures', choices=ARCHITECTURES, nargs='+',
                        default=ARCHITECTURES, help='Pick what architectures to work on.')
    parser.add_argument('--dry-run', dest='dryrun', action='store_const',
                        const=True, help='Dry run, show what would be done.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create-only', dest='create_only', choices=NODE_TYPES,
                        help='Create nodes of the given type and do nothing further.')
    group.add_argument('--compatibility-layer', dest='compat',
                        action='store_const', const=True, help='Build compatibility layer.')
    group.add_argument('--software-layer', dest='software',
                        action='store_const', const=True, help='Build software layer.')
    group.add_argument('--full-stack', dest='stack',
                        action='store_const', const=True, help='Build both layers.')
    group.add_argument('--status', dest='status',
                        action='store_const', const=True, help='Show current status')
    group.add_argument('--destroy', dest='destroy',
                        action='store_const', const=True, help='Destroy infrastructure.')
    args = parser.parse_args()

    if not required_environment_keys_are_set(['AWS_SECRET_ACCESS_KEY', 'AWS_ACCESS_KEY_ID']):
        parser.print_help()
        sys.exit(1)


    i = Infrastructure(mode, args.architectures)




    if args.create_only:
        if args.dryrun:
            print('Would create:')
            i.plan_infrastructure()
        else:
            i.apply_infrastructure()
        print(i)
    elif args.compat:
        print('compat not implemented')
        mode = 'build'
    elif args.software:
        print('software not implemented')
        mode = 'build'
    elif args.stack:
        print('stack not implemented')
        mode = 'build'
    elif args.status:
        print(i)
    elif args.destroy:
        if args.dryrun:
            sys.exit(0)
        destroy_infrastructure()
    else:
        parser.print_usage()

#    i = Infrastructure()
#    i.plan_infrastructure()
