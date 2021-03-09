import tkinter as tk
import socket
import threading
from tkinter import filedialog
import os
from functools import partial
from playsound import playsound
import tcp_sender as tcpsender
import tcp_receiver as tcpreceiver
import udp_receiver as udpreceiver
import udp_sender as udpsender

sounds = {0: 'Sound-1', 1: 'Sound-2', 2: 'Sound-3', 3: 'Sound-4', 4: 'Sound-5', 5: 'Sound-6'}


def get_message(message):
    if "mess" in message:
        return True
    for i in range(len(sounds)):
        if sounds[i] in message:
            if sounds[i] == 'Sound-1':
                playsound('Sound-1.mp3')
            elif sounds[i] == "Sound-2":
                playsound('Sound-2.mp3')
            elif sounds[i] == "Sound-3":
                playsound('Sound-3.mp3')
            elif sounds[i] == "Sound-4":
                playsound('Sound-4.mp3')
            elif sounds[i] == "Sound-5":
                playsound('Sound-5.mp3')
            elif sounds[i] == "Sound-6":
                playsound('Sound-6.mp3')
    return message


def mesage_locate(chatPart, message):
    if message != '':
        chatPart.config(state=tk.NORMAL)
        if chatPart.index('end') != None:
            LineNumber = float(chatPart.index('end')) - 1.0
            chatPart.insert(tk.END, "YOU: " + message)
            chatPart.tag_add("YOU", LineNumber, LineNumber + 0.5)
            chatPart.config(state=tk.DISABLED)
            chatPart.yview(tk.END)


def configure_message(chatPart, message):
    if message != '':
        chatPart.config(state=tk.NORMAL)
        if chatPart.index('end') != None:
            try:
                LineNumber = float(chatPart.index('end')) - 1.0
            except:
                pass
            chatPart.insert(tk.END, "Friend: " + message)
            chatPart.tag_add("Friend", LineNumber, LineNumber + 0.6)
            chatPart.config(state=tk.DISABLED)
            chatPart.yview(tk.END)


def connection_info(chatPart, message):
    if message != '':
        chatPart.config(state=tk.NORMAL)
        if chatPart.index('end') != None:
            chatPart.insert(tk.END, message + '\n')
            chatPart.config(state=tk.DISABLED)
            chatPart.yview(tk.END)


class GUI:
    def __init__(self, connection='', ip='', protocol_option=''):
        self.chat = tk.Tk()
        self.chat.title("Chat Window")
        self.chat.geometry("430x450")
        self.chat.resizable(width="false", height="false")
        self.chat.resizable(width="false", height="false")
        self.chat.configure(bg="lavender")
        self.connection = connection
        self.server_ip = ip
        self.server_port = 3000
        self.client_port = 3100
        self.protocol = protocol_option

        self.path = ""
        self.server_socket = connection
        threading.Thread(target=self.receive_file).start()
        self.chatPart = tk.Text(self.chat, bd=0, height="8", width="40", font="Consoles")
        self.chatPart.config(state="disabled")
        self.scroll = tk.Scrollbar(self.chat, command=self.chatPart.yview)

        self.label_send_status = tk.Label(self.chat, bg='snow', width=10, text='No files sent or received yet.')

        self.browse_button = tk.Button(self.chat, font=("Consoles", 10), text=u"BROWSE", width="40", height=5,
                                       bd=0, activebackground="#BDE096", justify="center",
                                       command=self.browse_app)
        self.cancel_button = tk.Button(self.chat, text='Cancel Upload', command=self.cancel_upload_function)

        self.download_button = tk.Button(self.chat, text='Download File', command=self.download_file_function)

        self.chatPart['yscrollcommand'] = self.scroll.set
        self.send_butt = tk.Button(self.chat, font=("Consoles", 10), text=u"SEND", width="50", height=5,
                                   bd=0, activebackground="#BDE096", justify="center",
                                   command=self.actionOnClick)
        self.sound_butt = tk.Button(self.chat, font="Consoles", text="\uD834\uDD60", width="50", height=5,
                                    bd=0, activebackground="#BDE096", justify="center",
                                    command=self.sound_list)

        self.textBox = tk.Text(self.chat, bd=0, width="17", height="5", font="Consoles")
        self.textBox.bind("<Return>", self.keyboardFocus)
        self.textBox.bind("<KeyRelease-Return>", self.enterAction)
        self.scroll.place(x=400, y=5, height=350)
        self.chatPart.place(x=15, y=5, height=350, width=400)

        self.browse_button.place(x=365, y=390, height=50, width=60)
        self.label_send_status.place(x=15, y=360, height=25, width=180)
        self.send_butt.place(x=255, y=390, height=50, width=50)
        self.sound_butt.place(x=310, y=390, height=50, width=50)
        self.textBox.place(x=15, y=390, height=50, width=240)

        self.chat.mainloop()

    def browse_app(self):
        path = filedialog.askopenfilename()
        self.label_send_status.config(text=(os.path.basename(path)))
        self.path = path
        self.cancel_button.place(x=250, y=360, height=25, width=160)

    def cancel_upload_function(self):
        self.path = ''
        self.label_send_status.config(text='')
        self.cancel_button.destroy()
        self.cancel_button = tk.Button(self.chat, text='Cancel Upload', command=self.cancel_upload_function)

    def receiving(self, name):
        self.label_send_status.config(text=name)
        self.download_button.place(x=250, y=360, height=25, width=160)

    def download_file_function(self):
        path = filedialog.asksaveasfilename()
        if self.protocol == "tcp":
            self.server_socket.sendall("mess".encode("utf-8"))
            tcpreceiver.tcp_connect(path)
        elif self.protocol == "udp":
            self.server_socket.sendto("mess".encode("utf-8"), (self.server_ip, self.client_port))
            udpreceiver.udp_receiver(path)
        self.download_button.destroy()
        self.download_button = tk.Button(self.chat, text='Download File', command=self.download_file_function)
        self.label_send_status.config(text="Received successfully.")

    def sending_func(self):
        print('SENDING FUNC')
        if self.protocol == 'tcp':
            self.file_tcp_sender = tcpsender.tcp_sending(self.server_ip[0], self.path)
        else:
            self.file_udp_sender = udpsender.udp_sender(self.server_ip, self.path)
        self.label_send_status.config(text='Sent successfully.')
        self.cancel_button.destroy()
        self.cancel_button = tk.Button(self.chat, text='Cancel Upload', command=self.cancel_upload_function)

    def receive_file(self):
        if self.protocol == "tcp":
            while 1:
                try:
                    data = self.server_socket.recv(1024).decode("utf-8")
                except Exception as m:
                    connection_info(self.chatPart, '\n friend left \n')
                    break
                if data != '':
                    # print(data)
                    data1 = get_message(data)
                    if data1 == True:  # if we have a file
                        if self.path != "":
                            self.sending_func()
                    elif "format_" in data1:
                        # print("DATA1", data1)
                        name = data1.split("format_")[-1]
                        name = os.path.basename(name)
                        name2 = data1.split("format_")[0]
                        # print("name2)
                        self.receiving(name)
                        configure_message(self.chatPart, name2)
                    else:
                        configure_message(self.chatPart, data1)
                else:
                    connection_info(self.chatPart, '\n friend left \n')
                    self.server_socket.close()
                    break

        elif self.protocol == "udp":
            while 1:
                try:
                    data, address = self.server_socket.recvfrom(1024)
                    data = data.decode("utf-8")
                    # print("000")
                except:
                    connection_info(self.chatPart, '\n friend left\n')
                    break
                if data != '':
                    data1 = get_message(data)
                    if data1 == True:  # if we have a file
                        if self.path != "":
                            self.sending_func()
                    elif "format_" in data1:
                        name = data1.split("format_")[-1]
                        name = os.path.basename(name)
                        name2 = data1.split("format_")[0]
                        self.receiving(name)
                        configure_message(self.chatPart, name2)
                    else:
                        configure_message(self.chatPart, data1)

                else:
                    connection_info(self.chatPart, '\n friend left \n')
                    break

    def actionOnClick(self):
        messageText = str(self.textBox.get("0.0", tk.END))
        if self.path != '':
            messageText += 'format_{}'.format(self.path)

        mesage_locate(self.chatPart, messageText.split('format_')[0])
        self.chatPart.yview(tk.END)
        self.textBox.delete("0.0", tk.END)
        if self.protocol == "tcp":
            self.server_socket.sendall(messageText.encode("utf-8"))
        else:
            self.server_socket.sendto(messageText.encode("utf-8"), (self.server_ip, self.client_port))

    def enterAction(self, event):
        self.textBox.config(state="normal")
        self.actionOnClick()

    def keyboardFocus(self, event):
        self.textBox.config(state="disabled")

    def sound_list(self):
        self.sound_list_box = tk.Tk()
        self.sound_list_box.title("Select a Music")
        self.sound_list_box.geometry("550x150")
        self.button_list = [range(len(sounds))]
        for i, j in sounds.items():
            tk.Button(self.sound_list_box, font="Consoles", text=j, bd=0, activebackground="#BDE096", justify="left",
                      command=partial(self.sound_index, i)).pack(side="left")

    def sound_index(self, ind):
        self.textBox.insert('end', sounds[ind])


class ConnectionGUI(tk.Frame):
    def __init__(self, connection_part):
        self.connection_part = connection_part

        tk.Label(self.connection_part, text="Project 2", bg='lavender', fg="black",
                 font=("Times New Roman", 17, "bold italic")) \
            .grid(column=0, row=0, sticky="EW", columnspan=4, padx=0)
        tk.Label(self.connection_part, text="Enter Destination IP: ", fg="black", bg='lavender',
                 font=("Times New Roman", 10)) \
            .grid(column=0, row=1)

        self.ip = tk.Entry(self.connection_part)
        self.ip.insert(tk.END, '192.168.1.107')
        self.ip.grid(column=2, row=1)

        self.new_frame = tk.Frame(self.connection_part, highlightbackground="black", bg='lavender',
                                  highlightcolor="black",
                                  highlightthickness=2, width=280, height=100)
        self.new_frame.grid(row=2, column=0, pady=10, columnspan=3)
        self.new_frame.grid_propagate(False)

        tk.Label(self.new_frame, text="Protocol: ", fg="black", font=("Times New Roman", 11), bg='lavender') \
            .grid(column=0, row=2, columnspan=1)

        self.protocol_option = tk.StringVar()
        self.protocol_option.set('tcp')
        self.protocol_option_1 = tk.Radiobutton(self.new_frame, text="TCP", variable=self.protocol_option,
                                                bg='lavender',
                                                value="tcp").grid(column=1, row=2)
        self.protocol_option_2 = tk.Radiobutton(self.new_frame, text="UDP", variable=self.protocol_option,
                                                bg='lavender',
                                                value="udp").grid(column=2, row=2)

        self.submit_button = tk.Button(self.new_frame, text=u'Start Connection=>', command=self.waitConnection,
                                       bg='lavender',
                                       width=23)
        self.submit_button.grid(row=3, column=1, columnspan=2, pady=10)
        self.connection_part.mainloop()

    def waitConnection(self):
        self.wait = tk.Label(self.new_frame, text="Waiting for Connection", fg="red",
                             font=("Times New Roman", 12), bg='lavender').grid(column=1, row=4, columnspan=3)
        get_ip = self.ip.get()
        port_num = 3000
        protocol_option = self.protocol_option.get()
        threading.Thread(target=self.start_connection, args=(get_ip, port_num, protocol_option)).start()

    def start_connection(self, ip, port, protocol):
        self.l = []
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.server_socket = None

        if self.protocol == "tcp":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", int(self.port)))
            self.server_socket.listen(1)
            self.wait = tk.Label(self.new_frame, text="Waiting for Connection", bg='lavender', fg="red",
                                 font=("Times New Roman", 12)).grid(column=1, row=4, columnspan=3)
            while True:
                cl_socket, cl_addr = self.server_socket.accept()
                self.wait = tk.Label(self.connection_part, text="Connected....").grid(column=1, row=4)

                GUI(cl_socket, cl_addr, self.protocol)

        elif self.protocol == "udp":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", int(self.port)))
            while True:
                message, addr = self.server_socket.recvfrom(1024)
                self.wait = tk.Label(self.connection_part, text="Connected").grid(column=1, row=4)

                if message.decode("utf-8") == "udp":
                    ab = GUI(self.server_socket, self.ip, self.protocol)
                    # threading.Thread(target=ab,args=("", self.ip, self.protocol)).start()
                # ab.chatBox.insert('end',message)
                #     threading.Thread(target=p1_server_gui_chat.GUI,args=("", self.ip, self.protocol)).start()
        else:
            print("Try to connect again.")


def main():
    root = tk.Tk()
    root.title("Server")
    root.configure(bg='lavender')
    app = ConnectionGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
