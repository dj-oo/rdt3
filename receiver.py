# receiver side - receiver.py

import socket
import random

socky = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a socket object
host = socket.gethostbyname(socket.gethostname()) # '0.0.0.0' for local machine
port = 7261
socky.bind((host, port)) # binds to the port
socky.listen(5) # queue up to 5 requests

client, info = socky.accept() # establishes a connection
print "RDT Receiver:"

# Initialization
expected_sequence_number = 0
old_received_message = ""

# Helper method to retrieve the sequence number, and it can also retrieve the data
def parse_message(message):
    if message == "":
        print "Terminating the program due to time limitation. Thanks for watching!"
        exit()
    array_message = message.split()
    data = array_message[0]
    received_sequence_number = int(array_message[1])
    return data, received_sequence_number

def neg(number):
    return 0 if number else 1

while True:
    received_message = client.recv(1024)
    data, received_sequence_number = parse_message(received_message)

    if (received_message != old_received_message):
        print "Receiver just correctly received a message: " + received_message
    else:
        print "Receiver just correctly received a duplicated message: " + received_message

    # Keeps track of the previous message to print duplication record
    old_received_message = received_message

    # This is where naughty receiving happens; we simulate unreliable packet transmission by using
    # random numbers to decide 4 possible downfalls that can happen
    if (received_sequence_number == expected_sequence_number):
        choice = random.randint(1,4)

        if choice == 1:
            client.send(str(received_sequence_number))
            print "Receiver responds with ACK " + str(received_sequence_number)
            expected_sequence_number = neg(expected_sequence_number)
            continue
        elif choice == 2:
            client.send("Bad ACK")
            print "A corrupted ACK is sent"
            continue
        elif choice == 3:
            print "Receiver does not send ACK"
            continue
        else:
            client.send(str(neg(received_sequence_number)))
            print "Receiver incorrectly responds with ACK " + str(neg(received_sequence_number))
            continue
