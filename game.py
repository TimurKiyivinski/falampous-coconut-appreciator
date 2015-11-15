from stockings import stockings
import pickle
from multiprocessing import Process, Queue

class Token:
    def __init__(self, name = 'Null', token = 'N', attacks = []):
        self.name = name
        self.token = token
        self.attacks = attacks
        pass
    def owner(self, player):
        self.player = player.id
    def attack(self, token):
        pass

class Board:
    def __init__(self, width = 8, height = 8):
        self.tokens = [[[] for i in range(width)] for ii in range(height)]
        pass
    def move(self, origin, destination):
        pass
    def tokens(self, tokens):
        #TODO: Create a token start function

class Player:
    def __init__(self):
        pass

class Input:
    def __init__(self):
        pass

class View:
    def __init__(self):
        pass
    def message(self, message):
        pass
    def board(self, board):
        pass

class State:
    def __init__(self):
        self.board = []
        pass

class GameState(State):
    def __init__(self, board, tokens, port):
        State.__init__(self)
        self.config = {}
        self.config['board'] = board
        self.config['tokens'] = tokens
        self.config['port'] = port

    def start(self):
        # Create server
        self.server = stockings.SocketServer(int(self.config['port']), 4096)
        # Create game board
        self.board = Board(int(self.config['board']['width']), int(self.config['board']['height']))
        # Create board tokens
        # self.board.tokens(self.config['tokens'])
        # Create empty connection list
        self.connections = []

        # Start server
        try:
            self.server.start(self.game)
        except KeyboardInterrupt:
            self.server.close()
            return False

    def game(self, pickle_dump):
        # Unpicked received data
        data = pickle.loads(pickle_dump)
        # Handle new connection
        if data.new:
            if len(self.connections) < 2:
                print('Connecting client.')
                self.connections.append(data)
                #TODO: Return confirmation ClientState
                print('Done')
            else:
                print('Session overpopulated.')
                #TODO: Return failed ClientState
        # Handle closing session
        elif data.close:
            print('Closing client session.')
            self.server.close()
        # Handle normal request
        else:
            print('Player %s says: %s' % data.name, "Cat")
            self.server.broadcast(data.copy())
            #TODO: Return game ClientState

class ClientState(State):
    def __init__(self):
        State.__init__(self)
        self.new = True
        self.close = False
    def interface(self, view, input):
        """
        Override view and input classes.
        This is possible if function compatibility is maintained.
        See help() for more information.
        """
        pass
    def copy(self, message = ''):
        clean = ClientState()
        clean.new = message == 'New'
        clean.close = message == 'Close'
        clean.board = self.board
        clean.name = "BOB"
        clean.message = "BOB"
        return clean
    def clone(self, data):
        #TODO: Create function that can clone itself from a pickle
    def start(self, server, port):
        # Establish a connection to the server
        self.client = stockings.SocketClient(server, int(port), 4096)
        self.client.connect()
        self.listener = Process(target=self.client.start, args=(self.game,))
        self.listener.start()
        try:
            print('Requesting new game session.')
            self.client.send(pickle.dumps(self.copy('New')))
        except KeyboardInterrupt:
            self.client.close()
            self.listener.join()
            return False
        self.listener.join()
    def game(self, data):
        print('Client game')
        if data.player.id = self.player.id:
            #TODO: Your turn
        else:
            #TODO: wait for other player
        pass
