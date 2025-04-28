#!/bin/bash

password="$(yad --center --width:400 --entry --hide-text --title="Login required" --button=gtk-ok:0 --button=gtk-cancel:1)"

if [[ "$password" == "$(< ~/password.txt)" ]]; then
    xfce-terminal
fi
