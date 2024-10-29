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
# Contains Ansible cliconf plugin methods for RAD network devices
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
author: Muly Ilan, Ruth Algor
name: rad (or ansible.legacy.rad)
short_description: Use rad cliconf to run command/s on RAD Data Communications platforms
description:
  - This plugin provides low level abstraction APIs for
    sending and receiving CLI commands from RAD Data Communications network devices.
'''

import re
import json

from ansible.module_utils._text import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible.plugins.cliconf import CliconfBase
from ansible.errors import AnsibleConnectionFailure


class Cliconf(CliconfBase):

    __rpc__ = ['get_config', 'edit_config', 'get_capabilities', 'get']

    def get_device_info(self):
        device_info = {}

        device_info['network_os'] = 'rad'
        reply = self.get('show configure system device-information')
        data = to_text(reply, errors='surrogate_or_strict').strip()

        match = re.search(r'Description\s+: (\S+)', data)
        if match:
            device_info['network_os_model'] = match.group(1)

        match = re.search(r'Sw: (\S+)', data)
        if match:
            device_info['network_os_version'] = match.group(1)

        match = re.search(r'Name:\s+: (.*)', data)
        if match:
            device_info['network_os_hostname'] = match.group(1).strip()

        return device_info

    def get_config(self, source='running', flags=None):
        if source == 'running':
            cmd = 'info'
        elif source == 'startup':
            cmd = 'show file startup-config'
        else:
            raise ValueError("fetching configuration from %s is not supported" % source)        

        flags = [] if flags is None else flags
        cmd += ' '.join(flags)
        cmd = cmd.strip()

        return self.send_command(cmd)

    def edit_config(self, command):
        resp = {}
        results = []
        requests = []
        self.send_command('exit all')
        for cmd in to_list(command):
            if isinstance(cmd, dict):
                command = cmd['command']
                prompt = cmd['prompt']
                answer = cmd['answer']
                newline = cmd.get('newline', True)
            else:
                command = cmd
                prompt = None
                answer = None
                newline = True

            if not cmd.startswith('#'):
                results.append(self.send_command(command, prompt, answer, False, newline))
                requests.append(cmd)

        resp['request'] = requests
        resp['response'] = results
        return resp

    def get(self, command, prompt=None, answer=None, sendonly=False, newline=True, check_all=False):
        return self.send_command(command=command, prompt=prompt, answer=answer, sendonly=sendonly, newline=newline, check_all=check_all)

    def get_capabilities(self):
        result = super(Cliconf, self).get_capabilities()
        result['rpc'] += ['run_commands']
        return json.dumps(result)

    def run_commands(self, commands=None, check_rc=True):
        if commands is None:
            raise ValueError("'commands' value is required")

        responses = list()
        for cmd in to_list(commands):
            try:
                out = self.send_command(command=cmd, prompt=r"Are you sure\s*\?{1,2} \[yes/no\] _\s+", answer='y', sendonly=False, newline=True)
            except AnsibleConnectionFailure as e:
                if check_rc:
                    raise
                out = getattr(e, "err", e)

            out = to_text(out, errors="surrogate_or_strict").strip()
            responses.append(out)

        return responses
