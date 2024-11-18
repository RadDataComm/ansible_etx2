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
module: etx2_list_parser
author: Ruth Algor
version_added: 1.0.0
short_description: Transltests arbitrary commands table output on ETX2 device to list or dictionary 
description:
  - Transltests arbitrary commands table output on ETX2 device to list
    or dictionary
options:
  intput_table:
    required: True
    type: string
  method_choice:
    - list
    - list_no_header
    - list_of_dict
'''

EXAMPLES = """
- name: Pretty Port Configuration
  ansible.legacy.etx2_list_parser:
    input_table:
      Port           Number         Name            Admin    Oper      Speed
      -----------------------------------------------------------------------------
      Ethernet       0/3            ETH-0/3         Up       Down      1000000000
      Ethernet       0/4            ETH-0/4         Up       Down      1000000000
      Ethernet       0/5            ETH-0/5         Up       Down      1000000000
      Ethernet       0/6            ETH-0/6         Up       Down      1000000000
      Ethernet       0/101          MNG-ETH         Up       Up        100000000
      Ethernet       1/1            ETH-1/1         Up       Down      1000000000
      Ethernet       1/2            ETH-1/2         Up       Down      1000000000
      SVI            1              SVI 1           Up       Up        0
  method_choice: list_of_dict

"""

RETURN = """
stdout:
  description: The set of responses from the commands
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: ['...', '...']
stdout_l---
- name: "Local play"
  hosts: all
  gather_facts: no

  vars:
    ansible_user: su
    ansible_password: 1234
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: ansible.legacy.rad

  tasks:

    - name: "Execute show configure port summary"
      ansible.legacy.etx2_command:
        commands:
        - show configure port summary
      register: port_summary
      
    - name: "Pretty Print output of Port Summary DICT"
      ansible.legacy.etx2_list_parser:
        input_table: "{{ port_summary.stdout }}"
        method_choice: list_of_dict
      register: pretty_dict

#    - name: "Pretty List printing DICT"
#      ansible.builtin.debug:
#        #var: pretty_list.result
#        var: pretty_dict
ines:
  description: The value of stdout split into a list
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: [['...', '...'], ['...'], ['...']]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_lines
#from ansible.utils.display import Display
import logging
import json  # For pretty printing the data structure
import sys
import ast
import os
import os.path

"""
# The Display class from Ansible is used to print warnings to the standard output, which can be useful for user feedback
# Initialize display
display = Display()
"""
module_name = os.path.splitext(os.path.basename(__file__))[0]  # Get the filename without extension
log_file = os.path.expanduser('/tmp/rad_ansible_' + module_name + '.log')
#log_file = os.path.expanduser('/tmp/rad_ansible_etx2_list_parser.log')
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(module_name)

@staticmethod
def parse_table(table_str=None, add_new_line_before=True):
    """
    :param table_str: table string to be parsed
    :param add_new_line_before: if True-adds a new line before the first line
    :return: A list of non-empty lines or an empty list if the input is empty.
    """
    if not table_str:
        return [] # returns an empty list when input is empty
    lines = []
    if isinstance(table_str, list):
        print("The input is a list.")
        for line in table_str: # Split the string into line
            line = line.strip(); # Remove leading/trailing whitespace
            if line: # Check if the line is not empty
                line = line.replace('|', ' '); # Replace '|' with a space
                lines.append(line)
    elif isinstance(table_str, str):
        print("The input is a string.")
        # Additional processing for string
        # Split the string into lines and filter out empty lines
        for line in table_str.splitlines(): # Split the string into line
            line = line.strip(); # Remove leading/trailing whitespace
            if line: # Check if the line is not empty
                line = line.replace('|', ' '); # Replace '|' with a space
                lines.append(line)
    else:
        lines = ["NAME TYPE","-------------------------------------------","Oiy Vaavoi"]

    logger.error("Python logging parse_table the result structure: %s", json.dumps(lines, indent=2))
    print("Python logging parse_table the result structure: {lines}", file=sys.stderr)
#   lines = [11,12,13,14,15,16,17,18,19,20,200,2000]
#   logger.error("Python logging parse_table the result structure: %s", json.dumps(lines, indent=2))
#   print("Python logging parse_table the result structure: {lines}")
    # Check if the line is not emptyleaned_lines_list = [line.strip().replace('\n', '') for line in lines]
    if lines and add_new_line_before:
        lines[0] = '\n' + lines[0].strip()
    lines = [item.strip() for item in lines] # Remove spaces before/after each entry
    return lines

@staticmethod
def parse_table_without_headers(table_str=None, header_rows_num=0, header_delimiter=False, add_new_line_before=True):
    """
    :param table_str: string. table string to be parsed
    :param header_rows_num: int. number of rows in header
    :param header_delimiter: boolean. True if delimiter (non-empty) exists
    :param add_new_line_before: if True-adds a new line before the first line
    :return: A list of non-empty lines or an empty list if the input is empty.
    """
    if not table_str:
      return [] # returns an empty list when input is empty
    # Split the string into lines and filter out empty lines
    lines = parse_table(table_str, False)
    if not lines:
        return []
    header_lines = header_rows_num if not header_delimiter else (header_rows_num + 1)
    # Remove the first kder_lines elements (sub-line that starts from header_lines index)
    new_lines = lines[header_lines:]
    if new_lines and add_new_line_before:
        new_lines[0] = '\n' + new_lines[0]

    logger.debug("Python logging parse_table_without_header the result structure: %s", json.dumps(lines, indent=2))
    return new_lines

@staticmethod
def create_dict_for_table_row(names, values):
    """
    :param names: A list of strings (names in the dictionary)
    :param values: A list of values (values in the dictionary). It assumes that values cannot contain spaces
    :return A disctionary built from names and values
    """
    # Create a dictionary with names as keys and values from the list, defaulting to None for missing values
    ret_dict = {}
    if ( names and values ):
        logger.error("Python create_dict_for_table_row names: %s", names);
        #print(f"names in create_dict_for_table_row {names}")

        length = min(len(names), len(values))
        diff_len = 0;
        name_index = -1;
        if len(values) > len(names): # We assume that if there' a name named 'Name' it will contain the additional values
            name_index = index = names.index('Name')
            len_diff = len(values) - len(names)
            if name_index > 0:
                # Put under Name all additional values the come after its index
                for i in range(name_index + 1, name_index + len_diff + 1):
                    values[name_index] = values[name_index] + " " + values[i]
                # put all values after 'Name'
                for i in range(name_index + 1, len(names)):
                    values[i] = values[i + len_diff]
                # Remove redundant values
                for i in range(len(names), len(values)):
                    values.pop()
        for i in range(0, length):
            ret_dict[names[i]] = values[i]
    ret_dict = {key.strip(): value.strip() for key, value in ret_dict.items()}
    return ret_dict

@staticmethod
def create_dict(names, values):
    """
    :param names: A list of strings (names in the dictionary)
    :param values: A list of values (values in the dictionary)
    :return A disctionary built from names and values
    """
    # Create a dictionary with names as keys and values from the list, defaulting to None for missing values
    return {name: values[i] if i < len(values) else None for i, name in enumerate(names)}

@staticmethod
def table_to_list_of_dict(table_str=None, header_rows_num=0, header_delimiter=False):
    """
    :param table_str: string. table string to be parsed
    :param header_rows_num: int. number of rows in header
    :param header_delimiter: boolean. True if delimiter (non-empty) exists
    :return: A list of dictionaries, with names taken from header and values from the rest of the table
    """
    if not table_str:
        return [] # returns an empty list when input is empty
    # Split the string into lines and filter out empty lines
    dict_lines = parse_table(table_str, False)
    header_and_delimiter_len = header_rows_num + 1 if header_delimiter else header_rows_num
    ret_dict = {}
    ret_list = []
    if dict_lines and (len(dict_lines) <= header_and_delimiter_len):
        return ret_list
    header = "";
    for i in range(header_rows_num):
        header = header + " " + dict_lines[i]
    # Split the header by spaces and filter out any empty strings
    header_names_list = [name for name in header.split() if name]
    start_index = header_and_delimiter_len
    for i in range(start_index, len(dict_lines)):
        line_vals_list = [val for val in dict_lines[i].split()]
#       print(line_vals_list)
        ret_list.append(create_dict_for_table_row(header_names_list, line_vals_list));

    logger.debug("Python logging table_to_list_of_dict the result structure: %s", json.dumps(ret_list, indent=2))
    return ret_list

@staticmethod
def list_of_dict_to_str(list_of_dict=None):
    if not list_of_dict:
        return ""
    # Convert the list of dictionaries to a JSON string
    return json.dumps(list_of_dict, indent=4, sort_keys=False)

@staticmethod
def print_list_elem_per_line(list_to_print=None):
    """
    :param list_to_print: List of elements to print (each element in a separate line)
    """
    for item in list_to_print:
        print(item)


def main():
    module = AnsibleModule(argument_spec={
      'input_table': {'type': 'str', 'required': True},
      'method_choice': {'type': 'str', 'choices': ['list', 'list_no_header', 'list_of_dict', 'list_of_dict_unsorted_str'], 'required': True},
    })

    """
    # Retrieve the log path from Ansible configuration
    log_path = os.path.expanduser("/tmp/rad_ansible_etx2_list_parser.log")

    # Set up logging
    logging.basicConfig(filename=log_path, level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    """


    input_table = module.params['input_table']
    method_choice = module.params['method_choice']

    print(f"Not main {__name__}")
    if method_choice == 'list':
        my_result = parse_table(input_table, False)
        print(f"result = {my_result}")
        #my_result = input_table.splitlines()
        #my_result = [item.strip() for item in my_result]
        module.exit_json(changed=False, result=my_result)
    elif method_choice == 'list_no_header':
        my_result = parse_table_without_headers(input_table, 1, True, False)
        #my_result = [item.strip() for item in my_result]
    elif method_choice == 'list_of_dict':
        my_result = table_to_list_of_dict(input_table, 1, True)
        # Log the entire data structure as JSON
        logger.debug("Python logging the result structure: %s", json.dumps(my_result, indent=2))
        print(f"Python logging the result structure: {my_result}")
    elif method_choice == 'list_of_dict_unsorted_str':
        my_result = list_of_dict_to_str(table_to_list_of_dict(input_table, 1, True))

    module.exit_json(changed=False, result=my_result)

if __name__ == '__main__':
    main()
else:
    print(f"Not main {__name__}")
