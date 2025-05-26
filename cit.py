
from datetime import datetime
from json import dumps
from subprocess import run
from os import mkdir
from os.path import exists, isdir, isfile, expanduser

import cv2
from requests import post


def dir_check(cit_dir):
    if cit_dir[0] == "~":
        home = expanduser('~')
        cit_dir = f'{home}{cit_dir[1:]}'
    if not exists(cit_dir):
        # TODO: Make this part less crude
        mkdir(cit_dir)
    if not isdir(cit_dir):
        # TODO: Make this part less crude
        raise Exception(f' Expected a directory at cit dir: "{cit_dir}" but found something else!')
    if not cit_dir.endswith("/"):
        cit_dir = f'{cit_dir}/'
    return cit_dir


def notify(title, message, _type='normal'):
    if _type not in ('normal', 'critical'):
        _type = 'normal'
    display_time = {
                'normal': 3000,
                'critical': 4000,
            }[_type]

    run([
        'notify-send',
        f'"{title}"',
        f'"{message}"',
        '-t',
        f'{display_time}',
        '-u',
        _type
    ])


def init_csv(cit_dir, date):
    with open('users.txt', 'r') as _f:
        lines = _f.readlines()
    new_csv = ["person;group;timestamp"]
    group = "NONE"
    for line in lines:
        if line.startswith('#'):
            continue
        if not line:
            continue
        if line.startswith('@'):
            line = line[1:]
            if not line:
                continue
            group = line
        else:
            new_csv.append(f'{group};{line};missing')

    with open(f'{cit_dir}{date}.csv', 'w') as _f:
        _f.writelines(new_csv)


def check_in(user, timestamp, cit_dir):
    date =  datetime.now().strftime('%Y_%m_%d')
    if not isfile(f'{cit_dir}{date}'):
        init_csv(cit_dir, date)
    with open(f'{cit_dir}{date}.csv', 'r') as _f:
        lines = _f.readlines()
    new_csv = []
    if user.endswith('\n'):
        user = user.rstrip('\n')
    found_user = False
    for line in lines:
        parts = line.split(';')
        if user in parts[0]:
            if parts[2] == 'missing':
                line = f'{parts[0]};{parts[1]};{timestamp}'
                found_user = True
        new_csv.append(line)
    if not found_user:
                line = f'{user};UNKNOWN;{timestamp}'
                new_csv.append(line)

    with open(f'{cit_dir}{date}.csv', 'w') as _f:
        _f.writelines(new_csv)

    return "Thank you!"


def main(cit_dir="~/cit/"):

    cit_dir = dir_check(cit_dir)

    window_name = 'webcam-stream'

    capture = cv2.VideoCapture(0)

    detector = cv2.QRCodeDetector()

    cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
    cv2.moveWindow(window_name, 1, 1)

    last_checkin = ''

    while True:
        ret, frame = capture.read()


        if ret:
            cv2.imshow(window_name, frame)
            data, bbox, _ = detector.detectAndDecode(frame)

            if data:
                if data != last_checkin:
                    last_checkin = data
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                    response = check_in(data, timestamp, cit_dir)

                    notify(response, data)

            cv2.waitKey(1)


if __name__ == '__main__':
    main()
