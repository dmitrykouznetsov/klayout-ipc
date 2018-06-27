''' Used QTcpServer
    Current state: only way to stop serving is close the application
'''
import socket
import pya

import lyipc
from lyipc import PORT, quickmsg


global server_running
server_running = False


class KlayoutServer(pya.QTcpServer):
    def new_connection(self):
        try:
            # Handle incoming connection
            connection = self.nextPendingConnection()
            payload = ''
            while connection.isOpen() and connection.state() == pya.QTcpSocket.ConnectedState:
                # connection.waitForReadyRead(1000)
                if connection.canReadLine():
                    line = connection.readLine()
                    payload = line.rstrip('\n').rstrip('\r')
                    connection.write('ACK')
                else:
                    connection.waitForReadyRead(500)

            print('payload=', payload)

            # automatically delete when disconnected
            connection.disconnectFromHost()
            signal = pya.qt_signal("disconnected()")
            slot = pya.qt_slot("deleteLater()")
            pya.QObject.connect(connection, signal, connection, slot)

            # Do something with what was received
            from lyipc.interpreter import parse_command
            parse_command(payload)
        except Exception as ex: 
          print("ERROR " + str(ex))

    def __init__(self, port=PORT, parent=None):
        pya.QTcpServer.__init__(self, parent)
        ha = pya.QHostAddress()
        self.listen(ha, port)
        self.newConnection(self.new_connection)
        quickmsg(f'Server initialized with {ha}, {port}')



def stop_serving():
    global server_running
    server_running = False


def start_serving(port=PORT):
    ''' 
    '''
    # Check for existing one
    # global server_running
    # if server_running:
    #     quickmsg('Server already running')
    #     stop_serving()
    # server_running = True
    server = KlayoutServer()


# if __name__ == '__main__':
#     start_serving()

