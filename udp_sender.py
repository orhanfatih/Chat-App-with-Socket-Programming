from socket import *
import time

def udp_sender(host, path):
    start_time = time.time()
    soc_ket = socket(AF_INET, SOCK_DGRAM)
    host = host
    port = 5000
    buff = 1000
    addr = (host, port)
    count = 0
    name_file = bytes(path, 'utf-8')
    soc_ket.sendto(name_file, addr)
    file_path = open(name_file, "rb")
    data = file_path.read(buff)
    while (data):
        if (soc_ket.sendto(data, addr)):
            print("sending")
            data = file_path.read(buff)
            count = count + 1

    end_time = time.time()
    total_time = str(end_time - start_time)[:3]
    soc_ket.close()
    file_path.close()
    print("Total time is: " + total_time + " to send the file", int(count * 1000.0 / float(total_time)),
          "bits per second with",
          count, "packets.")
