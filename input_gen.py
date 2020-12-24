#!/usr/bin/env python3

import socket

def main():
    keepRunning = 1
    host = input("please enter server ip address\n")
    port = input("please enter server port\n")
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSock.settimeout(5)
    try:
        print("trying to connect with {}:{}".format(host, port))
        clientSock.connect((host, int(port)))
    except:
        print("failed to connect socket")
        keepRunning = 0
    
    if keepRunning:
        clientSock.setblocking(1)
        
    while keepRunning:
        choice = input("\nplease enter any valid option:\n"
                           "1\tto send person-in event\n"
                           "2\tto send person-out event\n"
                           "3\texit input generator\n")
        if choice == '3':
            print("okay... exiting... :(")
            break
        
        try:
            print("sending choice {} to server".format(choice))
            clientSock.send(choice.encode())
        except:
            print("failed to send event... exiting... :(")
            break
            
        try:
            print("waiting for response from server")
            response = clientSock.recv(1024)
        except:
            print("failed to recv event response... exiting... :(")
            break
        
        print("response from server: ", response.decode())
    
    clientSock.close()
        
if __name__ == "__main__":
    main()