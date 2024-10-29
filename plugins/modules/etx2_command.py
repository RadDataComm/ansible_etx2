#!/usr/bin/python
#
# (c) 2024 RAD Data Communications LTD.
#
# This file is not part of Ansible
#
# GNU General Public License v3.0+
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# Module to execute commands on ETX-2 devices
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: etx2_command
author: Muly Ilan
version_added: 1.0.0
short_description: Run arbitrary commands on ETX-2 devices
description:
  - Sends arbitrary commands to an ETX-2 device and returns the results
    read from the device.
options:
  commands:
    description:
      - List of commands to send to the remote ETX-2 device.
        The resulting output from the command is returned.
    required: true
    type: list
'''

EXAMPLES = """
- name: Basic Configuration
  ansible.legacy.etx2_command:
    commands:
    - show configure system device-information
    - configure management dscp 4
  register: result

- name: Get output from single command
  ansible.legacy.etx2_command:
    commands: show configure system memory
  register: result
"""

RETURN = """
stdout:
  description: The set of responses from the commands
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: ['...', '...']
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: [['...', '...'], ['...'], ['...']]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_lines
from ansible_collections.rad.etx2.plugins.module_utils.network.etx2 import run_commands


def main():
    argument_spec = dict(
        commands=dict(type="list", required=True, elements="raw")
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    warnings = list()
    result = {'changed': False, 'warnings': warnings}

    commands = module.params['commands']

    responses = run_commands(module, commands)

    result.update({'stdout': responses, 'stdout_lines': list(to_lines(responses))})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
