# devbox
Defines my personal development environment in Ansible.

Anything provisioned here is done so from public sources like Github. Anything private, such as SSH keys, AWS keys and so on, need to be provisioned as a separate step. For that reason, it may be necessary to run the dotfiles bootstrap again, after those private aspects have been defined.

## Development and Testing

Vagrant can be used for development and testing. There's a Vagrantfile configured to run the Ansible localhost provisioner and apply the playbook. Just run `vagrant up` in the directory.

## Provision a Bare Metal Environment

Before the playbook can be applied, the user who will be applying it must have passwordless sudo access, and Ansible must also be setup.

To setup passwordless sudo on Debian, see the 2nd answer [here](http://serverfault.com/questions/160581/how-to-setup-passwordless-sudo-on-linux).

To install Ansible, run the setup.sh file as sudo.

Then, to run the playbook locally, run the following command:
```
ansible-playbook -i inventory playbook.yml --extra-vars "dev_user=$(whoami)"
```
