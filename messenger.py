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
                data = json.loads(response.text)

                chats = data['chats']
                self.lastupdate = data['lastupdate']

                for chat in chats:
                    print('%s %s: %s' %(datetime.fromtimestamp(chat['timestamp']).isoformat(), chat['user'], chat['message']))
                
                time.sleep(1)
            except Exception as e:
                print('failed to poll message from server')
                print(e)
                pass
    
    def send_message(self, message):
        data = json.dumps({ 'user': self.user, 'message': message })
        try:
            response = requests.post(f'{self.url}/chat', data=data)
            return json.loads(response.text)
        except Exception as e:
            print('faild to send message to server')
            pass