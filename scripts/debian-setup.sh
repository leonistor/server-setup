#!/usr/bin/env bash

# setup steps after bare install of a debian 12 system
# run as root!

# install prereq:
# - user `leo` as admin
# - openssh service
# - ssh-copy-id by user `leo`

# update packages
apt update
apt dist-upgrade -y

# vim
update-alternatives --install /usr/bin/editor editor /usr/bin/vim 100

# sudo
apt install sudo -y
echo "leo    ALL=(ALL:ALL) ALL" >/etc/sudoers.d/leo
echo "Defaults timestamp_timeout = -1" >/etc/sudoers.d/timeout
