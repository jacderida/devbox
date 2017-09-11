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

The machines in the Vagrantfile are setup to use the Ansible provisioner, which is, running Ansible on the host against the guest VMs. For this reason, Ansible obviously needs to be installed on the host machine. You can use the `setup.sh` file to install it.

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
source run_tests.sh
```
This script will activate a virtualenv if it doesn't exist (it uses virtualenvwrapper, so obviously that needs to be installed in the dev environment you're running in), brings the machines online with a `vagrant up`, then runs the tests against them. So that you can see new tests fail, it doesn't re-provision the machines; that should be done as an explicit 2nd step.

## Running with a GUI

To start up the environment with a GUI, run the following command:
```shell
DEVBOX_GUI='true' vagrant up
```

When the machine is completely provisioned, the GUI environment needs to be started from the VirtualBox UI. You can login to the debian box with 'vagrant' as both the username and password. The Ubuntu box unfortunately has a random password set. The password can be retrieved like so:
```shell
 cat ~/.vagrant.d/boxes/ubuntu-VAGRANTSLASH-xenial64/20170822.0.0/virtualbox/Vagrantfile
# Front load the includes
include_vagrantfile = File.expand_path("../include/_Vagrantfile", __FILE__)
load include_vagrantfile if File.exist?(include_vagrantfile)

Vagrant.configure("2") do |config|
  config.vm.base_mac = "022185D04910"
  config.ssh.username = "ubuntu"
  config.ssh.password = "27f8dbe40a2e195f6bd6434a"

  config.vm.provider "virtualbox" do |vb|
     vb.customize [ "modifyvm", :id, "--uart1", "0x3F8", "4" ]
     vb.customize [ "modifyvm", :id, "--uartmode1", "file", File.join(Dir.pwd, "ubuntu-xenial-16.04-cloudimg-console.log") ]
  end
end
```

I'm not sure if this location varies over time, but it should generally be located somewhere similar to that.

Once you're logged in to the VM via the VirtualBox GUI, the Linux GUI can be started with the following command:
```shell
sudo systemctl start lightdm
```

I'm using i3 as the window manager. You'll be able to select this from the login prompt. The machine should be running with 64MB of video RAM. The resolution can be changed with the following command:
```shell
xrandr --output VGA-1 --mode 1920x1080
```

## Provision a Bare Metal Environment

Before the playbook can be applied, the user who will be applying it must have passwordless sudo access, and Ansible must also be setup.

To setup passwordless sudo on Debian, see the 2nd answer [here](http://serverfault.com/questions/160581/how-to-setup-passwordless-sudo-on-linux).

To install Ansible, run the setup.sh file as sudo.

Then, to run the playbook locally, run the following command:
```shell
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
