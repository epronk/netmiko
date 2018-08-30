"""
Subclass specific to Cisco ESA.

Written by Eddy Pronk <epronk@muftor.com>
"""

from __future__ import unicode_literals
import re
import time
from netmiko.cisco_base_connection import CiscoSSHConnection, CiscoFileTransfer


class CiscoEsaSSH(CiscoSSHConnection):
    """Subclass specific to Cisco ASA."""
    def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self.base_prompt = '>'
        self.clear_buffer()

    def find_prompt(self, delay_factor=1):

        self.clear_buffer()
        self.write_channel(self.RETURN)

        found = False
        while not found:
            prompt = self.read_channel()
            if self.ansi_escape_codes:
                prompt = self.strip_ansi_escape_codes(prompt)
                
            time.sleep(0.5)
            if prompt.endswith('> '):
                found = True

        # If multiple lines in the output take the last line
        prompt = self.normalize_linefeeds(prompt)
        prompt = prompt.split(self.RESPONSE_RETURN)[-1]
        prompt = prompt.strip()

        return prompt

    def send_command(self, *args, **kwargs):
        kwargs['auto_find_prompt'] = False
        output = super(CiscoSSHConnection, self).send_command(*args, **kwargs)
        return output
