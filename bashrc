# history
HISTSIZE=10000
HISTFILESIZE=2000000
shopt -s histappend
HISTCONTROL=ignoreboth
HISTIGNORE='ls:ll:ls -alh:pwd:clear:history:d:..'
HISTTIMEFORMAT='%F %T '
shopt -s cmdhist
# aliases
alias d='ls -lAh --group-directories-first'
alias ..='cd ..'
# make and change to directory
mcd() { mkdir -p "$1" && cd "$1" || exit; }
# pager
export PAGER=moar
export MOAR="-no-linenumbers -no-statusbar -style onedark"
# npm
export NPM_PACKAGES="${HOME}/.npm-packages"

export PATH="$PATH:$HOME/bin:$HOME/.local/bin:$NPM_PACKAGES/bin"
