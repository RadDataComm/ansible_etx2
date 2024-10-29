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
# Contains Ansible terminal plugin methods for RAD network devices
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

from ansible.errors import AnsibleConnectionFailure
from ansible.plugins.terminal import TerminalBase


class TerminalModule(TerminalBase):

    terminal_stdout_re = [
        re.compile(br"[\r\n]?[\S ]+(?:[$#]) ?$")
    ]

    terminal_stderr_re = [
        re.compile(br"cli error: "),
        re.compile(br"\*\*\*\*\*Could not ")
    ]

    def on_open_shell(self):
        try:
            self._exec_cli_command(u'configure terminal length 0')
        except AnsibleConnectionFailure:
            raise AnsibleConnectionFailure('unable to set terminal parameters')
