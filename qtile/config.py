from libqtile import layout
from libqtile.config import Click, Drag, Key, Match, Group, Output
from libqtile.lazy import lazy
from libqtile.backend.wayland.inputs import InputConfig

from screens import default_screen, widget_defaults
from remaps import mod, keys
import layouts
from autostart import autostart

widget_defaults=widget_defaults

groups = [Group(i) for i in [" 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 "]]
for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

def generate_screens(outputs: list[Output]):
    screen_list = []
    for output in outputs:
        screen_list.append(default_screen)

    return screen_list

layouts = layouts.layouts

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
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
wl_input_rules = {
    "type:keyboard": InputConfig(
        kb_layout="es",
    )
}
# java ui toolkits shit, i don't even use that shit but here is it, nobody knows what the future holds.
wmname = "LG3D"

# auto start of defined packages in config.toml
autostart()
