# fzf
if check_command fzf; then
    if check_command fd; then
        export FZF_DEFAULT_COMMAND='fd --type f --hidden --exclude .git --exclude node_modules'
        export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
    fi

    export FZF_DEFAULT_OPTS="
      --height 45%
      --layout=reverse
      --border
      --info=inline
      --color=dark
      --color=fg:-1,bg:-1,hl:#c678dd,fg+:#ffffff,bg+:#4b5263,hl+:#c678dd
      --color=info:#98c379,prompt:#61afef,pointer:#be5046,marker:#e5c07b,header:#61afef
    "

    source <(fzf --zsh)

    bindkey -r '^T'
    bindkey '\ef' fzf-file-widget
    bindkey '\ec' fzf-cd-widget
    bindkey '\eh' fzf-history-widget
fi

# OpenSSH's systemd user socket
if [[ -n "$XDG_RUNTIME_DIR" && -S "$XDG_RUNTIME_DIR/ssh-agent.socket" ]]; then
    export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"
fi

# fuck
check_command thefuck && eval "$(thefuck --alias)"

# zoxide
check_command zoxide && eval "$(zoxide init --cmd cd zsh)"

# pyenv
if [[ -d "$HOME/.pyenv" ]]; then
    export PYENV_ROOT="$HOME/.pyenv"
    [[ -d "$PYENV_ROOT/bin" ]] && export PATH="$PYENV_ROOT/bin:$PATH"

    eval "$(pyenv init - zsh)"
fi

# bun
[[ -s "$HOME/.bun/_bun" ]] && source "$HOME/.bun/_bun"
[[ -d "$HOME/.bun/bin" ]] && export PATH="$PATH:$HOME/.bun/bin"
