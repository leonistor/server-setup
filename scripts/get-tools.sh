#!/usr/bin/env bash

# download latest versions of tools

echo "get: moar"
lastversion --assets --filter "linux-386" \
    --output ../tools/moar download walles/moar

echo "get: lf"
lastversion --assets --filter "linux-amd64" \
    --output lf.tar.gz download gokcehan/lf
tar xf lf.tar.gz
chmod +x lf
mv lf ../tools/lf
rm lf.tar.gz

echo "get: kitty-terminfo"
wget "https://github.com/kovidgoyal/kitty/raw/master/terminfo/x/xterm-kitty" \
    -q -O ../files/xterm-kitty
