#!/usr/bin/env bash

# download latest versions of tools

echo "get: moar"
lastversion --assets --filter "linux-386" \
    --output ../tools/moar download walles/moar

echo "get: fd"
lastversion --assets --filter "x86_64-unknown-linux-gnu" \
    --output fd.tar.gz download sharkdp/fd
mkdir fd-current
tar -xf fd.tar.gz -C fd-current --strip-components=1
mv ./fd-current/fd ../tools/fd
rm -rf fd-current fd.tar.gz

echo "rg"
lastversion --assets --filter "amd64.deb" \
    download BurntSushi/ripgrep
rm ./*.sha256
mv ./ripgrep*amd64.deb ../tools/

echo "get: lf"
lastversion --assets --filter "linux-amd64" \
    --output lf.tar.gz download gokcehan/lf
tar xf lf.tar.gz
chmod +x lf
mv lf ../tools/lf
rm lf.tar.gz

echo "get: ttyd"
lastversion --assets --filter "x86_64" \
    --output ttyd download tsl0922/ttyd
mv ttyd.x86_64 ttyd
chmod +x ttyd
mv ttyd ../tools/ttyd

echo "get: kitty-terminal"
wget "https://github.com/kovidgoyal/kitty/raw/master/terminfo/x/xterm-kitty" \
    -q -O ../files/xterm-kitty
