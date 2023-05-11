# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook

from colorscheme import colorscheme_GeekchanskiY as primary_colorscheme

mod = "mod4"
terminal = "kitty"


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/startup.sh')
    subprocess.call([home])

# Add widgets to add connected functions and keys to them

kb_widget = widget.KeyboardLayout(
                    **widget_defaults,
                    **widget_defaults_color,
                    fmt=' {} ',
                    configured_keyboards=["us", "ru"],
)

@lazy.function 
def change_keyboard_layout(qtile):
    kb_widget.next_keyboard()


#

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod], "d", lazy.spawn("amixer -c 0 -q -D pulse set Master 2%+")),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run")),

    Key([mod], "Print", lazy.spawn("gnome-screenshot -i")),

    Key([mod], "space", change_keyboard_layout),
    # Key([mod], "и", change_keyboard_layout)

]

# groups = [Group(i) for i in "1234567890"]

# I prefer to set groups like this because sometimes I work for a
# while with the same spawn or match for certain windows

groups = [
    Group(
        '1',
        label='Home',
    ),
    Group(
        '2',
        label='C1',
    ),
    Group(
        '3',
        label='C2',
    ),
    Group(
        '4',
        label='C3',
    ),
    Group(
        '5',
        label='S1',
    ),
    Group(
        '6',
        label='S2',
    ),
    Group(
        '7',
        label='S3',
    ),
    Group(
        '8',
        label='J1',
    ),
    Group(
        '9',
        label='J2',
    ),
    Group(
        '0',
        label='J3',
    ),

]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_focus="#808080",
        border_width=2,
        fair=True,
        grow_amount=4,
        margin=5,
        margin_on_single=5,
    ),
    # layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="CaskaydiaCove Nerd Font Mono",
    padding=0,
    fontsize=14,
)

widget_defaults_divider = dict(
    font="CaskaydiaCove Nerd Font Mono",
    padding=0,
    fontsize=20,
)

widget_defaults_color = dict(
    foreground=primary_colorscheme['fg'],
    background=primary_colorscheme['bg_transparent']
)

extension_defaults = widget_defaults.copy()

volume_config = {
    "get_volume_command": "awk -F'[][]' '/Left:/ { print $2 }' <(amixer -D pulse sget Master)",
    "mute_command": "amixer -D pulse set Master toggle",
}

screens = [
    Screen(
        wallpaper="~/Pictures/Wp.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            [

                # widget.CurrentLayout(), I use single columns layout, so I dont need it

                widget.GroupBox(
                    **widget_defaults,

                    active=primary_colorscheme['fg'],
                    background=primary_colorscheme['bg_transparent'],

                    inactive=primary_colorscheme['fg_inactive'],
                    highlight_color='#FFFF00',


                    this_screen_border=primary_colorscheme['fg'],
                    foreground=primary_colorscheme['fg'],

                    this_current_screen_border=primary_colorscheme['active'],

                    hide_unused=False,  # I love the true one, but it feels empty

                    fmt=' {}',

                    borderwidth=0,
                    center_aligned=False,
                    disable_drag=True,
                    fontshadow=None,
                    highlight_method="text",
                    markup=True,
                    rounded=False,
                ),

                # widget.WindowTabs(),

                widget.Spacer(
                    # background='#00000000',
                ),
                # widget.Systray(
                #     background=colorscheme["bg_transparent"],
                # ),

                widget.Clock(
                    **widget_defaults,
                    **widget_defaults_color,
                ),

                # widget.TaskList(),

                widget.Spacer(),

                # widget.Backlight(backlight_name="intel_backlight"), does not works on my machine :(

                widget.CPU(
                    **widget_defaults,
                    **widget_defaults_color,
                    format='CPU: {load_percent}%',
                ),


                widget.Net(
                    **widget_defaults,
                    **widget_defaults_color,
                    format=' {down} ↓↑{up} ',
                    prefix="M",
                ),

                widget.Memory(
                    **widget_defaults,
                    **widget_defaults_color,


                    format=" MEM: {MemUsed: .0f}{mm} / {MemTotal:.0f}{mm} ",
                    measure_mem='G',
                ),

                widget.PulseVolume(
                    **widget_defaults,
                    **widget_defaults_color,

                    limit_max_volume=True,

                    fmt=" VOL: {} ",
                ),

                widget.Battery(
                    **widget_defaults,
                    **widget_defaults_color,

                    format=" BTR: {percent:2.0%} ",
                ),

                kb_widget,

                widget.QuickExit(
                    default_text="  X",
                    countdown_start=3,
                    countdown_format="  {}",
                    background=primary_colorscheme['bg_transparent'],
                    foreground=primary_colorscheme['fg'],
                    **widget_defaults,
                ),
            ],
            20,
            background=primary_colorscheme['bg_transparent'],
            border_width=[2, 10, 2, 10],  # padding for the bar itself
            border_color=["00000000", "00000000", "00000000", "00000000"]  # make this 'padding' transparent
        ),
    ),
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
auto_minimize = True

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
