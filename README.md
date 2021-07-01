# Linux Development Environment

Defines my personal development environment for Linux.

I decided I wanted to use Arch Linux to improve my understanding. I also decided I didn't want to bother using Ansible any more, as I didn't feel I was getting any significant benefit from it. I think my setup is simple enough to define just using Bash.

## Arch Linux Installation

This section describes how to run the Arch installation on hardware, as opposed to a VM. Even though the [official installation guide](https://wiki.archlinux.org/title/installation_guide) is good, the intention here is to be a bit more succinct and also document the additional packages to install, which of course Arch isn't prescriptive about.

Creating a bootable USB install is covered in the guide above. This documentation will commence from being booted in the live environment.

### Connect to the Network

Run the following commands to set the keyboard layout, connect to my current wireless network and set the system clock.

```
loadkeys uk
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
pacstrap /mnt \
    base \              # minimal base: awk, bash, glibc, grep, pacman, systemd etc.
    grub \              # required for setting up boot menu
    efibootmgr \        # also required for use with grub
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

Finally, set the root password by running `passwd`, then `exit` the chroot, remove the bootable USB and run `reboot`.

### Configure Networking

When the system reboots, the network needs to be configured.

Before starting the networking services, enable DHCP by putting the following in `/etc/iwd/main.conf`:
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

### Configure User Account

Create a user account for day-to-day use and give it root privileges.

```
useradd -m chris
passwd chris
EDITOR=vim visudo
chris ALL=(ALL) ALL # add at the bottom of the file
```
Now logout of the root account by using `exit` and login with the new account.
