# Linux Development Environment

Defines my personal development environment for Linux.

It's an Ansible repository, so I'm going to try and use it for any Linux distribution I'm interested in. This can be controlled using the `when` condition with the `ansible_distribution` variable. For Windows I have a [separate repo](https://github.com/jacderida/devbox-windows), but ideally I'd be able to run this playbook in some kind of Bash emulation environment like [MSYS2](http://www.msys2.org/) or [the Windows Subsystem for Linux](https://msdn.microsoft.com/en-gb/commandline/wsl/about) in Windows 10. I want those environments to be as close as possible to my native Linux dev environment. Getting it to work in MSYS2 would be an interesting project for later. After having done some projects at work across both Linux and Windows, I'm very interested in a cross platform setup, and have achieved it to some extent, but there's still work to do.

Anything provisioned here is done so from public sources like Github. Anything private, such as SSH keys, AWS keys and so on, need to be provisioned as a separate step. For that reason, it may be necessary to run the dotfiles bootstrap again, after those private aspects have been defined.

## Development and Testing

Vagrant can be used for development and testing (and also if you just want to get a development machine running on a host). The Vagrantfile attempts to accomodate quite a few configurations, so a Makefile is used to make this easier.

Running `make ubuntu` or `make debian` will bring the box online then run the tests against it. The tests are defined using [Testinfra](https://testinfra.readthedocs.io/en/latest/). I've chosen this because in the past I had limited success with Serverspec, and I generally prefer Python to Ruby. The Makefile is quite straight forward, so it can be inspected for other tasks to run.

One thing that takes an extremely long time is cloning the nerdfonts repository; it's 2.5GB in size. If this is needed, it can be cloned on the host once, then mounted in as a shared folder. This is controlled using the `DEVBOX_NERDFONTS_SHARED_FOLDER` environment variable. Set this to the value of the folder on the host and run Vagrant like so:
```shell
export DEVBOX_NERDFONTS_SHARED_FOLDER=/home/jacderida/dev/nerd-fonts
make ubuntu
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

## Running with a GUI

To start up the environment with a GUI, run the following command:
```shell
make ubuntu-gui
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

Unfortunately, even if the guest additions are installed in advance, you'll sometimes see that `xrandr` only makes a few resolutions available. If this is the case, the guest additions need to be installed again. From the Virtualbox GUI, select the Devices menu, then choose the 'Insert Guest Additions CD image...' option. After that, open a terminal and run the following:
``` shell
sudo su -
mkdir /media/vbox-guest-additions
mount -r /dev/cdrom /media/vbox-guest-additions
cd /media/vbox-guest-additions
./VBoxLinuxAdditions.run
```

After this, restart the VM and run `xrandr` again.

## Corporate Mode

At work I can be involved in projects for large organisations who make use of proxies and custom self-signed SSL certificates. It can be especially complicated if the enterprise is running a proxy that requires Windows authentication (which most do). I'm calling this 'Corporate Mode'. To get `devbox` up and running in Corporate Mode, follow these steps:

* For authenticating with a Windows proxy, get an installation of CNTLM (its standard location is on sourceforge, which is often blocked - in that case get a copy of it and host it somewhere you can get access from within the network). You need to install this on your host OS; builds are available for both Windows and Linux. After you install this and have it running, the CNTLM proxy is available to the host at `http://localhost:3128`. If you want to use something other than `3128`, change the CNTLM configuration.
* With CNTLM running, set the `VAGRANT_HTTP_PROXY`, `VAGRANT_HTTPS_PROXY` and `NO_PROXY` environment variables in the host shell to `http://10.0.2.2:3128`. The IP address used there is the standard address Vagrant assigns to the host. This enables the guest VM to contact CNTLM running on the host.
* In the Vagrant install on the host, put any corporate self-signed SSL certificates in Vagrant's certificate database. On Windows, this is located at `C:\HashiCorp\vagrant\embedded\cacert.pem` and on a Linux system it's located at `/opt/vagrant/embedded/cacert.pem`. Just place it at the end of the file after the last one. It should be in Base-64 encoded X.509 format. If you need to obtain a copy of it, it can often be exported from Internet Explorer. (In 'Internet Options' it's under the 'Content' tab.)
* Install the `vagrant-proxyconf` plugin on the host using `vagrant plugin install vagrant-proxyconf` (if you get SSL errors you need to install the corporate SSL certificate in Vagrant's database).
* Drop the exported certificate in the same directory as the Vagrantfile and rename it to corp.crt.
* Run the `make X-corporate` targets, where X is the distro you're interested in, e.g. `make debian-gui-up-corporate`. If you want to run this from Windows, you'll need to install [MSYS2](https://www.msys2.org/) on the host and then install `make` with `pacman -S make`. You'll then need to put `c:\msys64\usr\bin` on `PATH` to make this available from `cmd.exe`.

Some Corporate Mode things worth being aware of:

* Git is built from source using an OpenSSL library rather than the standard GNUTLS library. For some reason, in some corporate environments, certain versions of Git have trouble cloning HTTPS based repositories. Replacing the GNUTLS library seems to solve the problem. This unfortunately adds an additional 10 minutes onto the build time.
* A file is located at `~/.proxy` that sets the standard proxy variables, and this is sourced in the `.zshrc` and `.bashrc`, so internet access should be available from terminal sessions.
* For Emacs, the proxy details need to be added to the `~/.emacs` file. See [here](https://stackoverflow.com/questions/1595418/emacs-behind-http-proxy). The environment section has more details on setting up Emacs.

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
* [i3-gaps](https://github.com/Airblader/i3) for the desktop environment with [Rofi](https://github.com/DaveDavenport/rofi/) as an application launcher
* [Terminator](https://gnometerminator.blogspot.co.uk/p/introduction.html) configured with [Roboto Mono](https://fonts.google.com/specimen/Roboto+Mono) at 12pt
* ZSH with Oh My Zsh and the [powerlevel9k theme](https://github.com/bhilburn/powerlevel9k)
* A whole bunch of packages installed (see the packages role; if I listed them here I'd need to keep 2 lists up-to-date)
* My [dotfiles](https://github.com/jacderida/dotfiles) repository bootstrapped with all files symlinked to the correct place
* All fonts from the [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) repository downloaded and installed (there are a couple of GB of them so this takes a long time)
* Vim 8 compiled from source with YouCompleteMe and other plugins installed
* Emacs 25 installed
* Docker version 17.09 (latest stable version at the time of writing)
* Vagrant version 2.0 with plugins installed
* Virtualbox version 5.2.6 (only in 'bare metal' mode)
* A 'screen temperature' application (only in 'bare metal' mode)
* Chrome installed

If the run was successful, it should all be ready to use.

The `setup.sh` file will install pip, Ansible and the things required to build that (even though Ansible is Python, it uses some C-based libraries). The `packages` role will install any of the prerequisite packages for anything else to build. Vim 8 still isn't available in most package managers at the moment, and the way I found to install it on Debian was using [this method](https://www.tecmint.com/vim-8-0-install-in-ubuntu-linux-systems/), which builds it from source. Other than the prerequisite packages, this solution should work across any distribution.

### Emacs

Emacs doesn't run straight out the box; there are a few minor steps to get it running:

* Copy the configuration file from dotfiles to `~/.emacs`. (It doesn't seem to work as a symlink; not sure why.)
* If in corporate mode, edit `~.emacs` to add the proxy details. See [here](https://stackoverflow.com/questions/1595418/emacs-behind-http-proxy) for details. *Imporant note:* when specifying the proxy host (usually `10.0.2.2` if CNTLM is running on the host), just use the IP address, *don't* specify the `http` protocol.
* Start Emacs and you'll get an error about the diminish package. Install the `diminish` package by running `M-x package-install RET diminish`.
* Restart Emacs and the `use-package` package should install all the packages specified in `~/.emacs`.

If you're running Emacs on a Windows host, the steps are pretty much identical to this.

### i3

My configuration for i3 uses the Windows Key as the modifier and h, j, k and l for the directions when switching between Windows. If running devbox on a Windows host, Windows Key + l is bound to lock the Windows host, so it will lock the entire machine any time you want to move right. You can disable this on the Windows host by editing the registry. Under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System`, create a new DWORD value named `DisableLockWorkstation` and set it to `1`. It takes effect immediately, without a restart.
