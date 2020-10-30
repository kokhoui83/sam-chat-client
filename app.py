import threading
import time
from datetime import datetime
import json
import requests
import argparse

event = threading.Event()

def poll_message(user):
    lastupdate = 0

    while not event.is_set():
        response = requests.get('http://localhost:3000/chat', params={ 'user': user, 'lastupdate': lastupdate })
        data = json.loads(response.text)
        chats = data['chats']
        lastupdate = data['lastupdate']

        for chat in chats:
            print('%s %s: %s' %(datetime.fromtimestamp(chat['timestamp']).isoformat(), chat['user'], chat['message']))
        
        time.sleep(1)


def send_message(user, message):
    response = requests.post('http://localhost:3000/chat', data=json.dumps({ 'user': user, 'message': message }))
    # print(response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sam chat client')
    parser.add_argument('-u', '--user', help='user help', required=True)
    args = parser.parse_args()

    user = args.user
    print('welcome', user)

    th = threading.Thread(target=poll_message, args=(user,))
    th.start()

    while True:
        data = input()
        if not data:
            break
        # clean previous line and place cursor onto beginning of the line
        print('\033[A                             \033[A')
        send_message(user, data)

    event.set()
    th.join()
    print('exiting..')
