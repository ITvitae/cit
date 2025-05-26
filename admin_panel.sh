#!/bin/bash

password="$(yad --center --width:400 --entry --hide-text --title="Login required" --button=gtk-ok:0 --button=gtk-cancel:1)"

if [[ "$password" == "$(< ~/password.txt)" ]]; then
    yad --center --width:400 --title="CIT Admin" \
        --button="Close"\!gtk-close\!"Close this window":0 \
        --button="Copy to USB"\!drive-harddisk-usb-symbolic\!"Copy CIT data to a USB flash drive":2 \
        --button="Terminal"\!\!"Close this window":3 \
        --button="View"\!\!"View today's CIT file":4
    result="$?"
    if [[ "$result" == "2" ]]; then
        bash /cit/usb_copy.sh
    fi
    if [[ "$result" == "3" ]]; then
        xfce4-terminal
    fi
    if [[ "$result" == "4" ]]; then
        xfce4-terminal -e "less $HOME/cit/$(date +"%Y_%m_%d").csv"
    fi
fi
