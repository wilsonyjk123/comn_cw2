from socket import *
import sys

def Sender(remoteHost, port, fileName):
    print("Start sending the files")

    serverName = remoteHost
    serverPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    server_address = (serverName, serverPort)

    # read the file(image) and save in a byte array
    file = fileName.read()
    bytes_data = bytearray(file)

    # size of the data
    rest_length = len(bytes_data)

    # initialize the sequence number
    sequenceNumber = 0
    EOF = 0

    while rest_length > 0:
        if rest_length > 1024:
            packet = bytearray(sequenceNumber.to_bytes(2,byteorder='big'))
            packet.append(EOF)
            packet.extend(bytes_data[sequenceNumber*1024:sequenceNumber*1024+1024])
            clientSocket.sendto(packet, server_address)
        else:
            packet = bytearray(sequenceNumber.to_bytes(2, byteorder='big'))
            EOF = 1
            packet.append(EOF)
            packet.extend(bytes_data[sequenceNumber * 1024:])
            clientSocket.sendto(packet, server_address)

        # update status
        sequenceNumber += 1
        rest_length -= 1024

    clientSocket.close()


if __name__ == '__main__':
    serverName = sys.argv[1]
    serverPort = sys.argv[2]
    fileName = open(sys.argv[3],'rb')
    Sender(serverName,serverPort,fileName)
