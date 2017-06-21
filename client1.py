import sys
import socket
import select


def chat_client():
    if (len(sys.argv) < 2):
        print 'Usage : python client1.py port'
        sys.exit()

    host = '127.0.0.1'
    port = int(sys.argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to host
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()

    print 'Connected to host. You can now send messages to chat.'
    sys.stdout.write('[You] ');
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data)
                    sys.stdout.write('[You] ');
                    sys.stdout.flush()

            else:
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[You] ');
                sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(chat_client())