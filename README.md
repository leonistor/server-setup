# infra setup using pyinfra

**Activate venv!**

`source ./venv/bin/activate.fish`

invoke deploys:

- fish shell: `set -x PYTHONPATH "."; pyinfra inventory/test.py debian.setup_bash -v`

invoke tests:

- `pytest -v --hosts='ssh://192.168.64.2' test/test_connection.py`

---

# TODO

For system status:

```sh

# hardware info
sudo lshw -short -class processor,memory,display,storage,disk

# disks
lsblk --output NAME,FSTYPE,FSAVAIL,FSUSE%,MOUNTPOINTS

# network
ip -brief addr show

```

Path: TODO.md

---

# old README

utility script to configure a new server, Debian or Clear Linux, with `admin` user.

- configure sudo, sshd
- configure updates
- kitty terminfo
- bashrc for root
- packages
  - system: cronie, devtools
  - platform: node, docker, python
- setup services
- prepare tools install
  - install `lastversion` from pip
  - check/mkdir `/usr/local/bin`
- install tools from binary releases to `/usr/local/bin` - [lf file manager](https://github.com/gokcehan/lf) - [moar pager](https://github.com/walles/moar) - [astrovim](https://astronvim.com/Recipes/unattended_install) - [fd find](https://github.com/sharkdp/fd) - [rip grep](https://github.com/BurntSushi/ripgrep) - [ttyd](https://github.com/tsl0922/ttyd)
  -add `admin` user - bashrc - create `.local/bin` - configure npm without sudo

---

## ideas

- setup services (e.g. cronie)
- add admin to cronie
- tools: https://github.com/dalance/procs
- tools: https://github.com/ogham/dog
- debian auto update: Allow installing updates from all origins (see tutorial below)

## tricks used

- [lastversion: find the latest release version of an arbitrary project](https://github.com/dvershinin/lastversion)
- consider using a good bash lib, like [scripts-common](https://gitlab.com/bertrand-benoit/scripts-common)
- consider python instead of bash (real IaC!): [pytinfra](https://docs.pyinfra.com/en/2.x/index.html)

## TIPS

- bash set debug: `bash -x script.sh`
- pip quiet mode, assume yes: `pip install --quiet -q lastversion`, `pip uninstall --yes --quiet -q lastversion`
- [files mode](https://ss64.com/bash/chmod.html)

### clear linux

list explicitly installed bundles:

```sh
sudo swupd bundle-list --status | grep "explicitly installed" \
    | cut -c2- | cut -d" " -f2 \
    | xargs -I{} -P1 echo {} | sort
```

package sources: https://github.com/orgs/clearlinux-pkgs/repositories?type=all

### debian

- good howtos: [server-world.info](https://www.server-world.info/en/)
- [unattended upgrades guide](https://techlabs.blog/categories/debian-linux/automatically-install-updates-using-unattended-upgrades-on-debian-11)
- [laptop prevent suspend](https://gitlab.com/-/snippets/2515869)
- vim default editor: `sudo update-alternatives --install /usr/bin/editor editor /usr/bin/vim 100`
- add sudo: root: `apt install -y sudo`; `echo "leo    ALL=(ALL:ALL) ALL" > /etc/sudoers.d/leo`
- sudo timeout: `echo "Defaults timestamp_timeout = -1" > /etc/sudoers.d/timeout`

### ubuntu

- [Keep Ubuntu 22.04 Servers Updated](https://www.digitalocean.com/community/tutorials/how-to-keep-ubuntu-22-04-servers-updated)
- [Livepatch Service](https://ubuntu.com/security/livepatch) free for 5 machines

### arch

- use `archinstall`
- must have: `base base-devel grub linux linux-firmware openssh`
- packages: `htop zip unzip wget ntp python python-pip openssh net-tools man-db man-pages grub kitty-terminfo`
- pacman config: uncomment in `/etc/pacman.conf`: `Color` and `ParallelDownloads = 5`
- cron [auto updates](https://linuxman.co/linux-desktop/keeping-arch-linux-shiny-with-automatic-updates-using-systemd/)

### uu(en/de)code

The uuencode command uses the syntax: `uuencode original_filename final_filename > encoded_filename`

Replace original_filename with the name of your binary file. Replace final_filename with the name that you want the file to have when it is eventually decoded (usually the same as original_filename). Replace encoded_filename with the name you want to give the uuencoded version of the binary as it will appear in your directory.

usage in project:

- encode: `uuencode -m -o bashrc.encoded bashrc bashrc`
- decode to console: `uudecode -o /dev/stdout bashrc.encoded`
