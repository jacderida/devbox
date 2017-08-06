# devbox
Defines my personal development environment in Ansible.

Anything provisioned here is done so from public sources like Github. Anything private, such as SSH keys, AWS keys and so on, need to be provisioned as a separate step. For that reason, it may be necessary to run the dotfiles bootstrap again, after those private aspects have been defined.

## Development and Testing

Vagrant can be used for development and testing. There's a Vagrantfile configured to run the Ansible localhost provisioner and apply the playbook. Just run `vagrant up` in the directory.

Certain tasks are long running. For a quicker testing workflow, they can be disabled:
```
ANSIBLE_ARGS='--skip-tags=slow' vagrant up
```

For testing large changes, for example, a completely new configuration for Vim, the best thing to do is create a branch in the dotfiles repository, then instruct our provision to use that branch. Since various files are symlinked from the dotfiles repository, it's better to clone a copy of it, create a branch, then make changes in that copy and push them to the branch. To run the provision, use this:
```
ANSIBLE_ARGS='-e "dotfiles_branch=<branch-name>"' vagrant up
```

## Provision a Bare Metal Environment

Before the playbook can be applied, the user who will be applying it must have passwordless sudo access, and Ansible must also be setup.

To setup passwordless sudo on Debian, see the 2nd answer [here](http://serverfault.com/questions/160581/how-to-setup-passwordless-sudo-on-linux).

To install Ansible, run the setup.sh file as sudo.

Then, to run the playbook locally, run the following command:
```
ansible-playbook -i inventory playbook.yml --extra-vars "dev_user=$(whoami)"
```
