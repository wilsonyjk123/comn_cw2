from socket import *
import math
import os
import sys
import time




def Sender(remoteHost, port, fileName,retryTimeout):
    serverName = remoteHost
    serverPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    server_address = (serverName, serverPort)

    # read the file(image) and save in a byte array
    file = fileName.read()
    bytes_data = bytearray(file)

    # size of the data
    rest_length = len(bytes_data)

    sequenceNumber = 0
    EOF = 0
    retransmission = 0
    start = time.perf_counter()

    while rest_length > 0:
        print(sequenceNumber)
        print(retransmission)
        isAckReceivedCorrect = False
        isAckReceived = False
        ackSequenceNumber = 0
        if rest_length > 1024:
            packet = bytearray(sequenceNumber.to_bytes(2,byteorder='big'))
            packet.append(EOF)
            packet.extend(bytes_data[sequenceNumber*1024:sequenceNumber*1024+1024])
            clientSocket.sendto(packet, server_address)


            while isAckReceivedCorrect == False:
                try:
                    clientSocket.settimeout(retryTimeout/1000)
                    ack, clientAddress = clientSocket.recvfrom(2)
                    ackSequenceNumber = int.from_bytes(ack[:2], 'big')
                    isAckReceived = True
                except timeout:
                    isAckReceived = False
                if sequenceNumber == ackSequenceNumber and isAckReceived == True:
                    isAckReceivedCorrect = True
                else:
                    clientSocket.sendto(packet, server_address)
                    retransmission += 1

            sequenceNumber += 1
            rest_length -= 1024

        else:
            packet = bytearray(sequenceNumber.to_bytes(2, byteorder='big'))
            EOF = 1
            packet.append(EOF)
            packet.extend(bytes_data[sequenceNumber * 1024:])
            clientSocket.sendto(packet, server_address)

            # isAckReceivedCorrect = False
            # isAckReceived = False
            # ackSequenceNumber = 0

            while isAckReceivedCorrect == False:
                try:
                    clientSocket.settimeout(retryTimeout / 1000)
                    packet, clientAddress = clientSocket.recvfrom(2)
                    ackSequenceNumber = int.from_bytes(packet[:2], 'big')
                    isAckReceived = True
                except timeout:
                    isAckReceived = False
                if sequenceNumber == ackSequenceNumber and isAckReceived == True:
                    isAckReceivedCorrect = True
                else:
                    clientSocket.sendto(packet, server_address)
                    retransmission += 1

            sequenceNumber += 1
            rest_length -= 1024

    end = time.perf_counter()
    total_time = end - start
    print("retryTimeout: " + str(retryTimeout))
    print("total time cost: " + str(total_time) +'\n')
    print("retransmission times: " + str(retransmission) + '\n')
    print("throughput: " + str(len(bytes_data)/total_time))
if __name__ == '__main__':
    serverName = sys.argv[1]
    serverPort = sys.argv[2]
    fileName = open(sys.argv[3], 'rb')
    retryTimeout = int(sys.argv[4])
    Sender(serverName, serverPort, fileName, retryTimeout)

