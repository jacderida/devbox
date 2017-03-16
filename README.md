# devbox
Defines my personal development environment in Ansible.

## Development and Testing

Vagrant can be used for development and testing. There is a Vagrantfile configured to run the Ansible localhost provisioner and apply playbook.yml. Just run `vagrant up` in the directory.

## Provision a Bare Metal Environment

Before the playbook can be applied, the user who will be applying it must have passwordless sudo access, and Ansible must also be setup.

To install Ansible, run the setup.sh file as sudo.

Then, to run the playbook locally, run the following command:
```
ansible-playbook -i "localhost" playbook.yml --extra-vars "dev_user=$(whoami)"
```
