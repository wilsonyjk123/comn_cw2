from socket import *
import math
import select
import sys
import time

def sendPacket(sequenceNumber, lastSequenceNumber, EOF,bytes_data, clientSocket,server_address):
    # check if the current sequence number is with the last package
    if sequenceNumber == lastSequenceNumber:
        EOF = 1
    packet = bytearray(sequenceNumber.to_bytes(2, byteorder='big'))
    packet.append(EOF)
    if EOF == 0:
        packet.extend(bytes_data[sequenceNumber * 1024:sequenceNumber * 1024 + 1024])
    if EOF == 1:
        packet.extend(bytes_data[sequenceNumber * 1024:])
    try:
        clientSocket.sendto(packet, server_address)
    except error:
        select.select([],[socket],[])

def receiveACK(base):
    # get data from receiver and set a timeout for the socket
    clientSocket.settimeout(retryTimeout / 1000)
    data, addr = clientSocket.recvfrom(2)
    ackSequenceNumber = int.from_bytes(data[:2], 'big')
    # if condition is true return ackseqnum
    if base < ackSequenceNumber:
        return ackSequenceNumber
    # otherwise keep waiting for packets
    else:
        return receiveACK(base)

# receiving parameters
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
fileName = open(sys.argv[3], 'rb')
retryTimeout = int(sys.argv[4])
windowSize = int(sys.argv[5])


# construct the server address
server_address = (serverName, serverPort)

# create the client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# set the socket to unblocking mode
clientSocket.setblocking(False)

# read the file(image) and save in a byte array
file = fileName.read()
bytes_data = bytearray(file)

# size of the data
numberOfPackets = len(bytes_data)

# Initiate the parameters
sequenceNumber = 0
lastSequenceNumber = math.ceil((len(bytes_data)/1024)-1)
EOF = 0
retransmission = 0
base = -1
lastAck = 0
fileSent = False

# start the timer
start = time.perf_counter()

# main loop
try:
    while fileSent == False:
        while sequenceNumber - base <= windowSize and sequenceNumber <= lastSequenceNumber:
            print('seqNum:' + str(sequenceNumber))
            sendPacket(sequenceNumber, lastSequenceNumber, EOF, bytes_data, clientSocket, server_address)
            sequenceNumber += 1
            try:
                base = receiveACK(base)
            except error as exc:
                sequenceNumber = base + 1
                retransmission += 1
            if base == lastSequenceNumber:
                print("sss")
                fileSent = True
except error as exc:
    print ("socket.error : %s" %exc)
end = time.perf_counter()
totalTimeUsed = end - start
print("retryTimeout: " + str(retryTimeout))
print("total time cost: " + str(totalTimeUsed) + '\n')
print("retransmission times: " + str(retransmission) + '\n')
print("throughput: " + str(len(bytes_data) / totalTimeUsed/1000))


