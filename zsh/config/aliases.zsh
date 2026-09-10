alias_if_command() {
    local definition="$1"
    local name="${definition%%=*}"
    local target="${definition#*=}"
    local command="${target%% *}"

    check_command "$command" && alias "$definition"
}

alias_if_command "zathura-dark=zathura -c ~/.config/zathura/zathura-darkrc"
alias_if_command pdf=zathura
alias_if_command cat=bat
alias_if_command neofetch=fastfetch
alias_if_command spt=spotify_player
alias_if_command vi=nvim
alias_if_command vim=nvim
alias_if_command "icat=kitten icat"

alias_if_command "ls=eza --icons --color=always --group-directories-first"
alias_if_command "ll=eza -lM@O --color=always --git --icons --group-directories-first --time-style long-iso"
alias_if_command "lla=eza -lM@Oa --color=always --git --icons --group-directories-first --time-style long-iso"
alias_if_command "la=eza -a --icons --color=always -g --group-directories-first"
alias_if_command 'l.=eza -a | egrep "^\."'

alias ip="ip -c"
alias off="shutdown now"
