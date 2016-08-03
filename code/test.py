from flask import Flask
import flask
import time
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():   
    value = flask.request.values.get('name', '')  
    data = value + '   ' + time.strftime('%H:%M:%S')  
    resp = flask.make_response(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5050)
