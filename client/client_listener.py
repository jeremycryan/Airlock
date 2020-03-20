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
                split = self.server_ip.split(":")
                if len(split) > 1 and is_integer(split[-1]):
                    self.server_ip = "".join(split[:-1])
                    Port = int(split[-1])
                else:
                    Port = 52801
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.connect((self.server_ip,Port))
                connected = True
            except socket.gaierror as s:
                print("Something went wrong. Try another IP.")

        #   Keep listening until you get a response
        self.id = None
        print()
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
        self.client.server_socket = self.server
        listen_thread = threading.Thread(target = self.listen_for_messages)
        listen_thread.start()
        self.main(self.run_game)

    def run_game(self):
        self.client.demo_card(self.players, self.name)

    def main(self, start_func):
        while True:
            start_func = start_func()

    def listen_for_messages(self):
        """ Listens for incoming messages and sends them to the clients. """

        while True:
            msg = self.server.recv(2048)
            if msg:
                print("%s received the following message: %s" % (self.name, msg.decode()))
                self.client.read_msg(msg.decode())


def is_integer(string):
    """ Returns true if the string is composed only of digits 0-9."""
    try:
        int(string)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    a = Listener()
