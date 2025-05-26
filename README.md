# cit: Check-in terminal

> WARNING: Alpha software, started on this yesterday, we are NOT open for pull requests atm.

Set up a check-in terminal that works with QR-codes.

## Setup and configuration

### Openbox (window manager)

Install `openbox`.

Copy openbox.autostart to `~/.config/openbox/autostart`
Copy openbox.environment to `~/.config/openbox/environment`
Copy openbox.rc.xml to `~/.config/openbox/rc.xml`
Copy openbox.menu.xml to `~/.config/openbox/menu.xml`

### Dunst (notification daemon)

Install `dunst` and get a version of `notify-send`.

Copy `dunst.dunstrc` to `~/.config/dunst/dunstrc`

### tint2

Install `tint2`.

Copy `tint2.tint2rc` to `~/.config/tint2/tint2rc`

### nm-applet

Install `nm-applet-gnome`.

### pmount

Install `pmount`.

### yad

Install `yad`.

### feh

Install `feh`.

Place a wallpaper at `~/cit_wallpaper.png`.

### Python, pip, venv

Get a working version of Python, including pip and venv.

### Opencv (qr code scanner and video grabber)

Pip install `opencv-python` in a new venv.

> A `requirements.txt` is available.

### Flask (web server)

Pip install `flask` and `requests`.

> A `requirements.txt` is available.

## A `users.txt` example

For whomever requires some testing data.

```
# CIT users.txt
#
# All lines that start with # are comments and are not read by cit.
# Empty lines are ignored.
# Lines that start with @ are used to start a new group.
# All other lines are treated as identities.
#
# Example: uncommenting the following two lines results in a group "Hello" with an id "world".
# @Hello
# World
#
@Example group D
user_u@example.com
user_v@example.com
user_w@example.com
user_x@example.com
user_y@example.com
user_z@example.com

@Example group A
user_a@example.com
user_b@example.com

@Example group B
user_e@example.com
user_d@example.com
user_c@example.com

@Example group C
user_f@example.com
user_g@example.com
user_h@example.com
user_i@example.com
user_j@example.com
user_k@example.com
user_l@example.com
user_m@example.com
user_n@example.com
user_o@example.com
user_p@example.com
user_q@example.com
user_r@example.com
user_s@example.com
user_t@example.com
```
