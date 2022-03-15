from socket import *
import math
import os
import sys


def Receiver(port, fileName):
    # define server name and port
    serverName = 'localhost'
    serverPort = int(port)

    lastPacket = False
    lastPacketFlag = False
    data = bytearray()

    # create a socket for Receiver
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverName, serverPort))

    # ready to receive msg
    print('The server is ready to receive')

    previousSequenceNumber = -1

    while lastPacket == False:
        packet, clientAddress = serverSocket.recvfrom(1027)
        currentSequenceNumber = int.from_bytes(packet[:2], byteorder='big')
        print(currentSequenceNumber)
        if currentSequenceNumber == previousSequenceNumber+1:
            previousSequenceNumber = currentSequenceNumber
            data.extend(packet[3:])
            pkt_back = bytearray(previousSequenceNumber.to_bytes(2, byteorder='big'))
            serverSocket.sendto(pkt_back, clientAddress)
        else:
            pkt_back = bytearray(previousSequenceNumber.to_bytes(2, byteorder='big'))
            serverSocket.sendto(pkt_back, clientAddress)
        if packet[2] == 1:
            lastPacketFlag = True

            pkt_back = bytearray(previousSequenceNumber.to_bytes(2, byteorder='big'))
            serverSocket.sendto(pkt_back, clientAddress)

            pkt_back = bytearray(previousSequenceNumber.to_bytes(2, byteorder='big'))
            serverSocket.sendto(pkt_back, clientAddress)
        if lastPacketFlag:
            lastPacket = True
    with open(fileName, 'wb') as f:
        f.write(data)
if __name__ == '__main__':
    port = sys.argv[1]
    fileName = sys.argv[2]
    Receiver(port,fileName)