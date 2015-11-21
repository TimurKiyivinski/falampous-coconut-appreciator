#!/bin/env python3
import game
import argparse, time, string, random
from multiprocessing import Process
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread

class Input():
    pass

class View(BoxLayout):
    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
        self.btn = Button(text='Connect to Server')
        self.btn.bind(on_press=self.connect)
        self.add_widget(self.btn)
        self.text = 'Bibimbap'
        self.connected = False
    def connect(self, *args, **kwargs):
        if self.connected:
            return False
        print('Connection button triggered.')
        self.client = game.ClientState()
        self.client.setIO(self, Input())
        self.client.connect('127.0.0.1', 4096)
        self.listener = Process(target=self.client.listen)
        self.listener.start()
        self.connection = Process(target=self.client.start)
        self.connection.start()
    @mainthread
    def message(self, *args, **kwargs):
        try:
            self.text = args[0]
            self.btn.text = self.text
            print(self.text)
        except Exception as e:
            print(e)
    def board(self, board, player):
        return
        for i in range(0, board.height):
            for ii in range(0, board.width):
                if (board.tokens[i][ii] == 0):
                    print('.,', end='')
                else:
                    if board.tokens[i][ii].player.id == player.id:
                        print("%s%s" % (board.tokens[i][ii].token, "+"), end='')
                    else:
                        print("%s%s" % (board.tokens[i][ii].token, "-"), end='')
            print('\n', end='')

class ClientApp(App):
    def build(self):
        self.view = View()
        return self.view
    def join(self):
        self.listener.join()
        self.connection.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Medieval Battle Chess client application.')
    parser.add_argument('-s', '--server', help='Server IP', default='127.0.0.1', required=False)
    parser.add_argument('-p', '--port', help='Server Port', default='4096', required=False)
    parser.add_argument('-v', '--verbose', help='Verbose logging', action='store_true')
    args = parser.parse_args()
    ClientApp().run()
