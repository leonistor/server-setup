# server setup scripts

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
- install tools from binary releases to `/usr/local/bin`
    - [lf file manager](https://github.com/gokcehan/lf)
    - [moar pager](https://github.com/walles/moar)
    - [astrovim](https://astronvim.com/Recipes/unattended_install)
    - [fd find](https://github.com/sharkdp/fd)
    - [rip grep](https://github.com/BurntSushi/ripgrep)
-add `admin` user
    - bashrc
    - create `.local/bin`
    - configure npm without sudo


---

## TODO

- [ ] setup services (e.g. cronie)
- [ ] add admin to cronie
- [ ] tools: https://github.com/dalance/procs
- [ ] tools: https://github.com/ogham/dog

## tricks used

- [lastversion: find the latest release version of an arbitrary project](https://github.com/dvershinin/lastversion)
- consider using a good bash lib, like [scripts-common](https://gitlab.com/bertrand-benoit/scripts-common)
- consider python instead of bash (real IaC!): [pytinfra](https://docs.pyinfra.com/en/2.x/index.html)

## TIPS

- bash set debug: `bash -x script.sh`
- pip quiet mode, assume yes: `pip install --quiet -q lastversion`, `pip uninstall --yes --quiet -q lastversion`

### clear linux

list explicitly installed bundles:

```sh
sudo swupd bundle-list --status | grep "explicitly installed" \
    | cut -c2- | cut -d" " -f2 \
    | xargs -I{} -P1 echo {} | sort
```

### debian

- good howtos: [server-world.info](https://www.server-world.info/en/)

### uu(en/de)code

The uuencode command uses the syntax: `uuencode original_filename final_filename > encoded_filename`

Replace original_filename with the name of your binary file. Replace final_filename with the name that you want the file to have when it is eventually decoded (usually the same as original_filename). Replace encoded_filename with the name you want to give the uuencoded version of the binary as it will appear in your directory.

usage in project:

- encode: `uuencode -m -o bashrc.encoded bashrc bashrc`
- decode to console: `uudecode -o /dev/stdout bashrc.encoded`