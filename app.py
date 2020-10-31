import threading
import argparse
from messenger import Messenger

SERVER = 'http://localhost:3000'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sam chat client')
    parser.add_argument('-u', '--user', help='user help', required=True)
    
    args = parser.parse_args()
    user = args.user
    print('welcome', user)

    msgr = Messenger(SERVER, user)
    event = threading.Event()
    th = threading.Thread(target=msgr.poll_message, args=(event,))
    th.start()

    while True:
        data = input()
        if not data:
            break
        # clean previous line and place cursor onto beginning of the line
        print('\033[A                             \033[A')
        msgr.send_message(data)

    event.set()
    th.join()
    print('exiting..')
