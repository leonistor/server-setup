#!/usr/bin/env bash

set -e

! {
    mv ~/.config/nvim ~/.config/nvim.bak || true
    mv ~/.local/share/nvim ~/.local/share/nvim.bak || true
    mv ~/.local/state/nvim ~/.local/state/nvim.bak || true
    mv ~/.cache/nvim ~/.cache/nvim.bak || true
}
