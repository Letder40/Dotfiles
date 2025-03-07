# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bins:/usr/local/bin:/home/letder/.local/share/gem/ruby/3.0.0/bin:$HOME/.local/bin:$HOME/.cargo/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="powerlevel10k/powerlevel10k"
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# CASE_SENSITIVE="true"

# HYPHEN_INSENSITIVE="true"

# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# zstyle ':omz:update' frequency 13

# DISABLE_MAGIC_FUNCTIONS="true"

# DISABLE_LS_COLORS="true"

# DISABLE_AUTO_TITLE="true"

# ENABLE_CORRECTION="true"

# DISABLE_UNTRACKED_FILES_DIRTY="true"

# HIST_STAMPS="mm/dd/yyyy"

# ZSH_CUSTOM=/path/to/new-custom-folder

plugins=(
	git
	zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh

# User configuration

export MANPATH="/usr/local/man:$MANPATH"
export EDITOR="nvim"
export LANG=es_ES.UTF-8

# Compilation flags
# export ARCHFLAGS="-arch x86_64"
#

### IME ###
#

#### LS ####

LS_COLORS="di=1;34"
alias ls='exa --icons --color=always -g --group-directories-first'
alias ll='exa -lF --icons --color=always -g --group-directories-first'
alias la='exa -a --icons --color=always -g --group-directories-first'
alias l='exa -F --icons --color=always -g --group-directories-first'
alias l.='exa -a | egrep "^\."'
export EXA_COLORS="ur=36;01:uw=36;01:ux=36;01:ue=36:gr=35:gw=35:gx=35:tr=32;01:tw=32;01:tx=32;01:uu=32:un=31:sn=34:gu=32:gn=31:da=37"

###########

### ALIAS ###

# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias dev="cd ~/workspace/dev/"
alias notes="cd ~/workspace/notes/"
alias cesur="cd ~/workspace/cesur/"
alias hacking="cd ~/workspace/hacking"
alias 日本語="cd ~/workspace/lang/日本語"
alias shared="cd ~/workspace/virtualBox/share_fold"
alias win="cd ~/workspace/virtualBox/share_fold/win"
alias ubuntu="cd ~/workspace/virtualBox/share_fold/ubuntu-server"
alias ip="ip -c"
alias cat="bat"
alias off="shutdown now"
alias camen="sudo modprobe -r uvcvideo"
alias vpn="sudo openvpn --config /etc/openvpn/client/nl-free-140090.protonvpn.udp.ovpn"
alias neofetch="fastfetch"
alias spt="spotify_player"
alias zathura-dark="zathura -c ~/.config/zathura/zathura-darkrc"
alias lorien="/opt/Lorien_v0.6.0_Linux/Lorien.x86_64"
alias vi="nvim"
alias vim="nvim"

alias リブート="reboot"
alias シャットダウン="shutdown now"
alias オフ="shutdown now"
############

### FUNCTIONS ###
man() {
  /usr/bin/man $* | \
    col -b | \
    nvim -R -c 'set ft=man nomod nolist' -
}

dug() {
   disk_usage=$(du -h -d1 . 2>/dev/null | grep -E "^[0-9]+.[0-9]+G" | head -n-1)
   files=($(du -h -d1 2>/dev/null | grep -E "^[0-9]+.[0-9]+G" | head -n-1 | awk '{print $2}' | sed 's/.\///' | tr "\n" " "))
   size_numbers=($(echo $disk_usage | awk '{print $1}' | tr -d 'G' | tr "\n" ' '))
   total=0;
   i=1;

   for number in $size_numbers; do
      echo "${files[i]} => ${number}GB"
      ((total += $number))
      ((i++))
   done

   echo "Total => ${total}GB" 
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

if command -v tmux &> /dev/null && [ -n "$PS1" ] && [[ ! "$TERM" =~ screen ]] && [[ ! "$TERM" =~ tmux ]] && [ -z "$TMUX" ]; then
    exec tmux
fi
