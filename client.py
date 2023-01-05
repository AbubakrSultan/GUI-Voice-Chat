import socket, threading, tkinter as tk
import pyaudio

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "10.0.0.189"
port = 5000

client.connect((host, port))
print("CLIENT CONNECTED")

p = pyaudio.PyAudio()

Format = pyaudio.paInt16
Chunks = 4096
Channels = 2
Rate = 44100

input_stream = p.open(format=Format, 
                      channels=Channels, 
                      rate=Rate,
                      input=True,
                      frames_per_buffer=Chunks)

output_stream = p.open(format=Format, 
                       channels=Channels, 
                       rate=Rate,
                       output=True,
                       frames_per_buffer=Chunks)



def send():
    while True:
        try:
            data = input_stream.read(Chunks)
            if unmuted == "Mute":
                client.send(data)
        except:
            break

def recive():
    while True:
        try:
            data = client.recv(Chunks)
            output_stream.write(data)
        except:
            break
unmuted = None

def GUI():
    window = tk.Tk()
    global unmuted
    unmuted = tk.StringVar(window, "Unmute")
    def muteOrUnmute():
        global unmuted
        if unmuted.get() == "Unmute":
            unmuted.set("Mute")
        else:
            unmuted.set("Unmute")

    window.geometry("500x500")
    window.title("Voice Chat")

    muteOrUnmuteButton = tk.Button(window, 
                                   textvariable=unmuted,
                                   bd="5",
                                   command=muteOrUnmute,
                                   height=16,
                                   width=30
                                   )
    muteOrUnmuteButton.pack()

    window.mainloop()

gui_thread = threading.Thread(target=GUI)
send_thread = threading.Thread(target=send)
recive_thread = threading.Thread(target=recive)

gui_thread.start()
send_thread.start()
recive_thread.start()

gui_thread.join
send_thread.join()
recive_thread.join()

input_stream.stop()
input_stream.close()
output_stream.stop()
output_stream.close()
p.terminate()