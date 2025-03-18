
from datetime import datetime
from json import dumps
from subprocess import run

import cv2
from requests import post


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

def main():

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
                    try:
                        json_dict = dumps (
                        {
                            "user": data,
                            "timestamp": timestamp
                            }
                                )
                    except TypeError:
                        notify("Fatal error", "Unusable data in QR code!", "critical")
                        cv2.waitKey(1)
                        continue
                    r = post("http://localhost:5003/listen", data=json_dict)

                    notify("Hello and thank you!", data)

            cv2.waitKey(1)


if __name__ == '__main__':
    main()
