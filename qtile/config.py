from typing import Any

from screens import generate_screens, widget_defaults, groups  # noqa: F401
from layouts import layouts, floating_layout  # noqa: F401
from keys import keys, mouse, mod  # noqa: F401
from autostart import autostart  # noqa: F401

dgroups_key_binder = None
dgroups_app_rules: list[Any] = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
# shutup baby don't resize
auto_minimize = False

# java ui toolkits shit
# i don't even use that shit but here is it,
# nobody knows what the future holds.
wmname = "LG3D"
