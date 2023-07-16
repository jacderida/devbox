# Linux Development Environment

Defines my personal development environment for Linux.

I'm updating this in February 2023 for running on the Dell XPS13.

## Arch Linux Installation

This section describes how to run the Arch installation on hardware, as opposed to a VM. Even though the [official installation guide](https://wiki.archlinux.org/title/installation_guide) is good, the intention here is to be a bit more succinct and also document the additional packages to install, which of course Arch isn't prescriptive about.

Creating a bootable USB install is covered in the guide above. This documentation will commence from being booted in the live environment.

### Connect to the Network

Run the following commands to set the keyboard layout, and if you don't have a wired connection, connect to my current wireless network and set the system clock.

```
loadkeys uk
# If we don't have a wired connection
iwctl station wlan0 scan
iwctl station wlan0 get-networks
iwctl station wlan0 connect TALKTALK616BF3
timedatectl set-ntp true
```

You can optionally verify you have a connection to the network by running `ip address show` and check the clock was set correctly by running `date`.

### Configure Disks

Make 3 partitions: one for EFI, one for swap and one for root. It's quite possible that the EFI partition will already exist. If you have any other partitions from previous OS installs, delete them.

```
fdisk /dev/nvme0n1

# use 'd' to delete any partitions except the EFI system partition.
# use 'n' to add 1GB swap partition, using '+1G' for the size.
# use 'n' to add a new partition to consume the rest of the disk.
# use 'w' to write the changes.
```

Create file systems on the newly created partitions. One will be for swap and the other will be ext4.

```
mkswap /dev/nvme0n1p2
swapon /dev/nvme0n1p2
mkfs.ext4 /dev/nvme0n1p3
```

Mount the EFI and root file systems.

```
mount /dev/nvme0n1p3 /mnt
mkdir /mnt/efi
mount /dev/nvme0n1p1 /mnt/efi
```

### Install Linux and Base Packages

Use `pacstrap` to setup the Linux Kernel and other essential packages.

```
pacstrap -K /mnt \
    base \              # minimal base: awk, bash, glibc, grep, pacman, systemd etc.
    base-devel \        # required for using AUR
    dhcpcd \            # For accessing a wired network via DHCP
    git \
    grub \              # required for setting up boot menu
    efibootmgr \        # also required for use with grub
    intel-ucode \       # microcode for intel processors
    linux \             # the kernel package
    linux-firmware \    # for wireless networking drivers etc.
    iw \                # wireless networking configuration
    iwd \               # wireless networking configuration
    man-db \
    man-pages \
    sudo \
    texinfo \           # required for man pages
    vim \
```

Before proceeding with change root, generate an fstab file.

```
genfstab -U /mnt >> /mnt/etc/fstab
```

### Configure New System

Change to the new system and pull and run a script that does some basic configuration and sets up grub.

```
arch-chroot /mnt
curl -O https://raw.githubusercontent.com/jacderida/devbox/arch/config-new-system.sh
chmod +x config-new-system.sh
./config-new-system.sh
```

The XPS13 has screen flickering with Arch. The suggested workaround is to [set a kernel parameter](https://wiki.archlinux.org/title/Intel_graphics#Screen_flickering):
```
vim /etc/default/grub
# Change GRUB_CMDLINE_LINUX_DEFAULT as below:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash i915.enable_psr=0"
# Then quit Vim and regenerate grub.cfg:
sudo grub-mkconfig -o /efi/grub/grub.cfg
```

Finally, set the root password by running `passwd`, then `exit` the chroot, remove the bootable USB and run `reboot`.

## Post Installation

This section describes post-installation configuration tasks.

### General

Create a user account and give it root privileges:
```
useradd -m chris
passwd chris
EDITOR=vim visudo
chris ALL=(ALL) ALL # add at the bottom of the file
```
Now logout of the root account by using `exit` and login with the new account.

Setup `yay` for use with the AUR:
```
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

Install `ghq` with `yay -S ghq`.

Now clone my dotfiles:
```
export GHQ_ROOT=~/dev
mkdir ~/dev
ghq get https://github.com/jacderida/dotfiles.git
```

Install `stow` and link the dotfiles:
```
cd ~/dev/github.com/jacderida/dotfiles
sudo pacman -S stow
make links
```

### Networking

Before starting the networking services, enable DHCP for wireless networking by putting the following in `/etc/iwd/main.conf`:
```
[General]
EnableNetworkConfiguration=true
```

Now start and enable the networking services:
```
systemctl enable systemd-networkd --now
systemctl enable systemd-resolved --now
systemctl enable iwd --now
```

To connect to the wireless network, you can now follow the same instructions for the live environment.

### Graphics and Graphical Environment

Use Wayland and [Sway](https://github.com/swaywm/sway) to get an i3 environment.

Install the following packages to facilitate this:
```
sudo pacman -S \
    otf-font-awesome \
    sway \
    swayidle \
    ttf-roboto-mono-nerd \
    waybar \
    wayland \
    wofi \
    xorg-server-xwayland \
    xorg-xkbcomp
```

Add your user account to the `seat` group:
```
sudo gpasswd -a chris seat
```

Now reboot.

### Apps/Tools

Now all that remains is the configurations of apps.

#### Rust

A lot of apps and tools are installed using `cargo`, which requires a Rust installation:
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

For using `cargo` with Fish, create a file with this content at `~/.cargo/env2`:
```
set -x PATH ~/.cargo/bin/ $PATH
```

#### Install

First, install Just: `cargo install just`.

Then install all apps/tools by running `just install`
