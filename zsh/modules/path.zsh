typeset -gU path PATH

path_append() {
    [[ -d "$1" ]] && path+=("$1")
}

path_append "$HOME/bins"
path_append "/usr/local/bin"
path_append "$HOME/.local/bin"


[[ -f "$HOME/.cargo/env" ]] && source "$HOME/.cargo/env"
