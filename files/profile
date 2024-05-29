me=${BASH_SOURCE[0]//\//_}; me=${me//./_}; if [[ ${SOURCED[${me}]} == "yes" ]]; then return; else declare -A SOURCED; SOURCED[${me}]=yes; fi # Only load once

if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi
