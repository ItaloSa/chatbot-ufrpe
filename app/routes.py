import os
from app import app
from flask import jsonify, request
import requests

import json

from app.controllers.core import handle
from app.controllers.telegram import handle_message, set_webhook, healthcheck
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

@app.route('/')
def index():
    return jsonify({ 'message': 'Hello from ufrpe-bot-api' })

@app.route('/core/message', methods=['POST'])
def core_message():
    data = request.json
    response = handle(data['message'])
    return jsonify(response)

@app.route(f'/telegram/{TELEGRAM_TOKEN}', methods=['POST'])
def telegram_handle():
    data = request.json
    handle_message(data['message']['text'], data['message']['chat']['id'])
    return jsonify({'message': 'ok'})

@app.route('/telegram/setwebhook')
def setwebhook():
    set_webhook()
    return jsonify({'message': 'ok'})

@app.route('/telegram/healthcheck')
def health_check():
    response = healthcheck()
    return jsonify(response)
