from flask import Flask, session, redirect, url_for, request, abort

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else:
        return '''
            <form method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''


@app.route('/sync', methods=['GET', 'POST'])
def sync():
    if request.method == 'POST':
        return 'asdf'
    else:
        abort(400, 'Missing request body.')


app.run()
