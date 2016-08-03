import run
import flask
from task import TaskManager
from flask import Flask
from flask.helpers import url_for
from flask.templating import render_template

plan = Flask(__name__)
tasks = TaskManager()

@plan.route('/')
@plan.route('/index')
def index():
    return plan.send_static_file('index.html')

@plan.route('/getTasks', methods=['GET', 'POST'])
def getTasks():
    name = flask.request.form.get('name')
    tasks.register(name)
    print(name)
    
    resp = flask.make_response(tasks.generateJson())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


