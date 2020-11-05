"""
Classes for managing EESSI infrastructure
:author: Terje Kvernes (University of Oslo)
"""

import os

from eessi.tools import is_acceptable_terraform_command, ensure_terraform_is_initialized
from eessi.tools import ARCHITECTURES, TERRAFORM_DIRECTORY, TF_ENV_PREFIX
from eessi.tools import execute, destroy_infrastructure, ROOT_DIRECTORY
from eessi.tools import is_acceptable_architecture, is_acceptable_node_type
from eessi.state import state

class Infrastructure:
    """
    Manage the infrastructure.
    """
    def __init__(self, mode='test', architectures=None):
        self.nodes = []
        self.mode = mode

        if not architectures:
            architectures = ARCHITECTURES

        for arch in architectures:
            self.add_node(mode, arch)

        self.update_state()

    def __str__(self):
        """
        Stringify object.
        """
        if self.state:
            print(self.state)
            string = "Mode: {}".format(self.mode)
            for node in self.nodes:
                if node.public_dns:
                    string = "{}\n {}: {}".format(string, node.arch, node.public_dns)
                else:
                    string = "{}\n {} (not applied)".format(string, node.arch)

            return string

        return "Mode: {}\n{}".format(self.mode,
                                     "\n ".join(str(n) for n in self.nodes))

    def update_state(self):
        """
        Updates object state based on terraform state.
        """
        self.state = state(self.nodes)

    def add_node(self, nodetype, arch):
        """
        Add a node of a given type and arch.
        """
        self.nodes.append(Node(nodetype, arch))

    def plan_infrastructure(self):
        """
        Performs a 'terraform plan' on the current infrastructure.
        """
        self.terraform('plan')

    def apply_infrastructure(self):
        """
        Performs a 'terraform apply' on the current infrastructure.
        """
        self.terraform('apply')

    def destroy_infrastructure(self):
        """
        Performs a terraform destroy.
        """
        self.terraform('destroy')

    def terraform(self, command):
        """
        Executes an appropriate terraform command based on the current infrastructure.
        """
        command = command.lower()
        if not is_acceptable_terraform_command(command):
            raise InfrastructureError("Unknown terraform command '{}'!".format(command))

        if command == 'destroy':
            return destroy_infrastructure()

        # TF_VAR_create_{aarch64,x86_64,power}=true 
        # TF_VAR_mode={test,build}

        os.chdir(TERRAFORM_DIRECTORY)

        ensure_terraform_is_initialized()

        for node in self.nodes:
            os.environ["{}_create_{}".format(TF_ENV_PREFIX, node.arch)] = 'true'

        os.environ["{}_mode".format(TF_ENV_PREFIX)] = self.mode

        if command == 'apply':
            print("Applying state, please wait...")
            execute(['terraform', command, '-auto-approve'], print_stdout=True)
            self.update_state()
        elif command == 'plan':
            print("Planning state, please wait...")
            execute(['terraform', command], print_stdout=True)
        else:
            raise InfrastructureError("Unexpected terraform command '{}'!".format(command))

        os.chdir(ROOT_DIRECTORY)


class Node:
    """
    An infrastructure node
    """
    def __init__(self, node_type, arch):
        if not is_acceptable_node_type(node_type):
            raise InfrastructureError("Unknown nodetype '{}' requested.".format(node_type))

        if not is_acceptable_architecture(arch):
            raise InfrastructureError("Unknown architecture '{}' requested.".format(arch))

        self.node_type = node_type
        self.arch = arch

        self.public_dns = None
        self.public_ipv4 = None
        self.public_ipv6 = None
        self.instance_type = None

    def __str__(self):
        """
        String representation of a node.
        """
        if self.public_dns:
            return "{}/{} ({})".format(self.node_type, self.arch, self.public_dns)
        else:
            return "{}/{}".format(self.node_type, self.arch)


class InfrastructureError(BaseException):
    """
    An generic exception class.
    """
