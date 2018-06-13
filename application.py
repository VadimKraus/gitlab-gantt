from flask import Flask, jsonify, render_template

from gitlab_tools import GitLabTools

app = Flask(__name__)
app.config.from_pyfile('.env', silent=True)


@app.route('/')
def welcome():
    return render_template('welcome.jinja2')


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
