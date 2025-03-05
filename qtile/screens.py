from libqtile import widget, bar
from libqtile.config import Screen

import os
import subprocess

user = os.getlogin()
target_path = f"/home/{user}/.local/share/qtile/target_widget.txt"

widget_defaults = dict(
    font="sans",
    fontsize=18,
    padding=3,
)

widgets = [
    widget.GroupBox (
        foreground=["#f1ffff","#f1ffff"],
        background=["#0f1011","#0f1011"],
        urgent_border=["#F07178","#F07178"],
        font='UbuntuMono Nerd Font',
        fontsize=20,
        margin_y=3,
        margin_x=0,
        padding_y=8,
        padding_x=10,
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

    widget.GenPollText(
        update_interval=1,
        font='UbuntuMono Nerd Font Bold',
        fontsize=18,
        func=lambda: open(target_path).readline().strip()
    ),

    widget.GenPollText(
        update_interval=1,
        font='UbuntuMono Nerd Font Bold',
        fontsize=18,
        func=lambda: subprocess.check_output(f"/home/{user}/scripts/get_addr.sh").decode("utf-8"),
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

   widget.Clock(
        background=["#000000","#000000"],
        foreground=['ffffff','ffffff'],
        format='   %d/%m/%Y - %H:%M  ',
        font='UbuntuMono Nerd Font',
        fontsize= 20,
    ),
]

default_screen = Screen(
        top=bar.Bar(
            [widget for widget in widgets],
            30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"] 
        ) 
    )
