# Checkin

> WARNING: Alpha software, started on this yesterday, we are NOT open for pull requests atm.

Set up a check-in kiosk that works with QR-codes.

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

### Python, pip, venv

Get a working version of Python, including pip and venv.

### Opencv (qr code scanner and video grabber)

Pip install `opencv-python` in a new venv.

> A `requirements.txt` is available.

### Flask (web server)

Pip install `flask` and `requests`.

> A `requirements.txt` is available.
