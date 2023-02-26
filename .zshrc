# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.

if [[ $(id | awk '{print $1}' FS=" " | awk '{print $2}' FS== | sed -E s/\[^0-9]//g) == 0 ]]; then
export HOME=/root
fi

if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.

export ZSH="$HOME/.oh-my-zsh"


# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="powerlevel10k/powerlevel10k"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
	      git
	     )

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
#source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

#my_functions
function mkt(){
   mkdir {content,exploits,nmap,scripts,tmp} 	
}

function extractports(){
   echo -e "\n Extracting relevant information...\n"
   ip_address=$(cat allports | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' | sort -u )
   echo -e "\t[*] ip address: $ip_address" 
   open_ports=$(cat allports | grep -oP "\d{1,5}/open" | awk '{print $1}' FS="/" | xargs | tr " " ",")
   echo -e "\t[*] ports: $open_ports\n"

   echo $open_ports | tr -d "\n" | xclip -sel clip
   echo -e " [*]Ports has been copied to clipboard"	
}

function cpd(){
   if [ -z $1 ]; then
      pwd | xclip
   elif [[ $1 == "-m" ]]; then
      if [[ $(xclip -o) == "" ]]; then
         echo -e "\t[*] Debes primero ejecutar cpd para copiar el directorio"
      else
         cd $(xclip -o)
      fi
   fi
}
#ls
LS_COLORS="di=1;34"
alias ls='exa --icons --color=always -g --group-directories-first'
alias ll='exa -alF --icons --color=always -g --group-directories-first'
alias la='exa -a --icons --color=always -g --group-directories-first'
alias l='exa -F --icons --color=always -g --group-directories-first'
alias l.='exa -a | egrep "^\."'
export EXA_COLORS="ur=36;01:uw=36;01:ux=36;01:ue=36:gr=35:gw=35:gx=35:tr=32;01:tw=32;01:tx=32;01:uu=32:un=31:sn=34:gu=32:gn=31:da=37"
export TZ=/usr/share/zoneinfo/Europe/Madrid 

#my_aliases
alias ll="ls -l"
alias dev="cd ~/workspace/dev"
alias apuntes="cd ~/workspace/apuntes"
alias hacking="cd ~/workspace/hacking"
alias appsrepos="cd ~/repositories/aplications"
alias ownrepos="cd ~/repositories/ownrepos"
alias htb="cd ~/workspace/hacking/HTB"
alias off="shutdown now"
alias vi="nvim"
alias cat="bat -p --paging=never"
alias catp="bat -p"
alias evil-winrm="docker run --rm -ti --name evil-winrm -v /home/foo/ps1_scripts:/ps1_scripts -v /home/foo/exe_files:/exe_files -v /home/foo/data:/data oscarakaelvis/evil-winrm"

#PATH
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/home/letder/scripts:/home/letder/workspace/dev/python  


source /home/letder/sware/normal/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
export HOME=/home/letder
