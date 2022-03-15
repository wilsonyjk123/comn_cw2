from socket import *
import sys

serverIP = 'localhost'
serverPort = int(sys.argv[1])
fileName = sys.argv[2]

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP,serverPort))
print('Server is running')
data = bytearray()

sequenceNumber = 0
expectedSequenceNumber = 0
fileReceived = False

while fileReceived == False:
    print(sequenceNumber)
    packet, addr = serverSocket.recvfrom(1027)
    print(len(packet))
    sequenceNumber = int.from_bytes(packet[:2],'big')
    if sequenceNumber == expectedSequenceNumber:
        data.extend(packet[3:])
        expectedSequenceNumber += 1
    if expectedSequenceNumber == 0:
        var = 0
    else:
        var = expectedSequenceNumber-1
    pktBack = bytearray(var.to_bytes(2, byteorder='big'))
    serverSocket.sendto(pktBack,addr)
    print(len(data))
    while expectedSequenceNumber-1 != sequenceNumber:
        print('expectedSequenceNumber: '+str(expectedSequenceNumber))
        print('sequenceNumber:'+str(sequenceNumber))
        packet, addr = serverSocket.recvfrom(1027)
        sequenceNumber = int.from_bytes(packet[:2], 'big')
        if expectedSequenceNumber == 0:
            var = 0
        else:
            var = expectedSequenceNumber - 1
        if sequenceNumber == expectedSequenceNumber:
            data.extend(packet[3:])
            expectedSequenceNumber += 1
            pktBack = bytearray(var.to_bytes(2, byteorder='big'))
            serverSocket.sendto(pktBack, addr)
    if packet[2] == 1:
        pktBack = bytearray(sequenceNumber.to_bytes(2, byteorder='big'))
        serverSocket.sendto(pktBack, addr)
        fileReceived = True
with open(fileName, 'wb') as f:
    f.write(data)