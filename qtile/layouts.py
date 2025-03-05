from libqtile import layout

default_layout_conf = {
    'border_focus':"#0047AF",
    'border_width':4,
    'margin':6
}

bsp_layout_conf = {
    'align': 1,
    'border_normal': "#000030",
    'border_focus': "#0047AF",
    'border_width':4,
    'margin':6
}

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    #layout.Stack(num_stacks=2),
     layout.Bsp(**bsp_layout_conf),
    #layout.Matrix(**default_layout_conf),
    #layout.MonadTall(**default_layout_conf),
    #layout.MonadWide(**default_layout_conf),
    #layout.RatioTile(**default_layout_conf),
    #layout.Tile(**default_layout_conf),
    #layout.TreeTab(**default_layout_conf),
    #layout.VerticalTile(),
    layout.Max(),
    #layout.Zoomy(**default_layout_conf),
]
