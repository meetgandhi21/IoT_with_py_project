#!/usr/bin/env python3

import socket
import threading
import time
import os
import sys
import datetime
import queue

global gVar
global ledLight

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
OKYELLOW = '\033[93m'
OKRED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
    
def print_msg(data=''):
    th = threading.current_thread()
    try:
        colour = th.mColour
    except Exception as ignore:
        colour = OKRED
    print(colour + "[{}]\t".format(th.getName()) + data + ENDC)
    
class global_var():
    def __init__(self):
        self.gKeepRunning = 1
        self.pplCnt = 0
        self.syncLock = threading.Lock()

class led_light(threading.Thread):
    global gVar
    def __init__(self):
        threading.Thread.__init__(self)
        self.mColour = OKYELLOW
        self.mPplCnt = 0
        self.startTm = self.endTm = datetime.datetime.now()
        self.mEventQueue = queue.Queue()
        self.setName("Light Handler")
        self.start()
        
    def run(self):
        while gVar.gKeepRunning:
            try:
                curCnt = self.mEventQueue.get(timeout=1)
            except queue.Empty as timeout:
                continue
            else:
                if curCnt == self.mPplCnt:
                    continue
                
                curTm = datetime.datetime.now()
                if curCnt > self.mPplCnt:
                    print_msg("someone entered in room at [{}]".format(curTm))
                else:
                    print_msg("someone exited from room at [{}]".format(curTm))
                
                if 0 == self.mPplCnt:
                    self.startTm = curTm
                    print_msg("light started at [{}]".format(curTm))
                elif 0 == curCnt:
                    self.endTm = curTm
                    print_msg("light stopped at [{}], was active for [{}] seconds".format(curTm,
                          self.endTm.timestamp()-self.startTm.timestamp()))
                else:
                    print_msg("light is active since [{}] seconds".format(
                            curTm.timestamp()-self.startTm.timestamp()))
                    
                self.mPplCnt =  curCnt

class client_socket(threading.Thread):
    global gVar
    global ledLight
    
    def __init__(self, clientSock, clientAddr):
        threading.Thread.__init__(self)
        self.mColour = OKGREEN
        self.mSock = clientSock
        self.mAddr = clientAddr
        self.mSock.settimeout(1)
        self.setName("sensor-{}".format(self.mAddr[1]))
        self.start()
        
    def run(self):
        while gVar.gKeepRunning:
            try:
                sockData = self.mSock.recv(1024)
            except socket.timeout as timeOut:
                continue
            except socket.error as SockErr:
                print_msg("failed to accept connections")
                break
            else:
                event = sockData.decode()
                if 0 == len(event):
                    print_msg("sensor connection is closed")
                    break
                if self.hndl_event(event):
                    break

        print_msg("closing local connection for sensor {}".format(self.mAddr))
        self.mSock.close()
        
    def hndl_event(self, event):
        if '1' == event:
            gVar.syncLock.acquire()
            if 10 == gVar.pplCnt:
                resp = "only {} person can enter the room".format(gVar.pplCnt)
            else:
                gVar.pplCnt += 1
                ledLight.mEventQueue.put(gVar.pplCnt)
                resp = "person entered, total[{}]".format(gVar.pplCnt)
            gVar.syncLock.release()
        elif '2' == event:
            gVar.syncLock.acquire()
            if 0 == gVar.pplCnt:
                resp = "there's no one in the room"
            else:
                gVar.pplCnt -= 1
                ledLight.mEventQueue.put(gVar.pplCnt)
                resp = "person exited,total[{}]".format(gVar.pplCnt)
            gVar.syncLock.release()
        else:
            resp = "bad event {}".format(event)
            
        try:
            self.mSock.send(resp.encode())
        except socket.error as sockErr:
            print_msg("failed to send resp,err[{}]".format(sockErr))
            return 1
        print_msg("client[{}] event[{}] response[{}]".format(self.mAddr, event, resp))
        return 0

class server_socket(threading.Thread):
    global gVar
    global ledLight
    
    host = ''
    port = 0
    clientList = []
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.mColour = OKBLUE
        self.setName("rpi-server")
        try:
            self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSock.bind((self.host, self.port))
            self.serverSock.listen()
            self.serverSock.settimeout(1)
        except socket.error as sockErr:
            print_msg("failed to create server sock,err[{}]".format(sockErr))
            self.serverSock.close()
            return
        
        print_msg("socket created successfully [{}]".format(self.serverSock))
        self.start()
    
    def run(self):        
        while gVar.gKeepRunning:
            try:
                clientSock, clientAddr = self.serverSock.accept()
            except socket.timeout as timeOut:
                continue
            except socket.error as SockErr:
                print_msg("failed to accept connections, exiting !!!")
                break
            else:
                print_msg("connected from [{}]".format(clientAddr))
                self.clientList.append(client_socket(clientSock, clientAddr))
        
        for clientTh in self.clientList:
            clientTh.join()
        self.serverSock.close()

def main():
    global gVar
    global ledLight
    
    gVar = global_var()
    ledLight = led_light()

    tServerSock = server_socket()
    while gVar.gKeepRunning:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print_msg("keyboard interrupt")
            gVar.gKeepRunning = 0
    tServerSock.join()

if __name__ == "__main__":
    main()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)