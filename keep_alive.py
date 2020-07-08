from flask import Flask
from threading import Thread
from flask import request

app = Flask('')

@app.route('/')
def home():
    return "BayaBot is hosted by UptimeRobot!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

def shutdown_server():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
    raise RuntimeError('Wrong Server Type')
  func()
@app.route('/shutdown', methods = ['POST'])
def shutdown():
  shutdown_server()
  return 'Server is shutting down'