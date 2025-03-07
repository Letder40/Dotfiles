from libqtile.config import EzKey as Key, EzKeyChord as KeyChord
from libqtile.lazy import lazy

mod = "mod4"

Key.modifier_keys = {
    "M": mod,
    "A": 'mod1',
    "S": 'shift',
    "C": 'control',
} 

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key("M-h", lazy.layout.left(), desc="Move focus to left"),
    Key("M-j", lazy.layout.down(), desc="Move focus down"),
    Key("M-k", lazy.layout.up(), desc="Move focus up"),
    Key("M-l", lazy.layout.right(), desc="Move focus to right"),
    Key("M-t", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key("M-S-h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key("M-S-j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key("M-S-k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key("M-S-l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key("M-C-h", lazy.layout.shrink_main(), desc="Grow window to the left"),
    Key("M-C-l", lazy.layout.grow_main(), desc="Grow window to the right"),
    Key("M-C-h", lazy.layout.grow_main(), desc="Grow window down"),
    Key("M-C-k", lazy.layout.shrink_main(), desc="Grow window up"),
    Key("M-r", lazy.layout.normalize(), desc="Reset all window sizes"),

    KeyChord("M-<space>", [
        # Flip layout
        Key("h", lazy.layout.flip_left()),
        Key("j", lazy.layout.flip_down()),
        Key("k", lazy.layout.flip_up()),
        Key("l", lazy.layout.flip_right()),

        # Toggle between split and unsplit sides of stack.
        # For Bsp layout:
            # Split = Horizontaly splited panels
            # Unsplit = Verticaly splited panels
        Key("s", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),
    ]),

    # software keybindings
    Key("M-<Return>", lazy.spawn("kitty"), desc="Launch terminal"),
    Key("M-b", lazy.spawn("firefox"), desc="Launch browser"),
    Key("M-m", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key("M-s", lazy.spawn("flameshot gui"), desc="Launch flameshot"),

    # Toggle between different layouts, layouts defined below
    Key("M-<Tab>", lazy.next_layout(), desc="Toggle between layouts"),

    # full screen
    Key("M-f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),

    # qtile actions
    Key("M-w", lazy.window.kill(), desc="Kill focused window"),
    Key("M-C-r", lazy.reload_config(), desc="Reload the config"),
    Key("M-C-q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key("M-p", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key("M-S-<space>", lazy.layout.flip(), desc="Move window focus to other window"),
]

