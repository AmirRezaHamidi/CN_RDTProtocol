import matplotlib.pyplot as plt


def text_maker(sentence="Hello World",
               number_of_repetition=2,
               file_to_write="TXT/sent.txt"):

    """ this function writes any sentences for any number in any file
    :param sentence: type = str
    :param number_of_repetition: type = int
    :param file_to_write: type = str
    :return: generates a file with parameters above
    """

    string_to_be_written = ""

    for i in range(number_of_repetition):

        string_to_be_written = f"{string_to_be_written}{sentence}\n"

    with open(file_to_write, "w") as file:

        file.write(string_to_be_written)


def str2byte(string):

    """ this function converts string to bytes
    :param string: type = str
    :return: type = list of str
    """

    byte_list = []

    for i in string:

        if 0 <= ord(i) & ord(i) <= 127:

            temp_byte = bin(ord(i) + 128).replace('0b', '')
            byte_list.append(temp_byte)

        else:

            raise ValueError("[NON-STANDARD CHARACTER]"
                             "\nonly English character and known symbol are supported")

    return byte_list


def byte2str(byte):

    """ this function converts bytes to string
    :param byte: type = list of str
    :return: type = str
    """

    i = 0
    byte_list = []
    string_list = []

    while True:

        temp_byte = "".join(byte[i*8:(i+1)*8])
        byte_list.append(temp_byte)
        i += 1

        if i*8 == len(byte):

            break

    for j in byte_list:

        temp_str = chr(int(j, 2)-128)
        string_list.append(temp_str)

    string = "".join(string_list)

    return string


def checksum_calculator(list_segment):

    """ this function calculates the checksum of a data packet
    :param list_segment: type = list of str
    :return: type = list of str
    """

    base = 1
    old = int("".join(list_segment[0:16]), 2)
    while True:

        new = int("".join(list_segment[base*16: (base + 1)*16]), 2)
        old += new
        base += 1

        if len(list(bin(old).replace("0b", ""))) == 17:

            old -= 65535

        if base*16 == len(list_segment):

            checksum = list(bin(old).replace("0b", ""))

            if len(checksum) < 16:

                zero_in_beginning = 16 - len(checksum)
                zeros = ["0"] * zero_in_beginning
                checksum = zeros + checksum

                for i in range(len(checksum)):

                    checksum[i] = str(int(not (int(checksum[i]))))

            break

    return checksum


def plotter(x_axis, file_to_read_y_axis):

    """ this function plots a figure
    :param x_axis: this is a list
    :param file_to_read_y_axis: this is an address of a file that contain some data
    """

    with open(file_to_read_y_axis, "r") as Results:

        y_axis = Results.read()

    y_axis = y_axis.split("\n")
    y_axis.pop()
    y_axis = [float(i) for i in y_axis]

    plt.plot(x_axis, y_axis, "k")
    plt.show()
