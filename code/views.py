import run
import flask
from task import TaskManager
from flask import Flask
from flask.helpers import url_for
from flask.templating import render_template
import os,sys

os.chdir(os.path.dirname(sys.argv[0]))
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
    
    resp = flask.make_response(tasks.generateJson())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


import autoCompile.log
compileLog = autoCompile.log.Log()

@plan.route('/autoCompile/sendLog', methods=['POST'])
def sendLog():
    data = flask.request.form.get('log')
    compileLog.send(data)
    return 'success'

@plan.route('/autoCompile/receiveLog', methods=['GET', 'POST'])
def receiveLog():
    resp = flask.make_response(compileLog.receive())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

