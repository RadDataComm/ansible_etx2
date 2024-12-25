# RAD ETX-2 Collection

The Ansible RAD ETX-2 collection includes a variety of Ansible content to help automate the management of RAD ETX-2 network devices.

This collection has been tested against ETX-2 version 6.8.5(4.46)

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.17.0**

<!--end requires_ansible-->

### Supported connections

The RAD ETX-2 collection supports ``network_cli`` connections.

## Included content
<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[raddatacomm.etx2.rad](https://github.com/raddatacomm/ansible_etx2/blob/main/docs/raddatacomm.etx2.rad_cliconf.rst)|Use rad cliconf to run command/s on RAD Data Communications platforms

### Modules
Name | Description
--- | ---
[raddatacomm.etx2.etx2_command](https://github.com/raddatacomm/ansible_etx2/blob/main/docs/raddatacomm.etx2.etx2_command_module.rst)|Module to run commands on remote ETX-2 devices

<!--end collection content-->


## Installing this collection

You can install the RAD ETX-2 collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install raddatacomm.etx2

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: raddatacomm.etx2
```

### Using modules from the RAD ETX-2 collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `raddatacomm.etx2.etx2_command`.
The following example task makes changes in the existing configuration on an ETX-2 network device, using the FQCN:

```yaml
---
 - name: Basic Configuration
   raddatacomm.etx2.etx2_command:
     commands:
     - configure system location Stockholm
     - configure management dscp 4
   register: result


```

### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes

Release notes are available [here](https://github.com/raddatacomm/ansible_etx2/blob/main/CHANGELOG.rst).

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
