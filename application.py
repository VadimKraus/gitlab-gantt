import os
from functools import wraps

from flask import Flask, jsonify, render_template, request, g, redirect
from flask_wtf import CSRFProtect

from gitlab_tools import GitLabTools

app = Flask(__name__)
app.config.from_pyfile('.env', silent=True)
csrf = CSRFProtect(app)


def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if (
                'GITLAB_URL' not in os.environ or
                'GITLAB_PRIVATE_TOKEN' not in os.environ
        ):
            return redirect('/login')
        else:
            return f(*args, **kwargs)

    return decorated


@app.route('/')
@check_token
def welcome():
    return render_template('welcome.jinja2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        os.environ['GITLAB_URL'] = request.form['gitlab_url']
        os.environ['GITLAB_PRIVATE_TOKEN'] = request.form['token']
        g.gitlab_url = request.form['gitlab_url']
        return welcome()
    else:
        return render_template('login.jinja2')


@app.route('/api/milestones')
def milestones():
    glt = GitLabTools()
    return jsonify(glt.list_all_milestones())


@app.route('/api/issues')
def issues():
    glt = GitLabTools()
    return jsonify(glt.list_all_issues())


if __name__ == '__main__':
    app.run()
