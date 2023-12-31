# shellcheck disable=SC1090

# history
HISTSIZE=10000
HISTFILESIZE=2000000
shopt -s histappend
HISTCONTROL=ignoreboth
HISTIGNORE='ls:ll:ls -alh:pwd:clear:history:d:..'
HISTTIMEFORMAT='%F %T '
shopt -s cmdhist

# aliases
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# pager
export PAGER=moar
export MOAR="-no-linenumbers -no-statusbar -style onedark"

# editor
export EDITOR=nvim

# npm
export NPM_PACKAGES="${HOME}/.npm-packages"

# PATH
export PATH="$PATH:$HOME/bin:$HOME/.local/bin:$NPM_PACKAGES/bin"
