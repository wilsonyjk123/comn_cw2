from socket import *
import time
import sys


def Receiver(port, fileName):
    lastPacket = False
    lastPacketFlag = False
    data = bytearray()

    # define server name and port
    serverName = 'localhost'
    serverPort = int(port)

    # create a socket for Receiver
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverName, serverPort))

    # ready to receive msg
    print('The server is ready to receive')

    while lastPacket == False:
        packet, clientAddress = serverSocket.recvfrom(1027)
        data_seg = packet[3:]
        sequenceNumber = int.from_bytes(packet[:2],byteorder='big')
        print(sequenceNumber)
        if packet[2] == 1:
            lastPacketFlag = True
        for i in data_seg:
            data.append(i)
        if lastPacketFlag:
            serverSocket.close()
            lastPacket = True
    with open(fileName, 'wb') as f:
        f.write(data)
if __name__ == '__main__':
    port = sys.argv[1]
    fileName = sys.argv[2]
    Receiver(port,fileName)
