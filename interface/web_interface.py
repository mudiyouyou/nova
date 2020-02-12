# coding=utf-8
import threading

from flask import Flask, jsonify
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import json
from service import app_service

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sockets = Sockets(app)

tail_task = dict()

tail_lock = threading.Condition()


@sockets.route('/ws')
def on_connect(ws):
    while not ws.closed:
        message = ws.receive()  # 接收到消息
        if message is not None:
            try:
                if message.startswith("&cmd"):
                    msg = message.split(",")
                    if msg[1] == "log" and ws not in tail_task:
                        app_name = msg[2]
                        tail_lock.acquire()
                        tail = app_service.get_tail_of_log(app_name)
                        tail_task[ws] = tail
                        tail_lock.release()
                        tail.register_callback(lambda log_msg: ws.send(log_msg))
                        tail.start()
            except Exception as e:
                print(e)
        else:
            if ws in tail_task:
                tail_lock.acquire()
                tail_task[ws].stop()
                del tail_task[ws]
                tail_lock.release()


@app.route("/api/install/<app_name>/<file_name>", methods=["GET"])
def install(app_name, file_name):
    app_service.install(app_name, file_name)
    return jsonify({"code": 0, "data": "执行成功"})


@app.route("/api/uninstall/<app_name>", methods=["GET"])
def uninstall(app_name):
    app_service.uninstall(app_name)
    return jsonify({"code": 0, "data": "执行成功"})


@app.route("/api/start/<app_name>", methods=["GET"])
def start(app_name):
    app_service.start(app_name)
    return jsonify({"code": 0, "data": "执行成功"})


@app.route("/api/stop/<app_name>", methods=["GET"])
def stop(app_name):
    app_service.stop(app_name)
    return jsonify({"code": 0, "data": "执行成功"})


def start(port=8080):
    server = pywsgi.WSGIServer(('0.0.0.0', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
