from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

import subprocess

mod = "mod4"
terminal = "kitty" 
browser = "firefox"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.shrink_main(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_main(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_main(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.shrink_main(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    
    # start software keybindings
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key([mod], "s", lazy.spawn("flameshot gui"), desc="Launch flameshot"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "space", lazy.layout.flip(), desc="Move window focus to other window"),
]

groups = [Group(i) for i in ["CMD", "WWW", "DEV", "VAR", "VMN", "SW1", "SW2", "SW3"]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layout.conf = {
    'border_focus':"#0047AF",
    'border_width':4,
    'margin':6
}

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
     layout.Bsp(**layout.conf),
    #layout.Matrix(**layout.conf),
    #layout.MonadTall(**layout.conf),
    #layout.MonadWide(**layout.conf),
    #layout.RatioTile(**layout.conf),
    #layout.Tile(**layout.conf),
    #layout.TreeTab(**layout.conf),
    #layout.VerticalTile(),
    layout.Zoomy(**layout.conf),
]

widget_defaults = dict(
    font="sans",
    fontsize=18,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    background=["#0f1011","#0f1011"],
                ),

                widget.GroupBox(
                    foreground=["#f1ffff","#f1ffff"],
                    background=["#0f1011","#0f1011"],
                    urgent_border=["#F07178","#F07178"],
                    font='UbuntuMono Nerd Font',
                    fontsize=20,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=5,
                    borderwidth=1,
                    active=["#f1ffff","#f1ffff"],
                    inactive=["#f1ffff","#f1ffff"],
                    rounded=False,
                    highlight_method='block',
                    urgent_alert_method='block',
                    this_current_screen_border=["#0047AF","#0047AF"],
                    this_screen_border=["#5c5c5c","#5c5c5c"],
                    other_current_screen_border=["#0f101a","#0f101a"],
                    other_screen_border=["#0f101a","#0f101a"],
                    disable_drag=True
                ),

                widget.Spacer(),

                widget.TextBox(
                    background=["#000000","#000000"],
                    text=" 󰓾 ",
                    font='UbuntuMono Nerd Font Bold',
                    fontsize=20,
                    foreground=["#ffffff","#ffffff"],
                ),
                widget.GenPollText(
                    update_interval=1,
                    font='UbuntuMono Nerd Font Bold',
                    fontsize=18,
                    func=lambda: subprocess.check_output("/home/letder/media/scripts/get-target.sh").decode("utf-8"),
                ),

                widget.TextBox(
                    background=["#000000","#000000"],
                    text="  ",
                    font='UbuntuMono Nerd Font Bold',
                    fontsize=20,
                    foreground=["#ffffff","#ffffff"],
                ),
                widget.GenPollText(
                    update_interval=1,
                    font='UbuntuMono Nerd Font Bold',
                    fontsize=18,
                    func=lambda: subprocess.check_output("/home/letder/media/scripts/local_ip.sh").decode("utf-8"),
                ),

                widget.Spacer(),

                widget.TextBox(
                    background=["#000000","#000000"],
                    text="  ",
                    font='UbuntuMono Nerd Font Bold',
                    fontsize=20,
                    foreground=["#ffffff","#ffffff"],
                ),
                widget.NetGraph(
                    interface='auto',
                    fill_color='3bfc29',
                    graph_color='306844',
                    border_color='#000000',
                    border_width=0,
                    background=["#000000","#000000"],
                    font='UbuntuMono Nerd Font',
                    fontsize=18,
                    margin_x=10,
                    line_width=3,
                ),
                

                widget.Sep(
                    linewidth=0,
                    padding=15,
                    background=["#000000","#000000"],
                ),
                widget.Systray(),
                widget.Sep(
                    linewidth=0,
                    padding=15,
                    background=["#000000","#000000"],
                ),

                widget.Clock(
                    background=["#000000","#000000"],
                    foreground=['ffffff','ffffff'],
                    format='   %d/%m/%Y - %H:%M  ',
                    font='UbuntuMono Nerd Font',
                    fontsize= 20,
                )
            ],
            30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ) 
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
