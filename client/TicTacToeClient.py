from client.ConsoleTicTacToeInput import ConsoleInput
from client.ConsoleTicTacToeOutput import ConsoleTicTacToeOutput
from Message import OnlineMessage
import socket

dim = 3


class TicTacToeClient:
    def __init__(self, socket):
        self._inputCon = ConsoleInput()
        self._outputCon = ConsoleTicTacToeOutput()
        self.sock = socket
        self.listen()

    def listen(self):

        data = None
        message = None
        try:
            while data != b'':
                data = self.sock.recv(512)
        except:
            print("exc")

        message = OnlineMessage().decode(data)
        self.parse(message)

    def parse(self, message):

        flag = message.get_header()
        data = message.get_body()

        if flag == 'FI':
            self._outputCon.first(data)
        elif flag == 'SC':
            self._outputCon.second(data)
        elif flag == 'WE':
            self._outputCon.welcome()
        elif flag == 'DB':
            board = data
            self._outputCon.draw_board(board)
        elif flag == 'GM':
            coord = self._inputCon.get_player_move(dim)
            message = OnlineMessage('', coord)
            self.sock.send(message.encode())
        elif flag == 'PM':
            player = data.decode('utf-8')[-1]
            self._outputCon.player_move(data)
        elif flag == 'GC':
            coord = data.decode('utf-8')[-1]
            self._outputCon.get_coord(data)
        elif flag == 'WC':
            self._outputCon.wrong_coord(dim, data)
        elif flag == 'WM':
            self._outputCon.wrong_move()
        elif flag == 'CW':
            self._outputCon.congratulate_winner(data)
            self.sock.close()
        elif flag == 'DR':
            self._outputCon.announce_draw()
            self.sock.close()

        self.listen()

        # elif flag == 'GS':
        #     size = self._inputCon.get_board_size()
        #     self.s.send(bytes(size, 'utf-8'))

        # elif flag == 'WS':
        #     self._outputCon.wrong_size()