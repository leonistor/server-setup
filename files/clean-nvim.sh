#!/usr/bin/env bash
# clean any previous versions of nvim

mv ~/.config/nvim ~/.config/nvim.bak &>/dev/null
mv ~/.local/share/nvim ~/.local/share/nvim.bak &>/dev/null
mv ~/.local/state/nvim ~/.local/state/nvim.bak &>/dev/null
mv ~/.cache/nvim ~/.cache/nvim.bak &>/dev/null
