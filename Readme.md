# Dotfiles

My personal Arch Linux desktop configuration and installer. It sets up a Qtile-based environment, installs the configured software, and links the repository's configuration files into the current user's home directory.

## Features

- Qtile configuration with multi-screen support, keybindings, autostart applications, and theming
- Package installation through `pacman`
- Configurable terminal, browser, font, icon theme, wallpaper, and package groups
- Optional Picom, Neovim, Zsh, and Tmux setup
- Declarative system and user services, including socket-activated `ssh-agent`
- Declarative installers for shell scripts and Git repositories
- Symlink-based deployment with automatic backups of existing files
- Zsh, Powerlevel10k, Kitty, Tmux, Rofi, `eza`, and desktop utility configuration

## Requirements

- Arch Linux
- Python 3.12 or newer
- `sudo`
- An internet connection for packages, scripts, and Git repositories

The installer must be run as your regular user. It validates your `sudo` credentials at startup and uses elevated privileges only to install packages and enable system services. User services, downloads, repository operations, and configuration links run as the current user.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Letder40/dotfiles.git
   cd dotfiles
   ```

2. Review and edit `config.toml`. In particular, check the package lists and every configured `curl` URL before running downloaded scripts.

3. Run the installer without `sudo`:

   ```bash
   python setup.py
   ```

The installer will:

- install missing packages;
- enable and start configured system and user services;
- run configured remote installers and clone or update configured repositories;
- install Oh My Zsh, Powerlevel10k, Zsh plugins, and Tmux plugins when enabled;
- set the configured GTK 3/4 icon theme and publish it to running X11 applications;
- link the Qtile and wallpaper configuration;
- link the selected Zsh, Kitty, Picom, Neovim, Rofi, `eza`, and Tmux configuration when applicable.

If a destination already exists, it is renamed with a timestamped `_bck` suffix before the new symlink is created. Running the installer again leaves correct symlinks and installed packages unchanged, and updates existing Git repositories with a fast-forward-only pull.

## Configuration

Most installation and desktop preferences live in `config.toml`.

### Preferences

```toml
[preferences]
wallpaper = 4
neovim = true
animations = true
tmux = true
zshrc = true

[preferences.icon_theme]
name = "Papirus-Dark"
package = "papirus-icon-theme"

[preferences.font]
name = "FiraCode Nerd Font Mono"
package = "ttf-firacode-nerd"

[preferences.terminal]
name = "kitty"
package = "*"

[preferences.browser]
name = "firefox"
package = "*"
```

The `name` fields are consumed by Qtile or GTK. Setting `package = "*"` derives the Arch package from `name`. `neovim`, `animations`, `tmux`, `zshrc` control their optional setup steps. Kitty configuration is linked when the selected terminal is `kitty`, and the `eza` configuration is linked when its package is present in `packages.utils`.

`wallpaper` can be either an integer matching a bundled `wallpaper<number>` file or a path to an existing image. Paths may start with `~`. If the configured image cannot be found, Qtile falls back to `wallpaper0.png`.

The installer writes the icon theme to the GTK 3 and GTK 4 settings files. Qtile starts `xsettingsd` to expose the same setting to tray applications; rerunning the installer reloads an already-running daemon, so applications can update without logging out.

### Pacman packages

```toml
[packages]
utils = ["flameshot", "eza"]
desktop = ["pavucontrol", "discord", "bitwarden"]
others = ["rustup", "npm"]

[packages.init]
services = [
    { name = "NetworkManager", package = "networkmanager" },
    { name = "dunst", package = "*", user = true },
    { name = "ssh-agent.socket", package = "openssh", user = true },
]

autostart = [
    { exec = "nm-applet", package = "network-manager-applet" },
    { exec = "setxkbmap es" },
]

[packages.base]
required = ["qtile", "zsh", "git", "curl"]
system = ["lightdm-gtk-greeter", "pipewire", "wireplumber"]

[packages.base.init]
services = [
    { name = "lightdm", package = "*" },
]
```

- `utils`, `desktop`, and `others` are optional package groups. They are separated only to keep the configuration readable.
- `packages.base.required` and `packages.base.system` contain essential packages. The setup stops if one of these groups cannot be installed.
- An `autostart` entry pairs a command with the package that provides it. Omit `package` when the command does not require an additional installation.
- A `services` entry uses `name` for the systemd unit and `package` for its Arch package. Set `user = true` for a user service.
- Set `package = "*"` to derive the package from `name`, or from the first word of `exec` in an autostart entry.
- Entries under `packages.base.init` are treated as essential; entries under `packages.init` are optional.

Commands in both `autostart` lists are launched by Qtile. Services are enabled immediately with `systemctl enable --now`; entries with `user = true` use the current user's systemd manager.

The terminal, browser, font, and icon-theme packages configured under `preferences` are also installed through `pacman`.

The configured `ssh-agent.socket` is provided by Arch's `openssh` package. The included Zsh configuration points `SSH_AUTH_SOCK` at `$XDG_RUNTIME_DIR/ssh-agent.socket`, so configured Zsh shells share the socket-activated agent instead of starting separate agent processes.

### Optional feature dependencies

Zsh, Tmux, and Rofi declare their own dependencies in top-level feature tables. These dependencies are processed only when the corresponding preference is enabled:

```toml
[[zshrc.package]]
name = "zsh"

[[zshrc.curl]]
url = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
params = "--keep-zshrc"
check_path = "~/.oh-my-zsh"

[[zshrc.git]]
src = "https://github.com"
repo = "romkatv/powerlevel10k.git"
path = "~/.oh-my-zsh/custom/themes/powerlevel10k"

[[tmux.package]]
name = "tmux"

[[tmux.git]]
src = "https://github.com"
repo = "tmux-plugins/tpm"
path = "~/.tmux/plugins/tpm"

[[rofi.package]]
name = "rofi"
```

Feature setup stops if one of its dependencies fails, but the rest of the dotfiles setup continues. Successful Tmux setup links `~/.config/tmux` and invokes TPM's plugin installer. Rofi uses Kitty to launch terminal applications. The imported Material theme is included in Arch's `rofi` package.

### Remote shell installers

Each `[[curl]]` entry downloads a script and runs it with `sh` as the current user:

```toml
[[curl]]
url = "https://example.com/install.sh"
params = "--example-option"
check_path = "~/.example"
required = false
```

- `url` is the script URL.
- `params` is an optional string of arguments passed to the script.
- `check_path` skips installation when that path already exists.
- `required = true` makes a failure stop the setup; optional failures are logged instead.

### Git repositories

Each `[[git]]` entry defines a repository to clone or update as the current user:

```toml
[[git]]
src = "https://github.com"
repo = "romkatv/powerlevel10k.git"
path = "~/.oh-my-zsh/custom/themes/powerlevel10k"
required = true
```

The clone URL is formed as `<src>/<repo>`. Missing parent directories are created automatically. New clones use a depth of one; existing repositories are updated with `git pull --ff-only`. Git operations disable interactive credential prompts and use timeouts so setup cannot wait indefinitely. As with remote installers, `required` controls whether a failure stops the setup.

## Customization

The installer is a starting point. Individual configurations can be changed directly in their repository directories, including `qtile/`, `kitty/`, `picom/`, `rofi/`, `tmux/`, `eza/`, and `zsh/`.

The Neovim configuration is maintained separately at [Letder40/nvim-config](https://github.com/Letder40/nvim-config) and is cloned into `nvim/` when enabled.

## Demo

![Setup Demo](./demo.png)
