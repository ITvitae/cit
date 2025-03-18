'''
check-in terminal server
check-in terminal client talks to this server to keep track of what
users have (not) checked in.
'''


from datetime import datetime

from flask import Flask, request, jsonify


class Userdata:
    def __init__(self, group):
        self.group = group
        self.check_in_time = None


class Database:
    def __init__(self):

        # Set the database date
        self.date =  datetime.now().strftime('%Y %m %d')

        # Configure from users.txt
        group = None
        with open('users.txt', 'r') as _f:
            lines = _f.readlines()
        ids = {}
        groups = []
        for line in lines:
            if line.startswith('#'):
                continue
            line = line.rsplit('\n')[0]
            if not line:
                continue
            if line.startswith('@'):
                line = line[1:]
                if not line.strip():
                    continue
                group = line
                if not group in groups:
                    groups.append(group)
                continue
            if not group:
                group = 'No group set'
                if not group in groups:
                    groups.append(group)
            ids.update({
                line: Userdata(group)
            })

        self.groups = groups
        self.groups.sort()

        sorted_ids = {}
        for _id in sorted(ids):
            sorted_ids.update({_id: ids[_id]})
        self.ids = sorted_ids

        # Set up a fallback group for unknown identities
        self.unknown = {}


app = Flask('cit server')
app.db = Database()


@app.route('/')
@app.route('/<mode>')
def index(mode='html'):

    data = {}
    for group in app.db.groups:
        data.update({group: []})

    if mode == 'json':
        for group in app.db.groups:
            data.update({group: {}})
        for user in app.db.ids:
            data[app.db.ids[user].group].update({user: app.db.ids[user].check_in_time})
        return jsonify(data)
    else:
        for group in app.db.groups:
            data.update({group: []})
        for user in app.db.ids:
            data[app.db.ids[user].group].append((user, app.db.ids[user].check_in_time))

    html_head = '''<!doctype HTML>
<html>
    <head>
    <title>Check-in terminal</title>
    <style>
    html {
    font-family: sans-serif;
    }
    table {
    background: #333333;
    color: white;
    }
    td {
    color: #000000;
    }
    #tables {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-evenly;
    align-items: flex-start;
    align-content: center;
    }
    .not_checked_in {
    background-color: #FFCCCC;
    }
    .checked_in {
    background-color: #DAF7A6;
    }
    </style>
    </head>
<body>'''
    html_tail = '</body></html>'



    body = []
    body.append(f'<h2>{app.db.date}</h2>')
    body.append('<div id="tables">')

    for group in data:
        body.append('<table>')
        body.append(f'<tr><th>{group}</th></tr>')
        for user in data[group]:
            markup = 'class="not_checked_in"'
            if user[1]:
                markup = 'class="checked_in"'
            body.append(f'<tr {markup}><td>{user[0]}</td><td>{user[1]}</td></tr>')
        body.append('</table>')

    if app.db.unknown:
        body.append('<table>')
        body.append(f'<tr><th>Unknown entries</th></tr>')
        for user in app.db.unknown:
            body.append(f'<tr class="checked_in"><td>{user}</td><td>{app.db.unknown[user]}</td></tr>')
        body.append('</table>')

    body.append('</div>')

    body = '\n'.join(body)

    return f'{html_head}\n{body}\n{html_tail}'


@app.route('/listen', methods=['POST'])
def listen():

    json_dict = request.get_json(force=True)

    if 'user' not in json_dict:
        return "Missing required key 'user'", 400

    if 'timestamp' not in json_dict:
        return "Missing required key 'timestamp'", 400

    user = json_dict['user']
    timestamp = json_dict['timestamp']

    if user in app.db.ids:
        if not app.db.ids[user]['check_in_time']:
            app.db.ids[user]['check_in_time'] = timestamp
    else:
        if user not in app.db.unknown:
            app.db.unknown.update({user: timestamp})

    return 'Accepted', 200


if __name__ == '__main__':
    app.run(
            debug=True,
            host='127.0.0.1',
            port=5003,
            )
