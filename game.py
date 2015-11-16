from stockings import stockings
import pickle, random, string, datetime
from multiprocessing import Process

class Token:
    def __init__(self, name = 'Null', token = 'N', attacks = {}):
        self.name = name
        self.token = token
        self.attacks = attacks
    def player(self, player):
        self.player = player
    def attack(self, token):
        pass

class Board:
    def __init__(self, width = 8, height = 8):
        self.tokens = [[0 for i in range(width)] for ii in range(height)]
        self.width = width
        self.height = height
    def move(self, origin, destination):
        pass
    def rand(self):
        """
        Return a random pair of coordinates.
        """
        return random.randint(0, self.height - 1), random.randint(0, self.width - 1)
    def token(self, tokens, player):
        for i in tokens:
            for ii in range(int(i['count'])):
                token = Token(i['name'], i['token'], i['hit'])
                token.player(player)
                x, y = self.rand()
                while not self.tokens[x][y] == 0:
                    x, y = self.rand()
                self.tokens[x][y] = token

class Player:
    def __init__(self):
        self.id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(32))

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
        # Create empty connection list
        self.connections = []
        # Has game started
        self.started = False

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
                try:
                    print('Connecting client %i.' % (len(self.connections) + 1))
                    client = ClientState.clone(data)
                    self.board.token(self.config['tokens'], client.player)
                    client.board = self.board
                    self.connections.append(client)
                    if len(self.connections) == 2:
                        print('Setting turn')
                        client.turn = self.connections[0].player.id
                except Exception as e:
                    print(e)
                print('Returning connection.')
                return pickle.dumps(client)
            else:
                print('Session overpopulated.')
                return pickle.dumps(ClientState.message('Overpopulated'))
        # Handle closing session
        elif data.close:
            print('Closing client session.')
            self.server.close()
        else:
            print('Normal operation')
            try:
                client = ClientState.clone(data)
                if data.turn == self.connections[0].player.id:
                    print('%s to %s' % (data.turn, self.connections[0].player.id))
                    client.turn = self.connections[1].player.id
                else:
                    print('%s to %s' % (data.turn, self.connections[1].player.id))
                    client.turn = self.connections[0].player.id
                return pickle.dumps(client)
            except Exception as e:
                print(e)

class ClientState(State):
    def __init__(self):
        State.__init__(self)
        self.new = False
        self.close = False
        self.over = False
        self.text = 'Hello'
        self.turn = 0
        self.player = Player()
    def message(self, message = ''):
        """
        Send a plain ClientState for the purpose of sending a message.
        """
        clean = ClientState()
        clean.new = message == 'New'
        clean.close = message == 'Close'
        clean.over = message == 'Overpopulated'
        clean.text = message
        clean.board = self.board
        clean.player = self.player
        clean.turn = self.turn
        return clean
    def clone(data):
        """
        Creates a ClientState object from a pickle.

        data: Pickled object.
        """
        clean = ClientState()
        clean.new = data.new
        clean.close = data.close
        clean.over = data.over
        clean.text = data.text
        clean.board = data.board
        clean.player = data.player
        clean.turn = data.turn
        return clean
    def connect(self, server, port):
        print('Establishing client connection.')
        self.client = stockings.SocketClient(server, int(port), 4096)
        self.client.connect()
    def listen(self):
        print('Establing client listener.')
        self.client.start(self.game)
        print('Closing listener')
    def start(self):
        # Establish a connection to the server
        try:
            self.client.send(pickle.dumps(self.message('New')))
        except:
            print('Closing connection.')
            self.client.send(pickle.dumps(self.message('Close')))
            self.client.close()
            self.listener.join()
            return False
    def game(self, pickle_dump):
        data = pickle.loads(pickle_dump)
        print('%s: %s says %s' % (str(datetime.datetime.utcnow()), data.player.id, data.text))
        try:
            if data.over:
                print('Server overpopulated.')
                return
            else:
                self.client.send(pickle.dumps(self.message(self.player.id)))
        except Exception as e:
            print(e)
