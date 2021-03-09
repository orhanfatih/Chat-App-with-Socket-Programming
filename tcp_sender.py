import socket  # socket module
import time

def tcp_sending(host, path):
    start_time = time.time()
    soc_ket = socket.socket()  # socket object initialized
    host = host  # socket.gethostname() # local machine name
    port = 4999  # port for you
    print("host: ", host, "path: ", path)
    soc_ket.connect((host, port))
    file_path = open(path, 'rb')
    print('sending in process')
    sth = file_path.read(1000)
    count = 0
    while (sth):
        print('sending in process')
        soc_ket.send(sth)
        sth = file_path.read(1000)
        count = count + 1

    file_path.close()
    print("Sending finished.")
    end_time = time.time()
    total_time = str(end_time - start_time)[:3]
    soc_ket.shutdown(socket.SHUT_WR)
    soc_ket.close()
    print("Total time is: " + total_time + " to send the file", int(count * 1000.0 / float(total_time)),
          "bits per second with", count, "packets.")
