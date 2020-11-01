import pytest
import requests_mock
import json
import threading

from messenger import Messenger

def test_poll_message():
    event = threading.Event()
    url = 'http://localhost:3000'
    user = 'tester'
    msgr = Messenger(url, user)

    with requests_mock.Mocker() as m:
        m.get(f'{url}/chat', text=json.dumps({ 'status': 'ok', 'chats': [], 'lastupdate': 12345678 }))

        th = threading.Thread(target=msgr.poll_message, args=(event,))
        th.start()
        event.set()
        th.join()

def test_send_message_success():
    url = 'http://localhost:3000'
    user = 'tester'
    message = 'testing'
    msgr = Messenger(url, user)

    with requests_mock.Mocker() as m:
        data = { 'status': 'ok', 'chat': { 'user': user, 'message': message }}
        m.post(f'{url}/chat', status_code=201,text=json.dumps(data))

        result = msgr.send_message(message)
        
        assert result['status'] == data['status']
        assert result['chat'] == data['chat']

def test_send_message_missing_param():
    url = 'http://localhost:3000'
    user = 'tester'
    message = None
    msgr = Messenger(url, user)

    with requests_mock.Mocker() as m:
        data = { 'error': 'missing parameter user or message' }
        m.post(f'{url}/chat', status_code=400,text=json.dumps(data))

        result = msgr.send_message(message)
        
        assert result == None

def test_send_message_server_error():
    url = 'http://localhost:3000'
    user = 'tester'
    message = 'testing'
    msgr = Messenger(url, user)

    with requests_mock.Mocker() as m:
        data = { 'error': 'server error' }
        m.post(f'{url}/chat', status_code=500,text=json.dumps(data))

        result = msgr.send_message(message)
        
        assert result == None