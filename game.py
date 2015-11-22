from stockings import stockings
import pickle, random, string, datetime
from multiprocessing import Process
import sys

class Token:
    def __init__(self, name = 'Null', token = 'N', attacks = {}):
        self.name = name
        self.token = token
        self.xp = 0
        self.attacks = attacks
    def player(self, player):
        self.player = player
    def attack(self, token):
        for attack in self.attacks:
            if attack['name'] == token.name:
                determine = random.randint(0, 100) / 100
                power = self.xp + float(attack['value'])
                if power > determine:
                    self.xp += 0.1
                    return self
                else:
                    token.xp += 0.1
                    return token
        return self

class Board:
    def __init__(self, width = 8, height = 8):
        self.tokens = [[0 for i in range(width)] for ii in range(height)]
        self.width = width
        self.height = height
    def move(self, origin, destination, player):
        try:
            from_x, from_y = origin.split()
            to_x, to_y = destination.split()
            from_x, from_y = int(from_x), int(from_y)
            to_x, to_y = int(to_x), int(to_y)
        except Exception as e:
            return False
        # Invalid: Cannot move from 0
        if self.tokens[from_x][from_y] == 0:
            return False
        # Check if token belongs to user
        if self.tokens[from_x][from_y].player.id == player.id:
            # Move to a blank space
            if self.tokens[to_x][to_y] == 0:
                self.tokens[to_x][to_y], self.tokens[from_x][from_y] = self.tokens[from_x][from_y], self.tokens[to_x][to_y]
                return True
            # Attack enemy
            elif self.tokens[to_x][to_y].player.id != player.id:
                self.tokens[to_x][to_y] = self.tokens[from_x][from_y].attack(self.tokens[to_x][to_y])
                self.tokens[from_x][from_y] = 0
                return True
            else:
                return False
        else:
            return False
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
    def count(self, player):
        count = 0
        for i in range(0, self.height):
            for ii in range(0, self.width):
                if self.tokens[i][ii] == 0:
                    continue
                elif self.tokens[i][ii].player.id == player.id:
                    count += 1
        return count

class Player:
    def __init__(self):
        self.id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(32))

class Input:
    def __init__(self):
        pass
    def get(self):
        pass

class View:
    def __init__(self):
        pass
    def message(self, message):
        pass
    def board(self, board, player):
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
                    self.connections.append(client)
                    if len(self.connections) == 2:
                        self.board.token(self.config['tokens'], self.connections[0].player)
                        self.board.token(self.config['tokens'], client.player)
                        client.board = self.board
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
        self.board = []
        self.player = Player()
        self.win = False
    def setIO(self, user_view, user_input):
        self.view = user_view
        self.input = user_input
    def message(self, message = ''):
        """
        Send a plain ClientState for the purpose of sending a message.
        """
        clean = ClientState()
        clean.new = message == 'New'
        clean.close = message == 'Close'
        clean.over = message == 'Overpopulated'
        clean.win = message == 'Lost'
        clean.text = message
        clean.board = self.board
        clean.player = self.player
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
        clean.win = data.win
        clean.text = data.text
        clean.board = data.board
        clean.player = data.player
        return clean
    def connect(self, server, port):
        self.client = stockings.SocketClient(server, int(port), 4096)
        self.client.connect()
    def listen(self):
        self.client.start(self.game)
    def start(self):
        # Establish a connection to the server
        try:
            self.client.send(pickle.dumps(self.message('New')))
        except:
            self.client.send(pickle.dumps(self.message('Close')))
            self.client.close()
            return False
    def game(self, pickle_dump):
        data = pickle.loads(pickle_dump)
        self.view.message('%s: %s says %s' % (str(datetime.datetime.utcnow()), data.player.id, data.text))
        try:
            if data.board != []:
                self.board = data.board
                self.view.board(data.board, self.player)
        except Exception as e:
            print(e)
            return e
        try:
            if data.over:
                return
            elif data.win:
                self.view.message('You win!')
                return
            else:
                if data.board != []:
                    self.turn()
                    self.client.send(pickle.dumps(self.message(self.text)))
                else:
                    return
        except Exception as e:
            print(e)
    def turn(self):
        if self.board.count(self.player) == 0:
            self.view.message('You lose!')
            self.client.send(pickle.dumps(self.message('Lost')))
            self.client.close()
            return False
        complete = False
        while not complete:
            self.view.message("Token from [X Y]:")
            origin = self.input.get()
            self.view.message("Token to [X Y]:")
            destination = self.input.get()
            complete = self.board.move(origin, destination, self.player)
            if complete:
                self.view.message('Valid move')
                self.view.board(self.board, self.player)
                self.text = "moved from %s to %s" % (origin, destination)
            else:
                self.view.message('Invalid move')

