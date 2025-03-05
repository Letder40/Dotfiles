from libqtile import layout
from libqtile.config import Click, Drag, Key, Match, Group
from libqtile.lazy import lazy

import screens
import remaps
import layouts

mod = "mod4"
terminal = "kitty"

keys = remaps.keys

groups = [Group(i) for i in ["CMD", "WWW", "DEV", "VAR", "VMN", "SW1", "SW2", "SW3"]]
for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

screen_n = 1
screens = [screens.default_screen for _ in range(screen_n)]

layouts = layouts.layouts

# Drag floating layouts.
mouse = [
    Drag([remaps.mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([remaps.mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([remaps.mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True

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
# shutup baby don't resize
auto_minimize = False
# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None
# java ui toolkits shit, i don't even use that shit but here is it, nobody knows what the future holds.
wmname = "LG3D"
