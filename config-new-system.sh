#!/usr/bin/env bash

set -e

ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime
hwclock --systohc
sed -i "s/#en_GB\.UTF-8 UTF-8/en_GB\.UTF-8 UTF-8/g" /etc/locale.gen
sed -i "s/#en_GB ISO-8859-1/en_GB ISO-8859-1/g" /etc/locale.gen
sed -i "s/#en_US\.UTF-8 UTF-8/en_US\.UTF-8 UTF-8/g" /etc/locale.gen
sed -i "s/#en_US ISO-8859-1/en_US ISO-8859-1/g" /etc/locale.gen
locale-gen

echo "LANG=en_GB.UTF8" > /etc/locale.conf
echo "KEYMAP=uk" > /etc/vconsole.conf
echo "devbox" > /etc/hostname
cat << EOF > /etc/hosts
127.0.0.1   localhost
::1         localhost
127.0.1.1   devbox.localdomain devbox
EOF

grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB
grub-mkconfig -o /efi/grub/grub.cfg
