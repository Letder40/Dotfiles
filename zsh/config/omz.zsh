ZSH_THEME="powerlevel10k/powerlevel10k"

plugins=(
	git
	zsh-syntax-highlighting
)

CASE_SENSITIVE="false"
DISABLE_MAGIC_FUNCTIONS="true"
DISABLE_LS_COLORS="false"
DISABLE_AUTO_TITLE="true"
ENABLE_CORRECTION="false"
DISABLE_UNTRACKED_FILES_DIRTY="true"
HIST_STAMPS="dd/mm/yyyy"

zstyle ':omz:update' mode auto  # update automatically without asking

export ZSH="$HOME/.oh-my-zsh"
