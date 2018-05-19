#!/usr/bin/env python

#   Python libraries
import socket
import select
import threading

#   My classes
from client import Client

class Listener(object):
    """ Listens to the server and calls a function whenever a message
    is received. """

    def __init__(self):

        #   Attempt to connect to server
        connected = False

        while not connected:
            try:
                self.server_ip = input("Input server IP address: ")
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                Port = 52801
                self.server.connect((self.server_ip,Port))
                connected = True
            except socket.gaierror:
                print("Something went wrong. Try another IP.")

        #   Keep listening until you get a response
        self.id = None
        while not self.id:
            message = self.server.recv(1024)
            if message:
                print("Connection established. ")
                print("Player ID: %s" % message.decode())
                self.id = int(message.decode())

        #   Send player name to server
        self.name = input("Input a name:")
        self.server.send(self.name.encode())

        print("Waiting for the host to start the game...")
        self.players = self.server.recv(2048).decode()
        print("Game started! Opening game in new window.")

        #   Open client.
        self.client = Client()
        listen_thread = threading.Thread(target = self.listen_for_messages)
        listen_thread.start()
        self.client.demo_card(self.players, self.name)

    def main(self):
        pass

    def listen_for_messages(self):
        """ Listens for incoming messages and sends them to the clients. """

        while True:
            msg = self.server.recv(2048)
            if msg:
                print("%s received the following message: %s" % (self.name, msg.decode()))
                self.client.read_msg(msg.decode())

if __name__ == '__main__':
    a = Listener()
