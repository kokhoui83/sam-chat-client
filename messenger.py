import requests
import json
from datetime import datetime
import time

class Messenger:
    def __init__(self, url, user):
        self.url = url
        self.user = user
        self.lastupdate = 0
    
    def poll_message(self, event):
        while not event.is_set():
            params = { 'user': self.user, 'lastupdate': self.lastupdate }

            try:
                response = requests.get(f'{self.url}/chat', params=params)

                if response.status_code == 200:
                    data = json.loads(response.text)

                    chats = data['chats']
                    self.lastupdate = data['lastupdate']

                    for chat in chats:
                        print('%s %s: %s' %(datetime.fromtimestamp(chat['timestamp']).isoformat(), chat['user'], chat['message']))
                elif response.status_code == 400:
                    print(response.text)
                else:
                    print('server error')

            except Exception as e:
                print('failed to poll message from server', e)
                pass
            
            time.sleep(1)
    
    def send_message(self, message):
        data = json.dumps({ 'user': self.user, 'message': message })
        try:
            response = requests.post(f'{self.url}/chat', data=data)

            if response.status_code == 201:
                return json.loads(response.text)
            elif response.status_code == 400:
                print(response.text)
            else:
                print('server error')
        except Exception as e:
            print('faild to send message to server', e)
            pass