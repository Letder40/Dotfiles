from typing import Any
from user_config import config

THEME: dict[str, Any] = {
    "font": config["preferences"]["font"]["name"],

    "colors": {
        # Neutral scale
        "background": "#111318",
        "background_transparent": "#111318C5",
        "background_alt": "#161920",
        "background_elevated": "#1C2028",
        "background_dark": "#0B0D11",
        "background_light": "#fcfcfc",

        "foreground": "#E6EAF0",
        "foreground_muted": "#9AA3B2",
        "foreground_dim": "#6F7785",

        # Borders / separators
        "border": "#343B47",
        "border_subtle": "#252B34",

        # Primary accent
        "accent": "#2667d1",
        "accent_dim": "#021a45c0",

        # Semantic
        "urgent": "#E26A75",

        # GroupBox
        "groupbox_current_screen": "#4C8DFF",
        "groupbox_screen": "#3A414D",
        "groupbox_other": "#20252D",

        # Network graph
        "net_fill": "#3D7059",
        "net_graph": "#62A982",
    },

    "bar": {
        "height": 30,
        "margin": 5,
    },

    "groupbox": {
        "border_width": 2,
    },

    "task_list": {
        "width": 700,
        "max_title_width": 150,
    },

    "network": {
        "update_interval": 5,
        "graph": {
            "border_width": 0,
            "line_width": 2,
            "margin_x": 2,
            "margin_y": 4,
        },
    },

    "systray": {
        "padding": 6,
    },

    "clock": {
        "format": " %d/%m/%Y   %H:%M ",
        "padding": 10,
    },

    "separator": {
        "line_width": 0,
        "padding": 10,
        "size_percent": 100,
    },

    "icons": {
        "network": "󰌗",
        "ip": "󰲐",
    },

    "font_sizes": {
        "default": 16,
        "icon": 24,
        "ip": 14,
    },

    "padding": {
        "default": 3,
        "network_icon": 8,
        "ip_icon": 5,
        "network_text": 8,
    },
}

colors: dict[str, str] = THEME["colors"]
