# sender side - sender.py

import socket
import time

socky = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname()) # '0.0.0.0' for local machine
port = 7261 

data = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
socky.connect((host, port)) # connection to hostname on the port
print "RDT Sender:"
print "Connected with server by (" + str(host) + ", " + str(port) + ")"

# Initialization
socky.settimeout(0.2) # socket timeout
sequence_number = 0
index = 0

def neg(number):
    return 0 if number else 1

script_start = time.time()

while True:
    message = data[index] + " " + str(sequence_number) # assemble message as a string
    socky.send(message)
    print("Sender sent a message: %s" % message)
    start_time = time.time() # trial timeout

    while True:
        if time.time() - script_start > 10:
            print "Terminating the program due to time limitation. Thanks for watching!"
            exit()

        if ((time.time() - start_time) < 1):
            try:
                received_message = socky.recv(1024)
            except socket.timeout:
                print "Continue waiting..."
                continue
            else:
                # Corrupted ACK is handled first to avoid value errors
                if received_message == "Bad ACK":
                    print "Sender received a corrupted ACK; keep waiting..."
                    continue
                # If ACK is not corrupted, check if it has the correct sequence number
                ack = int(received_message)
                # If it does, move on to the next data set, and adjust the sequence number
                if (ack == sequence_number):
                    print "Sender received a valid ACK for " + str(sequence_number) + ", send next message"
                    sequence_number = neg(sequence_number)
                    index += 1
                    index %= 7
                    break
                elif (ack == neg(sequence_number)):
                    print "Sender received an ACK with wrong sequency number; keep waiting..."
                    continue
        else:
            print "Timeout. Sending the message again:"
            break
