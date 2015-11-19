#!/bin/env python3
import game
import argparse, time
from multiprocessing import Process
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import StringProperty

class Input():
    pass

class View(BoxLayout):
    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
        self.btn = Button(text='Cat')
        self.btn.bind(on_press=self.message)
        self.add_widget(self.btn)
    def message(self, message):
        self.btn.text = 'Kivy totally sucks'
        self.add_widget(Button(text=message))
        try:
            self.btn.text = message
            self.btn.canvas.ask_update()
        except Exception as e:
            print(e)
    def board(self, board, player):
        for i in tokens:
            for ii in range(int(i['count'])):
                token = Token(i['name'], i['token'], i['hit'])
                token.player(player)
                x, y = self.rand()
                while not self.tokens[x][y] == 0:
                    x, y = self.rand()
                self.tokens[x][y] = token

class ClientApp(App):
    def build(self):
        self.view = View()
        run = True
        if run:
            self.client = game.ClientState()
            self.client.setIO(self.view, Input())
            self.client.connect(args.server, args.port)
            self.listener = Process(target=self.client.listen)
            self.listener.start()
            print('Waiting 10 seconds to connect.')
            time.sleep(10)
            print('Connect.')
            self.connection = Process(target=self.client.start)
            self.connection.start()
        else:
            self.view.message('1')
            self.view.message('2')
            self.view.message('3')
            pass
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
