#!/bin/bash

password="$(yad --center --width:400 --entry --hide-text --title="Login required" --button=gtk-ok:0 --button=gtk-cancel:1)"

if [[ "$password" == "$(< ~/password.txt)" ]]; then
    yad --center --width:400 --title="CIT Admin" \
        --button="Close"\!gtk-close\!"Close this window":0 \
        --button="Copy to USB"\!drive-harddisk-usb-symbolic\!"Copy CIT data to a USB flash drive":2 \
        --button="Terminal"\!\!"Close this window":3
    if [[ "$?" == "2" ]]; then
        bash /cit/usb_copy.sh
    fi
    if [[ "$?" == "3" ]]; then
        xfce4-terminal
    fi
fi
