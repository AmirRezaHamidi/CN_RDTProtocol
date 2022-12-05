from Functions import checksum_calculator, byte2str, text_maker
from socket import *
import random
import sys

# IP address and port number configuration
Receiver_IP_Address = "127.0.0.1"
Receiver_Port_Number = 60000
Receiver = (Receiver_IP_Address, Receiver_Port_Number)

# define some initial parameter
segment_loss_probability = 0.01
receiver_timeout = 0.000001          # (in second)
segment_indicator = "01" * 8
ACK_indicator = "10" * 8
auxiliary_byte = "11111111"
Format = "UTF-8"
end_check = ["1"]*32

# deliver the P value with argument value (optional)
if len(sys.argv) == 2:

    segment_loss_probability = float(sys.argv[1])

# creating UPD connection in the receiver side and listen for incoming messages
ReceiverSocket = socket(AF_INET, SOCK_DGRAM)
ReceiverSocket.bind(Receiver)

while True:

    # sequence number has been considered 1 byte instead of 1 bit (for simplicity)
    sequence_number = "00000000"  # current sequence number
    p_sequence_number = "00000001"  # previous sequence number
    delivered_message = ""
    status = "on"

    while status == "on":

        while True:

            try:

                ReceiverSocket.settimeout(receiver_timeout)
                segment, SenderAddress = ReceiverSocket.recvfrom(65536)
                break

            except timeout:

                pass

            except ConnectionResetError:

                pass

        r = random.random()
        segment = segment.decode(Format)

        # simulating segment loss
        if segment_loss_probability < r:

            segment = list(segment)

            # condition1: non-corrupted segment
            condition1 = segment[0:16] == checksum_calculator(segment[16:])

            if condition1:

                # removing checksum
                segment = segment[16:]

                # checking auxiliary byte
                if segment[0:8] == list(auxiliary_byte):

                    # removing auxiliary byte (if exist)
                    segment = segment[8:]

                # condition 2 = correct sequence number
                # condition 3 = segment indicator check
                condition2 = (segment[0:8] == list(sequence_number))
                condition3 = (segment[8:24] == list(segment_indicator))

                if condition2 & condition3:

                    # correct segment
                    # removing sequence number and segment indicator
                    segment = segment[24:]

                    if segment[-32:] == end_check:

                        segment = segment[:-32]
                        status = "off"

                    if len(segment) != 0:

                        message = byte2str(segment)
                        delivered_message = f"{delivered_message}{message}"

                    else:

                        pass

                    # building and sending ACK
                    ACK = f"{auxiliary_byte}{sequence_number}{ACK_indicator}"
                    checksum = checksum_calculator(ACK)
                    checksum = "".join(checksum)
                    ACK = f"{checksum}{ACK}"
                    ReceiverSocket.sendto(ACK.encode(Format), SenderAddress)

                    # changing sequence number
                    sequence_number, p_sequence_number = p_sequence_number, sequence_number

                else:  # sequence number failure

                    # out of order segment
                    ACK = f"{auxiliary_byte}{p_sequence_number}{ACK_indicator}"
                    checksum = checksum_calculator(ACK)
                    checksum = "".join(checksum)
                    ACK = f"{checksum}{ACK}"
                    ReceiverSocket.sendto(ACK.encode(Format), SenderAddress)

            else:  # checksum failure

                # corrupted segment
                ACK = f"{auxiliary_byte}{p_sequence_number}{ACK_indicator}"
                checksum = checksum_calculator(ACK)
                checksum = "".join(checksum)
                ACK = f"{checksum}{ACK}"
                ReceiverSocket.sendto(ACK.encode(Format), SenderAddress)

        else:  # segment loss

            # lost segment
            pass

    text_maker(delivered_message, 1, "TXTs/received.txt")
