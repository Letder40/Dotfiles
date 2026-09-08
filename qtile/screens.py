from os.path import exists
from pathlib import Path

from libqtile import widget, bar
from libqtile.config import Screen
import json
import subprocess

from user_config import config

widget_defaults = dict(
    font="FiraCode Nerd Font Mono",
    fontsize=16,
    padding=3,
)

def getWallpaperPath() -> str:
    try:
        wallpaper = config["preferences"]["wallpaper"]
        if type(wallpaper) is int:
            name = Path.home() / "media" / "wallpapers" / f"wallpaper{wallpaper}"
            if (name.with_suffix(".png").exists()):
                return name.with_suffix(".png").absolute().as_posix()
            elif (name.with_suffix(".jpg").exists()):
                return name.with_suffix(".jpg").absolute().as_posix()

        if type(wallpaper) is str and Path(wallpaper).exists():
            return Path(wallpaper).absolute().as_posix()

        return (Path.home() / "media" / "wallpapers" / "wallpaper0.png").absolute().as_posix()

    except:
        return (Path.home() / "media" / "wallpapers" / "wallpaper0.png").absolute().as_posix()

def currip():
    ip_route = subprocess.check_output(["ip", "-j", "route", "show", "default"])
    ip_addr = json.loads(ip_route)[0]["prefsrc"]

    return ip_addr

widgets = [
    widget.GroupBox (
        foreground=["#f1ffff","#f1ffff"],
        background=["#0f1011","#0f1011"],
        urgent_border=["#F07178","#F07178"],
        borderwidth=2,
        active=["#f1ffff","#f1ffff"],
        inactive=["#f1ffff","#f1ffff"],
        highlight_method='default',
        urgent_alert_method='block',
        this_current_screen_border=["#0047AF","#0047AF"],
        this_screen_border=["#5c5c5c","#5c5c5c"],
        other_current_screen_border=["#0f101a","#0f101a"],
        other_screen_border=["#0f101a","#0f101a"],
        disable_drag=True
    ),

    widget.Spacer(),

    widget.Sep(
        linewidth=1,
        padding=15,
        foreground="#ffffff",
    ),
    widget.TextBox(
        background=["#000000","#000000"],
        margin_x=10,
        foreground=["#ffffff","#ffffff"],
        fontsize=28,
        text="󰌗"
    ),
    widget.NetGraph(
        interface='auto',
        fill_color='3bfc29',
        graph_color='306844',
        border_color='#000000',
        border_width=0,
        background=["#000000","#000000"],
        line_width=3,
    ),
    widget.TextBox(
        background=["#000000","#000000"],
        foreground=["#ffffff","#ffffff"],
        fontsize=28,
        text="󰲐"
    ),
    widget.GenPollText(
        update_interval=5,
        fontsize=14,
        func=lambda: currip(),
    ),

    widget.Sep(
        linewidth=1,
        padding=15,
        foreground="#ffffff",
    ),
    widget.Systray(
        padding=5,
    ),
    widget.Sep(
        linewidth=1,
        padding=15,
        foreground="#ffffff",
    ),

    widget.Spacer(length=10),

    widget.Clock(
        background=["#000000","#000000"],
        foreground=['ffffff','ffffff'],
        format=' %d/%m/%Y   %H:%M  ',
        padding=5
    ),
]

default_screen = Screen(
        top=bar.Bar(
            widgets,
            30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]
            margin=5,
            opacity=0.8
        ),
        wallpaper=getWallpaperPath(),
        wallpaper_mode="fill"
    )
