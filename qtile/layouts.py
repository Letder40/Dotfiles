from libqtile import layout
from libqtile.config import Match
from theme import colors

default_layout_conf = {
    'border_focus': colors["accent"],
    'border_width': 4,
    'margin': 6
}

bsp_layout_conf = {
    'align': 1,
    'border_normal': colors["accent_dim"],
    'border_focus': colors["accent"],
    'border_width': 4,
    'margin': 6
}

layouts = [
    layout.Bsp(**bsp_layout_conf),
    layout.Max(),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"]),
    # layout.Stack(num_stacks=2),
    # layout.Matrix(**default_layout_conf),
    # layout.MonadTall(**default_layout_conf),
    # layout.MonadWide(**default_layout_conf),
    # layout.RatioTile(**default_layout_conf),
    # layout.Tile(**default_layout_conf),
    # layout.TreeTab(**default_layout_conf),
    # layout.VerticalTile(),
    # layout.Zoomy(**default_layout_conf),
]

floating_layout = layout.Floating(
    # Run the utility of `xprop` to see the wm class and name
    # of an X client.
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
