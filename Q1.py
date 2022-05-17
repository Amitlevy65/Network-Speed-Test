from matplotlib import pyplot as plt
from tkinter import *
import tkinter.messagebox as messagebox
import numpy as np
import speedtest as st
import time

# Variables
downloads = np.zeros(60)
uploads = np.zeros(60)
pings = np.zeros(60)
graph_time = np.arange(1, 61, dtype=int)
download_result = 0
upload_result = 0
ping_result = 0
wait = False


# Create Root
root = Tk()
root.geometry("400x800")
root.title("Network Speed Test Application")
root.resizable(False, False)
root['bg'] = '#95faa6'


# Functions
def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    clock_label.config(text=hour + ":" + minute + ":" + second)
    clock_label.after(1000, clock)


def check():
    global download_result
    global upload_result
    global ping_result
    global wait
    try:
        test = st.Speedtest()
    except st.ConfigRetrievalError:
        messagebox.showerror("Network Error", "Network is DOWN!")
    else:
        messagebox.showinfo("Calculating Network Speed", "Calculating Network Speed...")
        wait = True
        download_result = round(test.download() / 1024 / 1024, 2)
        maxAlert(download_result)
        minAlert(download_result)
        download_string.set(str(download_result))

        upload_result = round(test.upload() / 1024 / 1024, 2)
        upload_string.set(str(upload_result))

        ping_result = test.results.ping
        ping_string.set(str(ping_result))
        addToLists(download_result, upload_result, ping_result)
        wait = False


def addToLists(val1, val2, val3):
    global downloads
    global uploads
    global pings
    new_d = np.append(downloads, val1)
    new_u = np.append(uploads, val2)
    new_p = np.append(pings, val3)
    downloads = new_d[1:len(new_d)]
    uploads = new_u[1:len(new_u)]
    pings = new_p[1:len(new_p)]


def addToGraph():
    if not wait:
        addToLists(download_result, upload_result, ping_result)
        root.after(1000, addToGraph)


def setMax():
    new_max = enter_max.get()
    if validate(new_max):
        if new_max == "":
            messagebox.showerror("Max Set Status", "Can't be empty.")
            max_string.set(max_memory.get())
        elif int(new_max) > 1000:
            messagebox.showerror("Max Set Status", "Can't be greater then 1000 MB/s.")
            max_string.set(max_memory.get())
        elif int(new_max) <= int(enter_min.get()):
            messagebox.showerror("Max Set Status", "Can't be less then or equal to the Minimum speed.")
            max_string.set(max_memory.get())
        else:
            max_memory.set(new_max)
            max_string.set(new_max)
            messagebox.showinfo("Max Set Status", "Maximum Network Speed changed successfully.")
    else:
        messagebox.showerror("Invalid Input", "Expected value is numeric.")
        max_string.set(max_memory.get())


def setMin():
    new_min = enter_min.get()
    if validate(new_min):
        if new_min == "":
            messagebox.showerror("Min Set Status", "Can't be empty.")
            min_string.set(min_memory.get())
        elif int(new_min) < 0:
            messagebox.showerror("Min Set Status", "Can't be less then 0 MB/s.")
            min_string.set(min_memory.get())
        elif int(new_min) >= int(enter_max.get()):
            messagebox.showerror("Min Set Status", "Can't be greater then or equal to the Maximum speed.")
            min_string.set(min_memory.get())
        else:
            min_memory.set(new_min)
            min_string.set(new_min)
            messagebox.showinfo("Min Set Status", "Minimum Network Speed changed successfully.")
    else:
        messagebox.showerror("Invalid Input", "Expected value is numeric.")
        min_string.set(min_memory.get())


def validate(value):
    if value.isdigit():
        return True
    else:
        return False


def maxAlert(speed):
    if speed > int(enter_max.get()):
        messagebox.showerror("Maximum Alert", "Error, Network speed is greater then the Maximum Speed.")


def minAlert(speed):
    if speed < int(enter_min.get()):
        messagebox.showerror("Minimum Alert", "Error, Network speed is lower then the Minimum Speed.")


def downloadsGraph():
    plt.plot(graph_time, downloads)
    plt.title("Download Speed Graph")
    plt.xlabel("Time in seconds")
    plt.ylabel("Speed in MB/s")
    plt.show()


def uploadsGraph():
    plt.plot(graph_time, uploads)
    plt.title("Upload Speed Graph")
    plt.xlabel("Time in seconds")
    plt.ylabel("Speed in MB/s")
    plt.show()


def pingGraph():
    plt.plot(graph_time, pings)
    plt.title("Ping Graph")
    plt.xlabel("Time in seconds")
    plt.ylabel("Ping")
    plt.show()


# StringVars
download_string = StringVar(value="00")
upload_string = StringVar(value="00")
ping_string = StringVar(value="00")
min_string = StringVar(value="100")
min_memory = StringVar(value="100")
max_string = StringVar(value="1000")
max_memory = StringVar(value="1000")

# Buttons
start_btn = Button(root, text="Start Speed Calculation", bg="#10e5aa", bd=0, activebackground="#10c1aa", cursor="hand2",
                   command=check).place(x=180, y=100, anchor="center")
d_graph_btn = Button(root, text="Download Speed Graph", bg="#10e5aa", bd=0, activebackground="#10c1aa",
                     cursor="hand2", command=downloadsGraph).place(x=180, y=130, anchor="center")
u_graph_btn = Button(root, text="Upload Speed Graph", bg="#10e5aa", bd=0, activebackground="#10c1aa",
                     cursor="hand2", command=uploadsGraph).place(x=180, y=160, anchor="center")
p_graph_btn = Button(root, text="Ping Graph", bg="#10e5aa", bd=0, activebackground="#10c1aa", cursor="hand2",
                     command=pingGraph).place(
    x=180, y=190, anchor="center")
max_btn = Button(root, text="Set Max Speed", bg="#10e5aa", bd=0, activebackground="#10c1aa", cursor="hand2",
                 command=setMax).place(x=120, y=270, anchor="center")
min_btn = Button(root, text="Set Max Speed", bg="#10e5aa", bd=0, activebackground="#10c1aa", cursor="hand2",
                 command=setMin).place(x=240, y=270, anchor="center")

# Labels
Label(root, text="Ping", font="arian 13 bold", bg="#95faa6").place(x=50, y=0)
Label(root, text="Download", font="arian 13 bold", bg="#95faa6").place(x=140, y=0)
Label(root, text="Upload", font="arian 13 bold", bg="#95faa6").place(x=260, y=0)

download = Label(root, textvariable=download_string, font="arial 13 bold", bg="#10e5aa", fg="white").place(x=180, y=60,
                                                                                                           anchor="center")
download_mbs = Label(root, text="MB/s", font="arial 8 bold", bg="#10e5aa", fg="white").place(x=230, y=60,
                                                                                             anchor="center")

upload = Label(root, textvariable=upload_string, font="arial 13 bold", bg="#10e5aa", fg="white").place(x=290, y=60,
                                                                                                       anchor="center")
upload_mbs = Label(root, text="MB/s", font="arial 8 bold", bg="#10e5aa", fg="white").place(x=340, y=60, anchor="center")

ping = Label(root, textvariable=ping_string, font="arial 13 bold", bg="#10e5aa", fg="white").place(x=70, y=60,
                                                                                                   anchor="center")
max_label = Label(root, text="Max Speed", font="arial 13 bold", bg="#95faa6").place(x=120, y=240, anchor="center")
min_label = Label(root, text="Min Speed", font="arial 13 bold", bg="#95faa6").place(x=240, y=240, anchor="center")

clock_label = Label(root, text="", font="arial 30 bold", fg="red", bg="black")
clock_label.place(x=180, y=350, anchor="center")

# Entries
enter_max = Entry(root, width=10, textvariable=max_string, justify="center")
enter_max.place(x=120, y=300, anchor="center")

enter_min = Entry(root, width=10, textvariable=min_string, justify="center")
enter_min.place(x=240, y=300, anchor="center")

# Run
clock()
addToGraph()
root.mainloop()
