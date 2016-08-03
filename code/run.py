from flask import Flask  
import views

if __name__ == '__main__':
    views.plan.run('0.0.0.0', debug=True, port=5050)