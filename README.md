# devbox
Defines my personal development environment in Ansible. I'm going to try and use this same repo for any Linux distribution I'm interested in. This can be controlled using the `when` condition with the `ansible_distribution` variable.

Anything provisioned here is done so from public sources like Github. Anything private, such as SSH keys, AWS keys and so on, need to be provisioned as a separate step. For that reason, it may be necessary to run the dotfiles bootstrap again, after those private aspects have been defined.

## Development and Testing

Vagrant can be used for development and testing. There's a Vagrantfile configured to run the Ansible localhost provisioner and apply the playbook. Just run `vagrant up` in the directory.

Certain tasks are long running. For a quicker testing workflow, they can be disabled:
```
ANSIBLE_ARGS='--skip-tags=slow' vagrant up
```

For testing large changes, for example, a completely new configuration for Vim, the best thing to do is create a branch in the dotfiles repository, then instruct the provision to use that branch. Since various files are symlinked from the dotfiles repository on my dev machine, it's better to clone a new copy of it, create a branch, then make changes in that copy and push them to the branch. To run the provision, use this:
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

## The Environment

After applying the playbook, there should be an environment with the following:
* A whole bunch of packages installed (see the packages role; if I listed them here I'd need to keep 2 lists up-to-date)
* My [dotfiles](https://github.com/jacderida/dotfiles) repository bootstrapped with all files symlinked to the correct place
* All fonts from the [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) repository downloaded and installed (there are a couple of GB of them so this takes a long time)
* Vim 8 compiled from source with YouCompleteMe and other plugins installed
* Chrome installed

If the run was successful, it should all be ready to use. Vim 8 still isn't available in most package managers at the moment, and the official way I found to install it on Debian was using [this method](https://www.tecmint.com/vim-8-0-install-in-ubuntu-linux-systems/), to build it from source. Other than the prerequisite packages, this solution should work across any distribution.
