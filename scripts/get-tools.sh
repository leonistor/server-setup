#!/usr/bin/env bash

# download latest versions of tools

echo "moar"
lastversion --assets --filter "linux-386" \
    --output ../tools/moar download walles/moar

echo "fd"
lastversion --assets --filter "x86_64-unknown-linux-gnu" \
    --output fd.tar.gz download sharkdp/fd
mkdir fd-current
tar -xf fd.tar.gz -C fd-current --strip-components=1
mv ./fd-current/fd ../tools/fd
rm -rf fd-current fd.tar.gz

echo "rg"
lastversion --assets --filter "i686-unknown-linux-gnu.tar.gz" \
    download BurntSushi/ripgrep
rm ./*.sha256
mkdir rg-current
tar -xf ripgrep* -C rg-current --strip-components=1
mv ./rg-current/rg ../tools/rg
rm -rf rg-current ripgrep*.tar.gz

echo "lf"
lastversion --assets --filter "linux-amd64" \
    --output lf.tar.gz download gokcehan/lf
tar xf lf.tar.gz
chmod +x lf
mv lf ../tools/lf
rm lf.tar.gz

# TODO: ttyd: https://github.com/tsl0922/ttyd/releases
