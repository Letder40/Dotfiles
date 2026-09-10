import json
import subprocess
from pathlib import Path

from libqtile import bar, widget
from libqtile.config import Group, Output, Screen
from libqtile.lazy import lazy
from libqtile.widget.base import _Widget as WidgetType

from user_config import config
from theme import THEME, colors


groups = [
    Group(group_name)
    for group_name in [
        " 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 "
    ]
]


widget_defaults = {
    "font": THEME["font"],
    "fontsize": THEME["font_sizes"]["default"],
    "padding": THEME["padding"]["default"],
}


class FixedTaskList(widget.TaskList):
    """
    Task list with a fixed width.

    TaskList normally uses bar.STRETCH. This makes it STATIC so the two
    surrounding STRETCH spacers can centre it relative to the whole bar.
    """

    def __init__(self, width: int, **widget_config):
        self.fixed_width = width
        super().__init__(**widget_config)

    def _configure(self, qtile, bar_object):
        super()._configure(qtile, bar_object)
        self.length_type = bar.STATIC
        self.length = self.fixed_width


def get_wallpaper_path() -> str:
    fallback = (
        Path.home()
        / "media"
        / "wallpapers"
        / "wallpaper0.png"
    )

    try:
        wallpaper = config["preferences"]["wallpaper"]

        if isinstance(wallpaper, int):
            base = (
                Path.home()
                / "media"
                / "wallpapers"
                / f"wallpaper{wallpaper}"
            )

            for suffix in (".png", ".jpg", ".jpeg"):
                path = base.with_suffix(suffix)

                if path.exists():
                    return path.absolute().as_posix()

        elif isinstance(wallpaper, str):
            path = Path(wallpaper).expanduser()

            if path.exists():
                return path.absolute().as_posix()

    except (KeyError, TypeError):
        pass

    return fallback.absolute().as_posix()


def separator() -> widget.Sep:
    separator_config = THEME["separator"]

    return widget.Sep(
        linewidth=separator_config["line_width"],
        padding=separator_config["padding"],
        size_percent=separator_config["size_percent"],
        background=colors["background_alt"]
    )


def network_widgets() -> list[WidgetType]:
    def current_ip() -> str:
        try:
            raw_routes = subprocess.check_output(
                "ip -j route show default".split(),
                stderr=subprocess.DEVNULL,
            )

            routes = json.loads(raw_routes)

            if not routes:
                return "offline"

            ip_address = routes[0].get("prefsrc")

            if ip_address:
                return ip_address

            interface = routes[0].get("dev")

            if not interface:
                return "unknown"

            raw_addresses = subprocess.check_output(
                f"ip -j -4 addr show dev {interface}".split(),
                stderr=subprocess.DEVNULL,
            )

            addresses = json.loads(raw_addresses)

            for interface_data in addresses:
                for address in interface_data.get("addr_info", []):
                    if address.get("scope") == "global":
                        return address["local"]

            return "unknown"

        except (
            subprocess.CalledProcessError,
            json.JSONDecodeError,
            KeyError,
            IndexError,
            OSError,
        ):
            return "offline"

    background = colors["background_elevated"]
    graph = THEME["network"]["graph"]
    mouse_callbacks = {
        "Button1": lazy.spawn("nm-connection-editor"),
        "Button3": lazy.spawn("nm-connection-editor")
    }

    return [
        widget.TextBox(
            text=THEME["icons"]["network"],
            background=background,
            foreground=colors["foreground_muted"],
            fontsize=THEME["font_sizes"]["icon"],
            padding=THEME["padding"]["network_icon"],
            mouse_callbacks=mouse_callbacks,
        ),

        widget.NetGraph(
            interface="auto",
            background=background,
            fill_color=colors["net_fill"],
            graph_color=colors["net_graph"],
            border_width=graph["border_width"],
            line_width=graph["line_width"],
            margin_x=graph["margin_x"],
            margin_y=graph["margin_y"],
            mouse_callbacks=mouse_callbacks,
        ),

        widget.TextBox(
            text=THEME["icons"]["ip"],
            background=background,
            foreground=colors["foreground_muted"],
            fontsize=THEME["font_sizes"]["icon"],
            padding=THEME["padding"]["ip_icon"],
            mouse_callbacks=mouse_callbacks,
        ),

        widget.GenPollText(
            func=current_ip,
            update_interval=THEME["network"]["update_interval"],
            background=background,
            foreground=colors["foreground"],
            fontsize=THEME["font_sizes"]["ip"],
            padding=THEME["padding"]["network_text"],
            mouse_callbacks=mouse_callbacks,
        ),
    ]


def get_default_widgets(is_primary: bool) -> list[WidgetType]:
    def left() -> list[WidgetType]:
        return [
            widget.GroupBox(
                foreground=colors["foreground"],
                background=colors["background_alt"],

                active=colors["foreground"],
                inactive=colors["foreground_muted"],

                borderwidth=THEME["groupbox"]["border_width"],

                urgent_border=colors["urgent"],
                urgent_alert_method="block",

                highlight_method="line",

                this_current_screen_border=colors["groupbox_current_screen"],
                this_screen_border=colors["groupbox_screen"],

                other_current_screen_border=colors["groupbox_other"],
                other_screen_border=colors["groupbox_other"],

                disable_drag=True,
            ),
        ]

    def center() -> list[WidgetType]:
        background = colors["background_transparent"]

        return [
            widget.Spacer(
                length=bar.STRETCH,
                background=background,
            ),

            FixedTaskList(
                width=THEME["task_list"]["width"],
                border=colors["accent"],
                max_title_width=THEME["task_list"]["max_title_width"],
                background=background,
            ),

            widget.Spacer(
                length=bar.STRETCH,
                background=background,
            ),
        ]

    def right() -> list[WidgetType]:
        widgets: list[WidgetType] = [
            *network_widgets(),
        ]

        if is_primary:
            widgets.extend([
                separator(),

                widget.Systray(
                    padding=THEME["systray"]["padding"],
                    background=colors["background_alt"],
                ),
            ])

        widgets.extend([
            separator(),
            widget.Clock(
                background=colors["background_dark"],
                foreground=colors["foreground"],
                format=THEME["clock"]["format"],
                padding=THEME["clock"]["padding"],
            ),
        ])

        return widgets

    return [
        *left(),
        *center(),
        *right(),
    ]


def get_default_screen_config(is_primary: bool) -> Screen:
    return Screen(
        top=bar.Bar(
            get_default_widgets(is_primary),
            THEME["bar"]["height"],
            background=colors["background_dark"],
            margin=THEME["bar"]["margin"],
        ),

        wallpaper=get_wallpaper_path(),
        wallpaper_mode="fill",
    )


screen_list = [
    get_default_screen_config(True),
]


def generate_screens(outputs: list[Output]) -> list[Screen]:
    monitor_count = len(outputs)

    while len(screen_list) < monitor_count:
        screen_list.append(get_default_screen_config(False))

    return screen_list[:monitor_count]
