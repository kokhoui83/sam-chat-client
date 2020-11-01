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
        result = th.join()
        
        assert result == None

def test_send_message():
    url = 'http://localhost:3000'
    user = 'tester'
    message = 'testing'
    msgr = Messenger(url, user)

    with requests_mock.Mocker() as m:
        data = { 'status': 'ok', 'chat': { 'user': user, 'message': message }}
        m.post(f'{url}/chat', text=json.dumps(data))

        result = msgr.send_message(message)
        
        assert result['status'] == data['status']
        assert result['chat'] == data['chat']