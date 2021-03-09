from socket import *
import time

def udp_receiver(path):
    start_time = time.time()
    host = gethostname()
    port = 5000
    soc_ket = socket(AF_INET, SOCK_DGRAM)
    soc_ket.bind((host, port))

    addr = (host, port)
    buff = 1000
    count = 1
    data, addr = soc_ket.recvfrom(buff)
    file_path = open(path, 'wb')

    data, addr = soc_ket.recvfrom(buff)

    try:
        while (data):
            print("receiving")
            file_path.write(data)
            soc_ket.settimeout(2)
            data, addr = soc_ket.recvfrom(buff)
            count = count + 1
    except timeout:
        file_path.close()
        soc_ket.close()
        print("File Downloaded")
        end_time = time.time()
        total_time = str(end_time - start_time)[:3]
        print("Total time is: " + total_time + " seconds to download the file", int(count * 1000.0 / float(total_time)),
              "bits per second with", count, "packets.")
