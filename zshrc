# Powerlevel10k
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export PATH=$PATH:$HOME/bins:/usr/local/bin:/home/letder/.local/share/gem/ruby/3.0.0/bin:$HOME/.local/bin:$HOME/.cargo/bin
export ZSH="$HOME/.oh-my-zsh" # ohmyzsh installation

ZSH_THEME="powerlevel10k/powerlevel10k"

plugins=(
	git
	zsh-syntax-highlighting
    bun
)

source $ZSH/oh-my-zsh.sh

# User configuration
export MANPATH="/usr/local/man:$MANPATH"
export EDITOR="nvim"
export LANG=es_ES.UTF-8

# Compilation flags
export ARCHFLAGS="-arch x86_64"

### IME ###
#

#### LS ####
alias ls='eza --icons --color=always --group-directories-first'
alias ll='eza -lM@O --color=always --git --icons --group-directories-first --time-style long-iso'
alias lla='eza -lM@Oa --color=always --git --icons --group-directories-first --time-style long-iso'
alias la='eza -a --icons --color=always -g --group-directories-first'
alias l.='eza -a | egrep "^\."'
###########

### ALIAS ###

# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias pdf="zathura"
alias dev="cd ~/workspace/dev/"
alias notes="cd ~/workspace/notes/"
alias find="fd"
alias ip="ip -c"
alias icat="kitten icat"
alias cat="bat"
alias off="shutdown now"
alias vpn="sudo openvpn --config /etc/openvpn/client/nl-free-140090.protonvpn.udp.ovpn"
alias neofetch="fastfetch"
alias spt="spotify_player"
alias zathura-dark="zathura -c ~/.config/zathura/zathura-darkrc"
alias board="/opt/Lorien_v0.6.0_Linux/Lorien.x86_64"
alias vi="nvim"
alias vim="nvim"
############

### FUNCTIONS ###
man() {
  /usr/bin/man $* | \
    col -b | \
    nvim -R -c 'set ft=man nomod nolist' -
}

target() {
    echo " 󰓾  Target IP | $1 |" > /home/letder/.local/share/qtile/target_widget
}

mode() {
    case "$1" in
        1)  echo "paddr" > /home/letder/.local/share/qtile/mode; echo "[#] public address mode";;
        2)  echo "target" > /home/letder/.local/share/qtile/mode; echo "[#] target mode";;
        *)  echo "invalid mode"; return 1;;
    esac
}

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

export FZF_DEFAULT_OPTS='--color=fg:#f8f8f2,hl:#bd93f9 --color=fg+:#f8f8f2,bg+:#44475a,hl+:#bd93f9 --color=info:#ffb86c,prompt:#50fa7b,pointer:#50fa7b --color=marker:#ff79c6,spinner:#ffb86c,header:#6272a4'
source <(fzf --zsh)

bindkey -v

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
