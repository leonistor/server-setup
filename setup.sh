#!/usr/bin/env bash
# run as root: setup system

# no check for "appears unused"
# shellcheck disable=SC2317

# don't exit on errors
set -e
# the temp dir
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT
# error trap
function traperr() {
    echo "ERROR: at about ${BASH_LINENO[0]}"
    rm -rf "$TMP_DIR"
}
set -o errtrace
trap traperr ERR

# constants
readonly LINUX_DEBIAN="debian"
readonly LINUX_CLEARLINUX="clear-linux-os"

# log activity to console
log() {
    echo "INFO: $1"
}

# --- tasks functions

check_for_root_user() {
    log "Checking for root user"
    if [[ $EUID -ne 0 ]]; then
        echo "ERROR: this script must be run as root" 1>&2
        exit 1
    fi
}

get_distro() {
    if [ -f /etc/os-release ]; then
        # shellcheck disable=SC1091
        source /etc/os-release
        echo "$ID"
    fi
}

check_distro() {
    local DISTRO
    DISTRO=$(get_distro)

    case "$DISTRO" in
    "$LINUX_DEBIAN" | "$LINUX_CLEARLINUX")
        return
        ;;
    *)
        echo "ERROR: only for debian or clear-linux"
        exit 1
        ;;
    esac
}

configure_updates() {
    log "configure updates"
    DISTRO=$(get_distro)

    if [[ $DISTRO == "$LINUX_CLEARLINUX" ]]; then
        # automatic service restart after updates
        clr-service-restart allow NetworkManager.service dbus.service
        clr-service-restart allow docker.service cronie.service containerd.service
    fi
    if [[ $DISTRO == "$LINUX_DEBIAN" ]]; then
        # unattended upgrades
        apt-get install unattended-upgrades apt-listchanges apt-config-auto-update
        APTCONFIG="/etc/apt/apt.conf.d/50unattended-upgrades"
        # shellcheck disable=SC2016
        LINES_UNCOMMENT=(
            '//      "origin=Debian,codename=${distro_codename}-updates";'
        )

        # uncomment lines, using | separator here
        sed -i "29,104,107s|//||" "$APTCONFIG"
        # toggle true
        sed -i "111,115,119s/false/true/" "$APTCONFIG"
        # update daily
        UPGRADECONF="/etc/apt/apt.conf.d/20auto-upgrade"
        touch "$UPGRADECONF"
        echo 'APT::Periodic::Update-Package-Lists "1";' >>"$UPGRADECONF"
        echo 'APT::Periodic::Unattended-Upgrade "1";' >>"$UPGRADECONF"
    fi
}

sudoers_timeout() {
    log "sudoers timeout"
    SUDOERS_FILE="/etc/sudoers.d/timeout"
    if [ ! -f "$SUDOERS_FILE" ]; then
        echo "Defaults timestamp_timeout = -1" >"$SUDOERS_FILE"
    fi

}

install_packages() {
    log "install packages"
    DISTRO=$(get_distro)

    # clear-linux
    if [[ $DISTRO == "$LINUX_CLEARLINUX" ]]; then
        # add bundles
        BUNDLES="containers-basic
            cronie
            dev-utils
            dev-utils-dev
            docker-compose
            editors
            fuse
            go-basic
            kernel-native
            machine-learning-basic
            neovim
            network-basic
            NetworkManager
            openssh-server
            os-clr-on-clr
            os-core-update
            package-utils
            perl-basic
            python3-basic
            sysadmin-basic
            sysadmin-remote
            telemetrics
            tzdata
            user-basic"
        for BUNDLE in $BUNDLES; do
            bundle-add "$BUNDLE"
        done
    fi
    # debian
    if [[ $DISTRO == "$LINUX_DEBIAN" ]]; then
        # quiet
        export DEBIAN_FRONTEND=noninteractive
        # essentials
        apt install -y -qq sudo neovim kitty-terminfo
        # utils
        apt install -y -qq curl gnupg wget htop
        # dev
        apt install -y -qq build-essential
        apt install -y -qq autoconf automake gdb git
        apt install -y -qq libssl-dev libffi-dev zlib1g-dev
        # python
        apt install -y -qq python3-pip python3-venv python3-dev
        # node
        apt install -y -qq nodejs
    fi
}

root_bash_settings() {
    log "root bash settings"
    mkdir -p /root/.terminfo/x
    wget "https://github.com/kovidgoyal/kitty/raw/master/terminfo/x/xterm-kitty" \
        -q -O /root/.terminfo/x/xterm-kitty

    DISTRO=$(get_distro)
    if [[ $DISTRO == "$LINUX_CLEARLINUX" ]]; then
        if [ ! -f "/root/.profile" ]; then
            cp profile /root/.profile
        fi
        cp bashrc /root/.bashrc
        cp bash_aliases /root/.bash_aliases
    fi
}

# --- tools

prepare_tools_install() {
    log "prepare tools install"
    pip install --quiet -q lastversion
    mkdir -p /usr/local/bin
}

install_lf() {
    log "tool: lf"
    cd "$TMP_DIR"
    lastversion --assets --filter "linux-amd64" \
        --output lf.tar.gz download gokcehan/lf 1>/dev/null
    tar xf lf.tar.gz
    chmod +x lf
    mv lf /usr/local/bin/
    mkdir -p /etc/lf
    echo "set hidden true" >/etc/lf/lfrc
}

install_moar() {
    log "tool: moar pager"
    cd "$TMP_DIR"
    lastversion --assets --filter "linux-386" \
        --output moar.tmp download walles/moar 1>/dev/null
    chmod +x moar.tmp
    mv moar.tmp /usr/local/bin/moar
}

install_astrovim() {
    log "tool: astrovim"
    mkdir -p ~/.config
    git clone --quiet --depth 1 https://github.com/AstroNvim/AstroNvim ~/.config/nvim
    nvim --headless +q
}

install_fd() {
    log "tool: fd find"
    cd "$TMP_DIR"
    lastversion --assets --filter "x86_64-unknown-linux-gnu" \
        --output fd.tar.gz download sharkdp/fd 1>/dev/null
    mkdir fd-current
    tar -xf fd.tar.gz -C fd-current --strip-components=1
    mv ./fd-current/fd /usr/local/bin/fd
}

install_ripgrep() {
    log "tool: ripgrep"
    cd "$TMP_DIR"
    # using https://blog.markvincze.com/download-artifacts-from-a-latest-github-release-in-sh-and-powershell/
    LATEST_RELEASE=$(curl -L -s -H 'Accept: application/json' https://github.com/BurntSushi/ripgrep/releases/latest)
    LATEST_VERSION=$(echo "$LATEST_RELEASE" | sed -e 's/.*"tag_name":"\([^"]*\)".*/\1/')
    wget "https://github.com/BurntSushi/ripgrep/releases/download/${LATEST_VERSION}/ripgrep_${LATEST_VERSION}_amd64.deb" \
        -q -O rg.deb
    mkdir rg-current
    ar x rg.deb ./data.tar.xz
    tar xf data.tar.xz --strip-components=1 -C rg-current
    mv ./rg-current/bin/rg /usr/local/bin/rg
}
# --- admin user

create_admin() {
    log "creating admin user"
    useradd -m admin
    echo "admin:testing123" | chpasswd
}

configure_admin() {
    log "configure admin user"

    # debian: usermod -aG sudo
    # kitty only on clear-linux
    # kitty-term
    su - admin <<EOF
        mkdir -p ~/.terminfo/x
        wget "https://github.com/kovidgoyal/kitty/raw/master/terminfo/x/xterm-kitty" \
            -q -O ~/.terminfo/x/xterm-kitty
EOF
    # bash shell
    cp profile /home/admin/.profile
    chown admin:admin /home/admin/.profile
    cp bashrc /home/admin/.bashrc
    chown admin:admin /home/admin/.bashrc
    cp bash_aliases /home/admin/.bash_aliases
    chown admin:admin /home/admin/.bash_aliases
    mkdir -p ~/.local/bin
    # astrovim
    su - admin <<EOF
        mkdir -p ~/.config
        git clone --quiet --depth 1 https://github.com/AstroNvim/AstroNvim ~/.config/nvim
        nvim --headless +q
EOF
    # npm
    su - admin <<EOF
        mkdir -p ~/.npm-packages
        touch ~/.npmrc
        echo "prefix=/home/admin/.npm-packages" >~/.npmrc
EOF

}

# --- main script

main() {
    check_distro

    install_packages
    # configure_updates
    # sudoers_timeout

    # root_bash_settings

    # prepare_tools_install
    # install_lf
    # install_moar
    # install_astrovim
    # install_fd
    # install_ripgrep

    # create_admin
    # configure_admin
    log "DONE!"
}

check_for_root_user
main "$@"
