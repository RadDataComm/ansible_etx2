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
# Contains utility methods for ETX-2 network devices
#
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

#import json

#from ansible.module_utils._text import to_text
#from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list

@staticmethod
def parse_table(table_str=None, add_new_line_before=True):
    """
    :param table_str: table string to be parsed
    :param add_new_line_before: if True-adds a new line before the first line
    :return: A list of non-empty lines or an empty list if the input is empty.
    """
    if not table_str:
      return [] # returns an empty list when input is empty
    # Split the string into lines and filter out empty lines
    lines = [line for line in table_str.splitlines() if line.strip()]
    if lines and add_new_line_before:
        lines[0] = '\n' + lines[0]
  
    print(f"Number of lines = {len(lines)}")
    print(f"Output list: {lines}")
    cleaned_lines_list = [line.strip().replace('\n', '') for line in lines]

    stam = 'Port           Number         Name            Admin    Oper      Speed       \\n\\n-----------------------------------------------------------------------------\\n\\nEthernet       0/3            ETH-0/3         Up       Down      1000000000  \\n\\nEthernet       0/4            ETH-0/4         Up       Down      1000000000  \\n\\nEthernet       0/5            ETH-0/5         Up       Down      1000000000  \\n\\nEthernet       0/6            ETH-0/6         Up       Down      1000000000  \\n\\nEthernet       0/101          MNG-ETH         Up       Up        100000000   \\n\\nEthernet       1/1            ETH-1/1         Up       Down      1000000000  \\n\\nEthernet       1/2            ETH-1/2         Up       Down      1000000000  \\n\\nSVI            1              SVI 1           Up       Up        0'
    stam_lines = stam.split('\\n')
    print(f"stam_lines: {stam_lines}")

    print(f"Output cleaned_lines_list: {cleaned_lines_list}")
    return cleaned_lines_list

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
    lines = [line for line in table_str.splitlines() if line.strip()]
    header_lines = header_rows_num if not header_delimiter else (header_rows_num + 1)
    # Remove the first kder_lines elements (sub-line that starts from header_lines index)
    new_lines = lines[header_lines:]
    if new_lines and add_new_line_before:
        new_lines[0] = '\n' + new_lines[0]
  
    print(f"parse_table_without_headers: Number of lines = {len(lines)}")
    print(f"parse_table_without_headers: Output list: {lines}")
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
    if ( names and values):
        length = min(len(names), len(values))
        diff_len = 0;
        name_index = -1;
        if len(values) > len(names): # We assume that if there' a name named 'Name' it will contain the additional values
            name_index = index = names.index('Name')
            len_diff = len(values) - len(names)
            if name_index > 0:
                for i in range(name_index + 1, name_index + len_diff + 1):
                    values[name_index] = values[name_index] + " " + values[i]
                for i in range(name_index + 1, len(names)):
                    values[i] = values[i + len_diff]
                for i in range(len(names), len(values)):
                    values.pop()
        for i in range(0, length):
            ret_dict[names[i]] = values[i]
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
    lines = parse_table(table_str, False)
    ret_dict = {}
    ret_list = []
    if lines and ((len(lines) <= header_rows_num) or (header_delimiter and (len(lines) <= (header_rows_num + 1)))):
        return ret_list
    header = "";
    for i in range(header_rows_num):
        header = header + " " + lines[i]
    # Split the header by spaces and filter out any empty strings
    header_names_list = [name for name in header.split() if name]
    start_index = header_rows_num + 1 if header_delimiter else header_rows_num
    for i in range(start_index, len(lines)):
        line_vals_list = [val for val in lines[i].split()]
#       print(line_vals_list)
        ret_list.append(create_dict_for_table_row(header_names_list, line_vals_list));

    print(f"parse_table_without_headers: Number of lines = {len(lines)}")
    print(f"parse_table_without_headers: Output list: {lines}")
    return ret_list

@staticmethod
def print_list_elem_per_line(list_to_print=None):
    """
    :param list_to_print: List of elements to print (each element in a separate line)
    """
    for item in list_to_print:
#       print(item)
        print(f"{item}, ")

def main():
#   argument_spec = dict(
#       commands=dict(type="list", required=True, elements="raw")
#   )
    ports_table = """Port           Number         Name            Admin    Oper      Speed
-----------------------------------------------------------------------------
Ethernet       0/3            ETH-0/3         Up       Down      1000000000
Ethernet       0/4            ETH-0/4         Up       Down      1000000000
Ethernet       0/5            ETH-0/5         Up       Down      1000000000
Ethernet       0/6            ETH-0/6         Up       Down      1000000000
Ethernet       0/101          MNG-ETH         Up       Up        100000000
Ethernet       1/1            ETH-1/1         Up       Down      1000000000
Ethernet       1/2            ETH-1/2         Up       Down      1000000000
SVI            1              SVI 1           Up       Up        0"""

    print("\n--------------------- Ports-List without header -----------------------\n")
    ports_list = parse_table_without_headers(ports_table, 1, True, True);
    print(f"Ports list after parse_table_without_headers: {ports_list}")
    print_list_elem_per_line(ports_list)
    print("\n---------------------- Ports-List with header --------------------------\n")
    ports_list = parse_table(ports_table, False)
    print(f"Ports list after parse_table: {ports_list}")
    print_list_elem_per_line(ports_list)
    print("\n---------------------- Ports Dictionaries List --------------------------\n")
    ports_dict_list = table_to_list_of_dict(ports_table, 1, True)
    print(f"Ports list after table_to_list_of_dict: {ports_dict_list}")
    print_list_elem_per_line(ports_dict_list)
    print("\n----------------------------------------------------------------------\n")


if __name__ == '__main__':
    main()

