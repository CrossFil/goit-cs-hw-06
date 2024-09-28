from flask import Flask, render_template, request, send_from_directory, abort
import socket
import json
import os
from multiprocessing import Process
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Сторінка з формою
@app.route('/message.html')
def message():
    return render_template('message.html')

# Обробка форми
@app.route('/message', methods=['POST'])
def send_message():
    username = request.form['username']
    message = request.form['message']
    data = json.dumps({'username': username, 'message': message})
    
    # Відправляємо дані на Socket-сервер
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data.encode(), ('localhost', 5000))
    sock.close()

    return "Message sent!"

# Статичні файли
@app.route('/style.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'style.css')

@app.route('/logo.png')
def serve_logo():
    return send_from_directory(os.getcwd(), 'logo.png')

# Обробка 404 помилки
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# Socket-сервер
def socket_server():
    client = MongoClient('mongo', 27017)  # Підключення до MongoDB всередині Docker
    db = client['messages_db']
    collection = db['messages']

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5000))

    while True:
        data, addr = sock.recvfrom(1024)
        message = json.loads(data.decode())
        message['date'] = str(datetime.now())
        collection.insert_one(message)
        print(f"Received and saved message: {message}")

if __name__ == '__main__':
    # Запуск Socket-сервера у окремому процесі
    p = Process(target=socket_server)
    p.start()
    # Запуск HTTP-сервера Flask
    app.run(host='0.0.0.0', port=3000)
    p.join()
