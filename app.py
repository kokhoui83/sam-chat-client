import argparse
import threading
from messenger import Messenger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sam chat client')
    parser.add_argument('-u', '--user', help='user help', required=True)
    parser.add_argument('-s', '--server', help='server help', required=False)
    
    args = parser.parse_args()
    user = args.user
    
    if not args.server == None:
        server = args.server
    else:
        server = 'http://localhost:3000'
    
    print('welcome', user)

    msgr = Messenger(server, user)
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
