import socket  # socket module
import time

def tcp_connect(path):
    start_time = time.time()
    soc_ket = socket.socket()  # socket object initialized
    host = socket.gethostname()  # local machine name
    print("host: ", host)
    port = 4999  # Reserve a port for your service.
    # soc_ket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc_ket.bind((host, port))  # Bind to the port
    soc_ket.listen(5)  # Now wait for client connection.r
    count = 0

    while True:
        cl, addr = soc_ket.accept()  # Establish connection with client.
        print('Got connection from', addr)
        file_get = True
        print("receiving")
        file_path = open('{}'.format(path), 'wb')
        sth = cl.recv(1000)
        while (sth):
            print("receiving")
            file_path.write(sth)
            sth = cl.recv(1000)
            count = count + 1

        file_path.close()
        print("Receiving process finished.")
        end_time = time.time()
        total_time = str(end_time - start_time)[:3]
        soc_ket.close()
        print("Total time is: " + total_time + "  to send the file", int(count * 1000.0 / float(total_time)),
              "bits per second with",
              count, "packets.")
        break
