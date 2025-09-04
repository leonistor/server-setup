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

## install utils
# apt install -y kitty-terminfo zip

## install packages
apt install -y curl gnupg wget htop acl build-essential autoconf automake \
    gdb git libssl-dev libffi-dev zlib1g-dev \
    sqlite3 sqlite3-tools \
    python3-pip python3-venv python3-dev

# vim
update-alternatives --install /usr/bin/editor editor /usr/bin/vim 100

# sudo
apt install sudo -y
echo "leo    ALL=(ALL:ALL) ALL" >/etc/sudoers.d/leo
echo "Defaults timestamp_timeout = -1" >/etc/sudoers.d/timeout

## leo
adduser leo
echo "Passwd for leo:"
passwd leo
usermod -aG sudo leo

# files
wget -O /tmp/dist.zip ""
tar xzf /tmp/dist.zip
chmod -R + r /tmp/dist
echo "use dist files:"
ls -lah /tmp/dist
