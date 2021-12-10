import pytest
import sys
import os
import unittest
import unittest.mock
import socket
import threading
from serverlib.chat import *

# test ChatServer
class TestChatServer(unittest.TestCase):

    # test constructor
    def test_constructor(self):
        server = ChatServer(socket.gethostbyname(socket.gethostname()),9999)
        self.assertEqual(server.host,socket.gethostbyname(socket.gethostname()))
        self.assertEqual(server.port,9999)
        self.assertEqual(server.clients,list())
# test ChatClient
class TestChatClient(unittest.TestCase):

    #test constructor
    def test_constructor(self):
        pass

      

    


