import pytest
from messenger import Messenger
import threading

def test_poll_message():
    event = threading.Event()
    url = 'http://localhost:3000'
    user = 'tester'
    msgr = Messenger(url, user)
    
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
    
    result = msgr.send_message(message)
    
    assert result == True