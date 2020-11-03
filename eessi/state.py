"""
Classes for managing EESSI infrastructure
:author: Terje Kvernes (University of Oslo)
"""
import json

from eessi.tools import TERRAFORM_DIRECTORY

def state(nodes, filename=None):
    """
    Returns a dict of the current terraform state.
    """
    statefile = '{}/terraform.tfstate'.format(TERRAFORM_DIRECTORY)
    if filename:
        statefile = filename

    status_dict = {}

    try:
        with open(statefile, 'r') as file:
            status_dict = json.loads(file.read())

            # if we get nodes passed to us, populate the nodes with data from state.
            for node in nodes:
                arch = node.arch

                for resource in status_dict['resources']:
                    if resource['mode'] == 'managed':
                        if resource['name'] == 'infra-{}'.format(arch):
                            instance = resource['instances'][0]
                            attributes = instance['attributes']
                            node.public_dns = attributes['public_dns']
                            node.public_ipv4 = attributes['public_ip']
                            node.instance_type = attributes['instance_type']

                            if 'public_ipv6' in instance:
                                node.public_ipv6 = attributes['public_ipv6']
    except FileNotFoundError:
        pass

    return status_dict
