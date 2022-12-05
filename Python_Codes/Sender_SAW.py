from Functions import checksum_calculator, str2byte
from socket import *
import random
import sys
import time

# IP address and port number configuration
Receiver_IP_Address = "127.0.0.1"
Receiver_Port_Number = 60000
Receiver = (Receiver_IP_Address, Receiver_Port_Number)

# define some initial parameters(these are default values)
segment_corruption_probability = 0.01
maximum_segment_size = 1000       # (in byte)
sender_timeout = 0.01            # (in second)
end_check = ["11111111"] * 4
segment_indicator = "01" * 8
ACK_indicator = "10" * 8
file = "TXTs/sent.txt"
Format = "UTF-8"

# sequence numbers has been considered 1 byte instead of 1 bit (for simplicity)
sequence_number = "00000000"        # current sequence number
p_sequence_number = "00000001"      # previous sequence number
auxiliary_byte = "11111111"

# deliver maximum segment size and filename with argument values (optional)
if len(sys.argv) == 2:

    maximum_segment_size = float(sys.argv[1])
    maximum_segment_size = round(maximum_segment_size)

elif len(sys.argv) == 3:

    maximum_segment_size = float(sys.argv[1])
    maximum_segment_size = round(maximum_segment_size)
    file = sys.argv[2]

n = 5
average_elapsed_time = 0

for i in range(n):

    # processing the data file
    with open(file, "r") as file_to_read:
        data = file_to_read.read()

    byte_list = str2byte(data)

    # initialization for each iteration
    base = 0
    status = "on"
    total_elapsed_time = 0
    last_round = "no"

    while status == "on":  # responsible for message segmentation

        # stage1 segment: includes segmented payload with maximum segment size
        stage1_segment = []

        if len(byte_list) > (base+1) * maximum_segment_size:

            stage1_segment = byte_list[base * maximum_segment_size:
                                       (base+1) * maximum_segment_size]

        elif len(byte_list) == (base + 1) * maximum_segment_size:

            byte_list = byte_list + end_check
            continue

        elif len(byte_list) < (base+1) * maximum_segment_size:

            last_round = "yes"

            if byte_list[-4:] == end_check:

                stage1_segment = end_check

            else:

                stage1_segment = byte_list[base * maximum_segment_size:] + end_check

        stage1_segment = "".join(stage1_segment)
        base += 1

        # stage2 segment: includes the header and payload(without checksum)
        header = f"{sequence_number}{segment_indicator}"
        stage2_segment = f"{header}{stage1_segment}"
        stage2_segment = list(stage2_segment)

        # stage3 segment: includes an auxiliary byte which
        # is needed for calculation of checksum
        if len(stage2_segment) % 16 == 8:

            stage3_segment = list(auxiliary_byte) + stage2_segment

        else:

            stage3_segment = stage2_segment

        # starting the timer
        start = time.time()
        offset_time = 0

        while True:  # responsible for segment corruption and sequence number

            # stage4 segment: include header with checksum
            checksum = checksum_calculator(stage3_segment)
            stage4_segment = checksum + stage3_segment

            # stage5 segment: auxiliary segment to simulate segment corruption
            stage5_segment = stage4_segment
            r = random.random()

            # simulating segment corruption
            if r < segment_corruption_probability:

                random_bit = random.choice(range(len(stage5_segment)))
                stage5_segment[random_bit] = str(int(not (int(stage5_segment[random_bit]))))

            stage5_segment = "".join(stage5_segment)

            while True:  # responsible for segment loss

                try:

                    SenderSocket = socket(AF_INET, SOCK_DGRAM)
                    SenderSocket.sendto(stage5_segment.encode(Format), Receiver)
                    SenderSocket.settimeout(sender_timeout)
                    ACK, _ = SenderSocket.recvfrom(65536)
                    SenderSocket.close()
                    ACK = list(ACK.decode(Format))

                    # condition 1 = ACK indicator check
                    condition1 = (ACK[32:48] == list(ACK_indicator))

                    if condition1:

                        break

                    else:

                        pass

                except ConnectionResetError:

                    os_start = time.time()
                    input("\n[RECEIVER IS TURNED OFF]\nturn on the receiver and hit enter")
                    os_end = time.time()
                    offset_time += os_end - os_start

                except timeout:

                    pass

            # condition 2 = non-corrupted ACK
            # condition 3 = correct sequence number
            condition2 = (ACK[0:16] == checksum_calculator(ACK[16:]))
            condition3 = (ACK[24:32] == list(sequence_number))

            if condition2 & condition3:

                sequence_number, p_sequence_number = p_sequence_number, sequence_number

                if last_round == "yes":

                    status = "off"

                break

            else:

                pass

        # stopping the timer
        end = time.time()
        elapsed_time = (end - start) - offset_time
        total_elapsed_time += elapsed_time

    if i == 0:

        print(f"\n{total_elapsed_time}")

    else:

        print(total_elapsed_time)

    average_elapsed_time += total_elapsed_time / n

print(f"\naverage elapsed time for {n} iteration is \n{average_elapsed_time}")

results_file = "TXTs/results.txt"
with open(results_file, "a") as Results:

    Results.write(f"{average_elapsed_time}\n")

    Results.close()
