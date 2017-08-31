# Linux Development Environment

Defines my personal development environment for Linux.

It's an Ansible repository, so I'm going to try and use it for any Linux distribution I'm interested in. This can be controlled using the `when` condition with the `ansible_distribution` variable. For Windows I have a [separate repo](https://github.com/jacderida/devbox-windows), but ideally I'd be able to run this playbook in some kind of Bash emulation environment like [MSYS2](http://www.msys2.org/) or [the Windows Subsystem for Linux](https://msdn.microsoft.com/en-gb/commandline/wsl/about) in Windows 10. I want those environments to be as close as possible to my native Linux dev environment. Getting it to work in MSYS2 would be an interesting project for later. After having done some projects at work across both Linux and Windows, I'm very interested in a cross platform setup, and have achieved it to some extent, but there's still work to do.

Anything provisioned here is done so from public sources like Github. Anything private, such as SSH keys, AWS keys and so on, need to be provisioned as a separate step. For that reason, it may be necessary to run the dotfiles bootstrap again, after those private aspects have been defined.

## Development and Testing

Vagrant can be used for development and testing. There's a Vagrantfile configured to run the Ansible localhost provisioner and apply the playbook. Just run `vagrant up` in the directory.

Certain tasks are long running. For a quicker testing workflow, they can be disabled:
```
ANSIBLE_ARGS='--skip-tags=slow' vagrant up
```

For testing large changes, e.g. a completely new configuration for Vim, the best thing to do is create a branch in the dotfiles repository, then instruct the provision to use that branch. Since various files are symlinked from the dotfiles repository on my dev machine, it's better to clone a new copy of it, create a branch, then make changes in that copy and push them to the branch. To run the provision, use this:
```
ANSIBLE_ARGS='-e "dotfiles_branch=<branch-name>"' vagrant up
```
### Guidelines

Here are set of general development guidelines, for my own reference:
* Any new roles should be developed on a branch and tested using the guidelines below, before being merged to master; this ensures the master branch is always runnable for provisioning a new or existing machine.
* Make good use of the `ansible_distribution` variable in the `when` condition to ensure the repository will remain cross platform.
* If this variable isn't being used, the role should be truly cross platform.

Before merging a branch back into master, ideally the following tests would be performed:
* Perform a full `vagrant up` to make sure everything works OK when provisioning from scratch.
* Perform a `vagrant provision` to make sure everything works OK when the box has already had at least one provision.
* Perform a full `vagrant up` with the new role not applied, then apply it and run a `vagrant provision` and make sure everything runs ok.
* Do both tests on the Ubuntu box as well as the default Debian box.

### Running Tests

There are some tests defined using [Testinfra](https://testinfra.readthedocs.io/en/latest/). I've chosen this because in the past I had limited success with Serverspec, and I generally prefer Python to Ruby. For running the tests:
```shell
mkvirtualenv env # Obviously assumes a virtualenvwrapper installation.
pip install testinfra
vagrant ssh-config ubuntu > .vagrant/ubuntu-ssh-config
vagrant ssh-config debian > .vagrant/debian-ssh-config
testinfra -v tests.py --ssh-config=.vagrant/ubuntu-ssh-config --host=ubuntu
testinfra -v tests.py --ssh-config=.vagrant/debian-ssh-config --host=debian
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

If the run was successful, it should all be ready to use.

The `setup.sh` file will install pip, Ansible and the things required to build that (even though Ansible is Python, it uses some C-based libraries). The `packages` role will install any of the prerequisite packages for anything else to build. Vim 8 still isn't available in most package managers at the moment, and the way I found to install it on Debian was using [this method](https://www.tecmint.com/vim-8-0-install-in-ubuntu-linux-systems/), which builds it from source. Other than the prerequisite packages, this solution should work across any distribution.
