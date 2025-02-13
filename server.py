from datetime import datetime

from flask import Flask, request

app = Flask('app')

db = {}


def date_check():
    date = datetime.now().strftime('%Y %m %d')

    for entry in db:
        if entry != date:
            db.pop(entry)

    if date not in db:
        with open('users.txt') as _f:
            lines = _f.readlines()
        ids = []
        for line in lines:
            line = line.rsplit('\n')[0]
            ids.append(line)

        db.update({date: {'checked_in': {}, 'not_checked_in': ids, 'unknown': {}}})
    return date


@app.route('/')
def index():
    date = date_check()
    html_head = '<html><head><title>checkin</title></head><body>'
    html_tail = '</body></html>'
    body = []
    body.append('<h2>Checked in</h2>')
    for entry in db[date]['checked_in']:
        body.append(f'<p> {db[date]["checked_in"][entry]} : {entry}</p>')
    body.append('<h2>Not checked in</h2>')
    for _id in db[date]['not_checked_in']:
        body.append(f'<p>{_id}</p>')

    if db[date]['unknown']:
        body.append('<h2>Unknown IDs</h2>')
        for entry in db[date]['unknown']:
            body.append(f'<p>{db[date]["unknown"][entry]} : {entry}</p>')

    body = '\n'.join(body)

    return f'{html_head}\n{body}\n{html_tail}'

@app.route('/listen', methods=['POST'])
def listen():
    date = date_check()
    json_dict = request.get_json(force=True)
    if "user" not in json_dict:
        return "Missing required key 'user'", 400
    if "timestamp" not in json_dict:
        return "Missing required key 'timestamp'", 400
    user = json_dict['user']
    timestamp = json_dict['timestamp']
    if user not in db[date]['checked_in']:
        if user in db[date]['not_checked_in']:
            print(user)
            db[date]['not_checked_in'].remove(user)
            db[date]['checked_in'].update({user: timestamp})
        else:
            db[date]['unknown'].update({user: timestamp})

    return "Accepted", 200


if __name__ == '__main__':
    _ = date_check()
    print(db)
    app.run(
            debug=True,
            host='0.0.0.0',
            port=5003,
            )
